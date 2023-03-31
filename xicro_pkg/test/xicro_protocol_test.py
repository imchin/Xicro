#!/usr/bin/python3
import math
import struct
import time

import serial
from ament_index_python.packages import get_package_share_directory
import argparse
import os
import yaml
import multiprocessing as mp
import numpy as np
import socket
def get_params(qq):
    try:
        q=qq
        path = 'setup_xicro_test.yaml'
        with open(path,'r') as f:
            yml_dict = yaml.safe_load(f)
            q=q.split(".")
            ans = yml_dict.get(q[0])
            for i in range(1,len(q)):
                ans = ans.get(q[i])
        # print('Get '+qq+' Done.')
        return  ans
    except:
        print('Get '+qq+' Failed'+'Something went wrong when opening YAML.')
    return 0
def checkNofdata(dataType):
    S=dataType.find("[")
    F= dataType.find("]")
    if(S!=-1 and F!=-1):
        return int(dataType[S+1:F])
    else:
        return 1
def checkSubmsg(typee):
    supporttypee=["int8","int16","int32","int64","uint8","uint16","uint32","uint64","bool","float32","float64","string","xxicro_Empty"]
    ans=1
    for i in range(0,len(supporttypee)):
        if(typee.find(supporttypee[i])!= -1):
            ans=1
            break
        else:
            ans=0
    return ans
def expandSub(id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData,interfacein):
    for i in range(0,len(dataType)):
        for j in range(0,len(dataType[i])):
            if(checkSubmsg(dataType[i][j]) == 0):   
                if(dataType[i][j].find("/")!=-1):
                    path = os.path.join(get_package_share_directory(dataType[i][j].split("/")[0]),'msg', dataType[i][j].split("/")[1]+".msg")  
                    Op = dataType[i][j].split("/")[0]         
                else:
                    path = os.path.join(get_package_share_directory(interfacein[i][j].split("/")[0]),'msg', dataType[i][j]+".msg")
                    Op = interfacein[i][j]
                msg = open(path, 'r').read().splitlines()
                addinterfacein=[]
                addtype=[]
                addName=[]
                Sname=dataName[i][j]
                for k in range(0,len(msg)):
                    line=msg[k].split()
                    if(len(line)!=0 and line[0]!="#" ):
                        addtype.append(line[0])
                        addName.append(line[1])
                        addinterfacein.append(Op)
                for k in range(0,len(addName)):
                    addName[k]=Sname+"."+addName[k]     
                interfacein[i][j]=addinterfacein
                dataType[i][j]=addtype
                dataName[i][j]=addName         
    TempType=[]
    TempName=[]
    Tempinterfaein=[]
    for i in range(0,len(dataType)):  #delist
        q=[]
        w=[]
        e=[]
        for j in range(0,len(dataType[i])):
            if(type(dataType[i][j])==list):
                for k in range(0,len(dataType[i][j])):
                    q.append(dataType[i][j][k])
                    w.append(dataName[i][j][k])
                    e.append(interfacein[i][j][k])
            else:
                q.append(dataType[i][j])
                w.append(dataName[i][j])
                e.append(interfacein[i][j])
        TempType.append(q)
        TempName.append(w)
        Tempinterfaein.append(e)
    dataType=TempType.copy()
    dataName=TempName.copy()
    interfacein=Tempinterfaein.copy()
    NofData=[]
    for i in range(0,len(dataType)): #check N of data
        q=[]
        for j in range(0,len(dataType[i])):
            q.append(checkNofdata(dataType[i][j]))
        NofData.append(q)
    return id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData,interfacein
# def typetoProtocol(typee,Nofdata):
#     ans=0
#     Nofbyte=0
#     if(typee=="uint8"):
#         ans=  8
#         Nofbyte=1
#     elif(typee=="uint16"):
#         ans=  16
#         Nofbyte=2
#     elif(typee=="uint32"):
#         ans=  32
#         Nofbyte=4
#     elif(typee=="uint64"):
#         ans=  64
#         Nofbyte=8
#     elif(typee=="int8"):
#         ans=  18
#         Nofbyte=1
#     elif(typee=="int16"):
#         ans=  116
#         Nofbyte=2
#     elif(typee=="int32"):
#         ans=  132
#         Nofbyte=4
#     elif(typee=="int64"):
#         ans=  164
#         Nofbyte=8
#     elif(typee=="float32"):
#         ans=  111
#         Nofbyte=4
#     elif(typee=="float64" and ( input.mcu_type =="arduino" or input.mcu_type =="esp" )): # force float64 to float32
#         ans= 111
#         Nofbyte=4
#     elif(typee=="float64" ):
#         ans= 222
#         Nofbyte=8   
#     elif(typee=="string" ):
#         ans= 242
#         Nofbyte=888
#     elif(typee=="bool" ):
#         ans= 88
#         Nofbyte=2    # N = 1 auto terminater
#     elif(typee=="xxicro_Empty" ):
#         ans= 254
#         Nofbyte=1   

#     if(Nofdata==1):
#         return ans,Nofbyte
#     elif(typee=="bool" ):
#         return ans+1,math.ceil(Nofdata/8.00)
#     else:
#         return ans+1,Nofbyte*Nofdata
def typetoProtocol(typee,Nofdata):
    ans=0
    Nofbyte=0
    if(typee=="uint8"):

        ans=  8
        Nofbyte=1
    elif(typee=="uint16"):
        ans=  16
        Nofbyte=2
    elif(typee=="uint32"):
        ans=  32
        Nofbyte=4
    elif(typee=="uint64"):
        ans=  64
        Nofbyte=8
    elif(typee=="int8"):
        ans=  18
        Nofbyte=1
    elif(typee=="int16"):
        ans=  116
        Nofbyte=2
    elif(typee=="int32"):
        ans=  132
        Nofbyte=4
    elif(typee=="int64"):
        ans=  164
        Nofbyte=8
    elif(typee=="float32"):
        ans=  111
        Nofbyte=4
    elif(typee=="float64" and ( input.mcu_type =="arduino" or input.mcu_type =="esp" )): # force float64 to float32
        ans= 111
        Nofbyte=4
    elif(typee=="float64" ):
        ans= 222
        Nofbyte=8   
    elif(typee=="string" ):
        ans= 242
        Nofbyte=888
    elif(typee=="bool" ):
        ans= 88
        Nofbyte=1
    elif(typee=="xxicro_Empty" ):
        ans= 254
        Nofbyte=1   
    if(Nofdata==1):
        return ans,Nofbyte
    elif(typee=="bool" ):
        return ans+1,999
    else:
        return ans+1,Nofbyte

def setup_var_protocol():
    setup_pub=get_params('ros.publisher')
    Idmsg=[]
    nametopic=[]
    interfacetopic=[]
    interfacein=[]
    for i in range(0,len(setup_pub)):
        Idmsg.append(setup_pub[i][0])
        nametopic.append(setup_pub[i][1])
        interfacetopic.append(setup_pub[i][2])
    # print('Done load YAML pub.')
    dataType=[]
    dataName=[]
    NofData=[]
    datagrab=[]
    datatypeProtocol=[]
    bytetograb=[]
    for i in range (0,len(interfacetopic)):
        tempinterfacein=[]
        tempType=[]
        tempName=[]
        tempN=[]
        path = os.path.join(get_package_share_directory( interfacetopic[i].split("/")[0]),'msg', interfacetopic[i].split("/")[1])
        msg = open(path, 'r').read().splitlines()
        for j in range(0,len(msg)):
            line=msg[j].split()
            if(len(line)!=0 and line[0]!="#" ):
                tempType.append(line[0])
                tempName.append(line[1])
                tempN.append(checkNofdata(line[0]))
                tempinterfacein.append(interfacetopic[i].split("/")[0])
        NofData.append(tempN)
        dataType.append(tempType)
        dataName.append(tempName)
        interfacein.append(tempinterfacein)
    # print('Generate variable from msg Done.')
    for i in range(0,10):
            Idmsg,id_topic,nametopic,interfacetopic,dataType,dataName,NofData,interfacein=expandSub(Idmsg,[],nametopic,interfacetopic,dataType,dataName,NofData,interfacein)
    for i in range(0,len(dataType)): # bias float64 to float32
        for j in range(0,len(dataType[i])):
            if(dataType[i][j].split("[")[0] == "float64" and (input.mcu_type=="arduino" or input.mcu_type=="esp") ):
                dataType[i][j]="float32"
    for i in range(0,len(dataType)):
        tempbytetograb=[]
        tempdataprotocol=[]
        tempdatagrab=[]
        for j in range(0,len(dataType[i])):
            if(NofData[i][j]!=1):
                tt=[]
                for k in range(0,NofData[i][j]):
                    if(dataType[i][j].split("[")[0]=="string"):
                        tt.append("")
                    elif(dataType[i][j].split("[")[0]=="float32" or dataType[i][j].split("[")[0]=="float64"):
                        tt.append(0.0)
                    elif(dataType[i][j].split("[")[0]=="bool"):
                        tt.append(False)   
                    else:
                        tt.append(0)
                tempdatagrab.append(tt)
            else:
                if(dataType[i][j]=="string"):
                    tempdatagrab.append("")
                elif(dataType[i][j]=="float32" or dataType[i][j]=="float64"):
                    tempdatagrab.append(0.0)
                elif(dataType[i][j]=="bool"):
                    tempdatagrab.append(False)
                else:
                    tempdatagrab.append(0) 
            if(dataType[i][j].find("[")!=-1 ):
                dataType[i][j]=dataType[i][j][0:dataType[i][j].find("[")]
            a,b=typetoProtocol(dataType[i][j],NofData[i][j])
            tempdataprotocol.append(a)
            tempbytetograb.append(b)
        datatypeProtocol.append(tempdataprotocol)
        bytetograb.append(tempbytetograb)
        datagrab.append(tempdatagrab)
    return Idmsg,nametopic,interfacetopic,dataType,dataName,datagrab,NofData,datatypeProtocol,bytetograb


