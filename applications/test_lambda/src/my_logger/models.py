from dataclasses import dataclass
from typing import Any, Optional
from datetime import datetime


@dataclass
class LogData:
    """
    ログデータの構造を表現するデータクラス
    """

    timestamp: datetime
    user_id: str
    action: str
    details: dict[str, Any]

    @classmethod
    def create(
        cls,
        user_id: Optional[str],
        action: Optional[str],
        details: Optional[dict[str, Any]] = None,
    ) -> "LogData":
        """新しいログデータインスタンスを作成する"""

        user_id = user_id or ""
        action = action or ""
        details = details or {}

        return cls(
            timestamp=datetime.now(),
            user_id=user_id,
            action=action,
            details=details,
        )
