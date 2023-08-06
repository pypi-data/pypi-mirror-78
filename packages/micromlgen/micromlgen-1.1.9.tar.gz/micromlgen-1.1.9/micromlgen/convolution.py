from micromlgen.utils import jinja


def port_convolution2d(input_shape, kernel, suffix=''):
    """Port optimized convolution 2D"""
    W, H = input_shape
    k = int(kernel.shape[0] / 2)
    return jinja('convolution/convolution2d.jinja', locals())