def ConnectmcuAndCheck(Checklist):
    flag = 0
    if(get_params("microcontroller.connection.type")=="UART"):
        port = get_params("microcontroller.connection.serial_port")
        baudrate = get_params("microcontroller.connection.baudrate")
        print("Connect to mcu")
        ser = serial.Serial(port,baudrate, timeout=1000 ,stopbits=1)
        print(port + ': port is Open.')
        state=0
        Sign = Checklist[0]
        ii=0
        All=[]
        while(1):
            
            s = ser.read()
            data = int.from_bytes(s, byteorder="big",signed=0)
            print("data",data)
            All.append(data)
            if(state==0 and data == 73 ):
                state=1
            elif(state==1 and data  == 109 ):
                state=2
            elif(state==2 and data == 64 ):
                state=3
            elif(state==3 and data == 99 ):
                print("Done check Start")
                state=4
            elif(state==4 and data == Sign):
                print("Sign pass")
                state=5
            elif(state==5 and data == Checklist[1]): # ig msg match
                print("id_msg match")
                ii=-1
                print(Checklist[3])
                state=6
            elif(state==6 and data == Checklist[3][ii+1]): # check data head N data
                ByteIn=0
                if(Checklist[3][ii+1]!= 242):
                    state=7 
                elif(Checklist[3][ii+1]== 242):
                    state = 242 
                else:
                    break
            elif(state==7): 
                if(data == 42):
                    state=8
                else:
                    ByteIn=ByteIn+1

            elif(state==8 and data== 42): # confirm continue 
                if(ByteIn == Checklist[4][ii+1]):
                    ii=ii+1
                    state = 6
                else:
                    flag= 0 # protocol fail
                    break
            
            elif(state==242): # check 1 string
                if(data==42):
                    state = 243
                else:
                    state=242
            elif(state == 243):
                if(data == 126):
                    print("End string")
                    state = 244 
                    break
                break
            elif(state == 244):
                if(data==42):
                    state =245
            elif(state ==245):
                if(data==42):
                    state=6
def setupProtocol():
    Checklist = []
    id_mcu= get_params("microcontroller.idmcu")
    Idmsgg,nametopicc,interfacetopicc,dataTypee,dataNamee,datagrabb,NofDataa,datatypeProtocoll,bytetograbb=setup_var_protocol()
    for i in range(0,len(Idmsgg)):
        Checklist = [int((id_mcu)<<4 | 4),Idmsgg[i],nametopicc[i] ,datatypeProtocoll[i],bytetograbb[i]]
        print(Checklist)
        ConnectmcuAndCheck(Checklist)
    # Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res,timeOut=setup_srv_protocol()
    # Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res,timeOut=setup_srv_server_protocol()
    # Idaction,nameaction,interfaceaction,dataType_action_req,dataName_action_req,datagrab_action_req,NofData_action_req,datatypeProtocol_action_req,bytetograb_action_req,dataType_action_res,dataName_action_res,datagrab_action_res,NofData_action_res,datatypeProtocol_action_res,bytetograb_action_res,dataType_action_feed,dataName_action_feed,datagrab_action_feed,NofData_action_feed,datatypeProtocol_action_feed,bytetograb_action_feed,timeOut = setup_action_client_protocol()
    # Idaction,nameaction,interfaceaction,dataType_action_req,dataName_action_req,datagrab_action_req,NofData_action_req,datatypeProtocol_action_req,bytetograb_action_req,dataType_action_res,dataName_action_res,datagrab_action_res,NofData_action_res,datatypeProtocol_action_res,bytetograb_action_res,dataType_action_feed,dataName_action_feed,datagrab_action_feed,NofData_action_feed,datatypeProtocol_action_feed,bytetograb_action_feed,timeOut = setup_action_server_protocol()
    
    



def checkArgs():
    flagargs=0
    try:
        global input 
        input = argparse.ArgumentParser()
        input.add_argument("-mcu_type", help="type of microcontroller",choices=["arduino","esp","stm32"],type=str,required=1)
        input.add_argument("-scantime", help="scantime for scan protocol (second)",type=float,required=1)
        input = input.parse_args()
        if(input.mcu_type == "arduino" or input.mcu_type ==  "stm32" or input.mcu_type == "esp"):
            flagargs=1
    except:
        print('******  Please input argv [-mcu_type]  ******')

    if(flagargs):
        print("*******************************************************************************************************************\n")
        print("Protocol checks can only be done in 3 operating modes: publish, service client request, and action client send_goal")
        print("This test is a preliminary check for accepting protocol values from the microcontroller only.")
        print("Preliminary testing in other operating modes\n")
        print(" 1. Use a library and node generated from the same Yaml.")
        print(" 2. execute according to API in Xicro readthedocs.")
        print(" 3. Have a topic service action server on the ros2 network.")
        print(" 4. In microcontrollers have xicro.spin() in while, which can execute.\n")
        print("*******************************************************************************************************************\n")
        return 1
    else:
        return 0 
def select_pipe(obj_pipe):
    for i in range(0,16):
        if(obj_pipe[i]== 888):
            return i
    return None
class Uart():
    def __init__(self,mp):
        self.Buff = mp.Array('d',np.zeros(1000))
        self.index =  mp.Value('i',0)
        self.Indexpre_value =  mp.Value('i',0)
        self.Indexpre_value2 =  mp.Value('i',0)
        self.flag_send =  mp.Value('i',0)
        self.mana = mp.Manager()
        self.Buff_SSend = self.mana.list()
        if(get_params("microcontroller.connection.type")=="UART"):
            self.port = get_params("microcontroller.connection.serial_port")
            self.baudrate = get_params("microcontroller.connection.baudrate")
        elif():
            self.ip_address_mcu = get_params("microcontroller.connection.ip_address_mcu")
            self.udp_port_mcu = get_params("microcontroller.connection.udp_port_mcu")
        self.ser = self.check_port_open()

    def check_port_open(self):
        if(get_params("microcontroller.connection.type")=="UART"):
            try:
                ser = serial.Serial(self.port,self.baudrate, timeout=1000 ,stopbits=1)
                print(self.port + ': port is Open.')
                return ser
            except:
                print(self.port + ': open port Fail.')
            return 0

        elif(get_params("microcontroller.connection.type")=="UDP"):
            try:
                ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 
                ser.setblocking(1)
                ser.bind(('', self.udp_port_mcu))
                print('UDP open Connection done.')
                return ser
            except:
                print('UDP open Connection fail.')
                return 0
        else:
            print("Eror parameter")
        


    def queue_Send(self,send_ll):

        self.Buff_SSend.append(send_ll)

        return 1
def Receive_uart(Obj_uart): #processer 1
    print("Start Receive Xicro_protocol")
    while(1):
        try:
            s = Obj_uart.ser.read()
            Obj_uart.Buff[Obj_uart.index.value]=(int.from_bytes(s, byteorder="big",signed=0) )
            Obj_uart.index.value = (Obj_uart.index.value + 1 )%1000
        except:
            Obj_uart.ser = Obj_uart.check_port_open()
def Transmit_uart(Obj_uart): #processer 2
    print("Start Transmit Xicro_Protocol")
    while(1):
        if(len(Obj_uart.Buff_SSend)>0):
            try:
                Obj_uart.ser.write(bytearray(Obj_uart.Buff_SSend[0]))
                Obj_uart.Buff_SSend.pop(0)
            except:
                Obj_uart.ser = Obj_uart.check_port_open()
class CRC8_Xicro():
    def __init__(self):
        self.lookup = [0x00,0x5E,0xBC,0xE2,0x61,0x3F,0xDD,0x83,0xC2,0x9C,0x7E,0x20,0xA3,0xFD,0x1F,0x41,0x9D,0xC3,0x21,0x7F,0xFC,0xA2,0x40,0x1E,0x5F,0x01,0xE3,0xBD,0x3E,0x60,0x82,0xDC,0x23,0x7D,0x9F,0xC1,0x42,0x1C,0xFE,0xA0,0xE1,0xBF,0x5D,0x03,0x80,0xDE,0x3C,0x62,0xBE,0xE0,0x02,0x5C,0xDF,0x81,0x63,0x3D,0x7C,0x22,0xC0,0x9E,0x1D,0x43,0xA1,0xFF,0x46,0x18,0xFA,0xA4,0x27,0x79,0x9B,0xC5,0x84,0xDA,0x38,0x66,0xE5,0xBB,0x59,0x07,0xDB,0x85,0x67,0x39,0xBA,0xE4,0x06,0x58,0x19,0x47,0xA5,0xFB,0x78,0x26,0xC4,0x9A,0x65,0x3B,0xD9,0x87,0x04,0x5A,0xB8,0xE6,0xA7,0xF9,0x1B,0x45,0xC6,0x98,0x7A,0x24,0xF8,0xA6,0x44,0x1A,0x99,0xC7,0x25,0x7B,0x3A,0x64,0x86,0xD8,0x5B,0x05,0xE7,0xB9,0x8C,0xD2,0x30,0x6E,0xED,0xB3,0x51,0x0F,0x4E,0x10,0xF2,0xAC,0x2F,0x71,0x93,0xCD,0x11,0x4F,0xAD,0xF3,0x70,0x2E,0xCC,0x92,0xD3,0x8D,0x6F,0x31,0xB2,0xEC,0x0E,0x50,0xAF,0xF1,0x13,0x4D,0xCE,0x90,0x72,0x2C,0x6D,0x33,0xD1,0x8F,0x0C,0x52,0xB0,0xEE,0x32,0x6C,0x8E,0xD0,0x53,0x0D,0xEF,0xB1,0xF0,0xAE,0x4C,0x12,0x91,0xCF,0x2D,0x73,0xCA,0x94,0x76,0x28,0xAB,0xF5,0x17,0x49,0x08,0x56,0xB4,0xEA,0x69,0x37,0xD5,0x8B,0x57,0x09,0xEB,0xB5,0x36,0x68,0x8A,0xD4,0x95,0xCB,0x29,0x77,0xF4,0xAA,0x48,0x16,0xE9,0xB7,0x55,0x0B,0x88,0xD6,0x34,0x6A,0x2B,0x75,0x97,0xC9,0x4A,0x14,0xF6,0xA8,0x74,0x2A,0xC8,0x96,0x15,0x4B,0xA9,0xF7,0xB6,0xE8,0x0A,0x54,0xD7,0x89,0x6B,0x35]
        self.crc=0
        self.buff=[]
        self.index=0
        self.buffersize=0
    def resetCRC(self):
        self.crc=0
    def Add(self,buffer):
        CRC=0
        for i  in  range(0,len(buffer)):
            CRC = self.lookup[CRC ^ buffer[i]]
        buffer.append(CRC)
        return  buffer
    def CheckOne(self,crc,data):
        crc = self.lookup[crc ^ data]
        return crc
    def CheckList(self,CRC,buffer):
        for i  in  range(0,len(buffer)):
            CRC = self.lookup[CRC ^ buffer[i]]
        return  CRC
    def begin(self,BUFFER):
        self.buff=BUFFER
    def startCom(self,index):
        self.crc = 0
        self.crc = self.lookup[self.crc ^ self.buff[index]]
    def update(self,index):
        self.crc = self.lookup[self.crc ^ int(self.buff[index])]
    def result(self):
        return self.crc
    def FlagCheck(self,compairValue):
        if(compairValue==self.crc):
            return 1
        else:
            return 0
        
