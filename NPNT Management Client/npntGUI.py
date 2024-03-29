# -*- coding utf-8 -*-
"""
Created on Tue Oct 29 212314 2019

@author Asus
"""

# -*- coding utf-8 -*-
"""
Created on Sun Feb 24 114126 2019

@author Asus
"""

from tkinter import filedialog
#import tkFileDialog
from tkinter import *

from tkinter import *
#import tkMessageBox
import tkinter as tk
import tkinter.messagebox 
#from change_metadata import *
from datetime import date, datetime
from writeXml import *


def openFile():
    global file
    
    file = filedialog.askopenfilename(parent=root, initialdir= "/",title='Select public key',filetypes = (("pem files","*.pem"),("all files","*.*")))
    fileLabel = tk.Label(root, text=file, fg = "BLACK",bg = "white", bd=2,font = 'Calibri 10')
    fileLabel.place(relx=0.57,rely=0.43,anchor=W)
    
    
def checkDateTime(startDate,startTime,endDate,endTime):
    #if '-' not in startDate or '-' not in endDate or ':' not in startTime or ':' not in endTime:
    #        tkMessageBox.showinfo("Error","Enter correct format of date and time!")    
    
    check = False
    sd = startDate.split('-')
    ed = endDate.split('-')
    st = startTime.split(':')
    et = endTime.split(':')
    current_date = str(datetime.now())
    print(current_date)
    
    if (len(sd[0]),len(sd[1]),len(sd[2])) != (4,2,2) or (len(ed[0]),len(ed[1]),len(ed[2])) != (4,2,2):
        tkinter.messagebox.showinfo("Error","Enter correct format of date!")    
     
    ##check validity of date
    elif int(sd[2])>31 or int(ed[2]) >31 or int(sd[1]) > 13 or int(ed[1]) >13 or int(sd[0]) < 2020 or int(ed[0]) <2020:
    #elif not (0,0)<(sd[2],ed[2])<=(31,31) and (0,0)<(sd[1],ed[1])<(13,13) and (2019,2019)<(sd[0],ed[0]):
        tkinter.messagebox.showinfo("Error","Invalid date!")    
    
    elif (len(st[0]),len(st[1])) != (2,2) or (len(et[0]),len(et[1])) != (2,2):
        tkinter.messagebox.showinfo("Error","Enter correct format of time!")
    elif not (0,0)<(int(st[0]),int(et[0]))<=(24,24) and (0,0)<(int(st[1]),int(et[1]))<=(60,60):
        tkinter.messagebox.showinfo("Error","Invalid time!")    
    else:
        check = True
    return check
        
def callback():
    
    pilot = pltVal.get()
    UIN = UINVal.get()
    
    pt1lat = pt1latVal.get()
    pt2lat = pt2latVal.get()
    pt3lat = pt3latVal.get()
    pt4lat = pt4latVal.get()
    pt1lon = pt1lonVal.get()
    pt2lon = pt2lonVal.get()
    pt3lon = pt3lonVal.get()
    pt4lon = pt4lonVal.get()
    
    lat = [pt1lat,pt2lat,pt3lat,pt4lat]
    lon = [pt1lon,pt2lon,pt3lon,pt4lon]
    elev = altVal.get()
    weight = wghtVal.get()
    payload = pyLdVal.get()
    startDate = SDVal.get()
    endDate = EDVal.get()
    startTime = STVal.get()
    endTime = ETVal.get()
    FP = FPVal.get()
    
    if pt1lat == '' or pt2lat == '' or pt3lat =='' or pt4lat == '' or pt1lon == '' or pt2lon == '' or pt3lon =='' or pt4lon == '':
        tkinter.messagebox.showinfo("Error","Enter all points!")
        pass
    elif startDate =='' or endDate == '' or startTime =='' or endTime == '' or UIN == '':
        tkinter.messagebox.showinfo("Error","Enter all required fields!")
        pass
    
    
    else:
        check = checkDateTime(startDate,startTime,endDate,endTime)    
        if check == True:
            if pilot == '' :
                pilot = 'Not Specified'
            if weight == '':
                weight = 'Not Specified'
            if payload == '' :
                payload = 'Not Specified'
            if FP =='' :
                FP = 'Not Specified'
            if elev == '':
                 elev = 220
            
            xmlfile = ("xmlTemplate.xml")
            
            writeXML(xmlfile,pilot,UIN,lat,lon,elev,weight,payload,startTime,startDate,endDate,endTime,FP)
            tkinter.messagebox.showinfo("Info","Request generated!")
            root.destroy()
        else:
            pass
