import serial
from xmodem import XMODEM
from time import sleep

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=57600, bytesize=8)
# s.open()

# def getc(size, timeout=1):
#     return s.read(size)
# def putc(data, timeout=1):
#     s.write(data)
# modem = XMODEM(getc, putc)

# f = open('jjj.txt', 'rb')
# stream = f.readlines()
# status = modem.send(stream, retry=8)
# s.close()
# stream.close()


readline = lambda : iter(lambda:ser.read(1),"\n")
# while "".join(readline()) != "<<SENDFILE>>": #wait for client to request file
    # pass #do nothing ... just waiting ... we could time.sleep() if we didnt want to constantly loop
ser.write(open("command.txt","rb").read()) #send file
ser.write(b"\n<<EOF>>\n") #send message indicating file transmission complete
