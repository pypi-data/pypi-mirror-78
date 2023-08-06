import unittest
import sys

try:
    # python 3.4+ should use builtin unittest.mock not mock package
    from unittest.mock import patch
except ImportError:
    from mock import patch

from rabbitmqtesttool import commandline


class TestCommandLine(unittest.TestCase):

    def setUp(self):
        self.args = ["rabbit-tools", "127.0.0.1"]

    def testBasic(self):
        with patch.object(sys, 'argv', self.args):
            options = commandline.parse_command_line()
            self.assertTrue(isinstance(options.BROKER, list))
            self.assertEquals(len(options.BROKER), 1)
            self.assertEquals(options.BROKER[0], "127.0.0.1")
