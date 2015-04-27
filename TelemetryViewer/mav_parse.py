from libs.Mavlink.apm_mavlink_v1 import *
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from functools import partial

import sys
import struct

class TelemetryLog():

    
    def __init__(self,filepath, progbar, postread_cb, error_cb):
        self.filepath = filepath
        self.postread_cb = postread_cb
        self.error_cb = error_cb
        self.ParsePackets(progbar)
        self.decode_iterations = 100 #decode iterations per frame
        
        
    #return list of packets in file
    def ParsePackets(self, progbar):

        tlog = open(self.filepath,'r')
        self.mav = MAVLink(tlog)
        packets = []
        
        log_bytes = bytearray(tlog.read())
        log_bytes = log_bytes[8:]

        logstring = ''
        for i in range(len(log_bytes)):
            logstring += chr(int(log_bytes[i]))

        self.packets = []
        progbar.max = len(logstring)
        Clock.schedule_once(partial(self.decode_packet,
                                    logstring, progbar,
                                    len(logstring)))
        
    def decode_packet(self, logstring, progbar,initial_len,  dt):
        for i in xrange(self.decode_iterations):
            
                
            try:
            
                packet_len = ord(logstring[1])+8
            
                packet = self.mav.decode(
                    logstring[0:packet_len])
                self.packets.append(packet)
                logstring = logstring[packet_len+8:]
                progbar.value = initial_len-len(logstring)
            
            except MAVError as error:
                message = "Parsing Error:" + error.message
                Clock.schedule_once(partial(self.error_cb, message))
                return

            except:
                message = sys.exc_info()[:2]
                Clock.schedule_once(partial(self.error_cb,
                                            "Log Parse failed:" + str(message)[1:-1]))
                return

            if(len(logstring)<6):
                Clock.schedule_once(self.postread_cb)
                return
            
        Clock.schedule_once(partial(self.decode_packet,
                                    logstring,
                                    progbar,
                                    initial_len))
        
if __name__ == '__main__':
    try:
        log_path = str(sys.argv[1])
    except:
        print ("Exception: valid file path required")
        exit()
    
    TL = TelemetryLog(log_path)
    for packet in TL.packets:
        print(packet)
        
