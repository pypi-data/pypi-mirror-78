import random

import numpy
import tensorflow
import torch
import pandas
import pytest

from . import utils
from wandb import util


def pt_variable(nested_list, requires_grad=True):
    v = torch.autograd.Variable(utils.pytorch_tensor(nested_list))
    v.requires_grad = requires_grad
    return v


def r():
    return random.random()


def l(*shape):
    """Makes a nested list of lists with a "shape" argument like numpy,
    TensorFlow, etc.
    """
    if not shape:
        # reduce precision so we can use == for comparison regardless
        # of conversions between other libraries
        return float(numpy.float16(random.random()))
    else:
        return [l(*shape[1:]) for _ in range(shape[0])]


def json_friendly_test(orig_data, obj):
    data, converted = util.json_friendly(obj)
    utils.assert_deep_lists_equal(orig_data, data)
    assert converted


def tensorflow_json_friendly_test(orig_data):
    with tensorflow.Session().as_default() as s:
        json_friendly_test(
            orig_data, tensorflow.convert_to_tensor(orig_data))
        v = tensorflow.Variable(tensorflow.convert_to_tensor(orig_data))
        s.run(tensorflow.global_variables_initializer())
        json_friendly_test(orig_data, v)


@pytest.mark.skipif(utils.OLD_PYTORCH, reason='0d tensors not supported until 0.4')
def test_pytorch_json_0d():
    a = l()
    json_friendly_test(a, utils.pytorch_tensor(a))
    json_friendly_test(a, pt_variable(a))


def test_pytorch_json_1d_1x1():
    a = l(1)
    json_friendly_test(a, utils.pytorch_tensor(a))
    json_friendly_test(a, pt_variable(a))


def test_pytorch_json_1d():
    a = l(3)
    json_friendly_test(a, utils.pytorch_tensor(a))
    json_friendly_test(a, pt_variable(a))


def test_pytorch_json_1d_large():
    a = l(300)
    json_friendly_test(a, utils.pytorch_tensor(a))
    json_friendly_test(a, pt_variable(a))


def test_pytorch_json_2d():
    a = l(3, 3)
    json_friendly_test(a, utils.pytorch_tensor(a))
    json_friendly_test(a, pt_variable(a))


def test_pytorch_json_2d_large():
    a = l(300, 300)
    json_friendly_test(a, utils.pytorch_tensor(a))
    json_friendly_test(a, pt_variable(a))


def test_pytorch_json_3d():
    a = l(3, 3, 3)
    json_friendly_test(a, utils.pytorch_tensor(a))
    json_friendly_test(a, pt_variable(a))


def test_pytorch_json_4d():
    a = l(3, 3, 3, 3)
    json_friendly_test(a, utils.pytorch_tensor(a))
    json_friendly_test(a, pt_variable(a))


def test_pytorch_json_nd():
    a = l(1, 1, 1, 1, 1, 1, 1, 1)
    json_friendly_test(a, utils.pytorch_tensor(a))
    json_friendly_test(a, pt_variable(a))


def test_pytorch_json_nd_large():
    a = l(3, 3, 3, 3, 3, 3, 3, 3)
    json_friendly_test(a, utils.pytorch_tensor(a))
    json_friendly_test(a, pt_variable(a))


def test_tensorflow_json_0d():
    tensorflow_json_friendly_test(l())


def test_tensorflow_json_1d_1x1():
    tensorflow_json_friendly_test(l(1))


def test_tensorflow_json_1d():
    tensorflow_json_friendly_test(l(3))


def test_tensorflow_json_1d_large():
    tensorflow_json_friendly_test(l(300))


def test_tensorflow_json_2d():
    tensorflow_json_friendly_test(l(3, 3))


def test_tensorflow_json_2d_large():
    tensorflow_json_friendly_test(l(300, 300))


def test_tensorflow_json_nd():
    tensorflow_json_friendly_test(l(1, 1, 1, 1, 1, 1, 1, 1))


def test_tensorflow_json_nd_large():
    tensorflow_json_friendly_test(l(3, 3, 3, 3, 3, 3, 3, 3))


def test_image_from_docker_args_simple():
    image = util.image_from_docker_args([
        "run", "-v", "/foo:/bar", "-e", "NICE=foo", "-it", "wandb/deepo", "/bin/bash"])
    assert image == "wandb/deepo"


def test_image_from_docker_args_simple_no_namespace():
    image = util.image_from_docker_args([
        "run", "-e", "NICE=foo", "nginx", "/bin/bash"])
    assert image == "nginx"


def test_image_from_docker_args_simple_no_equals():
    image = util.image_from_docker_args([
        "run", "--runtime=runc", "ufoym/deepo:cpu-all"])
    assert image == "ufoym/deepo:cpu-all"


def test_image_from_docker_args_simple_no_namespace():
    image = util.image_from_docker_args([
        "run", "ufoym/deepo:cpu-all", "/bin/bash", "-c", "python train.py"])
    assert image == "ufoym/deepo:cpu-all"


def test_image_from_docker_args_sha():
    image = util.image_from_docker_args(
        ["wandb/deepo@sha256:3ddd2547d83a056804cac6aac48d46c5394a76df76b672539c4d2476eba38177"])
    assert image == "wandb/deepo@sha256:3ddd2547d83a056804cac6aac48d46c5394a76df76b672539c4d2476eba38177"
