import tensorflow as tf


def _fake_quant(x, num_bits):
    """Emulate the hardware quantization in float.
    The input x must be in range [0, 1.0], inclusive.

    Please note that we intentionally do not nudge quantized x to exact zero
    to mimic the hardware behavior.

    Returns:
        Fake-quantized x.
    """
    m = 2.0 ** num_bits - 1.0
    return tf.floor(x * m + 0.5) / m


def _identity_grad(dy):
    return dy


def fake_quant_weights(w, num_bits):
    """Special case for fake-quantization of weights.

    Returns:
        Fake-quantized w.
    """
    w = tf.tanh(w)
    # We do not use an epsilon for scale here, as a 0. scale indicates our training has gone wrong.
    # Stop gradient to prevent accidental updates.
    scale = tf.stop_gradient(tf.reduce_mean(tf.abs(w)))

    @tf.custom_gradient
    def ste(w):
        # Normalize scale to [-1.0, 1.0].
        w = w / scale
        w = tf.clip_by_value(w, -1.0, 1.0)
        # Convert the range to [0, 1.0], fake quant, then convert back to [-1., 1.].
        w = w / 2 + 0.5
        w = _fake_quant(w, num_bits)
        w = (w - 0.5) * 2
        # Restore scale.
        w = w * scale
        return w, _identity_grad

    return ste(w), scale


def fake_quant_activation(a, multiplier, num_bits):
    """Special case for fake-quantizing activations.

    Returns:
        Fake-quantized a.
    """
    a = tf.clip_by_value(a * multiplier, 0.0, 1.0)

    @tf.custom_gradient
    def ste(a):
        return _fake_quant(a, num_bits), _identity_grad

    return ste(a)
