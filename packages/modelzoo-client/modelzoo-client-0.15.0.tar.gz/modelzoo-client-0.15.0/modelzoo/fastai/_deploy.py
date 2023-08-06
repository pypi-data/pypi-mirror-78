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
from typing import Optional

import fastai.learner

from modelzoo import deploy_lib, ResourcesConfig, util


def deploy(
    learner: fastai.learner.Learner,
    model_name: Optional[str] = None,
    resources_config: Optional[ResourcesConfig] = None,
    api_key: Optional[str] = None,
    wait_until_healthy: bool = True,
) -> None:
    """
    Deploy a Fast AI Learner to your zoo.

    .. note::

        This function will serialize a model as a pickle file to a temporary
        directory on the filesystem before uploading it to Model Zoo.

    Args:
        model:
            A ``fastai.learner.Learner`` object to deploy.
        model_name:
            Optional string name of the model. If not provided, a random name
            will be generated. Model name must be unique across all of a user's
            models.
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

    Returns:
        The name of the created model.
    """
    model_name = model_name or util.generate_model_name()
    with tempfile.TemporaryDirectory() as tempdir:
        model_path = str(pathlib.Path(tempdir).joinpath("model.pkl"))
        learner.export(model_path)

        return deploy_lib.deploy_from_dir(
            model_name=model_name,
            model_dir=str(tempdir),
            api_key=api_key,
            wait_until_healthy=wait_until_healthy,
            resources_config=resources_config,
            documentation="",
            framework="FASTAI",
        )
