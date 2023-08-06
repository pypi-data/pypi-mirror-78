# -*- coding: utf-8 -*-
u"""Telegram Notifier module for SecureTea.

Project:
    ╔═╗┌─┐┌─┐┬ ┬┬─┐┌─┐╔╦╗┌─┐┌─┐
    ╚═╗├┤ │  │ │├┬┘├┤  ║ ├┤ ├─┤
    ╚═╝└─┘└─┘└─┘┴└─└─┘ ╩ └─┘┴ ┴

    Author: Mishal Shah <shahmishal1998@gmail.com> , Jan 26 2019
    Version: 1.1
    Module: SecureTea

"""
import telegram

from securetea import common
from securetea import logger


class SecureTeaTelegram():
    """Initialize the telegram."""

    modulename = "Telegram"
    enabled = True

    def __init__(self, cred, debug):
        """Init Telegram params.

        Args:
            debug (bool): Log on terminal or not
            cred (dict): Telegram user_id
        """
        self.logger = logger.SecureTeaLogger(
            self.modulename,
            debug
        )
        self.enabled = common.check_config(cred)
        if not self.enabled:
            self.logger.log(
                "Credentials not present, please set Telegram config at ~/.securetea/securetea.conf ",
                logtype="error"
            )

        self.token = cred['token']
        self.user_id = cred['user_id']

    def notify(self, msg):
        """
        Send the notification.

        Args:
            msg (str): Message to send

        Raises:
            None

        Returns:
            None
        """
        message = (str(msg) + " at " + common.getdatetime() +
                   " " + common.get_current_location() + common.get_platform())

        bot = telegram.Bot(token=self.token)
        bot.send_message(chat_id=self.user_id, text=message)
        self.logger.log(
            "Notification sent"
        )
        return
