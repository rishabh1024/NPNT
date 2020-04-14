from tkinter import filedialog
# import tkFileDialog
from tkinter import *

from tkinter import *
# import tkMessageBox
import tkinter as tk
import tkinter.messagebox
# from change_metadata import *
from datetime import date
from writeXml import *

from tkinter import ttk
import os

import paramiko

current_date = str(datetime.now().today())
current_time = str(datetime.now().strftime("%X"))


def uploadAction():
    global filename
    filename = filedialog.askopenfilename(parent=tab2)
    filename_label = tk.Label(tab2, text=filename, fg="BLACK", bg="white", bd=2, font='Calibri 10')
    filename_label.place(relx=0.1, rely=0.57, anchor=W)


def send():
    global filename
    ssh = paramiko.SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    server = "192.168.1.74"
    ssh.connect(server, username="pi", password="Omni@123")
    sftp = ssh.open_sftp()
    localpath = filename
    remotepath = "valid_permission_artifact.xml"
    sftp.put(localpath, remotepath)
    sftp.close()
    ssh.close()


def openFile():
    global file

    file = filedialog.askopenfilename(parent=tab1, initialdir="/", title='Select public key',
                                      filetypes=(("pem files", "*.pem"), ("all files", "*.*")))
    fileLabel = tk.Label(tab1, text=file, fg="BLACK", bg="white", bd=2, font='Calibri 10')
    fileLabel.place(relx=0.61, rely=0.43, anchor=W)


def checkDateTime(startDate, startTime, endDate, endTime):
    # if '-' not in startDate or '-' not in endDate or ':' not in startTime or ':' not in endTime:
    #        tkMessageBox.showinfo("Error","Enter correct format of date and time!")

    check = False
    sd = startDate.split('-')
    ed = endDate.split('-')
    st = startTime.split(':')
    et = endTime.split(':')
    print(sd[2], ed[2])
    if (len(sd[0]), len(sd[1]), len(sd[2])) != (4, 2, 2) or (len(ed[0]), len(ed[1]), len(ed[2])) != (4, 2, 2):
        tkinter.messagebox.showinfo("Error", "Enter correct format of date!")

    elif int(sd[2]) > 31 or int(ed[2]) > 31 or int(sd[1]) > 13 or int(ed[1]) > 13 or int(sd[0]) < 2020 or int(ed[0])< 2020 or startDate < current_date or endDate < current_date or endDate< startDate:
        # elif not (0,0)<(sd[2],ed[2])<=(31,31) and (0,0)<(sd[1],ed[1])<(13,13) and (2019,2019)<(sd[0],ed[0]):
        tkinter.messagebox.showinfo("Error", "Invalid date!")

    elif (len(st[0]), len(st[1])) != (2, 2) or (len(et[0]), len(et[1])) != (2, 2):
        tkinter.messagebox.showinfo("Error", "Enter correct format of time!")
    elif not (0, 0) < (int(st[0]), int(et[0])) <= (24, 24) and (0, 0) < (int(st[1]), int(et[1])) <= (60, 60):
        tkinter.messagebox.showinfo("Error", "Invalid time!")
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

    lat = [pt1lat, pt2lat, pt3lat, pt4lat]
    lon = [pt1lon, pt2lon, pt3lon, pt4lon]
    elev = altVal.get()
    weight = wghtVal.get()
    payload = pyLdVal.get()
    startDate = SDVal.get()
    endDate = EDVal.get()
    startTime = STVal.get()
    endTime = ETVal.get()
    FP = FPVal.get()

    if pt1lat == '' or pt2lat == '' or pt3lat == '' or pt4lat == '' or pt1lon == '' or pt2lon == '' or pt3lon == '' or pt4lon == '':
        tkinter.messagebox.showinfo("Error", "Enter all points!")
        pass
    elif startDate == '' or endDate == '' or startTime == '' or endTime == '' or UIN == '':
        tkinter.messagebox.showinfo("Error", "Enter all required fields!")
        pass


    else:
        check = checkDateTime(startDate, startTime, endDate, endTime)
        if check == True:
            if pilot == '':
                pilot = 'Not Specified'
            if weight == '':
                weight = 'Not Specified'
            if payload == '':
                payload = 'Not Specified'
            if FP == '':
                FP = 'Not Specified'
            if elev == '':
                elev = 220

            xmlfile = ("xmlTemplate.xml")

            writeXML(xmlfile, pilot, UIN, lat, lon, elev, weight, payload, startTime, startDate, endDate, endTime, FP)
            tkinter.messagebox.showinfo("Info", "Request generated!")
            root.destroy()
        else:
            pass


