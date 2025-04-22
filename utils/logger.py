# utils/logger.py

import logging

class Logger:
    _logger = None

    @staticmethod
    def setup_logger():
        if Logger._logger is None:
            Logger._logger = logging.getLogger("PortMasterLogger")
            Logger._logger.setLevel(logging.INFO)

            # Prevent adding multiple handlers
            if not Logger._logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                Logger._logger.addHandler(handler)

        return Logger._logger

    @staticmethod
    def log_info(message: str):
        Logger.setup_logger().info(message)

    @staticmethod
    def log_error(message: str):
        Logger.setup_logger().error(message)

    @staticmethod
    def log_success(message: str):
        Logger.setup_logger().info(f"[+] {message}")
