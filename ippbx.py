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

debug_enabled = config.get('DEBUG', 'debug')

ldap_host = config.get('ldap', 'host')
base_dn = config.get('ldap', 'base_dn')
search_user_name = config.get('ldap', 'search_user_name')
search_user_pw = config.get('ldap', 'search_user_pw')

asteriskusercontext = config.get('asterisk', 'usercontext')
asteriskserveraddress = config.get('asterisk', 'serveraddress')
asteriskcfgfilename = config.get('asterisk', 'filename')

tftpdir = config.get('tftp', 'dir')

ldapfilter = '(&(objectClass=person)(ipPhone=*))'
ldapattrs = ['employeeID', 'ipPhone', 'displayName']


# Functions
def log_debug(msg):
    """Debug log"""
    if debug_enabled == "True" or "true":
        print(msg)


def genuserpass(phonenum):
    """generate simple user password"""
    salt = config.get('user', 'pass_salt')
    return crypt.crypt(phonenum, salt)


def asteriskuserconfig(phonenum, username):
    """generate sip user config for Asterisk"""
    userconfig = ""
    userconfig += "[" + phonenum + "]" + "\n"
    userconfig += "type=friend" + "\n"
    userconfig += "host=dynamic" + "\n"
    userconfig += "username=" + phonenum + "\n"
    userconfig += "secret=" + genuserpass(phonenum) + "\n"
    userconfig += "fullname=" + phonenum + "\n"
    userconfig += "callerid=" + username + "\n"
    userconfig += "context=" + asteriskusercontext + "\n"
    userconfig += "transport=udp" + "\n"
    userconfig += "disallow=all" + "\n"
    userconfig += "allow=g729,ulaw,alaw,g722" + "\n"
    userconfig += "canreinvite=no" + "\n"
    userconfig += "nat=yes" + "\n"
    userconfig += "qualify=yes" + "\n"
    userconfig += "hassip=yes" + "\n"
    userconfig += "hasiax=no" + "\n"
    userconfig += "hash323=no" + "\n"
    userconfig += "hasmanager=no" + "\n"
    userconfig += "\n"
    return userconfig


def phoneconfig(phonetype, phonehwmac, phonenum, username):
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
        cfgdata += "SIPServerHost = " + asteriskserveraddress + "\n"
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
        cfgdata += "SIPServerHost = " + asteriskserveraddress + "\n"
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
            asteriskserveraddress + "\n"
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
    with open(tftpdir + filename, 'w') as f:
        f.write(cfgdata)


log_debug("LDAP host: " + ldap_host)
log_debug("LDAP base_dn: " + base_dn)
log_debug("LDAP search user: " + search_user_name)
log_debug("LDAP password: " + search_user_pw)

ldap_server = ldap3.Server(ldap_host, get_info=ldap3.ALL)
connection = ldap3.Connection(
    ldap_server,
    user=search_user_name,
    password=search_user_pw,
    authentication=ldap3.NTLM)
ldap_result_id = connection.search(
    base_dn, ldap3.SCOPE_SUBTREE, ldapfilter, ldapattrs)
result_set = []

while True:
    result_type, result_data = connection.result(ldap_result_id, 0)
    if (result_data == []):
        break
    else:
        if result_type == ldap3.RES_SEARCH_ENTRY:
            result_set.append(result_data)


log_debug("Search results:")
log_debug(result_set)
log_debug(type(result_set))

asteriskcfg = ""

for result in result_set:
    data = result[0][1]
    log_debug(data)

    phonenum = data['ipPhone'][0]
    username = data['displayName'][0]
    try:
        phoneid = data['employeeID'][0]
        phonetype = phoneid[:1]
        phonehwmac = str(phoneid[2:]).lower()
    except:
        phoneid = None
        phonetype = None
        phonehwmac = None
        log_debug("Num: " + str(phonenum))
        log_debug("User: " + str(username))
        log_debug("PhoneID: " + str(phoneid))
        log_debug("Phone type: " + str(phonetype))
        log_debug("Phone MAC: " + str(phonehwmac))
        log_debug("User password: " + genuserpass(phonenum))
        log_debug("Asterisk config:")
        log_debug(asteriskuserconfig(phonenum, username))
    if phonetype:
        phoneconfig(phonetype, phonehwmac, phonenum, username)
    asteriskcfg += asteriskuserconfig(phonenum, username)

with open(asteriskcfgfilename, 'w') as f:
    f.write(asteriskcfg)


# EOF
