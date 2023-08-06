import xml.etree.ElementTree as ET
import os
import csv
import pandas as pd

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
scan_folder("//WIN-6HNS1UBI6D7.hf.intel.com/HLKLogs/6-25-2020")




conn=mysql.connector.connect(host="maria3860-us-fm-in.iglb.intel.com",

user="wsivauto_so ",passwd="gYd3fX9NfA89qUy ", port=3307,

ssl_ca="C:\Migration-APT\SSL Connection\IntelSHA256RootCA-Base64.crt")
c=conn.cursor()
engine = create_engine("mysql+pymysql://wsivauto_so:gYd3fX9NfA89qUy@maria3860-us-fm-in.iglb.intel.com/wsivauto")


df1=pd.read_csv("rim.csv")
df1.to_sql(name="HCKLogsTable",
           con=engine,
           index=False,
           if_exists='append')


