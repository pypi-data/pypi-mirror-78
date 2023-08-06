#  Copyright (C) 2020 Servly AI.
#  See the LICENCE file distributed with this work for additional
#  information regarding copyright ownership.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pathlib
import tempfile
import torch
from typing import Any, Optional, Tuple

from modelzoo import deploy_lib, exceptions, util, ResourcesConfig
from modelzoo.torch import util as torch_util


def deploy(
    model: torch.nn.Module,
    args: Tuple[Any],
    model_name: Optional[str] = None,
    resources_config: Optional[ResourcesConfig] = None,
    api_key: Optional[str] = None,
    wait_until_healthy: bool = True,
    **export_kwargs
) -> None:
    """
    Deploy a PyTorch ``torch.nn.Module`` to your zoo via ONNX.

    This function signature matches `torch.onnx.export
    <https://pytorch.org/docs/stable/_modules/torch/onnx.html#export>`_, except
    for the filename argument. Specifically, it requires a ``torch.nn.Module``
    and a tuple representing the input ``args`` to the model as the first two
    arguments. All other keyword arguments are optional.

    .. note::

        This function will serialize a model to a temporary directory on the
        filesystem before uploading it to Model Zoo.

    Args:
        model:
            A ``torch.nn.Module`` to deploy. Conforms to the semantics of
            `torch.onnx.export
            <https://pytorch.org/docs/stable/_modules/torch/onnx.html#export>`_.
        args:
            The inputs to the model, e.g., such that ``model(*args)`` is a
            valid invocation of the model.  Any non-Tensor arguments will be
            hard-coded into the exported model; any Tensor arguments will
            become inputs of the exported model, in the order they occur in
            args.  If args is a Tensor, this is equivalent to having called it
            with a 1-ary tuple of that Tensor. Conforms to the semantics of
            `torch.onnx.export
            <https://pytorch.org/docs/stable/_modules/torch/onnx.html#export>`_.
        resources_config:
            An optional :py:class:`modelzoo.ResourcesConfig` that specifies the
            resources (e.g.  memory, CPU) to use for the model. Defaults to
            ``modelzoo.ResourcesConfig()``.
        api_key:
            Optional API key that, if provided, will override the API key
            available to the environment.
        wait_until_healthy:
            If True (default), this function will refrain from returning until
            the model has reached a :py:class:`HEALTHY <modelzoo.ModelState>` state.
        **export_kwargs:
            All other keyword arguments are forwarded to `torch.onnx.export
            <https://pytorch.org/docs/stable/_modules/torch/onnx.html#export>`_.

    Returns:
        The name of the created model.
    """
    model_name = model_name or util.generate_model_name()

    if isinstance(model, torch.nn.Module):
        with tempfile.TemporaryDirectory() as tempdir:
            model_path = str(pathlib.Path(tempdir).joinpath("model.onnx"))
            torch.onnx.export(model, args, model_path, **export_kwargs)
            documentation = torch_util.generate_default_pytorch_docs(model_name)
            return deploy_lib.deploy_from_dir(
                model_name=model_name,
                model_dir=tempdir,
                resources_config=resources_config,
                documentation=documentation,
                framework="ONNX",
                api_key=api_key,
                wait_until_healthy=wait_until_healthy,
            )
    else:
        raise exceptions.InvalidArgumentError(
            "Model type is not supported: {}".format(type(model))
        )
