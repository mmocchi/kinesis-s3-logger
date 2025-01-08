from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


def format_timestamp(timestamp: datetime) -> str:
    formatted_timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    if formatted_timestamp[-5:].startswith(("-", "+")):
        formatted_timestamp = formatted_timestamp[:-2] + ":" + formatted_timestamp[-2:]
    return formatted_timestamp


@dataclass
class UserInfo:
    user_id: str
    user_name: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "userId": self.user_id,
            "userName": self.user_name,
        }


@dataclass
class RequestInfo:
    request_id: str
    endpoint: str
    method: str
    parameters: list[Parameter]

    def to_dict(self) -> dict[str, Any]:
        return {
            "requestId": self.request_id,
            "endpoint": self.endpoint,
            "method": self.method,
            "parameters": [parameter.to_dict() for parameter in self.parameters],
        }


@dataclass
class Parameter:
    key: str
    value: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "value": self.value,
        }


@dataclass
class AccessInfo:
    text: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
        }


@dataclass
class ResultInfo:
    status: str
    error_message: Optional[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "errorMessage": self.error_message,
        }


@dataclass
class LogData:
    """
    ログデータの構造を表現するデータクラス
    """

    id: uuid.UUID
    timestamp: datetime
    user_info: UserInfo
    request_info: RequestInfo
    access_info: list[AccessInfo]
    result_info: ResultInfo

    def to_dict(self) -> dict[str, Any]:
        formatted_timestamp = format_timestamp(self.timestamp)

        return {
            "id": str(self.id),
            "timestamp": formatted_timestamp,
            "userInfo": self.user_info.to_dict(),
            "requestInfo": self.request_info.to_dict(),
            "accessInfo": [access_info.to_dict() for access_info in self.access_info],
            "resultInfo": self.result_info.to_dict(),
        }
