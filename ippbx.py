#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import ldap3
import sys
import crypt


__author__ = "Denis Gubanov"
__copyright__ = "Copyright 2017"
# __credits__ = ["Denis Gubanov"]
__license__ = "GPL-3.0"
__vcs_id__ = '$Id$'
__version__ = "2.0.0"
__maintainer__ = "Denis Gubanov"
__email__ = "v12aml@gmail.com"
__status__ = "Develompent"


config = configparser.RawConfigParser()
config.read('/etc/ippbx.cfg')

debug_enabled = config.get('DEFAULT', 'debug')

ldap_host = config.get('ldap', 'host')
search_base = config.get('ldap', 'search_base')
search_user_name = config.get('ldap', 'search_user_name')
search_user_pw = config.get('ldap', 'search_user_pw')

asterisk_user_context = config.get('asterisk', 'user_context')
asterisk_server_address = config.get('asterisk', 'server_address')
asterisk_pjsip_enables = config.get('asterisk', 'pjsip_enabled')
asterisk_pjsip_conf_dir = config.get('asterisk', 'pjsip_conf_dir')
asterisk_sip_enables = config.get('asterisk', 'sip_enabled')
asterisk_sip_conf_dir = config.get('asterisk', 'sip_conf_dir')
asterisk_codecs_allow = config.get('asterisk', 'codecs_allow')

tftp_dir = config.get('tftp', 'dir')

phone_num_prefix = config.get('asterisk', 'phone_num_prefix')
ldap_filter = "(&(objectClass=person)(ipPhone=" + phone_num_prefix + "*))"
ldap_attrs = ['sn', 'employeeID', 'ipPhone', 'displayName']


# Functions
def log_debug(msg):
    """Debug log"""
    if debug_enabled == "True" or "true":
        print(msg)


def genuserpass(phonenum):
    """generate simple user password"""
    salt = config.get('user', 'pass_salt')
    return crypt.crypt(phonenum, salt)


def asterisk_sip_user_config(phonenum, username):
    """generate sip user config for Asterisk"""
    log_debug("Generating SIP config for {} {}".format(phonenum, username))
    user_config = ""
    user_config += "[" + phonenum + "]" + "\n"
    user_config += "type=friend" + "\n"
    user_config += "host=dynamic" + "\n"
    user_config += "username=" + phonenum + "\n"
    user_config += "secret=" + genuserpass(phonenum) + "\n"
    user_config += "fullname=" + phonenum + "\n"
    user_config += "callerid=" + username + "\n"
    user_config += "context=" + asterisk_user_context + "\n"
    user_config += "transport=udp" + "\n"
    user_config += "disallow=all" + "\n"
    user_config += "allow=" + asterisk_codecs_allow + "\n"
    user_config += "canreinvite=no" + "\n"
    user_config += "nat=yes" + "\n"
    user_config += "qualify=yes" + "\n"
    user_config += "hassip=yes" + "\n"
    user_config += "hasiax=no" + "\n"
    user_config += "hash323=no" + "\n"
    user_config += "hasmanager=no" + "\n"
    user_config += "\n"
    cfg_file_name = asterisk_sip_conf_dir + "user" + username + ".conf"
    with open(cfg_file_name, 'w') as f:
        f.write(user_config)
    log_debug(cfg_file_name)
    log_debug(user_config)


def asterisk_pjsip_user_config(phonenum, username):
    """generate sip user config for Asterisk"""
    log_debug("Generating PJSIP config for {} {}".format(phonenum, username))
    user_pass = genuserpass(phonenum)
    user_config = ";{} <{}> {}".format(phonenum, username, user_pass)
    user_config += "\n"
    user_config += "[{}]".format(phonenum) + "\n"
    user_config += "type=auth" + "\n"
    user_config += "auth_type=userpass" + "\n"
    user_config += "username={}".format(phonenum) + "\n"
    user_config += "password={}".format(user_pass) + "\n"
    user_config += "" + "\n"
    user_config += "[{}]".format(phonenum) + "\n"
    user_config += "type=aor" + "\n"
    user_config += "max_contacts=1" + "\n"
    user_config += "remove_existing=yes" + "\n"
    user_config += "qualify_frequency=5" + "\n"
    user_config += "" + "\n"
    user_config += "[{}]".format(phonenum) + "\n"
    user_config += "type=endpoint" + "\n"
    user_config += "context=" + asterisk_user_context + "\n"
    user_config += "disallow=all" + "\n"
    user_config += "allow=" + asterisk_codecs_allow + "\n"
    user_config += "aors={}".format(phonenum) + "\n"
    user_config += "auth={}".format(phonenum) + "\n"
    user_config += "rtp_symmetric=yes" + "\n"
    user_config += "rtp_ipv6=yes" + "\n"
    user_config += "rewrite_contact=yes" + "\n"
    user_config += "send_rpid=yes" + "\n"
    user_config += "" + "\n"
    cfg_file_name = asterisk_pjsip_conf_dir + "user" + username + ".conf"
    with open(cfg_file_name, 'w') as f:
        f.write(user_config)
    log_debug(cfg_file_name)
    log_debug(user_config)


