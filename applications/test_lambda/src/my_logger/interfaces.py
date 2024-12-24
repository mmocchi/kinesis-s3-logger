from typing import Protocol, Any
from my_logger.models import LogData


class LogWriter(Protocol):
    """ログ書き込みの抽象インターフェース"""

    def write_log(self, log_data: dict[str, Any]) -> None:
        """
        ログデータを書き込む

        Args:
            log_data: 書き込むログデータ

        """
        ...


class LogFormatter(Protocol):
    """ログフォーマッターの抽象インターフェース"""

    def format(self, log_data: LogData) -> dict[str, Any]:
        """ログデータをフォーマットする"""
        ...


class Logger(Protocol):
    """ロガーインターフェース"""

    def info(self, log_data: LogData) -> None:
        """ログを書き込む"""
        ...
