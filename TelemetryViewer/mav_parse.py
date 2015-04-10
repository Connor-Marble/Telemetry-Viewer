from libs.Mavlink.apm_mavlink_v1 import *
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

import sys
import struct

class TelemetryLog():
    def __init__(self,filepath, progbar, postread_cb):
        self.filepath = filepath
        self.packets = self.ParsePackets(progbar)
        Clock.schedule_once(postread_cb)
        
    #return list of packets in file
    def ParsePackets(self, progbar):

        tlog = open(self.filepath,'r')
        mav = MAVLink(tlog)
        packets = []
        
        log_bytes = bytearray(tlog.read())
        log_bytes = log_bytes[8:]

        logstring = ''
        for i in range(len(log_bytes)):
            logstring += chr(int(log_bytes[i]))

        
        try:
            pack_start = 0
            
            while len(logstring)-pack_start>6:
                packet_len = ord(logstring[pack_start+1])+8
                
                packet = mav.decode(
                    logstring[pack_start:packet_len+pack_start])
                packets.append(packet)
                pack_start += packet_len+8
                
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
        