def bufferToType(BUFFER,Typee):
    if(Typee== "uint8" or Typee== "uint16" or Typee== "uint32" or Typee== "uint64"):
        bytes_val = bytearray(BUFFER)
        return int.from_bytes(bytes_val, byteorder="big",signed=0)
    elif(Typee=="int8" or Typee =="int16" or Typee== "int32" or Typee== "int64"):
        bytes_val = bytearray(BUFFER)
        return int.from_bytes(bytes_val, byteorder="big",signed=1)
    elif(Typee=="float32" ):
        bytes_val = bytearray(BUFFER)
        return struct.unpack('<f', bytes_val)[0]

    elif(Typee=="float64"):
        bytes_val = bytearray(BUFFER)
        return struct.unpack('<d', bytes_val)[0]
def setup_srv_protocol():
    setup_srv=get_params('ros.srv_client')
    Idmcu=get_params("microcontroller.idmcu")
    Idsrv=[]
    namesrv=[]
    interfacesrv=[]
    timeOut=[]
    for i in range(0,len(setup_srv)):
        Idsrv.append(setup_srv[i][0])
        namesrv.append(setup_srv[i][1])
        interfacesrv.append(setup_srv[i][2])
        timeOut.append(setup_srv[i][3])
    # print('Done load YAML srv_client.')
    # print(Idsrv,namesrv,interfacesrv )
    dataType_srv_req=[]
    dataName_srv_req=[]
    NofData_srv_req=[]
    datagrab_srv_req=[]
    datatypeProtocol_srv_req=[]
    bytetograb_srv_req=[]
    dataType_srv_res=[]
    dataName_srv_res=[]
    NofData_srv_res=[]
    datagrab_srv_res=[]
    datatypeProtocol_srv_res=[]
    bytetograb_srv_res=[]
    interfacein_srv_req=[]
    interfacein_srv_res=[]
    for i in range (0,len(interfacesrv)):  
        flagP=0
        tempType_req=[]
        tempName_req=[]
        tempN_req=[]
        tempType_res=[]
        tempName_res=[]
        tempN_res=[]
        tempinterfacein_req=[]
        tempinterfacein_res=[]
        path = os.path.join(get_package_share_directory( interfacesrv[i].split("/")[0]),'srv', interfacesrv[i].split("/")[1])
        srv = open(path, 'r').read().splitlines()
        for j in range(0,len(srv)):
            line=srv[j].split()
            if(len(line)>0):
                if(len(line)!=0 and line[0]!="#" and line[0]!="---" and flagP==0):
                    tempType_req.append(line[0])
                    tempName_req.append(line[1])
                    tempN_req.append(checkNofdata(line[0]))
                    tempinterfacein_req.append(interfacesrv[i].split("/")[0])
                elif(len(line)!=0 and line[0]!="#" and line[0]!="---" and flagP==1):
                    tempType_res.append(line[0])
                    tempName_res.append(line[1])
                    tempN_res.append(checkNofdata(line[0]))
                    tempinterfacein_res.append(interfacesrv[i].split("/")[0])
                if(line[0]=="---"):
                    flagP=1
        # print(tempN_req)
        # print(tempType_req)
        # print(tempName_req)
        # print(tempinterfacein_req)
        if(len(tempType_req)==0):
            NofData_srv_req.append([1])
            dataType_srv_req.append(["xxicro_Empty"])
            dataName_srv_req.append(["xxicro_Empty"])
            interfacein_srv_req.append([interfacesrv[i].split("/")[0]])
        else:
            NofData_srv_req.append(tempN_req)
            dataType_srv_req.append(tempType_req)
            dataName_srv_req.append(tempName_req)
            interfacein_srv_req.append(tempinterfacein_req)

        if(len(tempType_res)==0):
            NofData_srv_res.append([1])
            dataType_srv_res.append(["xxicro_Empty"])
            dataName_srv_res.append(["xxicro_Empty"])
            interfacein_srv_res.append([interfacesrv[i].split("/")[0]])
        else:
            NofData_srv_res.append(tempN_res)
            dataType_srv_res.append(tempType_res)
            dataName_srv_res.append(tempName_res)
            interfacein_srv_res.append(tempinterfacein_res)
    # print(Idsrv,namesrv,interfacesrv,NofData_srv_req,dataType_srv_req,dataName_srv_req,"res",NofData_srv_res,dataType_srv_res,dataName_srv_res)

    for i in range(0,10):
        Idmcu,Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,NofData_srv_req,interfacein_srv_req=expandSub(Idmcu,Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,NofData_srv_req,interfacein_srv_req)
        Idmcu,Idsrv,namesrv,interfacesrv,dataType_srv_res,dataName_srv_res,NofData_srv_res,interfacein_srv_res=expandSub(Idmcu,Idsrv,namesrv,interfacesrv,dataType_srv_res,dataName_srv_res,NofData_srv_res,interfacein_srv_res)
    # print(Idsrv,namesrv,interfacesrv,NofData_srv_req,dataType_srv_req,dataName_srv_req,"res",NofData_srv_res,dataType_srv_res,dataName_srv_res)
    for i in range(0,len(dataType_srv_req)): # bias float64 to float32
        for j in range(0,len(dataType_srv_req[i])):
            if(dataType_srv_req[i][j].split("[")[0] == "float64" and (input.mcu_type=="arduino" or input.mcu_type=="esp") ):
                dataType_srv_req[i][j]="float32"
    for i in range(0,len(dataType_srv_res)): # bias float64 to float32
        for j in range(0,len(dataType_srv_res[i])):
            if(dataType_srv_res[i][j].split("[")[0] == "float64" and (input.mcu_type=="arduino" or input.mcu_type=="esp") ):
                dataType_srv_res[i][j]="float32"

    # # cal  [ byte to grab , dataProtocol , datagrab   ] dataTyperemove_index 
    for p in range(0,2):
        if(p==0):
            dataType=dataType_srv_req
            NofData=NofData_srv_req
        elif(p==1):
            dataType=dataType_srv_res
            NofData=NofData_srv_res
        for i in range(0,len(dataType)):
            tempbytetograb=[]
            tempdataprotocol=[]
            tempdatagrab=[]
            for j in range(0,len(dataType[i])):
                #data type remove []
                if(NofData[i][j]!=1):
                    tt=[]
                    for k in range(0,NofData[i][j]):
                        if(dataType[i][j].split("[")[0]=="string"):
                            tt.append("")
                        elif(dataType[i][j].split("[")[0]=="float32" or dataType[i][j].split("[")[0]=="float64"):
                            tt.append(0.0)
                        elif(dataType[i][j].split("[")[0]=="bool"):
                            tt.append(False)   
                        else:
                            tt.append(0)
                    tempdatagrab.append(tt)
                else:
                    if(dataType[i][j]=="string"):
                        tempdatagrab.append("")
                    elif(dataType[i][j]=="float32" or dataType[i][j]=="float64"):
                        tempdatagrab.append(0.0)
                    elif(dataType[i][j]=="bool"):
                        tempdatagrab.append(False)
                    elif(dataType[i][j]=="xxicro_Empty"):
                        tempdatagrab.append("xxicro_Empty")
                    else:
                        tempdatagrab.append(0) 

                if(dataType[i][j].find("[")!=-1 ):
                    dataType[i][j]=dataType[i][j][0:dataType[i][j].find("[")]
                a,b=typetoProtocol(dataType[i][j],NofData[i][j])
                tempdataprotocol.append(a)
                tempbytetograb.append(b)
            
            if(p==0):
                datatypeProtocol_srv_req.append(tempdataprotocol)
                bytetograb_srv_req.append(tempbytetograb)
                datagrab_srv_req.append(tempdatagrab)
            elif(p==1):
                datatypeProtocol_srv_res.append(tempdataprotocol)
                bytetograb_srv_res.append(tempbytetograb)
                datagrab_srv_res.append(tempdatagrab)
    # print(Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res)
    return Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res,timeOut
