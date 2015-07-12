import serial
import tocotika
import time
import sys
from bottle import response,route,run

arduino_tty = '/dev/tty.usbmodem1411'
tocostick_tty = '/dev/tty.usbserial-AHXMUX35'
try:
    ser = serial.Serial(arduino_tty,115200)
    toco = tocotika.Toco(tocostick_tty)
except OSError as (errno,strerror):
    if errno == 2 : # No such file or directory
        print "USB device is not connected"
    else:
        print errno, strerror
    ser = False
except:
    print sys.exc_info()[0]
    raise

link = '''
<a href="http://localhost:8946/sensor">sensor</a>
<a href="http://localhost:8946/command/r0">r0</a>
<a href="http://localhost:8946/command/r9">r9</a>
'''

@route('/command/<command>')
def command(command):
    response.set_header('Access-Control-Allow-Origin','*')
    try:
        if command[0] == "r":
            toco.analogWrite(1,int(command[1])*20)
        if command[0] == "g":
            toco.analogWrite(1,int(command[1])*20)
    except ValueError:
        pass
    except:
        print sys.exc_info()[0]
        raise
    return link

@route('/sensor')
def sensor():
    response.set_header('Access-Control-Allow-Origin','*')
    for i in range(30):
        try:
            sensor = ser.readline().rstrip().split(",")
            val = int(sensor[0])/4
            val = int(val * val / 256)
            if toco:
                toco.analogWrite(1,val)
                print i,val
        except ValueError:
            pass
        except:
            print sys.exc_info()[0]
            raise
    return link+'<script>location.reload();</script>'

run(host="localhost",port=8946,debug=True)
