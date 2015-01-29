import mav_parse as mp
from pykml.factory import KML_ElementMaker as KML
from libs.Mavlink.apm_mavlink_v1 import\
    MAVLink_global_position_int_message as position 
from lxml import etree

def tlog_to_kml(log, output):

    INT_FLOAT_COORD_RATIO = 10000000
    
    isrelaventpacket = lambda x:type(x) is position
    
    locations = []
    locationpackets = filter(isrelaventpacket, log)

    locations = [(float(x.lon)/INT_FLOAT_COORD_RATIO,
                  float(x.lat)/INT_FLOAT_COORD_RATIO,
                  float(x.relative_alt)/100)
                 for x in locationpackets]

    kmlcontents = KML.Placemark(KML.LineString(
        KML.altitudeMode('absolute'),
        KML.coordinates(linefromcords(locations))))
    
    kmldoc = KML.kml(KML.Document(*kmlcontents))

    
    with open(output, 'w') as kml_file:
        kml_file.write(etree.tostring(kmldoc, pretty_print=True))
        
def linefromcords(coordinates):
    coordstr = str(coordinates)[1:-2]
    coordstr = coordstr.replace(' ', '')
    coordstr = coordstr.replace('),', ' ')
    coordstr = coordstr.replace('(', '')
    return coordstr
    
if __name__=='__main__':
    testpath = '/Logs/2014-09-29 14-14-38.tlog'
    log = mp.TelemetryLog(testpath).ParsePackets()
    tlog_to_kml(log, 'test.kml')
    
