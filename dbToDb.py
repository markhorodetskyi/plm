import pymysql
import time
from subprocess import Popen, PIPE
from pppd import PPPConnection
import RPi.GPIO as GPIO
import json

with open("settings.json", "r") as read_file:
    data = json.load(read_file)

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(40, GPIO.OUT, initial=GPIO.HIGH)
#
# GPIO.output(40, 0)
# print('reboot gprs module')
# time.sleep(4)
# GPIO.output(40, 1)
# print('reboot ok')
# GPIO.cleanup()
# print('whait 60 sec for search network')
# time.sleep(20)

maxId = 0
select = ''
avTabl= ''
col= 0
tabToIns=''
colToIns=''
dataToIns=''
command = ''
counter=0

# gprs = Popen(["sudo", "pppd", "call","gprs"], shell=False)

# time.sleep(30)
# print(gprs)
p = Popen(["ping", "-c", "3","www.google.com"], stdout=PIPE)
output, err = p.communicate()
output = str(output)
searchMAMM=output.find('min/avg/max/mdev')
stage1=output[searchMAMM:]
searchEquals=stage1.find('=')
stage2=stage1[searchEquals:]
searchSlash=stage2.find('/')
stage3=stage2[searchSlash+1:]
searchSlash2=stage3.find('/')
ping=stage3[:searchSlash2]
ping=float(ping)
print(ping)
if(ping<=800):
    print('Connected')
    print('ping is '+str(ping))
    dbOut = pymysql.connect(host="213.174.22.133", user="root", passwd="02071228", db="webPLA", port=3307)
    dbLoc = pymysql.connect(host="localhost", user="plaUser", passwd="plasystem", db="plm", port=8744)
    curOut = dbOut.cursor()
    curLoc = dbLoc.cursor()

    curOut.execute("show tables;")
    avTabl=curOut.fetchall();
    for i in range(2, len(avTabl)):
        counter=0
        tabToIns = str(avTabl[i])
        if (tabToIns[2:-3] =='user_gadget_hw_meter' or tabToIns[2:-3] =='user_gadget_hw_meter_max_dem_h'):
            command = 'show columns from '+ tabToIns[2:-3] + ';'
            curOut.execute(command)
            col = curOut.fetchall();
            colToIns=''

            for c in col:
                if c[0] != 'id':
                    if c[0] == 'gadget_HW_id_id':
                        colToIns += c[0]
                    else:
                        colToIns += c[0]+ ','
            command = 'SELECT MAX(meterDate) FROM %s WHERE gadget_HW_id_id = %i' %(tabToIns[2:-3],data[0]["id"])
            curOut.execute(command)
            maxId = curOut.fetchone();
            if(maxId[0]==None):
                curLoc.execute("SELECT * FROM %s" %(tabToIns[2:-3]))
                select=curLoc.fetchall();
                for a in select:
                    for c in a[1:]:
                        dataToIns +=str(c)+','
                    command = 'INSERT INTO webPLA.'+str(tabToIns[2:-3])+'('+str(colToIns)+') VALUES ('+dataToIns[:-1]+');'
                    curOut.execute(command)
                    dbOut.commit()
                    counter+=1
                    dataToIns = ''
                print("insert "+str(counter)+" row(s) to "+tabToIns[2:-3])
                print(ping)
            else:
                print("SELECT * FROM %s WHERE meterDate > %i" % (tabToIns[2:-3],maxId[0]))
                curLoc.execute("SELECT * FROM %s WHERE meterDate > %i" % (tabToIns[2:-3],maxId[0]))

                select = curLoc.fetchall();
                for a in select:
                    for c in a[1:]:
                        dataToIns +=str(c)+','
                    command = 'INSERT INTO webPLA.'+str(tabToIns[2:-3])+'('+str(colToIns)+') VALUES ('+dataToIns[:-1]+');'
                    curOut.execute(command)
                    dbOut.commit()
                    counter += 1
                    dataToIns = ''
                    print(counter)
                print("insert " + str(counter) + " row(s) to " + tabToIns[2:-3])
                print(ping)
    # gprs = Popen(["sudo", "poff", "gprs"], stdout=PIPE, shell=False)
