#!/usr/bin/env python3
"""

This package contains a class that will create and maintain a logging device for you

Returns:
    InspyLogger: A colored and formatted logging device.

"""

import logging, colorlog, inspect
from colorlog import ColoredFormatter
from logging import DEBUG, INFO, WARNING, getLogger, Logger

LEVELS = ["debug", "info", "warning"]
"""The names of the log output levels one can pick from"""


class InspyLogger(Logger):
    """
        Starts a colored and formatted logging device for you.

        Starts a colored and formatted logging device for you. No need to worry about handlers, etc

        Args:

            device_name (str): A string containing the name you'd like to choose for the root logger

            log_level (str): A string containing the name of the level you'd like InspyLogger to be limited to. You can choose between:

              - debug
              - info
              - warning

       """

    def adjust_level(self, l_lvl='info', silence_notif=False):
        """

        Adjust the level of the logger associated with this instance.

        Args:
            l_lvl (str): A string containing the name of the level you'd like InspyLogger to be limited to. You can choose between:

              - debug
              - info
              - warning

            silence_notif (bool): Silence notifications (of 'info' level) when adjusting the logger's level. True for
            no output and False to get these notifications.

        Returns:
            None

        """

        _log = getLogger(self.root_name)

        _caller = inspect.stack()[1][3]

        if self.last_lvl_change_by is None:
            _log.info('Setting logger level for first time')
            _log.debug('Signing in')
            self.last_lvl_change_by = 'Starting Logger'
        else:
            if not silence_notif:
                _log.info(f'{_caller} is changing logger level from {self.l_lvl} to {l_lvl}')
                _log.info(f'Last level change was implemented by: {self.last_lvl_change_by}')
                _log.info(f'Updating last level changer')

            self.last_lvl_change_by = _caller

        self.l_lvl = l_lvl

        if self.l_lvl == "debug":
            _ = DEBUG
        elif self.l_lvl == "info":
            _ = INFO
        elif self.l_lvl == "warn" or self.l_lvl == "warning":
            _ = WARNING

        _log.setLevel(_)

    def start(self):
        """

        Start the actual logging instance and fill the attributes that __init__ creates.

        Returns:
            None

        """
        if self.started:
            self.device.warning(
                "There already is a base logger for this program. I am using it to deliver this message."
            )
            return None

        formatter = ColoredFormatter(
            "%(bold_cyan)s%(asctime)-s%(reset)s%(log_color)s::%(name)s.%(module)-14s::%(levelname)-10s%(reset)s%("
            "blue)s%(message)-s",
            datefmt=None,
            reset=True,
            log_colors={
                "DEBUG": "bold_cyan",
                "INFO": "bold_green",
                "WARNING": "bold_yellow",
                "ERROR": "bold_red",
                "CRITICAL": "bold_red",
            },
        )

        self.device = logging.getLogger(self.root_name)
        self.main_handler = logging.StreamHandler()
        self.main_handler.setFormatter(formatter)
        self.device.addHandler(self.main_handler)
        self.adjust_level(self.l_lvl)
        self.device.info(f"Logger started for %s" % self.root_name)
        self.started = True

        return self.device

    def __init__(self, device_name, log_level):
        """

        Starts a colored and formatted logging device for you. No need to worry about handlers, etc

        Args:

            device_name (str): A string containing the name you'd like to choose for the root logger

            log_level (str): A string containing the name of the level you'd like InspyLogger to be limited to.

            You can choose between:
              - debug
              - info
              - warning
        """

        if log_level is None:
            log_level = "info"
        self.l_lvl = log_level.lower()
        self.root_name = device_name
        self.started = False
        self.last_lvl_change_by = None
        self.device = None
