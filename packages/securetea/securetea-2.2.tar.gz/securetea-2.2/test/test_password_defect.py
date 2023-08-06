# -*- coding: utf-8 -*-
import unittest
from securetea.lib.log_monitor.system_log.password_defect import PasswordDefect
from securetea.logger import SecureTeaLogger

try:
    # if python 3.x.x
    from unittest.mock import patch
except ImportError:  # python 2.x.x
    from mock import patch


class TestPasswordDefect(unittest.TestCase):
    """
    Test class for PasswordDefect.
    """

    def setUp(self):
        """
        Setup class for PasswordDefect.
        """
        self.os = "debian"

    @patch.object(PasswordDefect, "update_dict")
    @patch('securetea.lib.log_monitor.system_log.password_defect.utils')
    def test_parse_log_file(self, mock_utils, mock_up_dict):
        """
        Test parse_log_file.
        """
        mock_utils.categorize_os.return_value = self.os
        # Create PasswordDefect object
        self.pass_def = PasswordDefect()
        mock_utils.open_file.return_value = ["root::0:0:root:/root:/bin/bash"]
        self.pass_def.parse_log_file()
        mock_up_dict.assert_called_with("root", "")

    @patch('securetea.lib.log_monitor.system_log.password_defect.utils')
    @patch.object(SecureTeaLogger, "log")
    def test_update_dict(self, mock_log, mock_utils):
        """
        Test update_dict.
        """
        mock_utils.categorize_os.return_value = self.os
        # Create PasswordDefect object
        self.pass_def = PasswordDefect()
        self.pass_def.update_dict("user", "")
        self.assertEqual(self.pass_def.user_password.get("user"), "")
        mock_log.assert_called_with("Password not found for user: user",
                                    logtype="warning")
