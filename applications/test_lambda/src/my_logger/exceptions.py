class LogWriteError(Exception):
    """ログ書き込み時の基底例外クラス"""

    pass


class KinesisWriteError(LogWriteError):
    """Kinesis Firehoseへの書き込み失敗時の例外"""

    def __init__(self, message: str, original_error: Exception) -> None:
        self.original_error = original_error
        super().__init__(f"Failed to write log to Kinesis: {message}")
