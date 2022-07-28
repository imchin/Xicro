#!/usr/bin/python3
import os
import re
import yaml

def get_params(q):
    try:
        path = os.path.join(os.path.expanduser('~'), 'xicro_ws', 'src','xicro_pkg','config', 'setup_xicro.yaml')
        with open(path,'r') as f:
            yml_dict = yaml.safe_load(f)
            ans = yml_dict.get(q)
        print('Get '+q+' Done.')
        return  ans
    except:
        print('Get '+q+' Fail'+'Something went wrong when opening YAML.')


    return 0
def mkdir():
    path="Fail"
    try:
        path = get_params("path_arduino")
        ns= get_params("Namespace")
        id = get_params("Idmcu")
        path=path+"/libraries/Xicro_"+ns+"_ID_"+str(id)
        path = os.path.join(os.path.expanduser('~'), path)
        os.mkdir(path)
        print("make folder Done path: "+path)
        return path
    except:
        print("path: "+path)
        return path
def checkNofdata(dataType):
    S=dataType.find("[")
    F= dataType.find("]")
    if(S!=-1 and F!=-1):
        return int(dataType[S+1:F])
    else:
        return 1
   
def setupvarforcreatelibPub():
    id_mcu=0
    id_topic=[]
    nameofTopic=[]
    interfacefile=[]
    dataType=[]
    dataName=[]
    NofData=[]
    try:
        id_mcu=get_params("Idmcu")
        Setup_Pub=get_params("Setup_Publisher")
        for i in range(0,len(Setup_Pub)):
            id_topic.append(Setup_Pub[i][0])
            nameofTopic.append(Setup_Pub[i][1])
            interfacefile.append(Setup_Pub[i][2])
        for i in range (0,len(interfacefile)):
            tempType=[]
            tempName=[]
            tempdatagrab=[]
            tempN=[]
            path = os.path.join(os.path.expanduser('~'), 'xicro_ws', 'src','xicro_interfaces','msg',  interfacefile[i])
            msg = open(path, 'r').read().splitlines()
            for j in range(0,len(msg)):
                line=msg[j].split()
                tempType.append(line[0])
                tempName.append(line[1])
                tempN.append(checkNofdata(line[0]))
                tempdatagrab.append(0)
            NofData.append(tempN)
            dataType.append(tempType)
            dataName.append(tempName)
        
    except:
        print("Error setup variable.")
    return id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData

def setupvarforcreatelibSub():
    id_mcu=0
    id_topic=[]
    nameofTopic=[]
    interfacefile=[]
    dataType=[]
    dataName=[]
    NofData=[]
    try:
        id_mcu=get_params("Idmcu")
        Setup_Sub=get_params("Setup_Subscriber")
        for i in range(0,len(Setup_Sub)):
            id_topic.append(Setup_Sub[i][0])
            nameofTopic.append(Setup_Sub[i][1])
            interfacefile.append(Setup_Sub[i][2])

        for i in range (0,len(interfacefile)):
            tempType=[]
            tempName=[]
            tempdatagrab=[]
            tempN=[]
            path = os.path.join(os.path.expanduser('~'), 'xicro_ws', 'src','xicro_interfaces','msg',  interfacefile[i])
            msg = open(path, 'r').read().splitlines()
            for j in range(0,len(msg)):
                line=msg[j].split()
                tempType.append(line[0])
                tempName.append(line[1]),NofData
                tempdatagrab.append(0)
                tempN.append(checkNofdata(line[0]))
            NofData.append(tempN)
            dataType.append(tempType)
            dataName.append(tempName)
           

    except:
        print("Error setup variable.")

    return id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData


def create_hstruct(fw):
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData=setupvarforcreatelibSub()
    public_struct=[]
    fw.write("\r\r\r        // gen\r")
    for i in range (0,len(dataType)):
        q="        struct{\r"
        for j in range (0,len(dataType[i])):
            if(NofData[i][j]==1):
                if(convertdatatype(dataType[i][j])!="String"):
                    q=q+"            "+convertdatatype(dataType[i][j])+" "+dataName[i][j]+"= 0;\r"
                else:
                    q=q+"            "+convertdatatype(dataType[i][j])+" "+dataName[i][j]+"= \"\";\r"
            else:
                if(convertdatatype(dataType[i][j])!="String"):
                    q=q+"            "+convertdatatype(dataType[i][j])+" "+dataName[i][j]+"["+str(NofData[i][j])+"]={0};\r"
                else:
                    q=q+"            "+convertdatatype(dataType[i][j])+" "+dataName[i][j]+"["+str(NofData[i][j])+"]={"
                    for k in range(0,NofData[i][j]-1):
                        q=q+"\"\","
                    q=q+"\"\"};\r"
                            

        q=q+"        } Sub_"+nameofTopic[i]+";\r\r"
        public_struct.append(q)
        fw.write(q)
    return public_struct
