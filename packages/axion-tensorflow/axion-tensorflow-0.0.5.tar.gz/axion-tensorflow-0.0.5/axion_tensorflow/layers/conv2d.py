import numpy as np
import tensorflow as tf
from tensorflow import nn
from tensorflow.keras import layers
from tensorflow.python.keras import initializers
from axion_tensorflow import fake_quant


@tf.keras.utils.register_keras_serializable(package="Axion")
class Conv2D(layers.Layer):
    """ Quantization aware Conv2D. """

    def __init__(
        self,
        filters,
        kernel_size,
        groups=1,
        strides=1,
        kernel_bits=4,
        kernel_initializer="glorot_uniform",
        bias_initializer="zeros",
        data_format="channels_last",
        **kwargs
    ):
        super().__init__(**kwargs)
        if data_format not in ["channels_first"]:
            raise ValueError("data_format currently supports only channels_first.")
        self.filters = filters
        self.kernel_size = kernel_size
        self.kernel_bits = kernel_bits
        self.groups = groups
        self.strides = strides
        self.kernel_initializer = initializers.get(kernel_initializer)
        self.bias_initializer = initializers.get(bias_initializer)

    def build(self, input_shape):
        unused_N, C, unused_H, unused_W = input_shape
        kernel_shape = (
            self.kernel_size,
            self.kernel_size,
            C // self.groups,
            self.filters,
        )

        self.kernel = self.add_weight(
            name="kernel",
            shape=kernel_shape,
            initializer=self.kernel_initializer,
        )
        self.bias = self.add_weight(
            name="bias", shape=(self.filters,), initializer=self.bias_initializer
        )

    def call(self, inputs):
        q_kernel, unused_scale = fake_quant.fake_quant_weights(
            self.kernel, num_bits=self.kernel_bits
        )
        x = tf.pad(inputs, [[0, 0], [0, 0], [1, 1], [1, 1]])
        x = nn.conv2d(x, q_kernel, self.strides, padding="VALID", data_format="NCHW")
        x = nn.bias_add(x, self.bias, data_format="NCHW")
        return x

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "filters": self.filters,
                "kernel_size": self.kernel_size,
                "strides": self.strides,
                "groups": self.groups,
                "kernel_bits": self.kernel_bits,
                "kernel_initializer": initializers.serialize(self.kernel_initializer),
                "bias_initializer": initializers.serialize(self.bias_initializer),
                "data_format": "channels_first",
            }
        )
        return config

    def get_bitmeta(self):
        q_kernel, scale = fake_quant.fake_quant_weights(
            self.kernel, num_bits=self.kernel_bits
        )
        q_kernel = q_kernel / scale
        # bitmeta shape is (oc, ic, 3, 3), while tensorflow shape is (3, 3, ic, oc).
        q_kernel = tf.transpose(q_kernel, perm=(3, 2, 0, 1))
        # special treatment for the current converter.
        q_kernel, scale = q_kernel / 2, scale * 2
        return {
            "name": self.name,
            "type": "conv",
            "if_bit": None,
            "w_bit": self.kernel_bits,
            "of_bit": 0,
            "input": [],
            "groups": self.groups,
            "affine_k": np.zeros((self.filters,), dtype=np.float32) + scale.numpy(),
            "affine_b": self.bias.numpy(),
            "weight": q_kernel.numpy(),
            "stride": self.strides,
            "pooling": None,
            "compnode": "npu",
            # TODO: Remove data ratio.
            "data_ratio": 255,
        }
