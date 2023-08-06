# -*- coding: utf-8 -*-
u"""Web Shell Detection Module for SecureTea Server Log Monitor.

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


class WebShell(object):
    """WebShell Class."""

    def __init__(self, debug=False, test=False):
        """
        Initialize WebShell.

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
            # Path of file containing web_shell payloads
            self.PAYLOAD_FILE = "securetea/lib/log_monitor/server_log/rules/payloads/web_shell.txt"
        else:
            # Path of file containing web_shell payloads
            self.PAYLOAD_FILE = "/etc/securetea/log_monitor/server_log/payloads/web_shell.txt"

        # Load web_shell payloads
        self.payloads = utils.open_file(self.PAYLOAD_FILE)

        # Logged IP list
        self.logged_IP = list()

        # Initialize OSINT object
        self.osint_obj = OSINT(debug=debug)

    def detect_web_shell(self, data):
        """
        Detect possible Web Shell attacks.
        Use string comparison to scan GET request with the
        list of possible web shell payloads.

        Args:
            data (dict): Parsed log file data

        Raises:
            None

        Returns:
            None
        """
        for ip in data.keys():
            get_req = data[ip]["get"]
            if (self.payload_match(get_req)):
                if ip not in self.logged_IP:  # if not logged earlier
                    self.logged_IP.append(ip)
                    last_time = data[ip]["ep_time"][0]
                    msg = "Possible web shell detected from: " + str(ip) + \
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
        possible web shell payload.

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
