import logging

from ai_training_utils.path_helper import PathHelper
from ai_training_utils.singleton import Singleton


class Logger(Singleton):
    LOG_FILE_NAME = "logging.log"
    LOGGER_NAME = "root"

    def init(self) -> None:
        self.path_helper = PathHelper()
        self.logger = logging.getLogger(self.LOGGER_NAME)
        log_file_path = self.path_helper.get_logs_directory() + "/" + self.LOG_FILE_NAME
        try:
            file_handler = logging.FileHandler(
                filename=log_file_path
            )
        except Exception:
            raise IOError("Couldn't create/open file \"" + log_file_path + "\". Check permissions")

        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)-s] %(message)s"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)
