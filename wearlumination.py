import serial
import tocotika
import time

ser = serial.Serial('/dev/cu.usbmodem1411',9600)
toco = tocotika.Toco('/dev/tty.usbserial-AHXMUX35')

while True:
    sensor = ser.readline().rstrip().split(",")
    try:
        toco.analogWrite(1,int(sensor[0])/4)
    except ValueError:
        pass
    except:
        pass
