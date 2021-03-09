from typing import Any


class Response:
    class Type:
        STRING = 0
        ERROR = 1
        PERCENT = 2
        SEPARATOR = 3

    def __init__(self, body: Any, response_type=Type.STRING):
        self.body = body
        self.response_type = response_type
