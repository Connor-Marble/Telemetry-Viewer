import mav_parse as mp
from libs.Mavlink.apm_mavlink_v1 import MAVLink_global_position_int_message as position 

def tlog_to_kml(log, output):
    isrelaventpacket = lambda x:type(x) is position
    
    locations = []
    locationpackets = filter(isrelaventpacket, log)

    locations = [(x.lat, x.lon) for x in locationpackets]

    with open(output, 'w') as kml_file:
        pass #TODO: draw path of netquad in file using locations list
    
    print locations
            

if __name__=='__main__':
    testpath = '/Logs/2014-09-29 14-14-38.tlog'
    log = mp.TelemetryLog(testpath).ParsePackets()
    tlog_to_kml(log, 'test.kml')
