from libs.Mavlink.apm_mavlink_v1 import *
from kivy.uix.progressbar import ProgressBar

import sys
import struct

class TelemetryLog():
    def __init__(self,filepath, progbar, callback):
        self.filepath = filepath
        self.packets = self.ParsePackets(progbar)
        
    #return list of packets in file
    def ParsePackets(self, progbar):

        tlog = open(self.filepath,'r')
        mav = MAVLink(tlog)
        packets = []
        log_bytes = bytearray(tlog.read())
        log_bytes = log_bytes[8:]

        file_end = False

        logstring = ''
        for i in range(len(log_bytes)):
            logstring += chr(int(log_bytes[i]))

        try:
            while len(logstring)>6:
                packet_len = ord(logstring[1])+8
                
                packet = mav.decode(logstring[0:packet_len])
                packets.append(packet)
                logstring =  logstring[packet_len+8:]
                
        except MAVError as error:
            print("Parsing Error: ")
            print error
            return None

        return packets
             

if __name__ == '__main__':
    try:
        log_path = str(sys.argv[1])
    except:
        print ("Exception: valid file path required")
        exit()
    
    TL = TelemetryLog(log_path)
    for packet in TL.packets:
        print(packet)
        
