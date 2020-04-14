# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 16:03:05 2019

@author: Asus
"""

import xml.etree.ElementTree as ET 
from datetime import date , datetime
import cryptography
import signxml as sx
import os
import json

#to be used after generation of log
from helpers import sign_log, create_keys
from helpers import verify_flight_log_signature
from lxml import etree


def verifySig(file, certificate_path):
    result = verify_xml_signature(file, certificate_path)
    if result == True:
        return True
    else:
        return False

def verify_xml_signature(xml_file, certificate_path):
    """
    Verify the signature of a given xml file against a certificate
    :param path xml_file: path to the xml file for verification
    :param certificate_path: path to the certificate to be used for verification
    :return: bool: the success of verification
    """
    # TODO -  refactor such that this verifies for generic stuff
    tree = etree.parse(xml_file)
    root = tree.getroot()
    with open(certificate_path) as f:
        certificate = f.read()
        # for per_tag in root.iter('UAPermission'):
        #     data_to_sign = per_tag
        try:
            print("Verifying Signature......")
            verified_data = sx.XMLVerifier().verify(data=root, require_x509=True, x509_cert=certificate).signed_xml
            # The file signature is authentic
            return True
        except cryptography.exceptions.InvalidSignature:
            # print(verified_data)
            # add the type of exception
            return False
        
def coordCheck(coord): 
    
    coord_list = []
    
    for i,value in enumerate(coord):            
            lon = (value.attrib.get("longitude"))
            lat = (value.attrib.get("latitude"))
            coord_list.append((lat, lon))
            
    return coord_list

def timeCheck(startTime,endTime,coord):
    Time_check = False    
    nowTime = str(datetime.now().strftime("%H:%M:%S"))
    if endTime > startTime:
        if startTime <= nowTime <= endTime:
            #MAV.doARM(1)
            print("Time Check Pass")
            Time_check = True
            coord_list = coordCheck(coord)
            return coord_list, Time_check
        else:
            print("Time Check Failed")
            coord_list = []
            return coord_list, Time_check

def Telemetry_data_json(Lat, Lon, Alt):
    ## Writing to JSON TELEMETRY LOG
    if os.path.isfile("data.json"):
        with open("data.json", "r") as jsonFile:
            data = json.load(jsonFile)
    else:
        data = {}
        data['FlightLog'] = []
    
    time = str(datetime.now()).split(' ')[1]
    data['FlightLog'].append({
        'TimeStamp': (time),
        'Longitude': float(Lon),
        'Latitude': float(Lat),
        'Altitude': float(Alt),
        'CRC': 200
    })
        
    
    with open('data.json', 'w+') as outfile:
        json.dump(data, outfile, indent=4)

def parseXML(xml):
    tree = ET.parse(xml) 
    root = tree.getroot() 
    today = str(date.today())
    
    Date_check = False
    Time_check = False
            
    for item in root:
        
        # iterate child elements of item 
        for child in item: 
            
            pilot = child.find("Pilot")
            if pilot != None:
                p = pilot.attrib.get('uaplNo')
                #print("pilot id :",p) 
            for grandChild in child:
                grand = (grandChild.tag)

                ## extract corrdinates ##
                coord = grandChild.find("Coordinates")   
                if grand == "FlightParameters":
                    startDT = grandChild.attrib.get("flightStartTime")
                    endDT = grandChild.attrib.get("flightEndTime")
                    
                    startDate  = (startDT.split('T')[0])
                    endDate = endDT.split('T')[0]
                    startTime = startDT.split('T')[1].split('+')[0]
                    endTime = endDT.split('T')[1].split('+')[0]
                    print("Performing Pre-Arm checks")
                    if startDate <= today and endDate >= today:
                        print("Date Check Pass.")
                        Date_check = True;
                        coord_list, Time_check = timeCheck(startTime,endTime,coord)
                        return coord_list, Date_check, Time_check
                    else:
                        print("Date Check Failed.")
                        coord_list = []
                        return coord_list, Date_check, Time_check
                        
                    '''else:
                        msg = ("Invalid Date.Try another artifact.")
                        form = statusWindow(msg)
                        Application.Run(form)'''

'''                    
import chilkat2

dsig = chilkat2.XmlDSig()
success = dsig.LoadSignature('<Signature xmlns="http://www.w3.org/2000/09/xmldsig#"><SignedInfo><CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/><SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/><Reference><Transforms><Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/><Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/></Transforms><DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/><DigestValue>vRp3mPzONXuxHBJo+MLt44hz5f0lDV3nBvuIYsLxhNI=</DigestValue></Reference></SignedInfo><SignatureValue>rv5d/6VFgmWxYv1HVijWTE++j8S0SG1cQKfkniNf0Ah02kxeLDiI5y9eCZaqPRX5SztmCH1e6fDWKoRdm9shmvg85jNzkYfgbgZn2RhJ5ZH73eUqJUTN1cQajJKms6YHUHItVPRDxrAyrCAXuGhYa/k2wXO9silQ2bCee4Z3+Jr7pZCS/huNKu/1C2VDVsNy7whXUy2ina4VJF7kUDDO5bIc9nE3mxTjirLdDpNbpiuF2H9cBDsjdvHHrUo57atVPUYeMdvFOTqgjeJlpupInTCtOLktZMU+xzf8HAV5PrVy8cod+kqyuXtqYRG9gRWOEL/f6NPOBf9T1YY0ExP3GA==</SignatureValue><KeyInfo><X509Data><X509Certificate>MIIEdzCCA1+gAwIBAgIUNRGVDfGhq8Oxr1JyC1QuDaPMJmswDQYJKoZIhvcNAQEFBQAwgcoxCzAJBgNVBAYTAklOMQswCQYDVQQIDAJLQTESMBAGA1UEBwwJQmVuZ2FsdXJ1MSkwJwYDVQQKDCBBbGdvcGl4ZWwgVGVjaG5vbG9naWVzIFB2dC4gTHRkLjEeMBwGA1UECwwVaURyb25lUG9ydCBEUyBSZXBsaWNhMSgwJgYDVQQDDB9hbGdvcGl4ZWwtaWRyb25lcG9ydC1kcy1yZXBsaWNhMSUwIwYJKoZIhvcNAQkBFhZjb250YWN0QGFsZ29waXhlbC50ZWNoMB4XDTE5MDMxNDA5NDY1NFoXDTIwMDMxMzA5NDY1NFowgcoxCzAJBgNVBAYTAklOMQswCQYDVQQIDAJLQTESMBAGA1UEBwwJQmVuZ2FsdXJ1MSkwJwYDVQQKDCBBbGdvcGl4ZWwgVGVjaG5vbG9naWVzIFB2dC4gTHRkLjEeMBwGA1UECwwVaURyb25lUG9ydCBEUyBSZXBsaWNhMSgwJgYDVQQDDB9hbGdvcGl4ZWwtaWRyb25lcG9ydC1kcy1yZXBsaWNhMSUwIwYJKoZIhvcNAQkBFhZjb250YWN0QGFsZ29waXhlbC50ZWNoMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt0aHtTg/NPvWwksUY4kYbkatfmliGrUe30C3eDy0GFLpTqHQV+g4wkWovqfu3tvd0FMjlRdbPOI6gGBcG9yIA5tTXUcVEDwCi50TuiIAN4QINWzS6I+cvCqIwEZk3Yih64MRjPHoUrm4zyr0ihMU/XjDqG7cu2QNY/gBX+LD86qcQRcV+7wq/7OW+aWq1bZFiI9pMraHWhrMvj3kthjDT4RbeYNE9JjHIePMmH7hSi67rQLingQ8+ccK7P7bc+Yfj34FBxZIh0m0NPZO/nsgL1ZqqheV+WtY9eZs71CZK8hSJXTMEw5EaXaZMF7i5LjJnU09PHVXwoBHZ1FpqQyUZQIDAQABo1MwUTAdBgNVHQ4EFgQUAT2SZyZlEFy53FeRG4+vhFa1bsEwHwYDVR0jBBgwFoAUAT2SZyZlEFy53FeRG4+vhFa1bsEwDwYDVR0TAQH/BAUwAwEB/zANBgkqhkiG9w0BAQUFAAOCAQEAKRMAJH5Gyo1N2+ZDKuk3RIH+nKdSndD6nJRlAp2F3cW+RrAHPzpQVIgBHWXY95vY4rXG50JqJ+Vq485i/7MNOSCduFEwJK7K5fRTaSm8tPUwfowdcr5t4SEwZyYwmq3TZl8LZ+E0AJVHhfjio7Mmg1ruMDiOOy1d9EG9+/9WB3rKHjYL/wXr7WXhANz6w7tkxESkMPXjPY8Pxwj9H9wZonn+yOW+jgf1/+WGHqpH7VBsUfD1TEc8ygWX9iQUOD7pWtZ/VF1ETY9QzQhZb+1lHQyOLhWg55utmjGrFpbUM24SaiN88deMxd0lOp50tpYR8EbLuPH4LuHWvlgMKbepFw==</X509Certificate></X509Data></KeyInfo></Signature></UAPermission>')

numSignatures = dsig.NumSignatures
i = 0
print("Verifying signature......")

dsig.Selector = i

bVerifyRefDigests = False
bSignatureVerified = dsig.VerifySignature(bVerifyRefDigests)
if (bSignatureVerified):
    print("Signature " + str(i + 1) + " verified")
else:
    print("Signature " + str(i + 1) + " invalid")

# Check each of the reference digests separately..
numRefDigests = dsig.NumReferences
j = 0
while j < numRefDigests :
    bDigestVerified = dsig.VerifyReferenceDigest(j)
    print("reference digest " + str(j + 1) + " verified = " + str(bDigestVerified))
    if (bDigestVerified == False):
        print("    reference digest fail reason: " + str(dsig.RefFailReason))

    j = j + 1'''



    #xmlfile = r"D:\NPNT\f4a8db10-ee97-11e9-9987-6f120097227b\permission_artifact_3.xml"
    #xmlfile = ("permission_artifact_breach.xml")
    #parseXML(xmlfile)

'''
setWayPoints()
    Gidmavcmd = MAVLink.MAV_CMD.WAYPOINT
    id = int(idmavcmd)
    print("id",id)
    numWP = len(coord)     
    waypoint = []   
    homelng = float(coord[0].attrib.get("longitude"))
    homelat = float(coord[0].attrib.get("latitude"))
    home = Locationwp().Set(homelat, homelng,0, id)    
    takeoff = Locationwp()
    Locationwp.id.SetValue(takeoff, int(MAVLink.MAV_CMD.TAKEOFF))
    Locationwp.p1.SetValue(takeoff, 15) #pitch
    Locationwp.alt.SetValue(takeoff, 50) #launch altitude
    wp = Locationwp().Set(lat, lon,50, id)
    waypoint.append(wp)
    MAV.setWPTotal(numWP)
    MAV.setWP(home,0,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
    MAV.setWP(takeoff,1,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);        
    for j in range (len(waypoint)):
        #print(i)
        MAV.setWP(waypoint[j],j+1,MAVLink.MAV_FRAME.GLOBAL_RELATIVE_ALT);
    MAV.setWPACK();'''


#create_keys('./', 'first')
sign_log('data.json', 'first_private.pem') ## SIGN THE JSON LOG