import logging
import json
import sys


class JSONFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",    # Cyan
        "INFO": "\033[34m",     # ← Синий (Blue)
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",    # Red
        "CRITICAL": "\033[35m", # Magenta
    }
    RESET = "\033[0m"

    def __init__(self, colored: bool = False):
        super().__init__()
        self.colored = colored

    def format(self, record):
        log = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }

        if hasattr(record, "log_data"):
            log.update(record.log_data)

        output = json.dumps(log, ensure_ascii=False)

        if self.colored:
            color = self.COLORS.get(record.levelname, "")
            output = f"{color}{output}{self.RESET}"

        return output
    
def setup_logging(colored: bool = False):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter(colored=colored))
    logging.basicConfig(level=logging.INFO, handlers=[handler])
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)