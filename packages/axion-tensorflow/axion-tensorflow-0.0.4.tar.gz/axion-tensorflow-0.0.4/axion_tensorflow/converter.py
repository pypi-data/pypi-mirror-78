import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import models

from axion_tensorflow import layers as qlayers

__all__ = ["Converter"]


_AXION = 1
_MODEL = 2
_EMBEDDED = 3  # useful opr but not in axion, like unpool
_OTHERS = 4

_OPR_NAME_DICT = {
    layers.InputLayer: "data",
    qlayers.Activation: "activation",
    qlayers.Unpooling2D: "unpool",
    tf.python.keras.layers.normalization.BatchNormalizationBase: "bn",
    layers.MaxPooling2D: "pooling",
    layers.Flatten: "flatten",
    layers.Concatenate: "concat",
}


def get_node_type(node):
    if hasattr(node, "get_bitmeta"):
        return _AXION
    for key, val in _OPR_NAME_DICT.items():
        if isinstance(node, key):
            return _EMBEDDED
    if isinstance(node, (layers.Layer, models.Model)):
        return _MODEL
    return _OTHERS


def get_str_type(node):
    for key, val in _OPR_NAME_DICT.items():
        if isinstance(node, key):
            return val
    return None


class Converter:
    def convert_keras(self, keras_model, example):
        layer_metas_dict = {}
        # pay attention to the order of each operation and do not swap them
        self.full_name_dict = {}
        self.get_prefix_name(keras_model, is_first_layer=True)

        self.model_io_nodes = {}
        node_input, node_output, layer_metas_dict = self.search(
            layer_metas_dict, keras_model
        )

        layer_metas_dict = self.unfold_model_in_inputs(layer_metas_dict)
        layer_metas_dict = self.fuse(layer_metas_dict)
        layer_metas_dict = self.bit_type_check(layer_metas_dict)
        layer_metas_dict = self.fill_output(layer_metas_dict, example)
        layer_metas_dict = self.postprocess_mode_convert(layer_metas_dict)
        layer_metas_dict = self.int_bittype_to_str_bittype(layer_metas_dict)
        metas = list(layer_metas_dict.values())
        metas.reverse()
        return metas

    def get_module_io(self, node, io_node_type="origin"):
        def _list(x):
            return x if isinstance(x, list) else [x]

        def _name(_node):
            for full_name, node in self.full_name_dict.items():
                if node == _node:
                    return full_name
            assert False, "node not found {}".format(_node)

        assert io_node_type in ["origin", "string"]
        if isinstance(node, models.Model):
            opr_children_list = {i.name: i for i in node.layers}
            input_list = (
                [node.layers[0]]
                if isinstance(node, tf.keras.Sequential)
                else [opr_children_list[i] for i in _list(node.input_names)]
            )
            output_list = (
                [node.layers[-1]]
                if isinstance(node, tf.keras.Sequential)
                else [opr_children_list[i] for i in _list(node.output_names)]
            )
        else:
            # submodules of submodules are not opr_children
            submodules = list(node.submodules)
            subsubmodules = set([])
            for submodule in node.submodules:
                subsubmodules = subsubmodules.union(set(submodule.submodules))
            opr_children_list = {
                i.name: i
                for i in node.submodules
                if i in submodules and i not in subsubmodules
            }
            input_list = [
                i
                for i in opr_children_list.values()
                if i._inbound_nodes[0].inbound_layers
                == node._inbound_nodes[0].inbound_layers
            ]
            output_list = [
                i for i in opr_children_list.values() if len(i._outbound_nodes) == 0
            ]
        if io_node_type == "string":
            input_list = [_name(i) for i in input_list]
            output_list = [_name(i) for i in output_list]
        opr_children_list = list(opr_children_list.values())

        return opr_children_list, input_list, output_list

    def get_prefix_name(self, node, is_first_layer=False, layer_prefix=[]):
        def get_name(node):
            if isinstance(node, str):
                node_name = node
            else:
                node_name = node.name
            return "/".join(layer_prefix + [node_name])

        def _update(_dict):
            for node_name, node_to_add in _dict.items():
                if node_to_add not in self.full_name_dict:
                    self.full_name_dict.update({node_name: node_to_add})

        _update({get_name(node.name): node})
        if not is_first_layer:
            layer_prefix.append(node.name)
        opr_children_list, input_list, output_list = self.get_module_io(node)
        for cur_node in opr_children_list:
            if get_node_type(cur_node) in [_AXION, _EMBEDDED]:
                _update({get_name(cur_node): cur_node})
            elif get_node_type(cur_node) == _MODEL:
                self.get_prefix_name(cur_node, layer_prefix=layer_prefix.copy())

    def update_opr_info(self, node, node_name, layer_metas_dict):
        if layer_metas_dict.get(node_name, None) is None:
            layer_metas_dict[node_name] = {}
        if hasattr(node, "get_bitmeta"):
            layer_metas_dict[node_name].update(node.get_bitmeta())
            # use full name with prefix, not layer name
            layer_metas_dict[node_name].update({"name": node_name})
        else:
            layer_metas_dict[node_name].update(
                {"name": node_name, "type": get_str_type(node)}
            )
        layer_metas_dict[node_name]["opr"] = node
        return layer_metas_dict

    def search(self, layer_metas_dict, node, mrk={}):
        def _list(x):
            return x if isinstance(x, list) else [x]

        def _name(_node):
            for full_name, node in self.full_name_dict.items():
                if node == _node:
                    return full_name
            assert False, "node not found {}".format(_node)

        opr_children_list, input_list, output_list = self.get_module_io(
            node, io_node_type="string"
        )
        q = []  # queue
        for out_name in output_list:
            if mrk.get(out_name, None) is None:
                q.append(out_name)
                mrk[out_name] = 1

        while q:
            cur_name = q.pop(0)
            cur_node = self.full_name_dict[cur_name]
            if get_node_type(cur_node) in [_AXION, _EMBEDDED]:
                layer_metas_dict = self.update_opr_info(
                    cur_node, _name(cur_node), layer_metas_dict
                )
                if layer_metas_dict[cur_name]["type"] != "data":
                    if "input" not in layer_metas_dict[cur_name]:
                        layer_metas_dict[cur_name]["input"] = []
                    for next_node_iter in cur_node._inbound_nodes:
                        for next_node in _list(next_node_iter.inbound_layers):
                            next_name = _name(next_node)
                            layer_metas_dict[cur_name]["input"].append(next_name)
            elif get_node_type(cur_node) == _MODEL:
                if cur_name not in self.model_io_nodes:
                    self.search(layer_metas_dict, cur_node, mrk)
            else:
                assert False, "{} is unknown opr.".format(cur_node)
            for next_node_iter in cur_node._inbound_nodes:
                for next_node in _list(next_node_iter.inbound_layers):
                    if next_node not in opr_children_list:
                        continue
                    next_name = _name(next_node)
                    if mrk.get(next_name, None) is None:
                        q.append(next_name)
                        mrk[next_name] = 1

        # remove composed model recursively
        input_list_expanded = []
        for input_name in input_list:
            input_node = self.full_name_dict[input_name]
            if get_node_type(input_node) == _MODEL:
                input_list_expanded.extend(self.model_io_nodes[input_name]["input"])
            else:
                input_list_expanded.append(input_name)

        output_list_expanded = []
        for output_name in output_list:
            output_node = self.full_name_dict[output_name]
            if get_node_type(output_node) == _MODEL:
                output_list_expanded.extend(self.model_io_nodes[output_name]["output"])
            else:
                output_list_expanded.append(output_name)
        self.model_io_nodes.update(
            {
                _name(node): {
                    "input": input_list_expanded,
                    "output": output_list_expanded,
                }
            }
        )

        return (
            input_list_expanded,
            output_list_expanded,
            layer_metas_dict,
        )

    def unfold_model_in_inputs(self, layer_metas_dict):
        new_name = {}
        for name, metas in layer_metas_dict.items():
            if metas.get("input", None) is not None:
                new_name[name] = []
                for input_name in metas["input"]:
                    if input_name in self.model_io_nodes:
                        new_name[name].extend(self.model_io_nodes[input_name]["output"])
                    else:
                        new_name[name].append(input_name)
        for name, new_input_name in new_name.items():
            layer_metas_dict[name]["input"] = new_input_name

        for name, metas in layer_metas_dict.items():
            if metas.get("input", None) is not None:
                for input_name in metas["input"]:
                    input_node = self.full_name_dict[input_name]
                    assert get_node_type(input_node) != _MODEL
        return layer_metas_dict

    def fuse(self, layer_metas_dict):
        def fuse_meta(layer_name_to_del, data_to_push_up=[], is_unpool=False):
            # remove an opr and retain correct input struct (and push up parameters)
            assert layer_name_to_del in layer_metas_dict
            for layer_name in layer_metas_dict.keys():
                if layer_metas_dict[layer_name]["type"] == "data":
                    continue
                name_in_input = False
                for input_tuple in layer_metas_dict[layer_name]["input"]:
                    if input_tuple[0] == layer_name_to_del:
                        name_in_input = True
                        break
                if not name_in_input:
                    continue
                new_input_names = []
                for input_tuple in layer_metas_dict[layer_name]["input"]:
                    input_name = input_tuple[0]
                    if layer_name_to_del == input_name:
                        new_input_names.extend(
                            [
                                (i[0], True) if is_unpool else i
                                for i in layer_metas_dict[layer_name_to_del]["input"]
                            ]
                        )
                    else:
                        new_input_names.append(input_tuple)
                layer_metas_dict[layer_name]["input"] = new_input_names

            for layer_name, _ in layer_metas_dict[layer_name_to_del]["input"]:
                for data_name in data_to_push_up:
                    if data_name in layer_metas_dict[layer_name_to_del]:
                        # k1 *= k2
                        # b1 *= k2
                        # b1 += b2
                        if data_name == "affine_k":
                            layer_metas_dict[layer_name][
                                "affine_k"
                            ] *= layer_metas_dict[layer_name_to_del]["affine_k"]

                        elif data_name == "affine_b":
                            layer_metas_dict[layer_name][
                                "affine_b"
                            ] *= layer_metas_dict[layer_name_to_del]["affine_k"]
                            layer_metas_dict[layer_name][
                                "affine_b"
                            ] += layer_metas_dict[layer_name_to_del]["affine_b"]
                        else:
                            layer_metas_dict[layer_name][data_name] = layer_metas_dict[
                                layer_name_to_del
                            ][data_name]

            layer_metas_dict.pop(layer_name_to_del)

        # fix input format from "name" to "(name, is_unpool)"
        for layer_name in layer_metas_dict.keys():
            if layer_metas_dict[layer_name]["type"] == "data":
                continue
            for idx in range(len(layer_metas_dict[layer_name]["input"])):
                layer_metas_dict[layer_name]["input"][idx] = (
                    layer_metas_dict[layer_name]["input"][idx],
                    False,
                )

        # fill necessary infomation in metas
        for layer_name in layer_metas_dict.keys():
            # output_tensor will be the last output of some composed layers, like conv
            layer_metas_dict[layer_name]["output_tensor"] = layer_metas_dict[
                layer_name
            ]["opr"].output
            if layer_metas_dict[layer_name]["type"] == "data":
                layer_metas_dict[layer_name].update({"data_ratio": 255, "of_bit": 8})

            if layer_metas_dict[layer_name]["type"] == "pooling":
                ph, pw = layer_metas_dict[layer_name]["opr"].pool_size
                assert ph == pw, "pooling size in h,w must be the same"
                layer_metas_dict[layer_name]["pooling"] = (ph, pw)

            if layer_metas_dict[layer_name]["type"] == "bn":
                # y = (x - mean) * tf.rsqrt(variance + eps)
                # => y = (k * x + b - mean) * tf.rsqrt(variance + eps)
                # => k' = k * tf.rsqrt(variance + eps), \\
                # b' = (b - mean) * tf.rsqrt(variance + eps)
                opr = layer_metas_dict[layer_name]["opr"]
                inv_stddev = tf.math.rsqrt(opr.moving_variance + opr.epsilon).numpy()
                layer_metas_dict[layer_name]["affine_k"] = inv_stddev
                layer_metas_dict[layer_name]["affine_b"] = (
                    -opr.moving_mean.numpy() * inv_stddev
                )
                if opr.center or opr.scale:
                    raise ValueError(
                        "BatchNormalization should not enable center or scale."
                    )

            if layer_metas_dict[layer_name]["type"] == "activation":
                opr = layer_metas_dict[layer_name]["opr"]
                layer_metas_dict[layer_name]["of_bit"] = opr.activation_bits
                # y = multiplier * (gamma * x + beta)
                # => y = multiplier * (gamma * (k * x + b) + beta)
                # => k' = k * gamma * multiplier, \\
                # b' = b * multiplier * gamma + beta * multiplier
                layer_metas_dict[layer_name]["affine_k"] = (
                    opr.gamma.numpy() * opr.multiplier
                )
                layer_metas_dict[layer_name]["affine_b"] = (
                    opr.beta.numpy() * opr.multiplier
                )

        # remove all opr 'flatten', 'concat'
        opr_to_delete = []
        for layer_name in layer_metas_dict.keys():
            if layer_metas_dict[layer_name]["type"] in ["flatten", "concat"]:
                opr_to_delete.append(layer_name)
        for layer_name in opr_to_delete:
            fuse_meta(layer_name)

        # solve 'pooling', 'activation', 'bn' opr following a 'conv'
        # remove three kinds of operators one by one with parameters pushing up
        opr_to_delete = []
        for layer_name in layer_metas_dict.keys():
            if layer_metas_dict[layer_name]["type"] in ["pooling", "activation", "bn"]:
                assert len(layer_metas_dict[layer_name]["input"]) == 1
                assert layer_metas_dict[layer_metas_dict[layer_name]["input"][0][0]][
                    "type"
                ] in ["conv", "bn", "activation", "pooling"]

                opr_to_delete.append(layer_name)
        for layer_name in opr_to_delete:
            fuse_meta(
                layer_name,
                data_to_push_up=[
                    "pooling",
                    "of_bit",
                    "affine_k",
                    "affine_b",
                    "output_tensor",
                ],
            )

        # remove 'unpool'
        opr_to_delete = []
        for layer_name in layer_metas_dict.keys():
            if layer_metas_dict[layer_name]["type"] == "unpool":
                for input_name, _ in layer_metas_dict[layer_name]["input"]:
                    assert layer_metas_dict[input_name]["type"] != "unpool"
                opr_to_delete.append(layer_name)
        for layer_name in opr_to_delete:
            fuse_meta(layer_name, is_unpool=True)

        # remove all tensorflow oprs in metas
        for layer_name in layer_metas_dict.keys():
            layer_metas_dict[layer_name].pop("opr")

        return layer_metas_dict

    def bit_type_check(self, layer_metas_dict):
        """
        fill if_bit/of_bit in all oprs
        """
        q = []
        mrk = {}
        reversed_edges = {layer_name: [] for layer_name in layer_metas_dict.keys()}
        for layer_name in layer_metas_dict.keys():
            if layer_metas_dict[layer_name]["type"] == "data":
                assert layer_metas_dict[layer_name].get("of_bit") is not None
                q.append(layer_name)
                mrk[layer_name] = 1
            else:
                for input_name, _ in layer_metas_dict[layer_name]["input"]:
                    reversed_edges[input_name].append(layer_name)

        while q:
            cur = q.pop(0)
            cur_if_bit = layer_metas_dict[cur].get("if_bit")
            cur_of_bit = layer_metas_dict[cur].get("of_bit")
            if layer_metas_dict[cur].get("if_bit") is not None:
                if layer_metas_dict[cur].get("of_bit") is None:
                    layer_metas_dict[cur]["of_bit"] = cur_if_bit
                    cur_of_bit = cur_if_bit
            for output_name in reversed_edges[cur]:
                if layer_metas_dict[output_name].get("if_bit") is None:
                    layer_metas_dict[output_name]["if_bit"] = cur_of_bit
                else:
                    assert layer_metas_dict[output_name]["if_bit"] == cur_of_bit
                if output_name not in mrk:
                    q.append(output_name)
                    mrk[output_name] = 1

        return layer_metas_dict

    def fill_output(self, layer_metas_dict, example):
        md = {l: layer_metas_dict[l] for l in layer_metas_dict.keys()}
        inputs = [
            layer_metas_dict[l]["output_tensor"]
            for l in layer_metas_dict.keys()
            if layer_metas_dict[l]["type"] == "data"
        ]
        if len(inputs) != 1:
            raise ValueError("Unsupported number of inputs: {}.".format(len(inputs)))
        outputs = {
            l: layer_metas_dict[l]["output_tensor"] for l in layer_metas_dict.keys()
        }
        f = tf.keras.backend.function(inputs=inputs, outputs=outputs)
        output_values = f(example)
        for k, v in output_values.items():
            md[k]["output"] = v
        for l in layer_metas_dict.values():
            l.pop("output_tensor")
        return layer_metas_dict

    def postprocess_mode_convert(self, layer_metas_dict):
        def convert_postprocess_mode_to_integer(postprocess_mode):
            assert postprocess_mode in ["normal", "direct", "affine"]
            return {"normal": 0, "direct": 2, "affine": 3}[postprocess_mode]

        for m in layer_metas_dict.keys():
            if layer_metas_dict[m]["type"] in ["conv", "dense", "local_conv"]:
                if layer_metas_dict[m]["of_bit"] == 0:
                    layer_metas_dict[m]["of_bit"] = 16
                    layer_metas_dict[m][
                        "postprocess_mode"
                    ] = convert_postprocess_mode_to_integer("affine")
                else:
                    layer_metas_dict[m][
                        "postprocess_mode"
                    ] = convert_postprocess_mode_to_integer("normal")
        return layer_metas_dict

    def int_bittype_to_str_bittype(self, layer_metas_dict):
        def int_to_str(data):
            if data == 0:
                data = 16
            return "logic_uint" + str(data)

        for m in layer_metas_dict.keys():
            for bit_to_change in ["if_bit", "of_bit", "w_bit"]:
                if layer_metas_dict[m].get(bit_to_change, None) is not None:
                    origin_bit = layer_metas_dict[m][bit_to_change]
                    layer_metas_dict[m][bit_to_change] = (
                        origin_bit,
                        True,
                        False,
                        int_to_str(origin_bit),
                    )
        return layer_metas_dict
