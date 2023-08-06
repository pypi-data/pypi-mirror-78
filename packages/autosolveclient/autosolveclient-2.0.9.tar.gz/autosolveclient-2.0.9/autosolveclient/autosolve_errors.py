from enum import Enum


class AutoSolveConnectionError(Enum):
    CONNECTION_LOST_ERROR = "Connection lost, manual recovery expected"
    CONNECTION_REESTABLISH_FAILED = "Connection could not be re-established"
    CONNECTION_ERROR_INIT = "Connection error when initializing. Please retry"
    CONNECTION_CLOSED_UNEXPECTEDLY = "Connection closed unexpectedly."