def setup_srv_server_protocol():
    setup_srv=get_params('ros.srv_server')
    Idmcu=get_params("microcontroller.idmcu")
    Idsrv=[]
    namesrv=[]
    interfacesrv=[]
    timeOut=[]
    for i in range(0,len(setup_srv)):
        Idsrv.append(setup_srv[i][0])
        namesrv.append(setup_srv[i][1])
        interfacesrv.append(setup_srv[i][2])
        timeOut.append(setup_srv[i][3])
    # print('Done load YAML srv_server.')
    # print(Idsrv,namesrv,interfacesrv )
    dataType_srv_req=[]
    dataName_srv_req=[]
    NofData_srv_req=[]
    datagrab_srv_req=[]
    datatypeProtocol_srv_req=[]
    bytetograb_srv_req=[]
    dataType_srv_res=[]
    dataName_srv_res=[]
    NofData_srv_res=[]
    datagrab_srv_res=[]
    datatypeProtocol_srv_res=[]
    bytetograb_srv_res=[]
    interfacein_srv_req=[]
    interfacein_srv_res=[]
    for i in range (0,len(interfacesrv)):  
        flagP=0
        tempType_req=[]
        tempName_req=[]
        tempN_req=[]
        tempType_res=[]
        tempName_res=[]
        tempN_res=[]
        tempinterfacein_req=[]
        tempinterfacein_res=[]
        path = os.path.join(get_package_share_directory( interfacesrv[i].split("/")[0]),'srv', interfacesrv[i].split("/")[1])
        srv = open(path, 'r').read().splitlines()
        for j in range(0,len(srv)):
            line=srv[j].split()
            if(len(line)>0):
                if(len(line)!=0 and line[0]!="#" and line[0]!="---" and flagP==0):
                    tempType_req.append(line[0])
                    tempName_req.append(line[1])
                    tempN_req.append(checkNofdata(line[0]))
                    tempinterfacein_req.append(interfacesrv[i].split("/")[0])
                elif(len(line)!=0 and line[0]!="#" and line[0]!="---" and flagP==1):
                    tempType_res.append(line[0])
                    tempName_res.append(line[1])
                    tempN_res.append(checkNofdata(line[0]))
                    tempinterfacein_res.append(interfacesrv[i].split("/")[0])
                if(line[0]=="---"):
                    flagP=1
        # print(tempN_req)
        # print(tempType_req)
        # print(tempName_req)
        # print(tempinterfacein_req)
        if(len(tempType_req)==0):
            NofData_srv_req.append([1])
            dataType_srv_req.append(["xxicro_Empty"])
            dataName_srv_req.append(["xxicro_Empty"])
            interfacein_srv_req.append([interfacesrv[i].split("/")[0]])
        else:
            NofData_srv_req.append(tempN_req)
            dataType_srv_req.append(tempType_req)
            dataName_srv_req.append(tempName_req)
            interfacein_srv_req.append(tempinterfacein_req)

        if(len(tempType_res)==0):
            NofData_srv_res.append([1])
            dataType_srv_res.append(["xxicro_Empty"])
            dataName_srv_res.append(["xxicro_Empty"])
            interfacein_srv_res.append([interfacesrv[i].split("/")[0]])
        else:
            NofData_srv_res.append(tempN_res)
            dataType_srv_res.append(tempType_res)
            dataName_srv_res.append(tempName_res)
            interfacein_srv_res.append(tempinterfacein_res)
    # print(Idsrv,namesrv,interfacesrv,NofData_srv_req,dataType_srv_req,dataName_srv_req,"res",NofData_srv_res,dataType_srv_res,dataName_srv_res)

    for i in range(0,10):
        Idmcu,Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,NofData_srv_req,interfacein_srv_req=expandSub(Idmcu,Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,NofData_srv_req,interfacein_srv_req)
        Idmcu,Idsrv,namesrv,interfacesrv,dataType_srv_res,dataName_srv_res,NofData_srv_res,interfacein_srv_res=expandSub(Idmcu,Idsrv,namesrv,interfacesrv,dataType_srv_res,dataName_srv_res,NofData_srv_res,interfacein_srv_res)
    # print(Idsrv,namesrv,interfacesrv,NofData_srv_req,dataType_srv_req,dataName_srv_req,"res",NofData_srv_res,dataType_srv_res,dataName_srv_res)
    for i in range(0,len(dataType_srv_req)): # bias float64 to float32
        for j in range(0,len(dataType_srv_req[i])):
            if(dataType_srv_req[i][j].split("[")[0] == "float64" and (input.mcu_type=="arduino" or input.mcu_type=="esp") ):
                dataType_srv_req[i][j]="float32"
    for i in range(0,len(dataType_srv_res)): # bias float64 to float32
        for j in range(0,len(dataType_srv_res[i])):
            if(dataType_srv_res[i][j].split("[")[0] == "float64" and (input.mcu_type=="arduino" or input.mcu_type=="esp") ):
                dataType_srv_res[i][j]="float32"

    # # cal  [ byte to grab , dataProtocol , datagrab   ] dataTyperemove_index 
    for p in range(0,2):
        if(p==0):
            dataType=dataType_srv_req
            NofData=NofData_srv_req
        elif(p==1):
            dataType=dataType_srv_res
            NofData=NofData_srv_res
        for i in range(0,len(dataType)):
            tempbytetograb=[]
            tempdataprotocol=[]
            tempdatagrab=[]
            for j in range(0,len(dataType[i])):
                #data type remove []
                if(NofData[i][j]!=1):
                    tt=[]
                    for k in range(0,NofData[i][j]):
                        if(dataType[i][j].split("[")[0]=="string"):
                            tt.append("")
                        elif(dataType[i][j].split("[")[0]=="float32" or dataType[i][j].split("[")[0]=="float64"):
                            tt.append(0.0)
                        elif(dataType[i][j].split("[")[0]=="bool"):
                            tt.append(False)   
                        else:
                            tt.append(0)
                    tempdatagrab.append(tt)
                else:
                    if(dataType[i][j]=="string"):
                        tempdatagrab.append("")
                    elif(dataType[i][j]=="float32" or dataType[i][j]=="float64"):
                        tempdatagrab.append(0.0)
                    elif(dataType[i][j]=="bool"):
                        tempdatagrab.append(False)
                    elif(dataType[i][j]=="xxicro_Empty"):
                        tempdatagrab.append("xxicro_Empty")
                    else:
                        tempdatagrab.append(0) 

                if(dataType[i][j].find("[")!=-1 ):
                    dataType[i][j]=dataType[i][j][0:dataType[i][j].find("[")]
                a,b=typetoProtocol(dataType[i][j],NofData[i][j])
                tempdataprotocol.append(a)
                tempbytetograb.append(b)
            
            if(p==0):
                datatypeProtocol_srv_req.append(tempdataprotocol)
                bytetograb_srv_req.append(tempbytetograb)
                datagrab_srv_req.append(tempdatagrab)
            elif(p==1):
                datatypeProtocol_srv_res.append(tempdataprotocol)
                bytetograb_srv_res.append(tempbytetograb)
                datagrab_srv_res.append(tempdatagrab)
    # print(Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res)
    return Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res,timeOut

