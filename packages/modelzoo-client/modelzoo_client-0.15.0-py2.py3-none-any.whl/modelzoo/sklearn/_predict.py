from typing import Any, Dict, Optional

import numpy as np

from modelzoo import predict as base_predict


def predict(
    model_name: str,
    input_value: np.ndarray,
    return_prediction: bool = True,
    return_probabilities: bool = False,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send a prediction to a scikit-learn model.


    Args:
        model_name: String name of the model.
        input_value:
            A ``numpy.ndarray`` to use for prediction. The input data should
            conform to the shape expected by the model.
        return_prediction:
            Boolean (default: True) that specifies whether to return the
            prediction, e.g. the result from ``model.predict()``.
        return_probabilities:
            Boolean (default: False) that specifies whether to return a
            full dictionary of class names to probabilities , e.g. the
            result from ``model.predict_proba()``.
        api_key: Will override the environment api key, if present.

    Returns:
        An output dictionary containing one or both of the following, depending
        on whether ``return_prediction`` and/or ``return_probabilities`` were
        specified.

        * ``"prediction"``
            A list of predictions, e.g. the value returned by
            ``model.predict``.
        * ``"probabilities"``
            A list of dictionaries representing label probabilities, e.g.
            similar to the value returned by ``model.predict_proba``. Each
            dictionary maps class label strings to the respective probability
            for that label.
    """

    # Numpy arrays are not JSON serializable: convert to a native Python list
    # that can be serialized.
    if isinstance(input_value, np.ndarray):
        input_value = input_value.tolist()

    response = base_predict(
        model_name,
        {
            "input": input_value,
            "return_prediction": return_prediction,
            "return_probabilities": return_probabilities,
        },
        api_key=api_key,
    )

    return response
