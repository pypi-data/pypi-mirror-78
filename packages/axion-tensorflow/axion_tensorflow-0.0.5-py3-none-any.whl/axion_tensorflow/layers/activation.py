import tensorflow as tf
from tensorflow import nn
from tensorflow.keras import layers
from tensorflow.python.keras import initializers
from axion_tensorflow import fake_quant


@tf.keras.utils.register_keras_serializable(package="Axion")
class Activation(layers.Layer):
    """Activation clips and fake qunatizes the inputs into range [0.0, 1.0].
    Optionally the input could be scaled.
    """

    def __init__(
        self,
        multiplier=1.0,
        activation_bits=8,
        beta_initializer="zeros",
        gamma_initializer="ones",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.multiplier = multiplier
        self.activation_bits = activation_bits
        self.beta_initializer = initializers.get(beta_initializer)
        self.gamma_initializer = initializers.get(gamma_initializer)

    def build(self, input_shape):
        # Assuming NCHW data format.
        C = input_shape[1]

        self.beta = self.add_weight(
            name="beta",
            shape=(C,),
            initializer=self.beta_initializer,
        )
        self.gamma = self.add_weight(
            name="gamma",
            shape=(C,),
            initializer=self.gamma_initializer,
        )

    def call(self, inputs):
        input_shape = inputs.shape
        broadcast_shape = [1] * len(input_shape)
        broadcast_shape[1] = input_shape[1]  # NCHW
        beta = tf.reshape(self.beta, broadcast_shape)
        gamma = tf.reshape(self.gamma, broadcast_shape)

        x = gamma * inputs + beta
        if self.activation_bits > 0:
            x = fake_quant.fake_quant_activation(
                x, self.multiplier, num_bits=self.activation_bits
            )
        return x

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "multiplier": self.multiplier,
                "activation_bits": self.activation_bits,
                "beta_initializer": initializers.serialize(self.beta_initializer),
                "gamma_initializer": initializers.serialize(self.gamma_initializer),
            }
        )
        return config
