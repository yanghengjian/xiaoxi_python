from typing import Any, Dict, Optional
from fastapi.responses import JSONResponse
import json
class AjaxResult:
    CODE_TAG = "code"
    MSG_TAG = "msg"
    DATA_TAG = "data"
    SUCCESS_CODE = 200  # HttpStatus.SUCCESS equivalent
    ERROR_CODE = 500    # HttpStatus.ERROR equivalent

    def __init__(self, code: int = None, msg: str = None, data: Any = None):
        self._response = {}
        if code is not None:
            self._response[self.CODE_TAG] = code
        if msg is not None:
            self._response[self.MSG_TAG] = msg
        if data is not None:
            self._response[self.DATA_TAG] = data

    @staticmethod
    def success(msg: str = "操作成功", data: Any = None) -> 'AjaxResult':
        return AjaxResult(AjaxResult.SUCCESS_CODE, msg, data)

    @staticmethod
    def success_by_code(code: int, msg: str, data: Any = None) -> 'AjaxResult':
        return AjaxResult(AjaxResult.SUCCESS_CODE, "", AjaxResult(code, msg, data)._response)

    @staticmethod
    def error(msg: str = "操作失败", data: Any = None) -> 'AjaxResult':
        return AjaxResult(AjaxResult.ERROR_CODE, msg, data)

    @staticmethod
    def error_with_code(code: int, msg: str) -> 'AjaxResult':
        return AjaxResult(code, msg)

    def put(self, key: str, value: Any) -> 'AjaxResult':
        self._response[key] = value
        return self

    def to_dict(self) -> Dict[str, Any]:
        return self._response

    def to_response(self) -> JSONResponse:
        # Ensure the data can be serialized to JSON
        json_data = json.dumps(self.to_dict(), ensure_ascii=False, default=str)
        return JSONResponse(content=json.loads(json_data))

# Example usage
if __name__ == "__main__":
    success_result = AjaxResult.success("操作成功", {"key": "value"})
    print(success_result.to_dict())

    error_result = AjaxResult.error("操作失败")
    print(error_result.to_dict())
