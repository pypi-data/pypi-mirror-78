import xml.etree.ElementTree as ET
import os
import csv
import pandas as pd
from cryptography.fernet import Fernet
import sqlalchemy
from sqlalchemy import  create_engine
import mysql.connector

cnt=0

def fun1(file):
    tree = ET.parse(file)
    root = tree.getroot()

    type1 = root.attrib['Type']
    root1 = ET.Element('root')

    for jobrun in root.iter('JobRun'):
        root1 = ET.Element('root')
        root1 = jobrun
        runId = (root1.attrib['RunId'])
        guid = (root1.attrib['GUID'])
        tempGUID = (root1.attrib['TemplateGUID'])

    for joblist in root1.iter('Job'):
        root2 = ET.Element('root')
        root2 = (joblist)

        typencat = (root2.attrib['Type'], root2.attrib['Category'])
        # job1Tc=(root2.attrib['Name'])
        resultID = (root2.attrib['ResultId'], root2.attrib['TCMPath'])

    for joblist in root.iter('Dependency'):
        dep = (joblist.attrib)

    for par in root.iter('Parameter'):
        parameters = (par.attrib)

    for tlist in root1.iter('Task'):
        root4 = ET.Element('root')
        root4 = tlist
        tasklist = (root4.attrib['Type'], root4.attrib['Name'])

    for loginfo in root1.iter('LogShareInformation'):
        root4 = ET.Element('root')
        root4 = loginfo
        domain = (root4.attrib['Domain'], root4.attrib['Location'])
        Username = (root4.attrib['UserName'], root4.attrib['Password'])

    x = (root[0][0][0].attrib)
    y = (root[0][0][1].attrib)
    z = (root[0][0][2].attrib)
    firstTc = (x['Type'], x['Name'])
    secTc = (y['Type'], y['Name'])
    thirdTc = (z['Type'], z['Name'])
    AllTests = (firstTc, secTc, thirdTc)

    df = pd.DataFrame({'TempGUID': [tempGUID], 'RunID': [runId], 'GUID': [guid],
                       'TypeAndCategory': [typencat], 'TestCases': [AllTests], "ResultID and Path": [resultID],
                       "TaskList": [tasklist],
                        'Dependency': [dep]})


    global cnt
    cnt+=1

    if cnt== abs(1):

        df.to_csv('rim.csv', index=False, encoding='utf-8')
    else:

        df.to_csv('rim.csv', mode='a', index=False, encoding='utf-8', header=False)

def Credentials():
    key = b'f1A3NP9h1IAjVIUmX6x2Z2pUzIR3gvMuF4-llanNO24='
    Euser = b'gAAAAABfRP1FAES3Xt4068ayqJZOAzh3M-Yps3WAF9yG0aE069LD2pT2RVjbldpSVehJ-W6ZRjntHre9rP5-jnsis7m57MW30g=='
    Epswd = b'gAAAAABfRP1FjlvqkSN16MTJA_Q2NqGp2TNUq1l9H6ihZR3yAptplUtf61lBIY6kW_ERbjZHBuVWJZZOjyNkC0QYfemqe7HBHw=='
    f = Fernet(key)
    user = (f.decrypt(Euser)).decode()
    pswd = (f.decrypt(Epswd)).decode()
    #print(user,pswd)
    return [user,pswd]

def scan_folder(parent):
    count=0

    for file_name in os.listdir(parent):

        if file_name.startswith("WttJob"):
            count+=1
            current_path = "".join((parent, "/", file_name))
            fun1(current_path)

        else:
            current_path = "".join((parent, "/", file_name))
            if os.path.isdir(current_path):
                scan_folder(current_path)




c