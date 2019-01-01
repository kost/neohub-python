#!/usr/bin/env python

import neohub

print("= START =")
n=neohub.Neohub(**{'devkey':228420,'vendorid':1,'devicetypeid':2, 'debug':False})

print("= LOGIN = ")
resp=n.login("simple@example.org","password")
for device in resp['devices']:
	print("Device: ", device['devicename'],device['deviceid'])
	stat=n.device_status(device['deviceid'])
	status=stat['devices'][0]
	print("  Current temperature: ", status['CURRENT_TEMPERATURE'])
	devstatid=status['deviceid']
	print("  Current set temperature: ", status['CURRENT_SET_TEMPERATURE'])
	print("  Current program temperature: ", status['PROGRAM_TEMP'])
	print("  Current hold temperature: ", status['HOLD_TEMPERATURE'])

print("= END =")


