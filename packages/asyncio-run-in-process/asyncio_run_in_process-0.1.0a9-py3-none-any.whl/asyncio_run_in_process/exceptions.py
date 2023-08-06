class BaseRunInProcessException(Exception):
    pass


class ProcessKilled(BaseRunInProcessException):
    pass


class InvalidState(BaseRunInProcessException):
    pass


class ChildCancelled(BaseRunInProcessException):
    pass
