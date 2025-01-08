from my_logger.interfaces import LogFormatter, Logger, LogWriter
from my_logger.models import LogData


class MyLogger(Logger):
    """ロガー実装"""

    def __init__(self, writer: LogWriter, formatter: LogFormatter) -> None:
        """
        ロガーの初期化

        Args:
            writer (LogWriter): ログ出力の実装
            formatter (LogFormatter): ログデータのフォーマッター
        """
        self.writer = writer
        self.formatter = formatter

    def info(self, log_data: LogData) -> None:
        """
        ログデータをフォーマットしてログ出力する

        Args:
            log_data (LogData): ログデータ
        """
        formatted_log_data = self.formatter.format(log_data)
        self.writer.write_log(formatted_log_data)


class MultiLogger(Logger):
    """複数のロガーを管理するロガー"""

    def __init__(self, loggers: list[Logger]) -> None:
        self.loggers = loggers

    def info(self, log_data: LogData) -> None:
        for logger in self.loggers:
            logger.info(log_data)
