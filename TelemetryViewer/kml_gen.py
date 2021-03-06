import mav_parse as mp
from libs.pykml.factory import KML_ElementMaker as KML
from libs.Mavlink.apm_mavlink_v1 import\
    MAVLink_global_position_int_message as position 
from lxml import etree

def tlog_to_kml(log, output):

    INT_FLOAT_COORD_RATIO = 10000000
    CM_PER_METER = 100
    
    isrelaventpacket = lambda x:type(x) is position
    
    locations = []
    locationpackets = filter(isrelaventpacket, log)

    locations = [(float(x.lon)/INT_FLOAT_COORD_RATIO,
                  float(x.lat)/INT_FLOAT_COORD_RATIO,
                  float(x.relative_alt)/CM_PER_METER)
                 for x in locationpackets]

    kmlcontents = KML.Placemark(KML.LineString(
        KML.altitudeMode('absolute'),
        KML.coordinates(linefromcords(locations))))
    
    kmldoc = KML.kml(KML.Document(*kmlcontents))

    
    with open(output, 'w') as kml_file:
        kml_file.write(etree.tostring(kmldoc, pretty_print=True))

    print('saved ' + output)
        
def linefromcords(coordinates):
    #convert array to string and remove square brackets
    coordstr = str(coordinates)[1:-2]

    #remove all spaces
    coordstr = coordstr.replace(' ', '')

    #remove all parentheses and add space between points
    coordstr = coordstr.replace('),', ' ')
    coordstr = coordstr.replace('(', '')
    return coordstr
    
if __name__=='__main__':
    testpath = '/Logs/2014-09-29 14-14-38.tlog'
    log = mp.TelemetryLog(testpath).ParsePackets()
    tlog_to_kml(log, 'test.kml')
    
