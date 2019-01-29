from subprocess import Popen, PIPE
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT, initial=GPIO.HIGH)

GPIO.output(40, 0)
print('reboot gprs module')
time.sleep(4)
GPIO.output(40, 1)
print('reboot ok')
GPIO.cleanup()
print('whait 60 sec for search network')
time.sleep(60)

gprs = Popen(["sudo", "pppd", "call","gprs"], shell=False)

time.sleep(600)

gprs = Popen(["sudo", "poff", "gprs"], stdout=PIPE, shell=False)
