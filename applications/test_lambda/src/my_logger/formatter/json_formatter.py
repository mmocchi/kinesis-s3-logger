from typing import Any

from my_logger.interfaces import LogFormatter
from my_logger.models import LogData


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
        return log_data.to_dict()
