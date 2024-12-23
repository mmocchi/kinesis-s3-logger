from typing import Protocol, Dict, Any


class LogWriter(Protocol):
    """ログ書き込みの抽象インターフェース"""

    def write_log(self, log_data: Dict[str, Any]) -> None:
        """
        ログデータを書き込む

        Args:
            log_data: 書き込むログデータ

        """
        pass
