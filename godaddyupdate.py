#!/usr/bin/env python

import configparser
import logging
import sys
from datetime import datetime

import pif
import pygodaddy

recordsUpdated = 0

logFile = "./godaddyupdate.log"
configFile = "./godaddyupdate.conf"

logging.basicConfig(filename=logFile.decode('unicode-escape'),
		    format='%(asctime)s %(message)s',
		    level=logging.INFO)   
config = configparser.ConfigParser()
config.read(configFile.decode('unicode-escape'))

client = pygodaddy.GoDaddyClient()
is_logged_in = client.login(config.get('godaddy', 'username'),
			    config.get('godaddy', 'password'))
if not is_logged_in:
	logging.error('Loginfailed!')
	sys.exit(1)

public_ip = pif.get_public_ip()
logging.info("Found public ip '{0}'".format(public_ip))

domain = config.get('godaddy', 'domain')
hostnames = config.get('godaddy', 'hostnames')

record = list(client.find_dns_records(domain, record_type='A'))
for r in record:
	if r.hostname in(hostnames) and r.value != public_ip:
		url = r.hostname+'.'+domain
		client.update_dns_record(url, public_ip)
		logging.info("Updated record: '{0}' - '{1}".format(url, public_ip))
		recordsUpdated += 1

if recordsUpdated == 0:
	logging.info("No Records Updated")
logging.info("Done")
	