def setup_action_client_protocol():
    setup_action=get_params('ros.action_client')
    Idmcu=get_params("microcontroller.idmcu")
    Idaction=[]
    nameaction=[]
    interfaceaction=[]
    timeOut=[]
    for i in range(0,len(setup_action)):
        Idaction.append(setup_action[i][0])
        nameaction.append(setup_action[i][1])
        interfaceaction.append(setup_action[i][2])
        timeOut.append(setup_action[i][3])
    # print('Done load YAML action client.')
    # print(Idaction,nameaction,interfaceaction )
    dataType_action_req=[]
    dataName_action_req=[]
    NofData_action_req=[]
    datagrab_action_req=[]
    datatypeProtocol_action_req=[]
    bytetograb_action_req=[]

    dataType_action_res=[]
    dataName_action_res=[]
    NofData_action_res=[]
    datagrab_action_res=[]
    datatypeProtocol_action_res=[]
    bytetograb_action_res=[]

    dataType_action_feed=[]
    dataName_action_feed=[]
    NofData_action_feed=[]
    datagrab_action_feed=[]
    datatypeProtocol_action_feed=[]
    bytetograb_action_feed=[]


    interfacein_action_req=[]
    interfacein_action_res=[]
    interfacein_action_feed=[]
    for i in range (0,len(interfaceaction)):  
        flagP=0
        tempType_req=[]
        tempName_req=[]
        tempN_req=[]

        tempType_res=[]
        tempName_res=[]
        tempN_res=[]

        tempType_feed=[]
        tempName_feed=[]
        tempN_feed=[]

        tempinterfacein_req=[]
        tempinterfacein_res=[]
        tempinterfacein_feed=[]
        path = os.path.join(get_package_share_directory( interfaceaction[i].split("/")[0]),'action', interfaceaction[i].split("/")[1])
        action = open(path, 'r').read().splitlines()
        for j in range(0,len(action)):
            line=action[j].split()
            if(len(line)>0):
                if(len(line)!=0 and line[0]!="#" and line[0]!="---" and flagP==0):
                    tempType_req.append(line[0])
                    tempName_req.append(line[1])
                    tempN_req.append(checkNofdata(line[0]))
                    tempinterfacein_req.append(interfaceaction[i].split("/")[0])
                elif(len(line)!=0 and line[0]!="#" and line[0]!="---" and flagP==1):
                    tempType_res.append(line[0])
                    tempName_res.append(line[1])
                    tempN_res.append(checkNofdata(line[0]))
                    tempinterfacein_res.append(interfaceaction[i].split("/")[0])
                elif(len(line)!=0 and line[0]!="#" and line[0]!="---" and flagP==2):
                    tempType_feed.append(line[0])
                    tempName_feed.append(line[1])
                    tempN_feed.append(checkNofdata(line[0]))
                    tempinterfacein_feed.append(interfaceaction[i].split("/")[0])
                if(line[0]=="---"):
                    flagP=flagP+1
        # print(tempN_req)
        # print(tempType_req)
        # print(tempName_req)
        # print(tempinterfacein_req)
        if(len(tempType_req)==0):
            NofData_action_req.append([1])
            dataType_action_req.append(["xxicro_Empty"])
            dataName_action_req.append(["xxicro_Empty"])
            interfacein_action_req.append([interfaceaction[i].split("/")[0]])
        else:
            NofData_action_req.append(tempN_req)
            dataType_action_req.append(tempType_req)
            dataName_action_req.append(tempName_req)
            interfacein_action_req.append(tempinterfacein_req)

        if(len(tempType_res)==0):
            NofData_action_res.append([1])
            dataType_action_res.append(["xxicro_Empty"])
            dataName_action_res.append(["xxicro_Empty"])
            interfacein_action_res.append([interfaceaction[i].split("/")[0]])
        else:
            NofData_action_res.append(tempN_res)
            dataType_action_res.append(tempType_res)
            dataName_action_res.append(tempName_res)
            interfacein_action_res.append(tempinterfacein_res)

        if(len(tempType_feed)==0):
            NofData_action_feed.append([1])
            dataType_action_feed.append(["xxicro_Empty"])
            dataName_action_feed.append(["xxicro_Empty"])
            interfacein_action_feed.append([interfaceaction[i].split("/")[0]])
        else:
            NofData_action_feed.append(tempN_feed)
            dataType_action_feed.append(tempType_feed)
            dataName_action_feed.append(tempName_feed)
            interfacein_action_feed.append(tempinterfacein_feed)
        
    # print(Idsrv,namesrv,interfacesrv,NofData_srv_req,dataType_srv_req,dataName_srv_req,"res",NofData_srv_res,dataType_srv_res,dataName_srv_res)

    for i in range(0,10):
        Idmcu,Idaction,nameaction,interfaceaction,dataType_action_req,dataName_action_req,NofData_action_req,interfacein_action_req=expandSub(Idmcu,Idaction,nameaction,interfaceaction,dataType_action_req,dataName_action_req,NofData_action_req,interfacein_action_req)
        Idmcu,Idaction,nameaction,interfaceaction,dataType_action_res,dataName_action_res,NofData_action_res,interfacein_action_res=expandSub(Idmcu,Idaction,nameaction,interfaceaction,dataType_action_res,dataName_action_res,NofData_action_res,interfacein_action_res)
        Idmcu,Idaction,nameaction,interfaceaction,dataType_action_feed,dataName_action_feed,NofData_action_feed,interfacein_action_feed=expandSub(Idmcu,Idaction,nameaction,interfaceaction,dataType_action_feed,dataName_action_feed,NofData_action_feed,interfacein_action_feed)

    # print(Idsrv,namesrv,interfacesrv,NofData_srv_req,dataType_srv_req,dataName_srv_req,"res",NofData_srv_res,dataType_srv_res,dataName_srv_res)
    for i in range(0,len(dataType_action_req)): # bias float64 to float32
        for j in range(0,len(dataType_action_req[i])):
            if(dataType_action_req[i][j].split("[")[0] == "float64" and (input.mcu_type=="arduino" or input.mcu_type=="esp") ):
                dataType_action_req[i][j]="float32"
    for i in range(0,len(dataType_action_res)): # bias float64 to float32
        for j in range(0,len(dataType_action_res[i])):
            if(dataType_action_res[i][j].split("[")[0] == "float64" and (input.mcu_type=="arduino" or input.mcu_type=="esp") ):
                dataType_action_res[i][j]="float32"
    for i in range(0,len(dataType_action_feed)): # bias float64 to float32
        for j in range(0,len(dataType_action_feed[i])):
            if(dataType_action_feed[i][j].split("[")[0] == "float64" and (input.mcu_type=="arduino" or input.mcu_type=="esp") ):
                dataType_action_feed[i][j]="float32"

    # # cal  [ byte to grab , dataProtocol , datagrab   ] dataTyperemove_index 
    for p in range(0,3):
        if(p==0):
            dataType=dataType_action_req
            NofData=NofData_action_req
        elif(p==1):
            dataType=dataType_action_res
            NofData=NofData_action_res
        elif(p==2):
            dataType=dataType_action_feed
            NofData=NofData_action_feed
        for i in range(0,len(dataType)):
            tempbytetograb=[]
            tempdataprotocol=[]
            tempdatagrab=[]
            for j in range(0,len(dataType[i])):
                #data type remove []
                if(NofData[i][j]!=1):
                    tt=[]
                    for k in range(0,NofData[i][j]):
                        if(dataType[i][j].split("[")[0]=="string"):
                            tt.append("")
                        elif(dataType[i][j].split("[")[0]=="float32" or dataType[i][j].split("[")[0]=="float64"):
                            tt.append(0.0)
                        elif(dataType[i][j].split("[")[0]=="bool"):
                            tt.append(False)   
                        else:
                            tt.append(0)
                    tempdatagrab.append(tt)
                else:
                    if(dataType[i][j]=="string"):
                        tempdatagrab.append("")
                    elif(dataType[i][j]=="float32" or dataType[i][j]=="float64"):
                        tempdatagrab.append(0.0)
                    elif(dataType[i][j]=="bool"):
                        tempdatagrab.append(False)
                    elif(dataType[i][j]=="xxicro_Empty"):
                        tempdatagrab.append("xxicro_Empty")
                    else:
                        tempdatagrab.append(0) 

                if(dataType[i][j].find("[")!=-1 ):
                    dataType[i][j]=dataType[i][j][0:dataType[i][j].find("[")]
                a,b=typetoProtocol(dataType[i][j],NofData[i][j])
                tempdataprotocol.append(a)
                tempbytetograb.append(b)
            
            if(p==0):
                datatypeProtocol_action_req.append(tempdataprotocol)
                bytetograb_action_req.append(tempbytetograb)
                datagrab_action_req.append(tempdatagrab)
            elif(p==1):
                datatypeProtocol_action_res.append(tempdataprotocol)
                bytetograb_action_res.append(tempbytetograb)
                datagrab_action_res.append(tempdatagrab)
            elif(p==2):
                datatypeProtocol_action_feed.append(tempdataprotocol)
                bytetograb_action_feed.append(tempbytetograb)
                datagrab_action_feed.append(tempdatagrab)
    # print(Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res)
    return Idaction,nameaction,interfaceaction,dataType_action_req,dataName_action_req,datagrab_action_req,NofData_action_req,datatypeProtocol_action_req,bytetograb_action_req,dataType_action_res,dataName_action_res,datagrab_action_res,NofData_action_res,datatypeProtocol_action_res,bytetograb_action_res,dataType_action_feed,dataName_action_feed,datagrab_action_feed,NofData_action_feed,datatypeProtocol_action_feed,bytetograb_action_feed,timeOut

def setup_action_server_protocol():
    setup_action=get_params('ros.action_server')
    Idmcu=get_params("microcontroller.idmcu")
    Idaction=[]
    nameaction=[]
    interfaceaction=[]
    timeOut=[]
    for i in range(0,len(setup_action)):
        Idaction.append(setup_action[i][0])
        nameaction.append(setup_action[i][1])
        interfaceaction.append(setup_action[i][2])
        timeOut.append(setup_action[i][3])
    # print('Done load YAML action server.')
    # print(Idaction,nameaction,interfaceaction )
    dataType_action_req=[]
    dataName_action_req=[]
    NofData_action_req=[]
    datagrab_action_req=[]
    datatypeProtocol_action_req=[]
    bytetograb_action_req=[]

    dataType_action_res=[]
    dataName_action_res=[]
    NofData_action_res=[]
    datagrab_action_res=[]
    datatypeProtocol_action_res=[]
    bytetograb_action_res=[]

    dataType_action_feed=[]
    dataName_action_feed=[]
    NofData_action_feed=[]
    datagrab_action_feed=[]
    datatypeProtocol_action_feed=[]
    bytetograb_action_feed=[]


    interfacein_action_req=[]
    interfacein_action_res=[]
    interfacein_action_feed=[]
    for i in range (0,len(interfaceaction)):  
        flagP=0
        tempType_req=[]
        tempName_req=[]
        tempN_req=[]

        tempType_res=[]
        tempName_res=[]
        tempN_res=[]

        tempType_feed=[]
        tempName_feed=[]
        tempN_feed=[]

        tempinterfacein_req=[]
        tempinterfacein_res=[]
        tempinterfacein_feed=[]
        path = os.path.join(get_package_share_directory( interfaceaction[i].split("/")[0]),'action', interfaceaction[i].split("/")[1])
        action = open(path, 'r').read().splitlines()
        for j in range(0,len(action)):
            line=action[j].split()
            if(len(line)>0):
                if(len(line)!=0 and line[0]!="#" and line[0]!="---" and flagP==0):
                    tempType_req.append(line[0])
                    tempName_req.append(line[1])
                    tempN_req.append(checkNofdata(line[0]))
                    tempinterfacein_req.append(interfaceaction[i].split("/")[0])
                elif(len(line)!=0 and line[0]!="#" and line[0]!="---" and flagP==1):
                    tempType_res.append(line[0])
                    tempName_res.append(line[1])
                    tempN_res.append(checkNofdata(line[0]))
                    tempinterfacein_res.append(interfaceaction[i].split("/")[0])
                elif(len(line)!=0 and line[0]!="#" and line[0]!="---" and flagP==2):
                    tempType_feed.append(line[0])
                    tempName_feed.append(line[1])
                    tempN_feed.append(checkNofdata(line[0]))
                    tempinterfacein_feed.append(interfaceaction[i].split("/")[0])
                if(line[0]=="---"):
                    flagP=flagP+1
        # print(tempN_req)
        # print(tempType_req)
        # print(tempName_req)
        # print(tempinterfacein_req)
        if(len(tempType_req)==0):
            NofData_action_req.append([1])
            dataType_action_req.append(["xxicro_Empty"])
            dataName_action_req.append(["xxicro_Empty"])
            interfacein_action_req.append([interfaceaction[i].split("/")[0]])
        else:
            NofData_action_req.append(tempN_req)
            dataType_action_req.append(tempType_req)
            dataName_action_req.append(tempName_req)
            interfacein_action_req.append(tempinterfacein_req)

        if(len(tempType_res)==0):
            NofData_action_res.append([1])
            dataType_action_res.append(["xxicro_Empty"])
            dataName_action_res.append(["xxicro_Empty"])
            interfacein_action_res.append([interfaceaction[i].split("/")[0]])
        else:
            NofData_action_res.append(tempN_res)
            dataType_action_res.append(tempType_res)
            dataName_action_res.append(tempName_res)
            interfacein_action_res.append(tempinterfacein_res)

        if(len(tempType_feed)==0):
            NofData_action_feed.append([1])
            dataType_action_feed.append(["xxicro_Empty"])
            dataName_action_feed.append(["xxicro_Empty"])
            interfacein_action_feed.append([interfaceaction[i].split("/")[0]])
        else:
            NofData_action_feed.append(tempN_feed)
            dataType_action_feed.append(tempType_feed)
            dataName_action_feed.append(tempName_feed)
            interfacein_action_feed.append(tempinterfacein_feed)
        
    # print(Idsrv,namesrv,interfacesrv,NofData_srv_req,dataType_srv_req,dataName_srv_req,"res",NofData_srv_res,dataType_srv_res,dataName_srv_res)

    for i in range(0,10):
        Idmcu,Idaction,nameaction,interfaceaction,dataType_action_req,dataName_action_req,NofData_action_req,interfacein_action_req=expandSub(Idmcu,Idaction,nameaction,interfaceaction,dataType_action_req,dataName_action_req,NofData_action_req,interfacein_action_req)
        Idmcu,Idaction,nameaction,interfaceaction,dataType_action_res,dataName_action_res,NofData_action_res,interfacein_action_res=expandSub(Idmcu,Idaction,nameaction,interfaceaction,dataType_action_res,dataName_action_res,NofData_action_res,interfacein_action_res)
        Idmcu,Idaction,nameaction,interfaceaction,dataType_action_feed,dataName_action_feed,NofData_action_feed,interfacein_action_feed=expandSub(Idmcu,Idaction,nameaction,interfaceaction,dataType_action_feed,dataName_action_feed,NofData_action_feed,interfacein_action_feed)

    # print(Idsrv,namesrv,interfacesrv,NofData_srv_req,dataType_srv_req,dataName_srv_req,"res",NofData_srv_res,dataType_srv_res,dataName_srv_res)
    for i in range(0,len(dataType_action_req)): # bias float64 to float32
        for j in range(0,len(dataType_action_req[i])):
            if(dataType_action_req[i][j].split("[")[0] == "float64" and (input.mcu_type=="arduino" or input.mcu_type=="esp") ):
                dataType_action_req[i][j]="float32"
    for i in range(0,len(dataType_action_res)): # bias float64 to float32
        for j in range(0,len(dataType_action_res[i])):
            if(dataType_action_res[i][j].split("[")[0] == "float64" and (input.mcu_type=="arduino" or input.mcu_type=="esp") ):
                dataType_action_res[i][j]="float32"
    for i in range(0,len(dataType_action_feed)): # bias float64 to float32
        for j in range(0,len(dataType_action_feed[i])):
            if(dataType_action_feed[i][j].split("[")[0] == "float64" and (input.mcu_type=="arduino" or input.mcu_type=="esp") ):
                dataType_action_feed[i][j]="float32"

    # # cal  [ byte to grab , dataProtocol , datagrab   ] dataTyperemove_index 
    for p in range(0,3):
        if(p==0):
            dataType=dataType_action_req
            NofData=NofData_action_req
        elif(p==1):
            dataType=dataType_action_res
            NofData=NofData_action_res
        elif(p==2):
            dataType=dataType_action_feed
            NofData=NofData_action_feed
        for i in range(0,len(dataType)):
            tempbytetograb=[]
            tempdataprotocol=[]
            tempdatagrab=[]
            for j in range(0,len(dataType[i])):
                #data type remove []
                if(NofData[i][j]!=1):
                    tt=[]
                    for k in range(0,NofData[i][j]):
                        if(dataType[i][j].split("[")[0]=="string"):
                            tt.append("")
                        elif(dataType[i][j].split("[")[0]=="float32" or dataType[i][j].split("[")[0]=="float64"):
                            tt.append(0.0)
                        elif(dataType[i][j].split("[")[0]=="bool"):
                            tt.append(False)   
                        else:
                            tt.append(0)
                    tempdatagrab.append(tt)
                else:
                    if(dataType[i][j]=="string"):
                        tempdatagrab.append("")
                    elif(dataType[i][j]=="float32" or dataType[i][j]=="float64"):
                        tempdatagrab.append(0.0)
                    elif(dataType[i][j]=="bool"):
                        tempdatagrab.append(False)
                    elif(dataType[i][j]=="xxicro_Empty"):
                        tempdatagrab.append("xxicro_Empty")
                    else:
                        tempdatagrab.append(0) 

                if(dataType[i][j].find("[")!=-1 ):
                    dataType[i][j]=dataType[i][j][0:dataType[i][j].find("[")]
                a,b=typetoProtocol(dataType[i][j],NofData[i][j])
                tempdataprotocol.append(a)
                tempbytetograb.append(b)
            
            if(p==0):
                datatypeProtocol_action_req.append(tempdataprotocol)
                bytetograb_action_req.append(tempbytetograb)
                datagrab_action_req.append(tempdatagrab)
            elif(p==1):
                datatypeProtocol_action_res.append(tempdataprotocol)
                bytetograb_action_res.append(tempbytetograb)
                datagrab_action_res.append(tempdatagrab)
            elif(p==2):
                datatypeProtocol_action_feed.append(tempdataprotocol)
                bytetograb_action_feed.append(tempbytetograb)
                datagrab_action_feed.append(tempdatagrab)
    # print(Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res)
    return Idaction,nameaction,interfaceaction,dataType_action_req,dataName_action_req,datagrab_action_req,NofData_action_req,datatypeProtocol_action_req,bytetograb_action_req,dataType_action_res,dataName_action_res,datagrab_action_res,NofData_action_res,datatypeProtocol_action_res,bytetograb_action_res,dataType_action_feed,dataName_action_feed,datagrab_action_feed,NofData_action_feed,datatypeProtocol_action_feed,bytetograb_action_feed,timeOut
  
