"""
Application-wide logging setup

Sources:
https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/
https://medium.com/1mgofficial/
    how-to-override-uvicorn-logger-in-fastapi-using-loguru-124133cdcd4e
"""

import os
import sys
import logging
import loguru


LOG_LEVEL = logging.getLevelName(
    os.environ.get("OWS_AP_LOG_LEVEL", "DEBUG")
)
FORMAT_PLAIN = (
    "{level: <8} | "
    "{time:YYYY-MM-DD hh:mm:ss} | "
    "{name} - {message}"
)
FORMAT_COLOR = (
    "<level>{level: <8}</level> | "
    "{time:YYYY-MM-DD hh:mm:ss} | "
    "{name} - {message}"
)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = loguru.logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru.logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage()
        )


async def setup_logging():
    # Intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)

    # Remove every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # Configure loguru
    curdir = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(curdir, ".", "logs", "bot-{time}.log")
    handlers = [
        {"sink": sys.stdout, "format": FORMAT_COLOR, "colorize": True},
        {
            "sink": logdir,
            "rotation": "1 week",
            "format": FORMAT_PLAIN,
            "colorize": False,
        },
    ]
    loguru.logger.configure(handlers=handlers)
