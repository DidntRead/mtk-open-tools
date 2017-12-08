import serial
# DFROBOT SHIELD works with 115200, ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1)
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.1)
print(ser.name)
resp = bytearray(b'\x00')

while True:
    print "sending mtk beacon 0xa0"
    ser.write(b'\xa0')
    ser.flush()
    ser.readinto(resp)
    print " ".join("{:02x}".format(c) for c in resp)
    if resp == b'\x5f':
        print "got beacon response 0x5f, writing rest of init 0x0a 0x50 0x05"
        ser.write(b'\x0a\x50\x05')
        ser.flush()
        resp2 = ser.read(3)
        if resp2 == b'\xf5\xaf\xfa':
            print "got beacon response 0xf5 0xaf 0xfa"
            break

print "writing read address request 0xa2"
ser.write(b'\xa2')
ser.flush()

if (ser.read(1) == b'\xa2'):
    print "got read addr ack 0xa2, writing addr 0x80 0x00 0x00 0x08"
    ser.write(b'\x80\x00\x00\x08')
    ser.flush()
    resp2 = ser.read(4)
    print "got addr ack"
    print " ".join("{:02x}".format(ord(c)) for c in resp2)

    print "send read 1 word"
    ser.write(b'\x00\x00\x00\x01')
    ser.flush()
    resp2 = ser.read(6)
    print "read response:"
    print " ".join("{:02x}".format(ord(c)) for c in resp2)
    print "chip type is: {0:02x}{1:02x}".format(ord(resp2[4]),ord(resp2[5]))


else:
    print("bad response")


ser.close()
