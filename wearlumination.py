import serial
import tocotika
import time
import sys
import webbrowser
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
    toco = False
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
        toco.analogWrite(1,0)
        toco.analogWrite(2,0)
        raise
    return link

@route('/sensor')
def sensor():
    list1 = []
    response.set_header('Access-Control-Allow-Origin','*')
    for i in range(30):
        #print list1
        try:
            sensor = ser.readline().rstrip().split(",")
            list1.append(int(sensor[0]))

            val1 = map(int(sensor[0]),0,1024,0,256)
            val1 = int(val1 * val1 / 256)
            val2 = map(int(sensor[1]),0,1024,0,256)
            val2 = int(val2 * val2 / 256)

            if toco:
                toco.analogWrite(1,val1)
                toco.analogWrite(2,val2)

        except ValueError:
            pass
        except IndexError:
            pass
        except:
            print sys.exc_info()[0]
            if toco:
                toco.analogWrite(1,0)
                toco.analogWrite(2,0)
            raise
    min1 = sorted(list1)[0]
    max1 = sorted(list1,reverse=True)[0]
    desc = '''
        min:%(min)s,
        max:%(max)s,
    ''' % {"min":min1, "max":max1}
    return link+desc+'<script>location.reload();</script>'

def map(value, fromLow, fromHigh, toLow, toHigh):
    if value < fromLow:
        return toLow
    if value > fromHigh:
        return toHigh
    return int((value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow))

webbrowser.open("http://localhost:8946/sensor")
run(host="localhost",port=8946,debug=True)