def getMaxNdata(q):
    w=0
    for i in range (0,len(q)):
        if(len(q[i])>=w):
            w=len(q[i])
    return w
def getMaxofArray(q):
    w=0
    for i in range(0,len(q)):
        for j in range(0,len(q[i])):
            if(q[i][j]>w):
                w=q[i][j]
    return w
def Arraymaptype(dataType):
    q="{"
    for i in range(len(dataType)):
        q=q+"{"
        for j in range(len(dataType[i])):
            if(j<len(dataType[i])-1):
                q=q+typetoProtocol(dataType[i][j])+","
            else:
                q=q+typetoProtocol(dataType[i][j])
        if(i<len(dataType)-1):
            q=q+"},"
        else:
            q=q+"}"
    q=q+"};\r"
    return q
def typetoProtocol(typee):
    t=0
    flag=0
    if(typee.find("[")!=-1):
        typee=typee[0:typee.find("[")]
        flag=1
    if(typee=="uint8"):
        t=8
    elif(typee=="uint16"):
        t=16

    elif(typee=="uint32"):
        t=32
    elif(typee=="uint64"):
        t=64
    elif(typee=="int8"):
        t=18
    elif(typee=="int16"):
        t=116
    elif(typee=="int32"):
        t=132
    elif(typee=="int64"):
        t=164
    elif(typee=="float32" ):
        t=111
    elif(typee=="string" ):
        t=242
    elif(typee=="bool" ):
        t=88
    if(flag):
        return str(t+1)
    else:
        return str(t)
    
def ArraytotalVar(q):
    w="{"
    for i in range (0,len(q)):
        if(i<len(q)-1):
            w=w+str(len(q[i]))+","
        else:
            w=w+str(len(q[i]))
    w=w+"};\r"
    return w
def gen_privateStruct(fw):
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,Nofdata=setupvarforcreatelibSub()
    print(Nofdata)
    fw.write("\r\r\r        // gen\r")
    q="        void* _nonverify["+str(len(id_topic))+"]["+str(getMaxNdata(dataType))+"]["+str(getMaxofArray(Nofdata))+"];\r"
    q=q+"        void* _verify["+str(len(id_topic))+"]["+str(getMaxNdata(dataType))+"]["+str(getMaxofArray(Nofdata))+"];\r"
    q=q+"        uint8_t _Idtopic_sub["+str(len(id_topic))+"]={"
    for i in range (0,len(id_topic)):
        if(i<len(id_topic)-1):
            q=q+str(id_topic[i])+","
        else:
            q=q+str(id_topic[i])
    q=q+"};\r"
    q=q+"        uint8_t _TopicType["+str(len(id_topic))+"]["+str(getMaxNdata(dataType))+"]="+Arraymaptype(dataType)
    q=q+"        uint8_t _Totalvar["+str(len(id_topic))+"]="+ArraytotalVar(dataType)
    q=q+"        uint8_t _Nofdata["+str(len(id_topic))+"]["+str(getMaxNdata(dataType))+"]="+str(Nofdata).replace("[","{").replace("]","}")+";"
    fw.write(q)
    return 1
def publicStructToprivateStruct(fw,q):
    w=""
    tt=1
    fw.write("\r\r\r        // gen\r")
    for i in range(0,len(q)):
        e=""
        for j in range(0,len(q[i])):
            if(q[i][j]=="}" and q[i][j+1]!=";"):
                e=e+"}_"
                tt=0
            elif(tt):
                e=e+q[i][j]
            else:
                tt=1
        w=w+e
    fw.write(w)
    return 1
def create_hFile(listVoid,Idmcu):
    try:
        path = mkdir()
        path = path +"/Xicro_"+get_params("Namespace")+"_ID_"+str(Idmcu)+".h"
       
        fw  = open(path, "w+")
        pathr= os.path.join(os.path.expanduser('~'), 'xicro_ws', 'src','xicro_pkg','scripts', '.arduino_h_preSetup.txt')
        fr=open(pathr, 'r') 
        fw.write("// ***************************************************************************************************************************************************\r")
        fw.write("//      |              This script was auto-generated by generate_arduino_lib.py which received parameters from setup_xicro.yaml               |\r")
        fw.write("//      |                                         EDITING THIS FILE BY HAND IS NOT RECOMMENDED                                                 |\r")
        fw.write("// ***************************************************************************************************************************************************\r\r")
        public_struct=[]
        c=0
        for line in fr:
            c=c+1
            if(c==7):
                try:
                    fw.write("\r\r\r        // gen\r")
                    for i in range(0,len(listVoid)):
                        fw.write(listVoid[i])
                        fw.write("\n")
                    print("gen voidPub Done")
                    public_struct=create_hstruct(fw)
                    print("gen public_struct Done")
                except:
                    print("gen public_struct or voidPub Fail.")
            elif(c==55):
                try:
                    gen_privateStruct(fw)
                    publicStructToprivateStruct(fw,public_struct)
                    print("gen private_struct Done")
                except:
                    print("gen private_struct Fail")
            elif(c==12):
                fw.write("        uint8_t _Idmcu=" +str(Idmcu)+";\n\r")
            else:
                fw.write(line)
        print(".h Done.")
    except:
       
        print(".h Fail.")
    return 0

