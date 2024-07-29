from loguru import logger


def get_logger():
    logger.remove()  # Remove the default logger to avoid logging to the terminal
    logger.add(
        "./logs/logfile.log",
        rotation="1 MB",
        retention="10 days",
        compression="zip",
        level="DEBUG",
        format="{time} <{level}> {message}",
        enqueue=True,
        catch=True,
    )
    logger.add(
        "./logs/error.log",
        rotation="1 MB",
        retention="10 days",
        compression="zip",
        level="ERROR",
        format="{time} <{level}> {message}",
        enqueue=True,
        catch=True,
    )

    return logger