def Protocol_XicroToRos_spin(Obj_uart,ModeEx,checkIdOn,sh_res,st_index,sh_res_2,Buff_test): #processer 3,5,srv_server_res


    if(ModeEx==0):
        Indexpre_value=Obj_uart.index.value
        print("XicroToRos_spin pub")
    elif(ModeEx==1):
        Indexpre_value=Obj_uart.index.value
        Pn=888
        print("XicroToRos_spin Srv client")
    elif(ModeEx==2):
        Indexpre_value=st_index
        Pn=888
        print("XicroToROs_spin Srv server wait response IdOn : "+str(checkIdOn))
    elif(ModeEx==3):
        Indexpre_value=Obj_uart.index.value
        Pn=888
        print("XicroToRos_spin Action client")
    elif(ModeEx==4):
        Indexpre_value=st_index
        Pn=888
        print("XicroToROs_spin Action server wait feedback and result IdOn : "+str(checkIdOn))
    crcc=CRC8_Xicro() # create crc object
    crcc.begin(Obj_uart.Buff)  # crc begin
    state=0
    Idmsg,nametopic,interfacetopic,dataType,dataName,datagrab,NofData,datatypeProtocol,byteTograb=setup_var_protocol() # get variable from yaml
    pipe=[888, 888, 888, 888, 888, 888, 888, 888, 888, 888, 888, 888, 888, 888, 888, 888]
    Idsrv_client,namesrv_client,interfacesrv_client,dataType_srv_client_req,dataName_srv_client_req,datagrab_srv_client_req,NofData_srv_client_req,datatypeProtocol_srv_client_req,bytetograb_srv_client_req,dataType_srv_client_res,dataName_srv_client_res,datagrab_srv_client_res,NofData_srv_client_res,datatypeProtocol_srv_client_res,bytetograb_srv_client_res,timeOut_srv_client = setup_srv_protocol()
    Idsrv_server,namesrv_server,interfacesrv_server,dataType_srv_server_req,dataName_srv_server_req,datagrab_srv_server_req,NofData_srv_server_req,datatypeProtocol_srv_server_req,bytetograb_srv_server_req,dataType_srv_server_res,dataName_srv_server_res,datagrab_srv_server_res,NofData_srv_server_res,datatypeProtocol_srv_server_res,bytetograb_srv_server_res,timeOut_srv_server = setup_srv_server_protocol()
    Idaction_client,nameaction_client,interfaceaction_client,dataType_action_client_req,dataName_action_client_req,datagrab_action_client_req,NofData_action_client_req,datatypeProtocol_action_client_req,bytetograb_action_client_req,dataType_action_client_res,dataName_action_client_res,datagrab_action_client_res,NofData_action_client_res,datatypeProtocol_action_client_res,bytetograb_action_client_res,dataType_action_client_feed,dataName_action_client_feed,datagrab_action_client_feed,NofData_action_client_feed,datatypeProtocol_action_client_feed,bytetograb_action_client_feed,timeOut_action_client = setup_action_client_protocol()
    Idaction_server,nameaction_server,interfaceaction_server,dataType_action_server_req,dataName_action_server_req,datagrab_action_server_req,NofData_action_server_req,datatypeProtocol_action_server_req,bytetograb_action_server_req,dataType_action_server_res,dataName_action_server_res,datagrab_action_server_res,NofData_action_server_res,datatypeProtocol_action_server_res,bytetograb_action_server_res,dataType_action_server_feed,dataName_action_server_feed,datagrab_action_server_feed,NofData_action_server_feed,datatypeProtocol_action_server_feed,bytetograb_action_server_feed,timeOut_action_server = setup_action_server_protocol()
    r_pipe=0
    # gen Id
    Idmcu = 1
    OnIdsrv=0
    OnMode=0
    OnIdmsg=0
    OnIdaction=0
    Ongrab=[]
    Ontype=[]
    OnNofdata=[]
    OntypeIndex=0
    OntypeProtocol=[]
    OnbyteTograb=[]
    while(1):
        try:
            if(Indexpre_value != Obj_uart.index.value):  # state machine
                # print(Obj_uart.Buff[Indexpre_value])


                if(state==0 and Obj_uart.Buff[Indexpre_value] == 73 ):
                    state=1
                elif(state==1 and Obj_uart.Buff[Indexpre_value]  == 109 ):
                    state=2
                elif(state==2 and Obj_uart.Buff[Indexpre_value] == 64 ):
                    state=3
                elif(state==3 and Obj_uart.Buff[Indexpre_value] == 99 ):
                    # print("Done check Start")
                    state=4
                elif(state==4):  # signature
                    # print("Idmcu=",Idmcu)
                    if((ModeEx ==0 )and (int( (Obj_uart.Buff[Indexpre_value] ))&0b11110000 )>>4 == Idmcu  and int(Obj_uart.Buff[Indexpre_value])&0b1111 == 4  ):
                        OnMode=4
                        crcc.resetCRC()
                        # print("Handshaking Complete Pub.")
                        state=5
                    elif((ModeEx==1 )and (int( (Obj_uart.Buff[Indexpre_value] ))&0b11110000 )>>4 == Idmcu  and int(Obj_uart.Buff[Indexpre_value])&0b1111 == 11 ):
                        OnMode=11
                        crcc.resetCRC()
                        # print("Handshaking Complete Srv client req.")
                        state=5
                    elif((ModeEx==2 )and (int( (Obj_uart.Buff[Indexpre_value] ))&0b11110000 )>>4 == Idmcu  and int(Obj_uart.Buff[Indexpre_value])&0b1111 == 14 ):
                        OnMode=14
                        crcc.resetCRC()
                        # print("Handshaking Complete Srv server res.")
                        state=5  
                    elif((ModeEx==3 )and (int( (Obj_uart.Buff[Indexpre_value] ))&0b11110000 )>>4 == Idmcu  and int(Obj_uart.Buff[Indexpre_value])&0b1111 == 5 ):
                        OnMode=5
                        crcc.resetCRC()
                        # print("Handshaking Complete Action client req.")
                        state=5
                    elif((ModeEx==4 )and (int( (Obj_uart.Buff[Indexpre_value] ))&0b11110000 )>>4 == Idmcu  and int(Obj_uart.Buff[Indexpre_value])&0b1111 == 9 ):
                        OnMode=9
                        crcc.resetCRC()
                        # print("Handshaking Complete Action server feed.")
                        state=5
                    elif((ModeEx==4 )and (int( (Obj_uart.Buff[Indexpre_value] ))&0b11110000 )>>4 == Idmcu  and int(Obj_uart.Buff[Indexpre_value])&0b1111 == 10 ):
                        OnMode=10
                        crcc.resetCRC()
                        # print("Handshaking Complete Action server res.")
                        state=5
                    else:
                        # print("Fail handshake")
                        state=0
                elif(state==5):   # On id msg xxx
                    if(OnMode==4): # mode pub
                        for i in range (0,len(Idmsg)):
                            if(Obj_uart.Buff[Indexpre_value] == Idmsg[i]):
                                # print(Idmsg)
                                # print(dataType)
                                # print(datagrab)
                                OnIdmsg=Idmsg[i]
                                Ongrab=datagrab[i].copy()
                                Ontype=dataType[i].copy()
                                OnNofdata=NofData[i].copy()
                                OntypeProtocol=datatypeProtocol[i].copy()
                                OntypeIndex=-1
                                OnbyteTograb=byteTograb[i].copy()
                                # print("Ongrab",Ongrab)
                                # print("Ontype",Ontype)
                                # print("OnNof data",OnNofdata)
                                # print("OnProtocol",OntypeProtocol)
                                # print("OnbyteTograb",OnbyteTograb)
                                state=6
                                break
                            else:
                                state=0
                    elif(OnMode==11): # mode service client req
                        for i in range (0,len(Idsrv_client)):
                            # print(Obj_uart.Buff[Indexpre_value] , Idsrv[i])
                            if(Obj_uart.Buff[Indexpre_value] == Idsrv_client[i]):
                                OnIdsrv=Idsrv_client[i]
                                Ongrab=datagrab_srv_client_req[i].copy()
                                Ontype=dataType_srv_client_req[i].copy()
                                OnNofdata=NofData_srv_client_req[i].copy()
                                OntypeProtocol=datatypeProtocol_srv_client_req[i].copy()
                                # print(OntypeProtocol)
                                OntypeIndex=-1
                                OnbyteTograb=bytetograb_srv_client_req[i].copy()
                                state=6
                                break
                            else:
                                state=0
                    elif(OnMode==14): # mode service server wait response
                        for i in range (0,len(Idsrv_server)):
                            # print(Obj_uart.Buff[Indexpre_value] , Idsrv[i])
                            if(Obj_uart.Buff[Indexpre_value] == Idsrv_server[i] == checkIdOn):
                                OnIdsrv=Idsrv_server[i]
                                Ongrab=datagrab_srv_server_res[i].copy()
                                Ontype=dataType_srv_server_res[i].copy()
                                OnNofdata=NofData_srv_server_res[i].copy()
                                OntypeProtocol=datatypeProtocol_srv_server_res[i].copy()
                                # print(OntypeProtocol)
                                OntypeIndex=-1
                                OnbyteTograb=bytetograb_srv_server_res[i].copy()
                                state=6
                                break
                            else:
                                state=0
                    elif(OnMode==5): # mode action client req
                        for i in range (0,len(Idaction_client)):
                            # print(Obj_uart.Buff[Indexpre_value] , Idsrv[i])
                            if(Obj_uart.Buff[Indexpre_value] == Idaction_client[i]):
                                OnIdaction=Idaction_client[i]
                                Ongrab=datagrab_action_client_req[i].copy()
                                Ontype=dataType_action_client_req[i].copy()
                                OnNofdata=NofData_action_client_req[i].copy()
                                OntypeProtocol=datatypeProtocol_action_client_req[i].copy()
                                # print(OntypeProtocol)
                                OntypeIndex=-1
                                OnbyteTograb=bytetograb_action_client_req[i].copy()
                                state=6
                                break
                            else:
                                state=0
                    elif(OnMode==9): # mode action server feed
                        for i in range (0,len(Idaction_server)):
                            if(Obj_uart.Buff[Indexpre_value] == Idaction_server[i] == checkIdOn):
                                OnIdaction=Idaction_server[i]
                                Ongrab=datagrab_action_server_feed[i].copy()
                                Ontype=dataType_action_server_feed[i].copy()
                                OnNofdata=NofData_action_server_feed[i].copy()
                                OntypeProtocol=datatypeProtocol_action_server_feed[i].copy()
                                # print(OntypeProtocol)
                                OntypeIndex=-1
                                OnbyteTograb=bytetograb_action_server_feed[i].copy()
                                state=6
                                break
                            else:
                                state=0
                    elif(OnMode==10): # mode action server res
                        for i in range (0,len(Idaction_server)):
                            if(Obj_uart.Buff[Indexpre_value] == Idaction_server[i] == checkIdOn):
                                OnIdaction=Idaction_server[i]
                                Ongrab=datagrab_action_server_res[i].copy()
                                Ontype=dataType_action_server_res[i].copy()
                                OnNofdata=NofData_action_server_res[i].copy()
                                OntypeProtocol=datatypeProtocol_action_server_res[i].copy()
                                # print(OntypeProtocol)
                                OntypeIndex=-1
                                OnbyteTograb=bytetograb_action_server_res[i].copy()
                                state=6
                                break
                            else:
                                state=0
                    else:
                        state=0
                elif(state==6):

                    OntypeIndex=OntypeIndex+1
                    # print("ONTYPEEEINDEX",OntypeIndex)
                    # print("dddd",Obj_uart.Buff[Indexpre_value] ,OntypeProtocol[OntypeIndex])

                    if( Obj_uart.Buff[Indexpre_value] == OntypeProtocol[OntypeIndex]):
                        if(OntypeProtocol[OntypeIndex]==242 ):
                            INDEXstore=OntypeIndex
                            GETNround=OnNofdata[OntypeIndex]
                            PASSNround=0
                            TEMPstring=""
                            state=111  # getString
                        elif(OntypeProtocol[OntypeIndex]==243):
                            INDEXstore=OntypeIndex
                            GETNround=OnNofdata[OntypeIndex]
                            PASSNround=0
                            TEMPstring=""
                            state=110  # check N of data is correct
                        elif(OntypeProtocol[OntypeIndex]==88):
                            state=120  # get 1 Bool
                        elif(OntypeProtocol[OntypeIndex]==89):
                            GETNbool=OnNofdata[OntypeIndex]
                            GETNround=math.ceil(OnNofdata[OntypeIndex]/8.00)
                            COUNTbuffin=0
                            TEMPbool=[]
                            # print("GETNbool=",GETNbool)
                            # print("Bool round=",GETNround)
                            state=129  # get N Bool
                        elif(OntypeProtocol[OntypeIndex]== 8 or OntypeProtocol[OntypeIndex]==16 or OntypeProtocol[OntypeIndex]==32 or OntypeProtocol[OntypeIndex]==64 or OntypeProtocol[OntypeIndex]==18 or OntypeProtocol[OntypeIndex]==116 or OntypeProtocol[OntypeIndex]==132 or OntypeProtocol[OntypeIndex]==164 or OntypeProtocol[OntypeIndex]==111 or OntypeProtocol[OntypeIndex]==222 ):
                            INDEXstore=OntypeIndex
                            GETNround=OnNofdata[OntypeIndex]
                            PASSNround=0
                            COUNTbuffin=0
                            TEMPbuff=[]
                            state=200  # get1ofdata
                        elif(OntypeProtocol[OntypeIndex]== 9 or OntypeProtocol[OntypeIndex]==17 or OntypeProtocol[OntypeIndex]==33 or OntypeProtocol[OntypeIndex]==65 or OntypeProtocol[OntypeIndex]==19 or OntypeProtocol[OntypeIndex]==117 or OntypeProtocol[OntypeIndex]==133 or OntypeProtocol[OntypeIndex]==165 or OntypeProtocol[OntypeIndex]==112 or OntypeProtocol[OntypeIndex]==223 ):
                            INDEXstore=OntypeIndex
                            GETNround=OnNofdata[OntypeIndex]
                            PASSNround=0
                            COUNTbuffin=0
                            TEMPbuff=[]
                            state=201  # getNofdata
                        elif(OntypeProtocol[OntypeIndex]==254): # Empty
                            state=44 # main check stop
                        else:
                            state=0
                    else:
                        state=0

                elif(state==129):
                    if(Obj_uart.Buff[Indexpre_value]==GETNbool):
                        state=130
                    else:
                        state=0
                elif(state==130):
                    TEMPbool.append(int(Obj_uart.Buff[Indexpre_value]))
                    COUNTbuffin=COUNTbuffin+1
                    if(COUNTbuffin==GETNround):
                        for i in range(0,COUNTbuffin):
                            for j in range(0,GETNbool):
                                boolnow = (int(TEMPbool[i]) >> (j%8) )& 0x01
                                # print("boolnow=",boolnow,TEMPbool[i])
                                if(boolnow==1):
                                    Ongrab[OntypeIndex][j]= True
                                else:
                                    Ongrab[OntypeIndex][j]= False


                        state=44
                    else:
                        state=130



                elif(state==120):
                    print(Obj_uart.Buff[Indexpre_value])
                    if(Obj_uart.Buff[Indexpre_value]==250):
                        state=121 # to check true and continue
                    elif(Obj_uart.Buff[Indexpre_value]==47):
                        state=122 # to check false and continue
                    elif(Obj_uart.Buff[Indexpre_value]==254):
                        state=123 # to check true and stop
                    elif(Obj_uart.Buff[Indexpre_value]==127):
                        state=124 # to check false and stop
                    else:
                        state=0
                elif(state==121):
                    if(Obj_uart.Buff[Indexpre_value]==250):
                        Ongrab[OntypeIndex]=True
                        # print(Ongrab)
                        state=6 # confirm continue
                    else:
                        state=0
                elif(state==122):
                    if(Obj_uart.Buff[Indexpre_value]==47):
                        Ongrab[OntypeIndex]=False
                        # print(Ongrab)
                        state=6 # confirm continue
                    else:
                        state=0
                elif(state==123):
                    if(Obj_uart.Buff[Indexpre_value]==254):
                        Ongrab[OntypeIndex]=True
                        # print(Ongrab)
                        state=426 # confirm stop
                    else:
                        state=0
                elif(state==124):
                    if(Obj_uart.Buff[Indexpre_value]==127):
                        Ongrab[OntypeIndex]=False
                        # print(Ongrab)
                        state=426 # confirm stop
                    else:
                        state=0



                elif(state==201):
                    if(Obj_uart.Buff[Indexpre_value]==GETNround): # is correct N of data
                        state=200
                    else:
                        state=0

                elif(state==200):
                    TEMPbuff.append(int(Obj_uart.Buff[Indexpre_value]))
                    COUNTbuffin=COUNTbuffin+1

                    if(COUNTbuffin==OnbyteTograb[OntypeIndex]):
                        if(GETNround==1):
                            # print(TEMPbuff)
                            Ongrab[OntypeIndex]=bufferToType(TEMPbuff,Ontype[OntypeIndex])
                        else:
                            Ongrab[OntypeIndex][PASSNround]= bufferToType(TEMPbuff,Ontype[OntypeIndex])
                        TEMPbuff=[]
                        COUNTbuffin=0
                        PASSNround=PASSNround+1



                    if(PASSNround==GETNround):
                        state=44 # main check
                    else:
                        state=200


                elif(state==110):
                    if(Obj_uart.Buff[Indexpre_value]==GETNround): # is correct N of data
                        state=111
                    else:
                        state=0

                elif(state==111): # getString
                    if(Obj_uart.Buff[Indexpre_value]==42):
                        state=112   # check 126 for confirm end of text
                    else:
                        bytes_val = bytearray([int(Obj_uart.Buff[Indexpre_value])])
                        TEMPstring=TEMPstring+str(bytes_val ,'utf-8')



                elif(state==112): # check 126 for confirm end of string
                    if(Obj_uart.Buff[Indexpre_value]==126):
                        if(GETNround==1):
                            Ongrab[OntypeIndex]=TEMPstring
                        else:
                            Ongrab[OntypeIndex][PASSNround]=TEMPstring
                        PASSNround=PASSNround+1
                        if(PASSNround==GETNround):
                            state=44 # check main continue or stop
                        else:
                            state=111 # Get moreString
                    else:
                        state=0



                elif(state==44): # main check continue or stop
                    if(Obj_uart.Buff[Indexpre_value]==42):
                        state=45
                    elif(Obj_uart.Buff[Indexpre_value]==126):
                        state=46
                    else:
                        state=0

                elif(state==45): # confirm continue
                    if(Obj_uart.Buff[Indexpre_value]==42):
                        # print(Ongrab)
                        state=6
                    else:
                        state=0
                elif(state==46): # confirm stop
                    if(Obj_uart.Buff[Indexpre_value]==126):
                        # print("GET IT ALL",Ongrab)
                        state=426 # check crc
                    else:
                        state=0

                elif(state==426):
                    if(crcc.FlagCheck(int(Obj_uart.Buff[Indexpre_value]))):  # Done protocol
                        # print(crcc.result())
                        if(OnMode==4):   # protocol publish
                            # print("Pubbbbbbbb")
                            Buff_test.append(OnIdmsg)
                            state=0
                        elif(OnMode==11): # protocol service client request
                            print("Srv client call")
                            Buff_test.append(OnIdsrv)
                            state=0
                        elif(OnMode==5):  # protocol action client request
                            print("Action client call")
                            Buff_test.append(OnIdaction)
                            state=0
                        else:
                            state=0
                    else:
                        state=0




                crcc.update(int(Indexpre_value))
                Indexpre_value=(Indexpre_value+1)%1000

            if(ModeEx==1 or ModeEx==3):
                if(pipe[r_pipe]!= 888 and not pipe[r_pipe].is_alive()):
                    pipe[r_pipe].join()
                    pipe[r_pipe]=888
                    if(ModeEx==1):
                        print("pipe_srv_client["+str(r_pipe)+"].join Done")
                    if(ModeEx==3):
                        print("pipe_action_client["+str(r_pipe)+"].join Done")
                r_pipe=(r_pipe+1)%16
            
        except:
            print("Protocol recovery")

