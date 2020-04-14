# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 16:13:07 2019

@author: Asus
"""
from tkinter import filedialog
from tkinter import *
import tkinter.messagebox
import tkinter as tk
#from helpers import verify_xml_signature
import os
from helpers import create_keys
from drone_db import insert_drone_reg_data
from datetime import datetime


def openFile():
    global file
    
    file = filedialog.askopenfilename(parent=root, initialdir= "/",title='Select Permission Artifact',filetypes = (("xml files","*.xml"),("all files","*.*")))
    fileLabel = tk.Label(root, text=file, wraplength = 300,fg = "BLACK",bg = "white", bd=2,font = 'Calibri 10',justify=LEFT)
    fileLabel.place(relx=0.24,rely=0.52,anchor=W)

def verifySig():

    ## insert checks on info received #
    try:
        insert_drone_reg_data(int(dIDVal.get()),int(mIDVal.get()),int(bIDVal.get()), datetime.now())
        tkinter.messagebox.showinfo("Info!","Registered Device")
    except Exception as e:
        raise e

    # global file
    # certificate_path = "dgca.cert"
    # result = (verify_xml_signature(file, certificate_path))
    # if result == True:
    #     tkinter.messagebox.showinfo("Info","Valid Signature!")    
    #     os.startfile(r"C:\Program Files (x86)\Mission Planner\MissionPlanner.exe")
    # else:
    #     tkinter.messagebox.showinfo("Error!","Invalid Signature!")    
    
if __name__ == "__main__":
        
    root = tk.Tk()
    root.title("Management Server")
    
    root.geometry("400x450")
    frame=tk.Frame(root)
    root.configure(background='white')
    # root.iconbitmap(default=r"0.ico")

    frame.pack()
    
    # apiLabel = tk.Label(root, text="API Version", fg = "darkblue",bg = "white", bd=2,font = 'Calibri 12')
    # apiLabel.place(relx=0.05,rely=0.1,anchor=W)
    
    # apiVal = tk.Entry(root,width=28,bg = 'light grey')
    # apiVal.place(relx=0.4,rely=0.1,anchor=W)

    # txnLabel = tk.Label(root, text="Transaction ID", fg = "darkblue",bg = "white", bd=2,font = 'Calibri 12')
    # txnLabel.place(relx=0.05,rely=0.2,anchor=W)
    
    # txnVal = tk.Entry(root,width=28,bg = 'light grey')
    # txnVal.place(relx=0.4,rely=0.2,anchor=W)

    dIDLabel = tk.Label(root, text="Device ID", fg = "darkblue",bg = "white", bd=2,font = 'Calibri 12')
    dIDLabel.place(relx=0.05,rely=0.3,anchor=W)
    
    dIDVal = tk.Entry(root,width=28,bg = 'light grey')
    dIDVal.place(relx=0.4,rely=0.3,anchor=W)

    mIDLabel = tk.Label(root, text="Model ID", fg = "darkblue",bg = "white", bd=2,font = 'Calibri 12')
    mIDLabel.place(relx=0.05,rely=0.4,anchor=W)
    
    mIDVal = tk.Entry(root,width=28,bg = 'light grey')
    mIDVal.place(relx=0.4,rely=0.4,anchor=W)

    bIDLabel = tk.Label(root, text="Operator ID", fg = "darkblue",bg = "white", bd=2,font = 'Calibri 12')
    bIDLabel.place(relx=0.05,rely=0.5,anchor=W)
    
    bIDVal = tk.Entry(root,width=28,bg = 'light grey')
    bIDVal.place(relx=0.4,rely=0.5,anchor=W)

    sigLabel = tk.Button(root, text="Generate Key Pair", fg = "darkblue",bg = "white", bd=2,font = 'Calibri 12', command=create_keys('.\\', 'FlyKey'))
    sigLabel.place(relx=0.05,rely=0.6,anchor=W)
    
    # openSig = tk.Button(root, text='Browse file',height = 1,fg = "white",bg = "darkblue",font = 'Calibri 10', command = openFile)
    # openSig.place(relx=0.4,rely=0.6,anchor=W)

    certLabel = tk.Label(root, text="Digital Certificate", fg = "darkblue",bg = "white", bd=2,font = 'Calibri 12')
    certLabel.place(relx=0.05,rely=0.7,anchor=W)
    
    openCert = tk.Button(root, text='Browse file',height = 1,fg = "white",bg = "darkblue",font = 'Calibri 10', command = openFile)
    openCert.place(relx=0.4,rely=0.7,anchor=W)

    valid = tk.Button(root, text='Register Device',fg = "white",bg = "darkblue",font = 'Calibri 12', command = verifySig)
    valid.place(relx=0.35,rely=0.9,anchor=W)
    
    root.mainloop()