def genPointer(fw):
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,Nofdata=setupvarforcreatelibSub()
    fw.write("\r    // gen\r")
    q=""
    w=""
    for i in range(0,len(id_topic)):
        for j in range(0,len(dataName[i])):
            for k in range(0,Nofdata[i][j]):
                if(Nofdata[i][j]==1):
                    q=q+"    _nonverify["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Sub_"+nameofTopic[i]+"."+dataName[i][j]+";\r"
                    w=w+"    _verify["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Sub_"+nameofTopic[i]+"."+dataName[i][j]+";\r"
                else:
                    q=q+"    _nonverify["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Sub_"+nameofTopic[i]+"."+dataName[i][j]+"["+str(k) +"];\r"
                    w=w+"    _verify["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Sub_"+nameofTopic[i]+"."+dataName[i][j]+"["+str(k) +"];\r"
    q=q+"\r\r"
    q=q+w
    fw.write(q)
    fw.write("\r\r\r")
    return 1

def create_cppFile(listVoid,id_mcu,id_topic,dataType,dataName,Nofdata):
    try:
        # print(listVoid,id_mcu,id_topic,dataType,dataName,Nofdata)
        path = mkdir()
        path = path +"/Xicro_"+get_params("Namespace")+"_ID_"+str(id_mcu)+".cpp"
        fw  = open(path, "w+") 
        pathr= os.path.join(os.path.expanduser('~'), 'xicro_ws', 'src','xicro_pkg','scripts', '.arduino_cpp_preSetup.txt')
        fr=open(pathr, 'r') 
        fw.write("// ***************************************************************************************************************************************************\r")
        fw.write("//      |              This script was auto-generated by generate_arduino_lib.py which received parameters from setup_xicro.yaml               |\r")
        fw.write("//      |                                         EDITING THIS FILE BY HAND IS NOT RECOMMENDED                                                 |\r")
        fw.write("// ***************************************************************************************************************************************************\r\r")
        fw.write("\r\n#include \""+"Xicro_"+get_params("Namespace")+"_ID_"+str(id_mcu)+".h\"\r\n")
        c=0
        for line in fr:        
            c=c+1
            if(c==366): 
                try:
                    fw.write("\r\r\r// gen\r")
                    for i in range(0,len(listVoid)):
                        # print(listVoid[i][8:12])
                        fw.write(listVoid[i][8:12]+" Xicro::"+listVoid[i][13:len(listVoid[i])-1])
                        fw.write(("{\n"))
                        fw.write("    _crc=0;\r")
                        fw.write("    _Sendstart();\n")
                        fw.write("    _SendSignature("+str(id_mcu)+",4);\n")
                        fw.write("    _SendIdTopic("+str(id_topic[i])+");\n")
                        for j in range(0,len(dataType[i])):
                            cond=j<len(dataType[i])-1 #check flag continue or stop
                            fw.write(typetoVoid(dataType[i][j],dataName[i][j],Nofdata[i][j],cond))
                            if(dataType[i][j]=="bool" and Nofdata[i][j]==1 ):
                                fw.write("// auto by 1 bool\n")
                            elif(cond):
                                fw.write("    _Sendcontinue();\n")
                            else:
                                fw.write("    _Sendstop();\n")
                        fw.write("    _Sendcrc();\r")
                        fw.write("}\n")
                    print("gen functionPub Done.")
                except:
                    print("gen functionPub Fail.")
            elif(c==9):
                try:
                    genPointer(fw)
                    print("gen pointer Done.")
                except:
                    print("gen pointer Fail.")
            else:
                fw.write(line)
        fw.close
        print(".cpp Done.")
    except:
        print(".cpp Fail.")
    return 0
def convertdatatype(strr):
    if(strr.find("[")!=-1):
        strr=strr[0:strr.find("[")]
    if(strr=="uint8"or strr=="uint16" or strr=="uint32" or strr=="uint64" or strr=="int8"or strr=="int16" or strr=="int32" or strr=="int64" ):
        return (strr+"_t")
    elif(strr=="float32" or strr=="float64" ):
        return "float"
    elif(strr=="string"):
        return "String"
    elif(strr== "bool"):
        return "bool"
    else:
        return "ERRORTYPE"

    


    
