import sys
import string
import binascii
input1 = open("gujarati_in.txt","rb")
output= open("utf8encoder_out.txt","wb")

while True:
    byte1=input1.read(2)
    if byte1 =="":
        break;
    hex_bytes =binascii.hexlify(byte1) 
    i=int(hex_bytes,16)
    s='0000007F'
    oneByte=int(s,16)
    s='00000080'
    twoByteStart=int(s,16)
    s='000007FF'
    twoByteEnd=int(s,16)
    s='00000800'
    threeByteStart=int(s,16)
    s='0000FFFF'
    threeByteEnd=int(s,16)
    x=bin(i)[2:]
    if i>=0 and i<=oneByte:
        utfOneByte=x.zfill(7)
        utfOneByte = '0'+utfOneByte
        utfWrite =int(utfOneByte,2)
        output.write(chr(utfWrite))
        
    if i>=twoByteStart and i<=twoByteEnd:
        utfOneByte=x[-6:].zfill(6)
        utfOneByte = '10'+utfOneByte
        utfTwoByte=x[:-6].zfill(5)
        utfTwoByte = '110'+utfTwoByte
        utfWrite =int(utfTwoByte,2)
        #print utfTwoByte,utfOneByte
        output.write(chr(utfWrite))
        utfWrite =int(utfOneByte,2)
        output.write(chr(utfWrite))
        
    if i>=threeByteStart and i<=threeByteEnd:
        utfOneByte=x[-6:].zfill(6)
        utfOneByte = '10'+utfOneByte
        utfTwoByte=x[-12:-6].zfill(6)
        utfTwoByte = '10'+utfTwoByte
        utfThreeByte=x[:-12].zfill(4)
        utfThreeByte = '1110'+utfThreeByte
        utfWrite =int(utfThreeByte,2)
        output.write(chr(utfWrite))
        utfWrite =int(utfTwoByte,2)
        output.write(chr(utfWrite))
        utfWrite =int(utfOneByte,2)
        print utfThreeByte,utfTwoByte,utfOneByte
        output.write(chr(utfWrite))