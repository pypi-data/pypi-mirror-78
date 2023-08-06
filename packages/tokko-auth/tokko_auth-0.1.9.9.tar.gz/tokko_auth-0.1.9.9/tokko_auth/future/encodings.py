from dataclasses import dataclass


@dataclass(init=True)
class ErrorDataType:

    message: str
    exception: Exception = None
    status: int = None

    def __str__(self):

        exception = self.exception or Exception(self.message)
        status = self.status or "-"

        return f"{self.message} - " \
               f"{type(exception).__name__} " \
               f"[{status}]"