def typetoVoid(typee,namee,Nofdata,cond):
    if(typee.find("[")!=-1):
        typee=typee[0:typee.find("[")]
    if(typee=="uint8"and Nofdata==1):
        return  "    _SendUint8((uint8_t*)&"+namee+","+ str(Nofdata)+");\n"
    elif(typee=="uint8"and Nofdata!=1):
        return  "    _SendUint8("+namee+","+ str(Nofdata)+");\n"
    elif(typee=="uint16"and Nofdata==1):
        return  "    _SendUint16((uint16_t*)&"+namee+","+ str(Nofdata)+");\n"
    elif(typee=="uint16"and Nofdata!=1):
        return  "    _SendUint16("+namee+","+ str(Nofdata)+");\n"    
    elif(typee=="uint32"and Nofdata==1):
        return  "    _SendUint32((uint32_t*)&"+namee+","+ str(Nofdata)+");\n"
    elif(typee=="uint32"and Nofdata!=1):
        return  "    _SendUint32("+namee+","+ str(Nofdata)+");\n"
    elif(typee=="uint64"and Nofdata==1):
        return  "    _SendUint64((uint64_t*)&"+namee+","+ str(Nofdata)+");\n"
    elif(typee=="uint64"and Nofdata!=1):
        return  "    _SendUint64("+namee+","+ str(Nofdata)+");\n"
    elif(typee=="int8"and Nofdata==1):
        return  "    _SendInt8((int8_t*)&"+namee+","+ str(Nofdata)+");\n"
    elif(typee=="int8"and Nofdata!=1):
        return  "    _SendInt8("+namee+","+ str(Nofdata)+");\n"    
    elif(typee=="int16"and Nofdata==1):
        return  "    _SendInt16((int16_t*)&"+namee+","+ str(Nofdata)+");\n"
    elif(typee=="int16"and Nofdata!=1):
        return  "    _SendInt16("+namee+","+ str(Nofdata)+");\n"   
    elif(typee=="int32"and Nofdata==1):
        return  "    _SendInt32((int32_t*)&"+namee+","+ str(Nofdata)+");\n"
    elif(typee=="int32"and Nofdata!=1):
        return  "    _SendInt32("+namee+","+ str(Nofdata)+");\n"
    elif(typee=="int64"and Nofdata==1):
        return  "    _SendInt64((int64_t*)&"+namee+","+ str(Nofdata)+");\n"
    elif(typee=="int64"and Nofdata!=1):
        return  "    _SendInt64("+namee+","+ str(Nofdata)+");\n"    
    elif(typee=="float32" and Nofdata==1):
        return  "    _SendFloat32((float*)&"+namee+","+ str(Nofdata)+");\n"
    elif(typee=="float32" and Nofdata!=1):
        return  "    _SendFloat32("+namee+","+ str(Nofdata)+");\n"    
    elif(typee=="string" and Nofdata==1):
        return  "    _SendString(&"+namee+","+ str(Nofdata)+");\n"
    elif(typee=="string" and Nofdata!=1):
        return  "    _SendString("+namee+","+ str(Nofdata)+");\n" 
    elif(typee=="bool" and Nofdata==1):
        return  "    _SendBool((bool*)&"+namee+","+ str(Nofdata)+","+str(int(cond))+");\n"
    elif(typee=="bool" and Nofdata!=1):
        return  "    _SendBool("+namee+","+ str(Nofdata)+","+str(int(cond))+");\n"
    else:

        print(typee)
        return "1"

def strVoid(nameofTopic,dataType,dataName,Nofdata):
    temp=[]
    for i in range(0,len(nameofTopic)):
        t="        "
        t=t+"void publish_"+nameofTopic[i]+"("
        for j in range(0,len(dataType[i])):
            t=t+convertdatatype(dataType[i][j])+" "
            if(Nofdata[i][j]!=1):
                t=t+"*"
            t=t+dataName[i][j]+" "
            if(j>=0 and j<len(dataType[i])-1):
                t=t+","
        t=t+");"
        temp.append(t)
    # print(temp)
    return temp

def gen():
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,Nofdata=setupvarforcreatelibPub()
    listVoid=strVoid(nameofTopic,dataType,dataName,Nofdata)
   
    
    create_hFile(listVoid,id_mcu)
    create_cppFile(listVoid,id_mcu,id_topic,dataType,dataName,Nofdata)
 


def main():
    try:
        gen()
        print("*******Create library arduino complete*******")
    except:
        print("*******Create library arduino failed*******")
if __name__ == '__main__':
    main()