def timek(buff_test_pub,buff_test_srv_client_call,buff_test_action_call,flag_time_out):

    starttime= time.time()
    print("TIMER Start")
    while(1):
        if(time.time()-starttime>= input.scantime):
            flag_time_out.value = 1
            print("scan time pass ",input.scantime," s.")
            break
def remove_duplicate(input_list):
    unique_set = set(input_list)
    unique_list = list(unique_set)
    return unique_list      
        
def check(Buff_test_pub,Buff_test_srv,Buff_test_action):
    Buff_test_pub=remove_duplicate(Buff_test_pub)
    Buff_test_srv=remove_duplicate(Buff_test_srv)
    Buff_test_action=remove_duplicate(Buff_test_action)
    Idmsg,nametopic,interfacetopic,dataType,dataName,datagrab,NofData,datatypeProtocol,byteTograb=setup_var_protocol() # get variable from yaml
    Idsrv_client,namesrv_client,interfacesrv_client,dataType_srv_client_req,dataName_srv_client_req,datagrab_srv_client_req,NofData_srv_client_req,datatypeProtocol_srv_client_req,bytetograb_srv_client_req,dataType_srv_client_res,dataName_srv_client_res,datagrab_srv_client_res,NofData_srv_client_res,datatypeProtocol_srv_client_res,bytetograb_srv_client_res,timeOut_srv_client = setup_srv_protocol()
    Idaction_client,nameaction_client,interfaceaction_client,dataType_action_client_req,dataName_action_client_req,datagrab_action_client_req,NofData_action_client_req,datatypeProtocol_action_client_req,bytetograb_action_client_req,dataType_action_client_res,dataName_action_client_res,datagrab_action_client_res,NofData_action_client_res,datatypeProtocol_action_client_res,bytetograb_action_client_res,dataType_action_client_feed,dataName_action_client_feed,datagrab_action_client_feed,NofData_action_client_feed,datatypeProtocol_action_client_feed,bytetograb_action_client_feed,timeOut_action_client = setup_action_client_protocol()
    
    if(len(Idmsg)>0):
        c = np.zeros(len(Idmsg),dtype=bool)
        for i in range(0,len(Idmsg)):
            for j in range(0,len(Buff_test_pub)):
                if(Idmsg[i]==Buff_test_pub[j]):
                    c[i]=True
        print()
        for i in range(0,len(Idmsg)):
            if(c[i]):
                print("Check Protocol publish topic : "+nametopic[i] + " >>>>  Pass")
            else:
                print("Check Protocol publish topic : "+nametopic[i] + " >>>>  Fail")
  
    if(len(Idsrv_client)>0):
        c = np.zeros(len(Idsrv_client),dtype=bool)
        for i in range(0,len(Idsrv_client)):
            for j in range(0,len(Buff_test_srv)):
                if(Idsrv_client[i]==Buff_test_srv[j]):
                    c[i]=True
        for i in range(0,len(Idmsg)):
            if(c[i]):
                print("Check Protocol service client request : "+namesrv_client[i] + " >>>>  Pass")
            else:
                print("Check Protocol service client request : "+namesrv_client[i] + " >>>>  Fail")

    if(len(Idaction_client)>0):
        c = np.zeros(len(Idaction_client),dtype=bool)
        for i in range(0,len(Idaction_client)):
            for j in range(0,len(Buff_test_action)):
                if(Idaction_client[i]==Buff_test_action[j]):
                    c[i]=True
        
        for i in range(0,len(Idaction_client)):
            if(c[i]):
                print("Check Protocol action client send_goal : "+nametopic[i] + " >>>>  Pass")
            else:
                print("Check Protocol action client send_goal : "+nametopic[i] + " >>>>  Fail")



