# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 23:05:14 2019

@author: Asus
"""

import xml.etree.ElementTree as ET 
from datetime import date , datetime

#writeXML(xmlfile,pilot,UIN,lat,lon,elev,weight,payload,startTime,startDate,endDate,endTime,FP)
def writeXML(xmlfile,pilotID,UIN,lat,lon,elev,weight,pyld,startTime,startDate,endDate,endTime,FP):
    tree = ET.parse(xmlfile) 
    root = tree.getroot() 
    
    for item in root:
        for child in item: 
 
            pilot = child.find("Pilot")
            if pilot != None:
                pilot.set("uaplNo",pilotID)
            
            UA = child.find("UADetails")
            if UA != None:
                UA.set("uinNo",UIN)
            
            fP = child.find("FlightPurpose")
            if fP is not None:
                fP.set("shortDesc",FP)
            
            payload = child.find("PayloadDetails")
            if payload != None:
                payload.set("payloadDetails",pyld)
                payload.set("payloadWeight",weight)
            
            fParam = child.find("FlightParameters")
            if fParam is not None:
                fParam.set("flightStartTime",startDate+'T'+startTime)
                fParam.set("flightEndTime",endDate+'T'+endTime)
            latArr = lat
            lonArr = lon
            for grandChild in child:
                coord = grandChild.find("Coordinates")
                if coord is not None:
                    i=0
                    for c in (coord.iter('Coordinate')):
                        c.set("latitude",latArr[i])
                        c.set("longitude",lonArr[i])
                        i+=1
                        
        tree.write('output.xml')

