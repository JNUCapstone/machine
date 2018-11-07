#!/usr/bin/env python
#coding=utf-8
import subprocess as sub
#=========================================================================================
from datetime import datetime, timedelta
import pprint
from influxdb import InfluxDBClient
from copy import deepcopy
import pytz
#=========================================================================================
p = sub.Popen(('tcpdump', '-i', 'em1', '-s', '1500', 'tcp'), stdout=sub.PIPE)
#=========================================================================================
def get_ifdb(db, host='192.168.0.111', port=8086, user='root', passwd='root'):
	client = InfluxDBClient(host, port, user, passwd, db)
	try:
		client.create_database(db)
	except:
		pass
	return client
#=========================================================================================
def my_test(ifdb):
	tablename = 'real_test'
	tagname1 = 'dst_port'
	fieldname1 = 'contents'
	for row in iter(p.stdout.readline, b''):
		json_body = []
		row = row.decode()
		#print row.rstrip()   # process here
		host = row[row.find("IP")+3: row.find(">")]
		point = {
			"measurement": tablename,
			"tags": {
				tagname1: 0,
				'host':host
			},
			"fields": {
				fieldname1: 0
			},
		}
		port = row[row.find(">")+2:row.find("Flags")-2].split(".")
		if port[0]=='192' and port[1]=='168' and port[2]=='0' and port[3]=='111':
			if port[4]=='15000' or port[4]=='16000' or port[4]=='17000':
				print(port)
				np = deepcopy(point)
				np['tags'][tagname1] = port[4]
				#contents
				np['fields'][fieldname1] = row[row.find("Flags")+6:]
				json_body.append(np)
				#print(json_body)
				ifdb.write_points(json_body)
	result = ifdb.query('select * from %s' % tablename)
	pprint.pprint(result.raw)
#=========================================================================================
def do_test():
	ifdb = get_ifdb(db='grafana')
	my_test(ifdb)

#=========================================================================================
if __name__ == '__main__':
	do_test()
#=========================================================================================
