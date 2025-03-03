from typing import Any
from fastapi.responses import JSONResponse


class SubsonicResponse:
    def __init__(self) -> None:
        self.data: dict[str, Any] = {
            "status": "ok",
            "version": "1.16.1",
            "type": "MusicRitmo",
            "serverVersion": "0.1",
            "openSubsonic": True,
        }

    def set_error(self, code: int, message: str) -> None:
        self.data["status"] = "failed"
        self.data["error"] = {"code": code, "message": message}

    def to_json_rsp(self) -> JSONResponse:
        return JSONResponse({"subsonic-response": self.data})
