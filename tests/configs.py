#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest
from ippbxpy.ippbx import asterisk_pjsip_user_config
from ippbxpy.ippbx import asterisk_sip_user_config
from ippbxpy.ippbx import yealink_phone_config


def log_debug(msg):
    pass


class ConfigGeneratorsTests(unittest.TestCase):
    def test_pjsip(self):
        """asterisk_pjsip_user_config(
            phonenum,
            username,
            userpass,
            pickupgroup)
        """
        r1 = """
        """
        self.assertEqual(
            asterisk_pjsip_user_config(
                "1001",
                "User Name",
                "pass",
                "p1"),
            r1)

    def test_sip(self):
        """asterisk_sip_user_config(
            phonenum,
            username,
            userpass,
            pickupgroup)
        """
        r1 = """
        """
        self.assertEqual(
            asterisk_sip_user_config(
                "1001",
                "User Name",
                "pass",
                "p1"),
            r1)

    def test_yealink(self):
        """yealink_phone_config(
            phonetype,
            phonehwmac,
            phonenum,
            username,
            userpass)
        """
        r1 = """
        """
        self.assertEqual(
            yealink_phone_config(
                "5",
                "123123123",
                "1001",
                "User Name",
                "pass"),
            r1)


# EOF
