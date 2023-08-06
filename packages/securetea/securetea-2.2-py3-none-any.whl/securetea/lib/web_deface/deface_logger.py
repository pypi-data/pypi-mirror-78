# -*- coding: utf-8 -*-
u"""DefaceLogger for SecureTea Web Deface Detection.

Project:
    ╔═╗┌─┐┌─┐┬ ┬┬─┐┌─┐╔╦╗┌─┐┌─┐
    ╚═╗├┤ │  │ │├┬┘├┤  ║ ├┤ ├─┤
    ╚═╝└─┘└─┘└─┘┴└─└─┘ ╩ └─┘┴ ┴
    Author: Abhishek Sharma <abhishek_official@hotmail.com> , Jun 26 2019
    Version: 1.4
    Module: SecureTea

"""

from securetea import logger
import time


class DefaceLogger(logger.SecureTeaLogger):
    """DefaceLogger Class."""

    def __init__(self, modulename, debug=False):
        """
        Initialize DefaceLogger.

        Args:
            modulename (str): Name of the module
            debug (bool): Log on terminal or not

        Raises:
            None

        Returns:
            None
        """
        self._PATH = "/etc/securetea/web_deface.log"
        # Call the parent class
        logger.SecureTeaLogger.__init__(self, modulename, debug)

    def write_data(self, data):
        """
        Write data to the log file.

        Args:
            data (str): Data to write

        Raises:
            None

        Returns:
            None
        """
        with open(self._PATH, "a") as f:
            LEGEND = '[' + self.modulename + ']' + ' [' + \
                           str(time.strftime("%Y-%m-%d %H:%M")) + '] '
            message = LEGEND + data + "\n"
            f.write(message)

    def printinfo(self, message):
        """
        Over-ride the parent class printinfo method.

        Args:
            message (str): Message to log

        Raises:
            None

        Returns:
            None
        """
        # Call the parent method
        super().printinfo(message)
        self.write_data(message)

    def printerror(self, message):
        """
        Over-ride the parent class printerror method.

        Args:
            message (str): Message to log

        Raises:
            None

        Returns:
            None
        """
        # Call the parent method
        super().printerror(message)
        self.write_data(message)

    def printwarning(self, message):
        """
        Over-ride the parent class printwarning method.

        Args:
            message (str): Message to log

        Raises:
            None

        Returns:
            None
        """
        # Call the parent method
        super().printwarning(message)
        self.write_data(message)
