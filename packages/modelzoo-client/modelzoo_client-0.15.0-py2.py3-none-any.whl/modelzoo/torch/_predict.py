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

from typing import Any, Dict, Optional

import onnx

from modelzoo import exceptions
from modelzoo import predict as base_predict


def _validate_tensor_input(data: Dict) -> bool:
    field_names = onnx.TensorProto.DESCRIPTOR.fields_by_name
    for k, v in data.items():
        if k not in field_names:
            raise exceptions.InvalidArgumentError(
                "Invalid tensor attribute: {}. Must be one of {}."
                "The input dictionary must parse into a valid "
                "onnx.TensorProto.".format(k, field_names.keys())
            )


def predict(
    model_name: str, inputs: Dict[str, Any], api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Send a prediction to a PyTorch model.

    The input data must be a Python dictionary that maps input string names to
    dictionaries that conform to the `onnx.TensorProto
    <https://github.com/onnx/onnx/blob/9b7c2b4f0b4a16a0cf31145eae9425abe7cbe2a9/onnx/onnx-ml.proto#L451>`_
    schema.  This function will do some lightweight validation of the input
    data dictionaries before making the prediction request.

    Args:
        model_name: String name of the model.
        inputs:
            A Python dictionary that maps input string names to dictionaries
            that conform to the `onnx.TensorProto
            <https://github.com/onnx/onnx/blob/9b7c2b4f0b4a16a0cf31145eae9425abe7cbe2a9/onnx/onnx-ml.proto#L451>`_
            schema.
        api_key: Will override the environment api key, if present.

    Returns:
        The output prediction

    **Examples**:

        Send a prediction to a model with a single input layer that accepts a
        float array with a shape of [1, 3, 224, 224]::

            modelzoo.torch.predict(
                model_name="model",
                {
                    "input": {
                        "dims": [1, 3, 224, 224],
                        "data_type": onnx.TensorProto.DataType.FLOAT,
                        "float_data": image_data
                    }
                }
            )
    """

    for val in inputs.values():
        _validate_tensor_input(val)

    return base_predict(
        model_name, {"inputs": inputs}, headers={"Accept": "application/json"}
    )
