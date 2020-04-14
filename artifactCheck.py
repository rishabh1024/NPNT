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

# VERIFY THE XML FILE
def verifySig(file, certificate_path):
    result = verify_xml_signature(file, certificate_path)
    if result == True:
        return True
    else:
        return False

# VERIFYING THE SIGNATURE OF XML FILE
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

# Performing Time check for NPNT
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

# To create log file for telemetry data
def Telemetry_data_json(Lat, Lon, Alt):
    ## Writing to JSON TELEMETRY LOG
    if os.path.isfile("/home/pi/Current_Log/data.json"):
        with open("/home/pi/Current_Log/data.json", "r") as jsonFile:
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
        
    
    with open('/home/pi/Current_Log/data.json', 'w+') as outfile:
        json.dump(data, outfile, indent=4)


# Called in mavproxy.py for the PreArm Check required for NPNT Compliance
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
                        
                        
#create_keys('./', 'first')
##### SIGNING THE LOG FILE : TO BE EXECUTED AFTER DRONE FLIGHT i.e. DISARMING####
#sign_log('/home/pi/Current_Log/data.json', 'first_private.pem') ## SIGN THE JSON LOG
