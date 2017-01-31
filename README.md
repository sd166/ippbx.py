# ippbx.py

[![Build Status](https://travis-ci.org/v12aml/ippbx.py.svg?branch=dev)](https://travis-ci.org/v12aml/ippbx.py)

irc://chat.freenode.net/#ippbx.py


## Eng
small script for Yealink SIP Phones, Asterisk and ActiveDirectory (LDAP)


IP phone type and hw MAC stored in 'employeeID' field in MS AD (format like 5:00112233445566). 1 - old yealink firmware, 5 - firmware version 80 and above

## Rus
Небольшой скрипт для генерации конфигов asterisk и телефонов yealink, в качестве источника данных MS ActiveDirectory.
MAC-адрес телефона и его тип помещаются в поле 'employeeID'. Формат такой ТИП_ТЕЛЕФОНА:MAC_адрес, где тип телефона:
 * 1 старая прошивка yealink
 * 5 новая прошивка yealink
