import tensorflow as tf
from tensorflow.keras import layers
from axion_tensorflow import fake_quant


@tf.keras.utils.register_keras_serializable(package="Axion")
class GlobalAveragePooling2D(layers.Layer):
    """ Quantization aware GlobalAveragePooling2D. """

    def __init__(
        self,
        num_bits=4,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.num_bits = num_bits

    def build(self, input_shape):
        pass

    def call(self, inputs):
        x = tf.reduce_mean(inputs, axis=[2, 3])
        x = fake_quant._fake_quant(x, self.num_bits)
        return x

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "num_bits": self.num_bits,
            }
        )
        return config

    def get_bitmeta(self):

        return {
            "name": self.name,
            "type": "global_pooling",
            "mode": "average",
            "input": [],
            "of_bit": self.num_bits,
            "compnode": "npu",
        }
