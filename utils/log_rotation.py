import logging
from logging.handlers import TimedRotatingFileHandler

def get_rotating_file_handler(
    log_path,
    when="midnight",          # Rotate at midnight (daily)
    interval=1,               # Every 1 day
    backup_count=14,          # Keep 14 log files (2 weeks)
    level=logging.INFO
):
    """
    Returns a TimedRotatingFileHandler for daily/weekly log rotation.
    :param log_path: Path to the log file.
    :param when: "midnight" for daily, "W0" for weekly (Monday), etc.
    :param interval: Interval for rotation.
    :param backup_count: How many rotated logs to keep.
    :param level: Log level (default: INFO).
    """
    handler = TimedRotatingFileHandler(
        log_path,
        when=when,
        interval=interval,
        backupCount=backup_count,
        encoding="utf-8"
    )
    handler.setLevel(level)
    return handler
