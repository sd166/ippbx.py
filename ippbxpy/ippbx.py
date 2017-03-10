#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import ldap3
import crypt
import hashlib
from subprocess import call

from ippbxpy.confgens import asterisk_pjsip_user_config
from ippbxpy.confgens import asterisk_sip_user_config
from ippbxpy.confgens import yealink_phone_config


__author__ = "Denis Gubanov"
__copyright__ = "Copyright 2017"
# __credits__ = ["Denis Gubanov"]
__license__ = "GPL-3.0"
__vcs_id__ = '$Id$'
__version__ = "2.1.1"
__maintainer__ = "Denis Gubanov"
__email__ = "v12aml@gmail.com"
__status__ = "Production"


# Functions
def log_debug(cfg, msg):
    """Debug log"""
    if cfg.getboolean('DEFAULT', 'debug'):
        print(msg)


def gen_user_pass(cfg, phonenum):
    """generate simple user password"""
    log_debug(cfg, "called func gen_user_pass({})".format(phonenum))
    salt = cfg.get('user', 'pass_salt')
    return crypt.crypt(str(phonenum), salt=salt)


def main():
    # Reading config file
    cfg = configparser.ConfigParser()
    cfg.read('/etc/ippbx.cfg')
    search_user = "{}\{}".format(
        cfg.get('ldap', 'search_user_domain'),
        cfg.get('ldap', 'search_user_name'))
    # Main body
    log_debug(cfg, "LDAP host:" + cfg.get('ldap', 'host'))
    log_debug(cfg, "LDAP search_base:" + cfg.get('ldap', 'search_base'))
    log_debug(cfg, "LDAP search user:" + search_user)

    # Connecting to LDAP
    log_debug(cfg, "Connecting to LDAP server")
    ldap_server = ldap3.Server(
        cfg.get('ldap', 'host'),
        get_info=ldap3.ALL)

    connection = ldap3.Connection(
        ldap_server,
        user=search_user,
        password=cfg.get('ldap', 'search_user_pw'),
        authentication=ldap3.NTLM)

    connection.bind()
    connection.start_tls()

    log_debug(cfg, connection.usage)

    # Fetching data
    log_debug(cfg, "Fetching data")
    for phone_prefix in cfg.get('asterisk', 'phone_num_prefix').split(","):
        ldap_filter = "(&(objectClass=person)(ipPhone=" + phone_prefix + "*))"
        ldap_attrs = ['employeeID', 'ipPhone', 'displayName', 'canonicalName']
        log_debug(cfg, "LDAP filter:" + ldap_filter)
        log_debug(cfg, "LDAP attributes:" + str(ldap_attrs))
        connection.search(
            cfg.get('ldap', 'search_base'),
            ldap_filter,
            attributes=ldap_attrs)

        # Processing data
        for entry in connection.entries:
            try:
                phone_num = "{}".format(entry.ipPhone)
                log_debug(cfg, phone_num)
                user_name = "{}".format(entry.displayName)
                log_debug(cfg, user_name)
                phone_id = "{}".format(entry.employeeID)
                log_debug(cfg, phone_id)
                user_can_name = "{}".format(entry.canonicalName)
                user_ou = '/'.join(user_can_name.split('/')[0:-1])
                pickupgroup = hashlib.md5(user_ou.encode('utf-8')).hexdigest()
            except:
                log_debug(cfg, "Can't fetch some data")

            # Generating asterisk config (SIP or/and PJSIP)
            user_pass = gen_user_pass(phone_num)
            if cfg.getboolean('asterisk', 'pjsip_enabled'):
                log_debug(cfg, "PJSIP enabled")
                cfg_file_name = "{}/user{}.conf".format(
                    cfg.get('asterisk', 'pjsip_conf_dir'),
                    phone_num)
                log_debug(cfg, cfg_file_name)
                with open(cfg_file_name, 'w') as f:
                    user_config = asterisk_pjsip_user_config(
                        phone_num,
                        user_name,
                        user_pass,
                        pickupgroup)
                    f.write(user_config)
            else:
                log_debug(cfg, "PJSIP disabled")
            if cfg.getboolean('asterisk', 'sip_enabled'):
                log_debug(cfg, "SIP enabled")
                cfg_file_name = "{}/user{}.conf".format(
                    cfg.get('asterisk', 'sip_conf_dir'),
                    phone_num)
                log_debug(cfg, cfg_file_name)
                with open(cfg_file_name, 'w') as f:
                    user_config = asterisk_sip_user_config(
                        phone_num,
                        user_name,
                        user_pass,
                        pickupgroup)
                    f.write(user_config)
            else:
                log_debug(cfg, "SIP disabled")
            # Generating Yelink phone config
            try:
                phone_type = phone_id[:1]
                phone_hwmac = phone_id[2:].lower()
            except:
                phone_type = None
                phone_hwmac = None
                log_debug(cfg, "Wrong format of employeeID LDAP field")
            if phone_type:
                cfg_file_name = phone_hwmac + ".cfg"
                log_debug(cfg, cfg_file_name)
                with open(cfg.get('tftp', 'dir') + cfg_file_name, 'w') as f:
                    cfgdata = yealink_phone_config(
                        phone_type,
                        phone_hwmac,
                        phone_num,
                        user_name,
                        user_pass)
                    f.write(cfgdata)
            log_debug(cfg, "We are done with {}".format(user_name))
            log_debug(cfg, connection.usage)
        log_debug(cfg, connection.usage)


if __name__ == "__main__":
    # execute only if run as a script
    main()
    print("All done")
    # print("Now you should reload asterisk configuration:")
    # print("\tsystemctl reload asterisk.service")
    call(["systemctl", "reload", "asterisk.service"])


# EOF
