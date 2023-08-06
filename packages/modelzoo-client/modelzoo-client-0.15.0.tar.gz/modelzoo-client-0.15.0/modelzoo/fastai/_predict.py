from typing import Any, Optional

from modelzoo import predict as base_predict


def predict(model_name: str, input_value: Any, api_key: Optional[str] = None,) -> Any:
    """
    Send a prediction to a FastAI Learner.

    Args:
        model_name: String name of the model.
        input_value:
            A value to send for a prediction, e.g. a value that would be passed to
            ``model.predict()``. Must be JSON-serializable.
        api_key: Will override the environment api key, if present.

    Returns:
        The output value returned by the model.
    """
    response = base_predict(model_name, {"input": input_value}, api_key=api_key,)
    return response.get("response")
