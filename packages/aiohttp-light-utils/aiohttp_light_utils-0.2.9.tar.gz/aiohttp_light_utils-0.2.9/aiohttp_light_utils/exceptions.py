class RpcClientError(Exception):
    def __init__(self, code: str, status_code: int = None) -> None:
        super().__init__("Received {} code".format(code))
        self.code = code
        self.status_code = status_code
