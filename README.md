Neohub
======
Python module to control Neohub supported thermostats

Requirements
============

It should work with both python2 and python3 with simple pip commands:
```
sudo apt-get update
sudo apt-get install -y python3 python3-pip
sudo pip3 install neohub
```

Examples
========

Simple example to get devices and its current status:
```
# you should obtain devkeys and IDs somehow
n=neohub.Neohub(**{'devkey':1,'vendorid':1,'devicetypeid':1, 'debug':False})
# e-mail of account and password
resp=n.login("simple@example.org","password")
for device in resp['devices']:
        print("=Device: ", device['devicename'],device['deviceid'])
        stat=n.device_status(device['deviceid'])
        status=stat['devices'][0]
        print(status)
```

