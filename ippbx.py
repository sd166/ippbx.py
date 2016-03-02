#!/usr/bin/python
# -*- coding: utf-8

import ConfigParser
import ldap
import sys

DEBUG = False

config = ConfigParser.RawConfigParser()
config.read('ippbx.cfg')

ldaphost = config.get('ldap', 'host')
basedn = config.get('ldap', 'basedn')
searchuserdn = config.get('ldap', 'searchuserdn')
searchuserpw = config.get('ldap', 'searchuserpw')

userpassprefix = config.get('user', 'passprefix')
userpassbasenum = config.get('user', 'passbasenum')

asteriskusercontext = config.get('asterisk', 'usercontext')
asteriskserveraddress = config.get('asterisk', 'serveraddress')
asteriskcfgfilename = config.get('asterisk', 'filename')

tftpdir = config.get('tftp', 'dir')

ldapfilter = '(&(objectClass=person)(ipPhone=*))'
ldapattrs = ['employeeID', 'ipPhone', 'displayName']


# Functions
def genuserpass(phonenum):
	"generate simple user password"
	userpasstrail =  int(userpassbasenum) - int(phonenum)
	userpass = userpassprefix + str(userpasstrail)[1:4]
	return userpass 

def asteriskuserconfig(phonenum, username):
	"generate sip user config for Asterisk"
	userconfig = ""
	userconfig += "[" + phonenum + "]" + "\n"
	userconfig += "type=friend" + "\n"
	userconfig += "host=dynamic" + "\n"
	userconfig += "username=" + phonenum + "\n"
	userconfig += "secret=" + genuserpass(phonenum) + "\n"
	userconfig += "callerid=" + username + "\n"
	userconfig += "context=" + asteriskusercontext  + "\n"
	userconfig += "transport=udp,tcp" + "\n"
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
	"generate and write phone cfg file"
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
		
		if DEBUG:
			print "Generating phone config: "
			print "phonetype: " + phonetype
			print "phonehwmac: " + phonehwmac
			print "phonenum: " + phonenum
			print "username: " + username
			print filename
			print cfgdata
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
                
                if DEBUG:
                        print "Generating phone config: "
                        print "phonetype: " + phonetype
                        print "phonehwmac: " + phonehwmac
                        print "phonenum: " + phonenum
                        print "username: " + username
                        print filename
                        print cfgdata
	elif phonetype == "5":
		cfgdata = ""
		filename = phonehwmac + ".cfg"
		
		cfgdata += "#!version:1.0.0.1" + "\n"
		cfgdata += "account.1.enable = 1" + "\n"
		cfgdata += "account.1.label = " + str(phonenum) + " - " + str(username) + "\n"
		cfgdata += "account.1.display_name = " + str(phonenum) + "\n"
		cfgdata += "account.1.auth_name = " + str(phonenum) + "\n"
		cfgdata += "account.1.user_name = " + str(phonenum) + "\n"
		cfgdata += "account.1.password = " + genuserpass(phonenum) + "\n"
		cfgdata += "account.1.sip_server.1.address = " + asteriskserveraddress + "\n"
		cfgdata += "account.1.sip_server.1.port = 5060" + "\n"
		cfgdata += "" + "\n" 
		
		if DEBUG:
                        print "Generating phone config: "
                        print "phonetype: " + phonetype
                        print "phonehwmac: " + phonehwmac
                        print "phonenum: " + phonenum
                        print "username: " + username
			print filename
			print cfgdata
	else:
		print "Unknown phone type"
		sys.exit(1)
	with open(tftpdir + filename, 'w') as f:
		f.write(cfgdata)


if DEBUG:
	print "LDAP host: " + ldaphost
	print "LDAP baseDN: " + basedn
	print "LDAP search user: " + searchuserdn
	print "LDAP password: " + searchuserpw


connection = ldap.initialize(ldaphost)
connection.set_option(ldap.OPT_REFERRALS,0)
connection.simple_bind_s(searchuserdn, searchuserpw)
ldap_result_id = connection.search(basedn, ldap.SCOPE_SUBTREE, ldapfilter, ldapattrs)
result_set = []

while True:
	result_type, result_data = connection.result(ldap_result_id, 0)
	if (result_data == []):
		break
	else:
		if result_type == ldap.RES_SEARCH_ENTRY:
			result_set.append(result_data)

if DEBUG:
	print "Search results:"
	print result_set
	print type(result_set)

asteriskcfg = ""

for result in result_set:
	data = result[0][1]
	if DEBUG:
		print data
	
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
	if DEBUG:
		print "Num: " + str(phonenum)
		print "User: " + str(username)
		print "PhoneID: " + str(phoneid)
		print "Phone type: " + str(phonetype)
		print "Phone MAC: " + str(phonehwmac)
		print "User password: " + genuserpass(phonenum)
		print "Asterisk config:"
		print asteriskuserconfig(phonenum, username)
	if phonetype:
		phoneconfig(phonetype, phonehwmac, phonenum, username)
	asteriskcfg += asteriskuserconfig(phonenum, username)

with open(asteriskcfgfilename, 'w') as f:
	f.write(asteriskcfg)


