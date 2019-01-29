import serial
import time
import pymysql
from time import localtime, strftime
from convObis import ConvObis
import json

with open("settings.json", "r") as read_file:
    data = json.load(read_file)


db = pymysql.connect(host="localhost", user="plaUser", passwd="plasystem", db="plm", port=8744)
cur = db.cursor()

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=0.5)

obis_code={'kW':'1.5.0',
           'date': '0.9.2',
           'time': '0.9.1'}
try:
	ser.isOpen()

except:
	exit()

if (ser.isOpen()):
    ser.write(str.encode('\x2f\x3f'+str(data[0]['meter_id'])+'\x21\x0d\x0a'))
    time.sleep(0.2)
    ser.write(bytes.fromhex('06 30 35 31 0d 0a'))
    time.sleep(1.5)
    for x in range(0,20):
        time.sleep(0.5)
        if (ser.inWaiting() > 0):
            x = ser.readline()
            ser.flush()
    obis = ConvObis()
    for i in obis_code:
        obis.toHex(obis_code[i])
        hex = obis.command
        ser.write(bytes.fromhex(hex))
        for x in range(0, 1):
            obis_code[i] = str(ser.readline())
            indexIn = obis_code[i].find('(')
            indexOut = obis_code[i].find(')')
            obis_code[i] = obis_code[i][indexIn + 1:indexOut+1]
            indexOut = obis_code[i].find('*')
            obis_code[i] = obis_code[i][:indexOut]

    cur.execute('INSERT INTO user_gadget_hw_meter_max_dem_h (gadget_HW_id_id,kW,meterDate)'
                'VALUES ("%i","%f","%s");' %(data[0]['id'],float(obis_code['kW']),obis_code['date']+obis_code['time']))
    db.commit()
    print('append to db')
else:
	print("Cannot open serial port")
