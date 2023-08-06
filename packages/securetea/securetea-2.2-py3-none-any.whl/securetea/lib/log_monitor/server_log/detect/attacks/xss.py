# -*- coding: utf-8 -*-
u"""Cross Site Scripting (XSS) Detection Module for SecureTea Server Log Monitor.

Project:
    ╔═╗┌─┐┌─┐┬ ┬┬─┐┌─┐╔╦╗┌─┐┌─┐
    ╚═╗├┤ │  │ │├┬┘├┤  ║ ├┤ ├─┤
    ╚═╝└─┘└─┘└─┘┴└─└─┘ ╩ └─┘┴ ┴
    Author: Abhishek Sharma <abhishek_official@hotmail.com> , Jun 12 2019
    Version: 1.3
    Module: SecureTea

"""

from securetea.lib.log_monitor.server_log.server_logger import ServerLogger
from securetea.lib.log_monitor.server_log import utils
from securetea.lib.osint.osint import OSINT
from securetea.common import write_mal_ip

import re


class CrossSite(object):
    """CrossSite Class."""

    def __init__(self, debug=False, test=False):
        """
        Initialize CrossSite.

        Args:
            debug (bool): Log on terminal or not

        Raises:
            None

        Returns:
            None
        """
        # Initialize logger
        self.logger = ServerLogger(
            __name__,
            debug=debug
        )

        if test:
            # Path of file containing XSS payloads
            self.PAYLOAD_FILE = "securetea/lib/log_monitor/server_log/rules/payloads/xss.txt"
            # Path of file containing XSS regex rules
            self.REGEX_FILE = "securetea/lib/log_monitor/server_log/rules/regex/xss.txt"
        else:
            # Path of file containing XSS payloads
            self.PAYLOAD_FILE = "/etc/securetea/log_monitor/server_log/payloads/xss.txt"
            # Path of file containing XSS regex rules
            self.REGEX_FILE = "/etc/securetea/log_monitor/server_log/regex/xss.txt"

        # Load XSS payloads
        self.payloads = utils.open_file(self.PAYLOAD_FILE)
        # Load XSS regex rules
        self.regex = utils.open_file(self.REGEX_FILE)

        # Logged IP list
        self.logged_IP = list()

        # Initialize OSINT object
        self.osint_obj = OSINT(debug=debug)

    def detect_xss(self, data):
        """
        Detect possible Cross Site Scripting (XSS) attacks.
        Use regex rules and string matching to detect
        XSS attacks.
        4 Level rules:
            - Simple regex
            - Hex regex
            - Payload string matching
            - URI encoded string matching

        Args:
            data (dict): Parsed log file data

        Raises:
            None

        Returns:
            None
        """
        for ip in data.keys():
            get_req = data[ip]["get"]
            last_time = data[ip]["ep_time"][0]
            if (self.payload_match(get_req) or self.regex_check(get_req)):
                if ip not in self.logged_IP:  # if not logged earlier
                    self.logged_IP.append(ip)
                    msg = "Possible Cross Site Scripting (XSS) detected from: " + str(ip) + \
                          " on: " + str(utils.epoch_to_date(last_time))
                    self.logger.log(
                        msg,
                        logtype="warning"
                    )
                    utils.write_ip(str(ip))
                    # Generate CSV report using OSINT tools
                    self.osint_obj.perform_osint_scan(ip.strip(" "))
                    # Write malicious IP to file, to teach Firewall about the IP
                    write_mal_ip(ip.strip(" "))

    def payload_match(self, get_req):
        """
        Match parsed GET request for a
        possible XSS payload.

        Args:
            get_req (str): GET request on which to perform
                           payload string matching

        Raises:
            None

        Returns:
            TYPE: bool
        """
        for req in get_req:
            for payload in self.payloads:
                payload = payload.strip(" ").strip("\n")
                if (payload in req or
                    utils.uri_encode(payload) in req):
                    return True

    def regex_check(self, get_req):
        """
        Match parsed GET request with
        a XSS regex rules.

        Args:
            get_req (str): GET request on which to perform
                           regex matching

        Raises:
            None

        Returns:
            TYPE: bool
        """
        for req in get_req:
            for reg in self.regex:
                reg = reg.strip(" ").strip("\n")
                if re.findall(reg, req) != []:
                    return True
