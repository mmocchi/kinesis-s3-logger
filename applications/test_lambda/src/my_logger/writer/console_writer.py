from my_logger.interfaces import LogWriter
from typing import Any
import json


class ConsoleWriter(LogWriter):
    """標準出力へのログ出力実装"""

    def write_log(self, log_data: dict[str, Any]) -> None:
        """
        ログデータを標準出力に出力する

        Args:
            log_data (dict[str, Any]): ログデータ
        """
        print(json.dumps(log_data, ensure_ascii=False))