if __name__ == "__main__":
        
    root = tk.Tk()
    root.title("NPNT Management Client")
    
    root.geometry("700x450")
    frame=tk.Frame(root)
    root.configure(background='white')
    root.iconbitmap(default=r"0.ico")

    frame.pack()
    
    pltLabel = tk.Label(root, text="Pilot No", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 12')
    pltLabel.place(relx=0.05,rely=0.1,anchor=W)
    
    pltVal = tk.Entry(root,width=25,bg = 'light grey')
    pltVal.place(relx=0.25,rely=0.1,anchor=W)
    
    UINLabel = tk.Label(root, text="Drone UIN", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 12 ')
    UINstarLabel = tk.Label(root, text="*", fg = "red",bg = "white", bd=2,font = 'Calibri 10')
    UINLabel.place(relx=0.5,rely=0.1,anchor=W)
    UINstarLabel.place(relx=0.6,rely=0.1,anchor=W)
    
    UINVal = tk.Entry(root,width=28,bg = 'light grey')
    UINVal.place(relx=0.67,rely=0.1,anchor=W)
    
    
    latLabel = tk.Label(root, text="Latitude", fg = "BLACK",bg = "white", bd=2,font = 'Calibri 13')
    latLabel.place(relx=0.27,rely=0.18,anchor=W)
    lonLabel = tk.Label(root, text="Longitude", fg = "BLACK",bg = "white", bd=2,font = 'Calibri 13')
    lonLabel.place(relx=0.41,rely=0.18,anchor=W)
    
    pt1Label = tk.Label(root, text="Point 1", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 12')
    pt1Label.place(relx=0.05,rely=0.26,anchor=W)
    pt1starLabel = tk.Label(root, text="*", fg = "red",bg = "white", bd=2,font = 'Calibri 10')
    pt1starLabel.place(relx=0.12,rely=0.26,anchor=W)
    
    pt2Label = tk.Label(root, text="Point 2", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 12 ')
    pt2Label.place(relx=0.05,rely=0.32,anchor=W)
    pt2starLabel = tk.Label(root, text="*", fg = "red",bg = "white", bd=2,font = 'Calibri 10')
    pt2starLabel.place(relx=0.12,rely=0.32,anchor=W)
    
    pt3Label = tk.Label(root, text="Point 3", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 12 ')
    pt3Label.place(relx=0.05,rely=0.38,anchor=W)
    pt3starLabel = tk.Label(root, text="*", fg = "red",bg = "white", bd=2,font = 'Calibri 10')
    pt3starLabel.place(relx=0.12,rely=0.38,anchor=W)
    
    pt4Label = tk.Label(root, text="Point 4", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 12 ')
    pt4Label.place(relx=0.05,rely=0.44,anchor=W)
    pt4starLabel = tk.Label(root, text="*", fg = "red",bg = "white", bd=2,font = 'Calibri 10')
    pt4starLabel.place(relx=0.12,rely=0.44,anchor=W)
    
    pt1latVal = tk.Entry(root,width=15,bg = 'light grey')
    pt1latVal.place(relx=0.25,rely=0.26,anchor=W)
    pt1lonVal = tk.Entry(root,width=15,bg = 'light grey')
    pt1lonVal.place(relx=0.4,rely=0.26,anchor=W)
    
    pt2latVal = tk.Entry(root,width=15,bg = 'light grey')
    pt2latVal.place(relx=0.25,rely=0.32,anchor=W)
    pt2lonVal = tk.Entry(root,width=15,bg = 'light grey')
    pt2lonVal.place(relx=0.4,rely=0.32,anchor=W)
    
    pt3latVal = tk.Entry(root,width=15,bg = 'light grey')
    pt3latVal.place(relx=0.25,rely=0.38,anchor=W)
    pt3lonVal = tk.Entry(root,width=15,bg = 'light grey')
    pt3lonVal.place(relx=0.4,rely=0.38,anchor=W)

    pt4latVal = tk.Entry(root,width=15,bg = 'light grey')
    pt4latVal.place(relx=0.25,rely=0.44,anchor=W)
    pt4lonVal = tk.Entry(root,width=15,bg = 'light grey')
    pt4lonVal.place(relx=0.4,rely=0.44,anchor=W)
    
    altLabel = tk.Label(root, text="Altitude", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 12 ')
    altLabel.place(relx=0.57,rely=0.26,anchor=W)
    
    altVal = tk.Entry(root,width=28,bg = 'light grey')
    altVal.place(relx=0.67,rely=0.26,anchor=W)
    
    openDir = tk.Button(root, text='Select Public Key',width = 29,fg = "white",bg = "darkblue",font = 'Calibri 12', command = openFile)
    openDir.place(relx=0.57,rely=0.36,anchor=W)
    
    FPLabel = tk.Label(root, text="Flight Purpose", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 12')
    FPLabel.place(relx=0.05,rely=0.52,anchor=W)
    
    FPVal = tk.Entry(root,width=77,bg = 'light grey')
    FPVal.place(relx=0.25,rely=0.52,anchor=W)
    
    wghtLabel = tk.Label(root, text="Payload Weight", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 12 ')
    wghtLabel.place(relx=0.05,rely=0.6,anchor=W)
    
    wghtVal = tk.Entry(root,width=25,bg = 'light grey')
    wghtVal.place(relx=0.25,rely=0.6,anchor=W)
        
    pyLdLabel = tk.Label(root, text="Payload Details", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 12 ')
    pyLdLabel.place(relx=0.5,rely=0.6,anchor=W)
    
    pyLdVal = tk.Entry(root,width=28,bg = 'light grey')
    pyLdVal.place(relx=0.67,rely=0.6,anchor=W)
    
    SDLabel = tk.Label(root, text="Start Date", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 12 ')
    SDLabel.place(relx=0.05,rely=0.68,anchor=W)
    SDstarLabel = tk.Label(root, text="*", fg = "red",bg = "white", bd=2,font = 'Calibri 10')
    SDstarLabel.place(relx=0.15,rely=0.68,anchor=W)
    SDfrmtLabel = tk.Label(root, text="(YYYY-MM-DD)", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 9')
    SDfrmtLabel.place(relx=0.05,rely=0.725,anchor=W)
    
    SDVal = tk.Entry(root,width=25,bg = 'light grey')
    SDVal.place(relx=0.25,rely=0.68,anchor=W)
    
    EDLabel = tk.Label(root, text="End Date", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 12')
    EDLabel.place(relx=0.5,rely=0.68,anchor=W)
    EDstarLabel = tk.Label(root, text="*", fg = "red",bg = "white", bd=2,font = 'Calibri 10')
    EDstarLabel.place(relx=0.59,rely=0.68,anchor=W)
    EDfrmtLabel = tk.Label(root, text="(YYYY-MM-DD)", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 9')
    EDfrmtLabel.place(relx=0.5,rely=0.725,anchor=W)
    
    EDVal = tk.Entry(root,width=28,bg = 'light grey')
    EDVal.place(relx=0.67,rely=0.68,anchor=W)
    
    STLabel = tk.Label(root, text="Start Time", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 12 ')
    STLabel.place(relx=0.05,rely=0.78,anchor=W)
    STstarLabel = tk.Label(root, text="*", fg = "red",bg = "white", bd=2,font = 'Calibri 10')
    STstarLabel.place(relx=0.15,rely=0.78,anchor=W)
    STfrmtLabel = tk.Label(root, text="(hh:mm:ss)", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 9')
    STfrmtLabel.place(relx=0.05,rely=0.82,anchor=W)
    
    STVal = tk.Entry(root,width=25,bg = 'light grey')
    STVal.place(relx=0.25,rely=0.78,anchor=W)
    
    ETLabel = tk.Label(root, text="End Time", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 12')
    ETLabel.place(relx=0.5,rely=0.78,anchor=W)
    ETstarLabel = tk.Label(root, text="*", fg = "red",bg = "white", bd=2,font = 'Calibri 10')
    ETstarLabel.place(relx=0.59,rely=0.78,anchor=W)
    ETfrmtLabel = tk.Label(root, text="(hh:mm:ss)", fg = "DarkBlue",bg = "white", bd=2,font = 'Calibri 9')
    ETfrmtLabel.place(relx=0.5,rely=0.82,anchor=W)
    
    ETVal = tk.Entry(root,width=28,bg = 'light grey')
    ETVal.place(relx=0.67,rely=0.78,anchor=W)
    
    
    
    xml = tk.Button(root,text ="Generate Request",fg = "white",bg = "Darkblue", width=20,bd=2,font = 'Calibri 14 bold', command=callback)
    xml.place(relx=0.5, rely=0.93, anchor=CENTER)

    root.mainloop()
    
