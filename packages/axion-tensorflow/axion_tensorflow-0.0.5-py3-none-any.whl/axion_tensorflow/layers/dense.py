import numpy as np
import tensorflow as tf
from tensorflow import linalg
from tensorflow import nn
from tensorflow.keras import layers
from tensorflow.keras import initializers
from axion_tensorflow import fake_quant


@tf.keras.utils.register_keras_serializable(package="Axion")
class Dense(layers.Layer):
    """ Quantization aware Dense. """

    def __init__(
        self,
        units,
        kernel_bits=4,
        kernel_initializer="glorot_uniform",
        bias_initializer="zeros",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.units = units
        self.kernel_bits = kernel_bits
        self.kernel_initializer = initializers.get(kernel_initializer)
        self.bias_initializer = initializers.get(bias_initializer)

    def build(self, input_shape):
        unused_N, C = input_shape
        self.kernel = self.add_weight(
            "kernel",
            shape=(C, self.units),
            initializer=self.kernel_initializer,
        )
        self.bias = self.add_weight(
            "bias",
            shape=(self.units,),
            initializer=self.bias_initializer,
        )

    def call(self, inputs):
        q_kernel, unused_scale = fake_quant.fake_quant_weights(
            self.kernel, num_bits=self.kernel_bits
        )
        x = linalg.matmul(inputs, q_kernel)
        x = nn.bias_add(x, self.bias)
        return x

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "units": self.units,
                "kernel_bits": self.kernel_bits,
                "kernel_initializer": initializers.serialize(self.kernel_initializer),
                "bias_initializer": initializers.serialize(self.bias_initializer),
            }
        )
        return config

    def get_bitmeta(self):
        q_kernel, scale = fake_quant.fake_quant_weights(
            self.kernel, num_bits=self.kernel_bits
        )
        q_kernel = q_kernel / scale
        # bitmeta shape is (oc, ic), while tensorflow shape is (ic, oc).
        q_kernel = tf.transpose(q_kernel, perm=(1, 0))
        # special treatment for the current converter.
        q_kernel, scale = q_kernel / 2, scale * 2
        return {
            "name": self.name,
            "type": "dense",
            "if_bit": None,
            "w_bit": self.kernel_bits,
            "of_bit": 0,
            "input": [],
            "affine_k": np.zeros((self.units,), dtype=np.float32) + scale.numpy(),
            "affine_b": self.bias.numpy(),
            "weight": q_kernel.numpy(),
            "compnode": "npu",
            "data_ratio": 255,
        }
