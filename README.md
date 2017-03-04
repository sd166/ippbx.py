# ippbx.py

[![Build Status](https://travis-ci.org/v12aml/ippbx.py.svg?branch=dev)](https://travis-ci.org/v12aml/ippbx.py)

irc://chat.freenode.net/#ippbx.py


## Eng
small script for Yealink SIP Phones, Asterisk and ActiveDirectory (LDAP)


IP phone type and hw MAC stored in 'employeeID' field in MS AD (format like 5:00112233445566). 1 - old yealink firmware, 5 - firmware version 80 and above

### Asterisk configs

#### chan_sip
Config files will be placed in /etc/asterisk/sip.d (configured in ippbx.cfg)

#### chan_pjsip
Config files will be placed in /etc/asterisk/pjsip.d (configured in ippbx.cfg)

### Configs for IP Phones
Config files will be placed in /srv/tftp/ (configured in ippbx.cfg) for serving by TFTP server.


## Rus
Небольшой скрипт для генерации конфигов asterisk и телефонов yealink, в качестве источника данных MS ActiveDirectory.
MAC-адрес телефона и его тип помещаются в поле 'employeeID'. Формат такой ТИП_ТЕЛЕФОНА:MAC_адрес, где тип телефона:
 * 1 старая прошивка yealink
 * 5 новая прошивка yealink, версии 80 и выше


### Конфигурация для Asterisk
Скрипт умеет гененрировать конфигурацию как для SIP, так и для pjsip

#### chan_sip
Файлы конфигурации размещаются в /etc/asterisk/sip.d (размещение можно поменять в ippbx.cfg)

#### chan_pjsip
Файлы конфигурации размещаются в /etc/asterisk/pjsip.d (размещение можно поменять в ippbx.cfg)


### Конфигурация для телефонных апаратов
Файлы конфигурации размещаются в /srv/tftp/ (размещение можно поменять в  ippbx.cfg), содержимое данной директории должно быть опубликовано с помощью любого TFTP-сервера.
