import pathlib
import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv


load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")
D_GUILD_ID = os.getenv("GUILD_ID")
D_TESTGUILD_ID = int(os.getenv("TESTGUILD_ID"))
D_REPORT_CHAN_ID = int(os.getenv("REPORT_CHANNEL_ID"))
D_REP_MENU_BUILD_ROLE = os.getenv("DISCORD_CALL_REPORTMENU_REQUIRED_ROLE")
D_TIMEOUT_USE_ROLE = os.getenv("DISCORD_TIMEOUT_POLL_REQUIRED_ROLE")

DB_DATABASE = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = os.getenv("DB_URI")


BASE_DIR = pathlib.Path(__file__).parent


CMDS_DIR = BASE_DIR / "cmds"
COGS_DIR = BASE_DIR / "cogs"
TESTCOGS_DIR = BASE_DIR / "testcogs"
CUSTOM_CLASSES_DIR = BASE_DIR / "custom_classes"


LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {"format": "%(levelname)-10s - %(name)-15s : %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "bot": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)
