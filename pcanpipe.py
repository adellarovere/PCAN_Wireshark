#pipe stream to wireshark ..can?? ;)
#
# "C:\Program Files\Wireshark\Wireshark.exe" -i\\.\pipe\wireshark -k
# wireshark_cmd=['C:\Program Files\Wireshark\Wireshark.exe', r'-i\\.\pipe\wireshark','-k']

#pip install pywin32

import win32pipe, win32file
import time
import subprocess
import struct

from PCANBasic import *        ## PCAN-Basic library import


def compose_packet(_id, _len, _data, timestamp_seconds, timestamp_microseconds):
    #b'\xc5\xea\x11Y\xceM\n\x00' #seconds + microseconds
    
    incl_len  = b'\x10\x00\x00\x00'
    orig_len  = b'\x10\x00\x00\x00'

    #can_id    = b'\x00\x00\x07\xdf'
    can_id = struct.pack(">I", _id)

    #can_len   = b'\x08\x00\x00\x00'
    can_len = struct.pack("<I", _len)

    #can_data  = b'\x02\x01\x11UUUUU'
    can_data = _data

    packet_data = can_id + can_len + can_data 

    packet = timestamp_seconds + timestamp_microseconds + incl_len + orig_len + packet_data

    return packet

###*****************************************************************        
if __name__ == '__main__':
    print ("                               ")
    print ("-------------------------------")
    print ("-  PCAN Wireshark pipe        -")
    print ("-  by Antonio Della Rovere    -")
    print ("-  cmd: \"C:\Program Files\Wireshark\Wireshark.exe\" -i\\.\pipe\wireshark -k -")
    print ("-------------------------------")

    pcan = PCANBasic()
    baudrate = PCAN_BAUD_500K
    hwtype = PCAN_TYPE_ISA
    ioport = 0x2A0
    interrupt = 11
    
    # Connects a selected PCAN-Basic channel
    #
    result =  pcan.Initialize(PCAN_USBBUS1,baudrate,hwtype,ioport,interrupt)    
    pcan.Reset(PCAN_USBBUS1)

    CAN_Receive = TPCANMsg()
    
    #create the named pipe \\.\pipe\wireshark
    pipe = win32pipe.CreateNamedPipe(
        r'\\.\pipe\wireshark',
        win32pipe.PIPE_ACCESS_OUTBOUND,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        300,
        None)
    
    #connect to pipe
    win32pipe.ConnectNamedPipe(pipe, None)
    
    # libpcap header for CAN Bus data. See https://wiki.wireshark.org/Development/LibpcapFileFormat
    #
    header = b'\xd4\xc3\xb2\xa1\x02\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\xe3\x00\x00\x00'

    first = 1
    #wait 2 second (not mandatory, but this let watching data coming trough the pipe)
    time.sleep(2)

    while(1):
        Status, CAN_Receive, Timestamp = pcan.Read(PCAN_USBBUS1)
        if CAN_Receive.ID > 0:
            #timestamp = int(time.time()) 
            #timestamp_seconds = struct.pack("<I", timestamp)
            timestamp_seconds = struct.pack("<I", int(Timestamp.millis//1000))
        
            #timestamp_microseconds = b'\x00\x00\x00\x00'
            timestamp_microseconds = struct.pack("<I", int((Timestamp.millis%1000)*1000 + Timestamp.micros))
    
            print (Timestamp.millis/1000, Timestamp.micros, '\n')
            packet = compose_packet(CAN_Receive.ID, CAN_Receive.LEN, bytes(CAN_Receive.DATA), timestamp_seconds, timestamp_microseconds)
            if first == 1:
                first = 0
                packet = header + packet
            else:
                packet = packet
        win32file.WriteFile(pipe, packet)

    #open and read an arbitrary pcap file (file must in same folder than script)
    #cf = open(r'ipv4frags.pcap', 'rb')
    #cf = open(r'pipetest.pcap', 'rb')
    #data = cf.read()

#then pcap data appears into wireshark
