from my_logger.interfaces import LogFormatter
from my_logger.models import LogData
from typing import Any


class JsonFormatter(LogFormatter):
    """JSON形式のフォーマッターの実装"""

    def format(self, log_data: LogData) -> dict[str, Any]:
        """
        LogDataをJSON形式にフォーマットする

        Args:
            log_data (LogData): ログデータ

        Returns:
            dict[str, Any]: フォーマットされたJSON形式のログデータ
        """
        return {
            "timestamp": log_data.timestamp.isoformat(),
            "user_id": log_data.user_id,
            "action": log_data.action,
            "details": log_data.details,
        }
