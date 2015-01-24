import mav_parse as mp
from pykml.factory import KML_ElementMaker as KML
from libs.Mavlink.apm_mavlink_v1 import MAVLink_global_position_int_message as position 
from lxml import etree

def tlog_to_kml(log, output):
    
    isrelaventpacket = lambda x:type(x) is position
    
    locations = []
    locationpackets = filter(isrelaventpacket, log)

    locations = [(x.lat, x.lon) for x in locationpackets]

    kmldoc = KML.kml(
        KML.Placemark(
            KML.name("kml_name")))

    
    with open(output, 'w') as kml_file:
        kml_file.write(etree.tostring(kmldoc, pretty_print=True))
    

            

if __name__=='__main__':
    testpath = '/Logs/2014-09-29 14-14-38.tlog'
    log = mp.TelemetryLog(testpath).ParsePackets()
    tlog_to_kml(log, 'test.kml')
    