def main():
    try:
        if(checkArgs()):
            Obj_uart = Uart(mp)    # create Uart object
            mana = mp.Manager()
            Buff_test_pub = mana.list()
            Buff_test_srv = mana.list()
            Buff_test_action = mana.list()
            flagtime_out =  mp.Value('i',0)
            if(Obj_uart.ser!=0):
                p  = mp.Process(target=Receive_uart,args=(Obj_uart,))
                p2 = mp.Process(target=Transmit_uart,args=(Obj_uart,))
                p3 = mp.Process(target=Protocol_XicroToRos_spin,args=(Obj_uart,0,888,888,888,888,Buff_test_pub,))   # Spin test pub
                p4 = mp.Process(target=Protocol_XicroToRos_spin,args=(Obj_uart,1,888,888,888,888,Buff_test_srv,))   # Spin srv Client
                p5 = mp.Process(target=Protocol_XicroToRos_spin,args=(Obj_uart,3,888,888,888,888,Buff_test_action,))   # Spin action Client
                p6 = mp.Process(target=timek,args=(Buff_test_pub,Buff_test_srv,Buff_test_action,flagtime_out,))

                p.start()
                p2.start()
                p3.start()
                p4.start()
                p5.start()
                p6.start()

                while(1):
                    if(flagtime_out.value):
                        p.kill()
                        p2.kill()
                        p3.kill()
                        p4.kill()
                        p5.kill()
                        p6.kill()
                        break
                check(Buff_test_pub,Buff_test_srv,Buff_test_action)           
                

            else:
                print("Connect to mcu fail.")
            print("*******Check protocol Done*******")
    except KeyboardInterrupt:
        if(Obj_uart.ser!=0):
            p.kill()
            p2.kill()
            p3.kill()
            p4.kill()
            p5.kill()
            p6.kill()

    finally:
        print("\n\nXicro all process is shutdown.")
    
if __name__ == '__main__':
    main()