if __name__ == '__main__':
    root = tk.Tk()  # main window
    root.title("NPNT Management Client")
    root.geometry("700x495")
    root.configure(background='white')
    root.iconbitmap()

    s = ttk.Style()
    s.configure('new.TFrame', background='#FFFFFF')

    tab_parent = ttk.Notebook(root)

    tab1 = ttk.Frame(tab_parent, style='new.TFrame')
    tab2 = ttk.Frame(tab_parent, style='new.TFrame')

    tab_parent.add(tab1, text="Generate Request")
    tab_parent.add(tab2, text="Upload File")

    pltLabel = tk.Label(tab1, text="Pilot No", fg="DarkBlue", bg="white", bd=2, font='Calibri 12')
    pltLabel.place(relx=0.05, rely=0.1, anchor=W)

    pltVal = tk.Entry(tab1, width=25, bg='light grey')
    pltVal.place(relx=0.25, rely=0.1, anchor=W)

    UINLabel = tk.Label(tab1, text="Drone UIN", fg="DarkBlue", bg="white", bd=2, font='Calibri 12 ')
    UINstarLabel = tk.Label(tab1, text="*", fg="red", bg="white", bd=2, font='Calibri 10')
    UINLabel.place(relx=0.545, rely=0.1, anchor=W)
    UINstarLabel.place(relx=0.645, rely=0.1, anchor=W)

    UINVal = tk.Entry(tab1, width=28, bg='light grey')
    UINVal.place(relx=0.715, rely=0.1, anchor=W)

    latLabel = tk.Label(tab1, text="Latitude", fg="BLACK", bg="white", bd=2, font='Calibri 13')
    latLabel.place(relx=0.27, rely=0.18, anchor=W)
    lonLabel = tk.Label(tab1, text="Longitude", fg="BLACK", bg="white", bd=2, font='Calibri 13')
    lonLabel.place(relx=0.41, rely=0.18, anchor=W)

    pt1Label = tk.Label(tab1, text="Point 1", fg="DarkBlue", bg="white", bd=2, font='Calibri 12')
    pt1Label.place(relx=0.05, rely=0.26, anchor=W)
    pt1starLabel = tk.Label(tab1, text="*", fg="red", bg="white", bd=2, font='Calibri 10')
    pt1starLabel.place(relx=0.12, rely=0.26, anchor=W)

    pt2Label = tk.Label(tab1, text="Point 2", fg="DarkBlue", bg="white", bd=2, font='Calibri 12 ')
    pt2Label.place(relx=0.05, rely=0.32, anchor=W)
    pt2starLabel = tk.Label(tab1, text="*", fg="red", bg="white", bd=2, font='Calibri 10')
    pt2starLabel.place(relx=0.12, rely=0.32, anchor=W)

    pt3Label = tk.Label(tab1, text="Point 3", fg="DarkBlue", bg="white", bd=2, font='Calibri 12 ')
    pt3Label.place(relx=0.05, rely=0.38, anchor=W)
    pt3starLabel = tk.Label(tab1, text="*", fg="red", bg="white", bd=2, font='Calibri 10')
    pt3starLabel.place(relx=0.12, rely=0.38, anchor=W)

    pt4Label = tk.Label(tab1, text="Point 4", fg="DarkBlue", bg="white", bd=2, font='Calibri 12 ')
    pt4Label.place(relx=0.05, rely=0.44, anchor=W)
    pt4starLabel = tk.Label(tab1, text="*", fg="red", bg="white", bd=2, font='Calibri 10')
    pt4starLabel.place(relx=0.12, rely=0.44, anchor=W)

    pt1latVal = tk.Entry(tab1, width=15, bg='light grey')
    pt1latVal.place(relx=0.25, rely=0.26, anchor=W)
    pt1lonVal = tk.Entry(tab1, width=15, bg='light grey')
    pt1lonVal.place(relx=0.4, rely=0.26, anchor=W)

    pt2latVal = tk.Entry(tab1, width=15, bg='light grey')
    pt2latVal.place(relx=0.25, rely=0.32, anchor=W)
    pt2lonVal = tk.Entry(tab1, width=15, bg='light grey')
    pt2lonVal.place(relx=0.4, rely=0.32, anchor=W)

    pt3latVal = tk.Entry(tab1, width=15, bg='light grey')
    pt3latVal.place(relx=0.25, rely=0.38, anchor=W)
    pt3lonVal = tk.Entry(tab1, width=15, bg='light grey')
    pt3lonVal.place(relx=0.4, rely=0.38, anchor=W)

    pt4latVal = tk.Entry(tab1, width=15, bg='light grey')
    pt4latVal.place(relx=0.25, rely=0.44, anchor=W)
    pt4lonVal = tk.Entry(tab1, width=15, bg='light grey')
    pt4lonVal.place(relx=0.4, rely=0.44, anchor=W)

    altLabel = tk.Label(tab1, text="Altitude", fg="DarkBlue", bg="white", bd=2, font='Calibri 12 ')
    altLabel.place(relx=0.615, rely=0.26, anchor=W)

    altVal = tk.Entry(tab1, width=28, bg='light grey')
    altVal.place(relx=0.715, rely=0.26, anchor=W)

    openDir = tk.Button(tab1, text='Select Public Key', width=29, fg="white", bg="darkblue", font='Calibri 12',
                        command=openFile)
    openDir.place(relx=0.615, rely=0.36, anchor=W)

    FPLabel = tk.Label(tab1, text="Flight Purpose", fg="DarkBlue", bg="white", bd=2, font='Calibri 12')
    FPLabel.place(relx=0.05, rely=0.52, anchor=W)

    FPVal = tk.Entry(tab1, width=77, bg='light grey')
    FPVal.place(relx=0.25, rely=0.52, anchor=W)

    wghtLabel = tk.Label(tab1, text="Payload Weight", fg="DarkBlue", bg="white", bd=2, font='Calibri 12 ')
    wghtLabel.place(relx=0.05, rely=0.6, anchor=W)

    wghtVal = tk.Entry(tab1, width=25, bg='light grey')
    wghtVal.place(relx=0.25, rely=0.6, anchor=W)

    pyLdLabel = tk.Label(tab1, text="Payload Details", fg="DarkBlue", bg="white", bd=2, font='Calibri 12 ')
    pyLdLabel.place(relx=0.5, rely=0.6, anchor=W)

    pyLdVal = tk.Entry(tab1, width=28, bg='light grey')
    pyLdVal.place(relx=0.67, rely=0.6, anchor=W)

    SDLabel = tk.Label(tab1, text="Start Date", fg="DarkBlue", bg="white", bd=2, font='Calibri 12 ')
    SDLabel.place(relx=0.05, rely=0.68, anchor=W)
    SDstarLabel = tk.Label(tab1, text="*", fg="red", bg="white", bd=2, font='Calibri 10')
    SDstarLabel.place(relx=0.15, rely=0.68, anchor=W)
    SDfrmtLabel = tk.Label(tab1, text="(YYYY-MM-DD)", fg="DarkBlue", bg="white", bd=2, font='Calibri 9')
    SDfrmtLabel.place(relx=0.05, rely=0.725, anchor=W)

    SDVal = tk.Entry(tab1, width=25, bg='light grey')
    SDVal.place(relx=0.25, rely=0.68, anchor=W)

    EDLabel = tk.Label(tab1, text="End Date", fg="DarkBlue", bg="white", bd=2, font='Calibri 12')
    EDLabel.place(relx=0.5, rely=0.68, anchor=W)
    EDstarLabel = tk.Label(tab1, text="*", fg="red", bg="white", bd=2, font='Calibri 10')
    EDstarLabel.place(relx=0.59, rely=0.68, anchor=W)
    EDfrmtLabel = tk.Label(tab1, text="(YYYY-MM-DD)", fg="DarkBlue", bg="white", bd=2, font='Calibri 9')
    EDfrmtLabel.place(relx=0.5, rely=0.725, anchor=W)

    EDVal = tk.Entry(tab1, width=28, bg='light grey')
    EDVal.place(relx=0.67, rely=0.68, anchor=W)

    STLabel = tk.Label(tab1, text="Start Time", fg="DarkBlue", bg="white", bd=2, font='Calibri 12 ')
    STLabel.place(relx=0.05, rely=0.78, anchor=W)
    STstarLabel = tk.Label(tab1, text="*", fg="red", bg="white", bd=2, font='Calibri 10')
    STstarLabel.place(relx=0.15, rely=0.78, anchor=W)
    STfrmtLabel = tk.Label(tab1, text="(hh:mm:ss)", fg="DarkBlue", bg="white", bd=2, font='Calibri 9')
    STfrmtLabel.place(relx=0.05, rely=0.82, anchor=W)

    STVal = tk.Entry(tab1, width=25, bg='light grey')
    STVal.place(relx=0.25, rely=0.78, anchor=W)

    ETLabel = tk.Label(tab1, text="End Time", fg="DarkBlue", bg="white", bd=2, font='Calibri 12')
    ETLabel.place(relx=0.5, rely=0.78, anchor=W)
    ETstarLabel = tk.Label(tab1, text="*", fg="red", bg="white", bd=2, font='Calibri 10')
    ETstarLabel.place(relx=0.59, rely=0.78, anchor=W)
    ETfrmtLabel = tk.Label(tab1, text="(hh:mm:ss)", fg="DarkBlue", bg="white", bd=2, font='Calibri 9')
    ETfrmtLabel.place(relx=0.5, rely=0.82, anchor=W)

    ETVal = tk.Entry(tab1, width=28, bg='light grey')
    ETVal.place(relx=0.67, rely=0.78, anchor=W)

    xml = tk.Button(tab1, text="Generate Request", fg="white", bg="Darkblue", width=20, bd=2, font='Calibri 14 bold',
                    command=callback)
    xml.place(relx=0.5, rely=0.93, anchor=CENTER)

    fileUpload = tk.Button(tab2, text='Upload File', width=29, fg="white", bg="darkblue", font='Calibri 12',
                           command=uploadAction)
    fileUpload.place(relx=0.1, rely=0.5, anchor=W)

    sendFile = tk.Button(tab2, text='Send', width=29, fg="white", bg="darkblue", font='Calibri 12',
                         command=send)
    sendFile.place(relx=0.55, rely=0.5, anchor=W)

    tab_parent.pack(expand=1, fill="both")

    root.mainloop()
