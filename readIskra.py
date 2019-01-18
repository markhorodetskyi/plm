import serial
import time
import pymysql
from convObis import ConvObis

db = pymysql.connect(host="127.0.0.1", user="plaUser", passwd="plasystem", db="plm", port=8744)
cur = db.cursor()

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=0.5)

obis_code={'kWh':'1.8.0',
           'kVArh_p': '3.8.0',
           'kVArh_n': '4.8.0',
           'kVAh': '9.8.0',
           'cur_sum_V': '12.7.0',
           'cur_L1_V': '32.7.0',
           'cur_L2_V': '52.7.0',
           'cur_L3_V': '72.7.0',
           'cur_F': '14.7.0',
           'date':'0.9.2',
           'time':'0.9.1'}
try:
	ser.isOpen()

except:
	exit()

if (ser.isOpen()):
    ser.write(str.encode('\x2f\x3f'+'67872235'+'\x21\x0d\x0a'))
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

    cur.execute('INSERT INTO gadget_HW_meter (gadget_HW_id,kWh,kVArh_p,kVArh_n,kVAh,cur_sum_V,cur_L1_V,cur_L2_V,cur_L3_V,cur_F,meterDate)'
                'VALUES (01,"%f","%f","%f","%f","%f","%f","%f","%f","%f","%f");' %(float(obis_code['kWh']),
                                                                                   float(obis_code['kVArh_p']),
                                                                                   float(obis_code['kVArh_n']),
                                                                                   float(obis_code['kVAh']),
                                                                                   float(obis_code['cur_sum_V']),
                                                                                   float(obis_code['cur_L1_V']),
                                                                                   float(obis_code['cur_L2_V']),
                                                                                   float(obis_code['cur_L3_V']),
                                                                                   float(obis_code['cur_F']),
                                                                                   float(obis_code['date']+obis_code['time'])))
    db.commit()
    print('append to db')
else:
	print("Cannot open serial port")