def yealink_phone_config(phonetype, phonehwmac, phonenum, username):
    """generate and write phone cfg file"""
    if phonetype == "1":
        cfgdata = ""
        filename = phonehwmac + ".cfg"

        cfgdata += "[ account ]" + "\n"
        cfgdata += "path = /config/voip/sipAccount0.cfg" + "\n"
        cfgdata += "Enable = 1" + "\n"
        cfgdata += "Label = " + str(phonenum) + " - " + str(username) + "\n"
        cfgdata += "DisplayName = " + str(phonenum) + "\n"
        cfgdata += "AuthName = " + str(phonenum) + "\n"
        cfgdata += "UserName = " + str(phonenum) + "\n"
        cfgdata += "password = " + genuserpass(phonenum) + "\n"
        cfgdata += "SIPServerHost = " + asterisk_server_address + "\n"
        cfgdata += "SIPServerPort = 5060" + "\n"
        cfgdata += "Transport = 0" + "\n"
        cfgdata += "" + "\n"

        log_debug("Generating phone config: ")
        log_debug("phonetype: " + phonetype)
        log_debug("phonehwmac: " + phonehwmac)
        log_debug("phonenum: " + phonenum)
        log_debug("username: " + username)
        log_debug(filename)
        log_debug(cfgdata)
    elif phonetype == "2":
        cfgdata = ""
        filename = phonehwmac + ".cfg"

        cfgdata += "[ account ]" + "\n"
        cfgdata += "path = /config/voip/sipAccount0.cfg" + "\n"
        cfgdata += "Enable = 1" + "\n"
        cfgdata += "Label = " + str(phonenum) + " - " + str(username) + "\n"
        cfgdata += "DisplayName = " + str(phonenum) + "\n"
        cfgdata += "AuthName = " + str(phonenum) + "\n"
        cfgdata += "UserName = " + str(phonenum) + "\n"
        cfgdata += "password = " + genuserpass(phonenum) + "\n"
        cfgdata += "SIPServerHost = " + asterisk_server_address + "\n"
        cfgdata += "SIPServerPort = 5060" + "\n"
        cfgdata += "Transport = 0" + "\n"
        cfgdata += "" + "\n"

        log_debug("Generating phone config: ")
        log_debug("phonetype: " + phonetype)
        log_debug("phonehwmac: " + phonehwmac)
        log_debug("phonenum: " + phonenum)
        log_debug("username: " + username)
        log_debug(filename)
        log_debug(cfgdata)
    elif phonetype == "5":
        cfgdata = ""
        filename = phonehwmac + ".cfg"

        cfgdata += "#!version:1.0.0.1" + "\n"
        cfgdata += "account.1.enable = 1" + "\n"
        cfgdata += "account.1.label = " + \
            str(phonenum) + " - " + str(username) + "\n"
        cfgdata += "account.1.display_name = " + str(phonenum) + "\n"
        cfgdata += "account.1.auth_name = " + str(phonenum) + "\n"
        cfgdata += "account.1.user_name = " + str(phonenum) + "\n"
        cfgdata += "account.1.password = " + genuserpass(phonenum) + "\n"
        cfgdata += "account.1.sip_server.1.address = " + \
            asterisk_server_address + "\n"
        cfgdata += "account.1.sip_server.1.port = 5060" + "\n"
        cfgdata += "" + "\n"

        log_debug("Generating phone config: ")
        log_debug("phonetype: " + phonetype)
        log_debug("phonehwmac: " + phonehwmac)
        log_debug("phonenum: " + phonenum)
        log_debug("username: " + username)
        log_debug(filename)
        log_debug(cfgdata)
    else:
        print("Unknown phone type")
        sys.exit(1)
    with open(tftp_dir + filename, 'w') as f:
        f.write(cfgdata)


# Main body
log_debug("LDAP host: " + ldap_host)
log_debug("LDAP search_base: " + search_base)
log_debug("LDAP search user: " + search_user_name)
log_debug("LDAP filter: " + ldap_filter)
log_debug("LDAP attributes: " + str(ldap_attrs))

# Connecting to LDAP
log_debug("Connecting to LDAP server")
ldap_server = ldap3.Server(
    ldap_host,
    get_info=ldap3.ALL)

connection = ldap3.Connection(
    ldap_server,
    user=search_user_name,
    password=search_user_pw,
    authentication=ldap3.NTLM)

connection.bind()
connection.start_tls()

log_debug(connection.usage)


# Fetching data
log_debug("Fetching data")
connection.search(
    search_base,
    ldap_filter,
    attributes=ldap_attrs)

# Processing data
for entry in connection.entries:
    log_debug(entry.sn)
    log_debug(entry.displayName)
    log_debug(entry.ipPhone)
    log_debug(entry.employeeID)
    # Generating asterisk config (SIP or/and PJSIP)
    if asterisk_pjsip_enables == "True" or "true":
        asterisk_pjsip_user_config(entry.ipPhone, entry.displayName)
    if asterisk_sip_enables == "True" or "true":
        asterisk_sip_user_config(entry.ipPhone, entry.displayName)
    # Generating Yelink phone config
    try:
        phone_id = entry.employeeID
        phone_type = phone_id[:1]
        phone_hwmac = str(phone_id[2:]).lower()
    except:
        phone_id = None
        phone_type = None
        phone_hwmac = None
        log_debug("Wrong format of employeeID LDAP field")
    if phone_type:
        yealink_phone_config(
            phone_type,
            phone_hwmac,
            entry.ipPhone,
            entry.displayName)
    log_debug("We are done with {}".format(entry.displayName))
    log_debug(connection.usage)
log_debug(connection.usage)


# EOF
