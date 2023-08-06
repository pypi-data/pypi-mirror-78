from typing import Any, Mapping

class ClientError(BaseException):
    MSG_TEMPLATE: str
    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Mapping[str, Any]
        self.operation_name: str
