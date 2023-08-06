import enum


class ModelState(str, enum.Enum):
    """
    Represents the possible states of a model in the zoo. Use
    :py:func:`modelzoo.start()` and :py:func:`modelzoo.stop()` to change the
    state of a model.

    HEALTHY:
        The model is ready to make predictions.
    STOPPED:
        The model is stopped.
    STARTING:
        The model is transitioning into a HEALTHY state but not yet ready to
        make predictions.
    STOPPING:
        The model is transitioning into a STOPPED state and will not be able to
        make predictions.
    ERROR:
        Something went wrong when loading the model.
    """

    HEALTHY = "HEALTHY"
    STARTING = "STARTING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    ERROR = "ERROR"


TERMINAL_STATES = {ModelState.HEALTHY, ModelState.STOPPED, ModelState.ERROR}
