import serial
from xmodem import XMODEM
from time import sleep

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=57600)
#s.open()

'''def getc(size, timeout=1):
    return s.read(size)
def putc(data, timeout=1):
    s.write(data)
modem = XMODEM(getc, putc)

stream = open('file.txt', 'wb')
modem.recv(stream)
s.close()'''

ser.write("<<SENDFILE>>\n") #tell server we are ready to recieve
readline = lambda : iter(lambda:ser.read(1),"\n")
with open("some.json","wb") as outfile:
   while True:
       line = "".join(readline())
       if line == "<<EOF>>":
           break #done so stop accumulating lines
       print >> outfile,line
