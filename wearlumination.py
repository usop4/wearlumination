import serial
import tocotika
import time
import sys
import webbrowser
from bottle import response,route,run,static_file

arduino_tty = '/dev/tty.usbmodem14121'
tocostick_tty = '/dev/tty.usbserial-AHXMUX35'

try:
    ser = serial.Serial(arduino_tty,baudrate=115200, timeout=0.1)
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
r:
<a href="http://localhost:8946/command/r0">0</a>
<a href="http://localhost:8946/command/r9">9</a>
g:
<a href="http://localhost:8946/command/g0">0</a>
<a href="http://localhost:8946/command/g9">9</a>
<br />
'''

graph1 = '''
<canvas id="lineChart" height="300" width="200" style="width:210px;height:300px;"></canvas>
<script src="/static/jQuery-2.1.4.min.js"></script>
<script src="/static/Chart.min.js" type="text/javascript"></script>
<script>
    var areaChartData;
    $(document).ready(function() {
        areaChartData = {
            labels: [1,2,3,4,5,6,7,8,9,10],
            datasets: [
                {
                    label: "sensor1",
                    strokeColor: "rgba(94, 2, 49, 1)",
                    data: []
                },
                {
                    label: "sensor2",
                    strokeColor: "rgba(60,141,188,0.8)",
                    data: []
                }
            ]
        };
        var areaChartOptions = {
            pointDot: false,
            datasetStroke: true,
            datasetFill: true,
        };
'''

graph2 = '''

        var lineChartCanvas = $("#lineChart").get(0).getContext("2d");
        var lineChart = new Chart(lineChartCanvas);
        var lineChartOptions = areaChartOptions;
        lineChartOptions.datasetFill = false;
        lineChart.Line(areaChartData, lineChartOptions);
    });
</script>'''
count = 0;

@route('/')
def send_index():
    return static_file('index.html', root='./')

@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static')

@route('/img/<filename:path>')
def send_img(filename):
    return static_file(filename, root='./img')

@route('/command/<command>')
def command(command):
    response.set_header('Access-Control-Allow-Origin','*')
    try:
        if command[0] == "r":
            toco.analogWrite(1,int(command[1])*10)
        if command[0] == "g":
            toco.analogWrite(2,int(command[1])*10)
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
    global count
    list1 = []
    list2 = []
    response.set_header('Access-Control-Allow-Origin','*')
    for i in range(30):
        #print list1
        try:
            sensor = ser.readline().rstrip().split(",")

            list1.append(int(sensor[0]))
            list2.append(int(sensor[1]))

            val1 = map(int(sensor[0]),0,1024,0,128)
            val1 = int(val1 * val1 / 256)
            val2 = map(int(sensor[1]),0,1024,0,128)
            val2 = int(val2 * val2 / 256)

            if toco:
                count = count + 1;
                if count % 2 == 0:
                    toco.analogWrite(1,val1)
                else:
                    toco.analogWrite(2,val2)
                print sensor,val1,val2

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
    desc = "";
    i = 0;
    for val in list1:
        desc = desc + "areaChartData.datasets[0].data["+str(i)+"] = "+str(val)+";"
        i = i + 1
    i = 0;
    for val in list2:
        desc = desc + "areaChartData.datasets[1].data["+str(i)+"] = "+str(val)+";"
        i = i + 1

    desc = graph1 + desc + graph2
    return link+desc+'<script>location.reload();</script>'

def map(value, fromLow, fromHigh, toLow, toHigh):
    if value < fromLow:
        return toLow
    if value > fromHigh:
        return toHigh
    return int((value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow))

webbrowser.open("http://localhost:8946/")
#webbrowser.open("http://localhost:8946/command/r0")
run(host="localhost",port=8946,debug=True)
