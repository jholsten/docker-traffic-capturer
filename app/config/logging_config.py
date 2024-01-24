import logging


class LoggerFormatter(logging.Formatter):
    """Custom formatter for log outputs.
    Includes log level, package name and message and aligns info."""

    def format(self, record: logging.LogRecord) -> str:
        time = self.formatTime(record, self.datefmt)
        log_level = self._set_to_width(record.levelname, width=7)
        package = self._get_shortened_package_name(record)
        return f"{time}  {log_level} {package} {record.getMessage()}"

    def _set_to_width(self, value: str, width: int) -> str:
        """Sets the given value to the given width and adds padding if necessary."""
        padding = width - len(value)
        return f"{value} {''.ljust(padding)}"

    def _get_shortened_package_name(self, record: logging.LogRecord) -> str:
        """Returns the package name with format `[{logger_name}.{function}:{line}]`.
        Shortens logger name if necessary."""
        width = 70
        name = record.name
        if len(self._get_package_name(name, record.funcName, record.lineno)) > width:
            name_parts = name.split(".")
            for i in range(len(name_parts)):
                length = len(self._get_package_name(".".join(name_parts), record.funcName, record.lineno))
                if length > width:
                    name_parts[i] = name_parts[i][:1]
                else:
                    break
            name = ".".join(name_parts)

        return self._set_to_width(self._get_package_name(name, record.funcName, record.lineno), width=width)

    def _get_package_name(self, name: str, function: str, line: int) -> str:
        """Returns package name with format `[{logger_name}.{function}:{line}]`."""
        return f"[{name}.{function}:{line}]"


def configure_root_logger():
    """Configures root logger to use the custom formatter."""
    logger = logging.getLogger()
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    logging.getLogger("app").setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(LoggerFormatter())
    logger.addHandler(stream_handler)


def get_logger(name: str) -> logging.Logger:
    """Returns configured logger with the given name."""
    return logging.getLogger("app").getChild(name)
