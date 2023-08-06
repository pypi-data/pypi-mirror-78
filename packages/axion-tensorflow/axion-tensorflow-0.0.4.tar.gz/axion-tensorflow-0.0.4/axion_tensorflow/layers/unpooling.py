import tensorflow as tf
from tensorflow.keras import layers


@tf.keras.utils.register_keras_serializable(package="Axion")
class Unpooling2D(layers.Layer):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def build(self, input_shape):
        pass

    def call(self, inputs):
        N = -1
        C = inputs.get_shape().as_list()[1]
        h, w = tf.shape(inputs)[2], tf.shape(inputs)[3]
        mask = tf.reshape(tf.constant([[1.0, 0.0], [0.0, 0.0]]), [1, 1, 1, 2, 1, 2])
        x = tf.reshape(inputs, [N, C, h, 1, w, 1]) * mask
        x = tf.reshape(x, [N, C, h * 2, w * 2])
        return x

    def get_config(self):
        config = super().get_config()
        return config

    def get_bitmeta(self):
        return {
            "name": self.name,
            "type": "unpool",
            "input": [],
            "compnode": "npu",
        }
