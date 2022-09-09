#!/usr/bin/python3
import os
import sys
import yaml
from ament_index_python.packages import get_package_share_directory

def get_params(q):
    
    try:
        path = os.path.join(get_package_share_directory('xicro_pkg'),'config', 'setup_xicro.yaml')
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
        path = get_params("generate_library_Path")
        ns= get_params("Namespace")
        id = get_params("Idmcu")
        path=path+"/Xicro_"+ns+"_ID_"+str(id)
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

def checkSubmsg(typee):
    supporttypee=["int8","int16","int32","int64","uint8","uint16","uint32","uint64","bool","float32","float64","string"]
    ans=1
    for i in range(0,len(supporttypee)):
        if(typee.find(supporttypee[i])!= -1):
            ans=1
            break
        else:
            ans=0
    return ans

def expandSub(id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData):
    # print("Datatype :",dataType)
    # print("DataName :",dataName)
    # print("Nofdata :",NofData)
    # print("interfacefile :",interfacefile)

    for i in range(0,len(dataType)):
        for j in range(0,len(dataType[i])):
            if(checkSubmsg(dataType[i][j]) == 0):   
                path = os.path.join(get_package_share_directory(dataType[i][j].split("/")[0]),'msg', dataType[i][j].split("/")[1]+".msg")
                msg = open(path, 'r').read().splitlines()
                addtype=[]
                addName=[]
                Sname=dataName[i][j]
                for k in range(0,len(msg)):
                    line=msg[k].split()
                    if(len(line)!=0 and line[0]!="#" ):
                        addtype.append(line[0])
                        addName.append(line[1])
                for k in range(0,len(addName)):
                    addName[k]=Sname+"."+addName[k]     
                dataType[i][j]=addtype
                dataName[i][j]=addName
                # print(addtype,addName)
    TempType=[]
    TempName=[]
    for i in range(0,len(dataType)):  #delist
        q=[]
        w=[]
        for j in range(0,len(dataType[i])):
            if(type(dataType[i][j])==list):
                for k in range(0,len(dataType[i][j])):
                    q.append(dataType[i][j][k])
                    w.append(dataName[i][j][k])
            else:
                q.append(dataType[i][j])
                w.append(dataName[i][j])
        TempType.append(q)
        TempName.append(w)
    dataType=TempType.copy()
    dataName=TempName.copy()
    NofData=[]
    for i in range(0,len(dataType)): #check N of data
        q=[]
        for j in range(0,len(dataType[i])):
            q.append(checkNofdata(dataType[i][j]))
        NofData.append(q)

    for i in range(0,len(dataName)): #Rename . to _of_
        q=[]
        for j in range(0,len(dataName[i])):
            dataName[i][j]=dataName[i][j].replace(".","__of__")
    
    # print("Datatype :",dataType)
    # print("DataName :",dataName)
    # print("Nofdata :",NofData)
    return id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData
def setupvarforcreatelibPub():
    id_mcu=0
    id_topic=[]
    nameofTopic=[]
    interfacefile=[]
    interfacepkg=[]
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
            path = os.path.join(get_package_share_directory(interfacefile[i].split("/")[0]),'msg',  interfacefile[i].split("/")[1])
            print(path)
            msg = open(path, 'r').read().splitlines()
            for j in range(0,len(msg)):
                line=msg[j].split()
                if(len(line)!=0 and line[0]!="#" ):
                    tempType.append(line[0])
                    tempName.append(line[1])
                    tempN.append(checkNofdata(line[0]))
                    tempdatagrab.append(0)
                
            NofData.append(tempN)
            dataType.append(tempType)
            dataName.append(tempName)
        for i in range(0,10):
            id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData=expandSub(id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData)

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
            path = os.path.join(get_package_share_directory( interfacefile[i].split("/")[0]),'msg',  interfacefile[i].split("/")[1])
            msg = open(path, 'r').read().splitlines()
            for j in range(0,len(msg)):
                line=msg[j].split()
                if(len(line)!=0 and line[0]!="#" ):
                    tempType.append(line[0])
                    tempName.append(line[1]),NofData
                    tempdatagrab.append(0)
                    tempN.append(checkNofdata(line[0]))
            NofData.append(tempN)
            dataType.append(tempType)
            dataName.append(tempName)
        for i in range(0,10):
            id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData=expandSub(id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData)


    except:
        print("Error setup variable.")

    return id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData
def exStruct(st,an,i,nn,NN):
    j=0
    tempStructName=""
    tempStructName=an[i][0][len(an[i][0])-2]
    st="\r\r"+"        struct{\r" + st
    while(1):
        # print(an[i][j][len(an[i][j])-2])
        
        if(len(an[i][j])>1 and an[i][j][len(an[i][j])-2]==tempStructName):
            if(NN[0]==1):
                if(convertdatatype(nn[0])!="String" and convertdatatype(nn[0])!="std::string"):
                    st=st+"            "+convertdatatype(nn[0])+" "+an[i][j][len(an[i][j])-1]+"= 0;\r"  
                else:
                    st=st+"            "+convertdatatype(nn[0])+" "+an[i][j][len(an[i][j])-1]+"= \"\";\r"
            else:
                if(convertdatatype(nn[0])!="String" and convertdatatype(nn[0])!="std::string"):
                    st=st+"            "+convertdatatype(nn[0])+" "+an[i][j][len(an[i][j])-1]+"["+str(NN[0])+"]={0};\r"
                else:
                    st=st+"            "+convertdatatype(nn[0])+" "+an[i][j][len(an[i][j])-1]+"["+str(NN[0])+"]={"
                    for k in range(0,NN[0]-1):
                        st=st+"\"\","
                    st=st+"\"\"};\r"


            an[i][j].pop(len(an[i][j])-1)
            an[i][j].pop(len(an[i][j])-1)
            NN.pop(0)
            nn.pop(0)
            
          

        j=j+1 
      
        if(j>len(an[i])-1 ):
            st=st+"        } "+tempStructName+";\r"
            break
    return st

def create_hstruct(fw):
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData=setupvarforcreatelibSub()
    public_struct=[]
    fw.write("\r\r\r        // gen\r")
    for i in range (0,len(dataType)):
        nn=[] #name
        ss=[] # list sub in sub
        NN=[] #N of data 
        q="        struct{\r"
        for j in range (0,len(dataType[i])):
            if(dataName[i][j].find("__of__")==-1):  # normal struct
                if(NofData[i][j]==1):
                    if(convertdatatype(dataType[i][j])!="String" and convertdatatype(dataType[i][j])!="std::string"):
                        q=q+"            "+convertdatatype(dataType[i][j])+" "+dataName[i][j]+"= 0;\r"
                    else:
                        q=q+"            "+convertdatatype(dataType[i][j])+" "+dataName[i][j]+"= \"\";\r"
                else:
                    if(convertdatatype(dataType[i][j])!="String" and convertdatatype(dataType[i][j])!="std::string"):
                        q=q+"            "+convertdatatype(dataType[i][j])+" "+dataName[i][j]+"["+str(NofData[i][j])+"]={0};\r"
                    else:
                        q=q+"            "+convertdatatype(dataType[i][j])+" "+dataName[i][j]+"["+str(NofData[i][j])+"]={"
                        for k in range(0,NofData[i][j]-1):
                            q=q+"\"\","
                        q=q+"\"\"};\r"
            else:
                ss.append(dataName[i][j].split("__of__")   )    
                NN.append(NofData[i][j])
                nn.append(dataType[i][j])
                  
        # print("ssssssss",ss)
        # print("nnnnnnn",nn)

        an=[]
        for k in range(0,len(ss)):
            w=[]
            for j in range(0,len(ss)):
                if(ss[k][0]==ss[j][0]):
                    w.append(ss[j])
            an.append(w)
        an.append(["append"])
        we=[]
        for k in range(0,len(an)-1):
            if(an[k]!=an[k+1]):
                we.append(an[k])
        an=we.copy()
        # print("------------------------------------------")
        # print(an)
        # print("------------------------------------------")
        stt=""
        for k in range(0,len(an)):
            # an[i].pop(0)
            # print(an[k])
            st=""
            flagg=0
            while(1):
                for j in range(0,len(an[k])):
                    if(len(an[k][j])==0):
                        flagg=1
                if(flagg):
                    break
                st=exStruct(st,an,k,nn,NN)

                


            q=q+st
        
            
            
                
        # print("---------------")
        # print(stt)
        
        # print("00000000000000000000")
        # for k in range(0,len(an)):
        #     print(an[k])


                    
        # print("annnn=",an)
      
        q=q+"        } Sub_"+nameofTopic[i]+";\r\r"
        public_struct.append(q)
        fw.write(q)
    # an=[]
    # for i in range(0,len(ss)):
    #     w=[]
    #     for j in range(0,len(ss)):
    #         if(ss[i][0]==ss[j][0]):
    #             w.append(ss[j])
    #     an.append(w)

    # we=[]
    # for i in range(0,len(an)-1):
    #     if(an[i]!=an[i+1]):
    #         we.append(an[i])
    # an=we.copy()
    
    # print(an)
    # print("------------------------------------------")
    # stt=""
    # for i in range(0,len(an)):
    #     # an[i].pop(0)
    #     print(an[i])
    #     st=""
    #     flagg=0
    #     while(1):
    #         for j in range(0,len(an[i])):
    #             if(len(an[i][j])==0):
    #                 flagg=1
    #         if(flagg):
    #             break
    #         st=exStruct(st,an,i)
        
            


    #     stt=stt+st
    
        
        
            
    # print("---------------")
    # print(stt)
    
    # print("00000000000000000000")
    # for i in range(0,len(an)):
    #     print(an[i])


                
    # print("annnn=",an)
    # fw.write(stt)
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
    elif(typee=="float64" and sys.argv[1]=="stm32"):
        t=222
    elif(typee=="float64"):
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
    # print(Nofdata)
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
            if(q[i][j]=="}" and q[i][j+1]!=";" and q[i][j+2]=="S" and q[i][j+3]=="u" and q[i][j+4]=="b"):
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
        if(sys.argv[1]=="stm32"):
            pathr = os.path.join(get_package_share_directory('xicro_pkg'),'config', '.stm32_h_preSetup.txt')
        else:
            pathr = os.path.join(get_package_share_directory('xicro_pkg'),'config', '.arduino_h_preSetup.txt')
        fr=open(pathr, 'r') 
        fw.write("// ***************************************************************************************************************************************************\r")
        fw.write("//      |              This script was auto-generated by generate_library.py which received parameters from setup_xicro.yaml                   |\r")
        fw.write("//      |                                         EDITING THIS FILE BY HAND IS NOT RECOMMENDED                                                 |\r")
        fw.write("// ***************************************************************************************************************************************************\r\r")
        fw.write("\r\r#ifndef "+path[1:len(path)-2].split("/")[-1].upper()+"_H\r")
        fw.write("#define "+path[1:len(path)-2].split("/")[-1].upper()+"_H\r")
        public_struct=[]
        c=0
        for line in fr:
            c=c+1
            if(c==8):
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
            elif(c==56):
                try:
                    gen_privateStruct(fw)
                    publicStructToprivateStruct(fw,public_struct)
                    print("gen private_struct Done")
                except:
                    print("gen private_struct Fail")
            elif(c==12):
                fw.write("        uint8_t _Idmcu=" +str(Idmcu)+";\n\r")
            elif(c==1 and sys.argv[1]=="stm32"):
                fw.write("#include "+'"' + sys.argv[2]+'"\r')
                fw.write("#include \"string\"\r")
                fw.write("#include \"string.h\"\r")
                fw.write("#include \"math.h\"\r")
            else:
                fw.write(line)
        fw.write("\r\r#endif\r\r\r")
        fw.close()
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
            if(dataName[i][j].find("__of__")!=-1):
                dataName[i][j]=dataName[i][j].replace("__of__",".")
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
        if(sys.argv[1]=="stm32"):
            pathr = os.path.join(get_package_share_directory('xicro_pkg'),'config', '.stm32_cpp_preSetup.txt')
        else:
            pathr = os.path.join(get_package_share_directory('xicro_pkg'),'config', '.arduino_cpp_preSetup.txt')
        fr=open(pathr, 'r') 
        fw.write("// ***************************************************************************************************************************************************\r")
        fw.write("//      |              This script was auto-generated by generate_arduino_lib.py which received parameters from setup_xicro.yaml               |\r")
        fw.write("//      |                                         EDITING THIS FILE BY HAND IS NOT RECOMMENDED                                                 |\r")
        fw.write("// ***************************************************************************************************************************************************\r\r")
        fw.write("\r\n#include \""+"Xicro_"+get_params("Namespace")+"_ID_"+str(id_mcu)+".h\"\r\n")
        c=0
        for line in fr:        
            c=c+1
            if(c==388): 
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
    elif(strr=="float32" or (strr=="float64" and sys.argv[1]!="stm32") ):
        return "float"
    elif(strr=="float64"):
        return "double"
    elif(strr=="string" and sys.argv[1]!="stm32"):
        return "String"
    elif(strr=="string" ):
        return "std::string"
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
    elif( (typee=="float32" or (typee=="float64" and sys.argv[1]!="stm32")  ) and Nofdata==1):
        return  "    _SendFloat32((float*)&"+namee+","+ str(Nofdata)+");\n"
    elif( (typee=="float32" or (typee=="float64" and sys.argv[1]!="stm32")  ) and Nofdata!=1):
        return  "    _SendFloat32("+namee+","+ str(Nofdata)+");\n"    
    elif(typee=="float64"  and Nofdata==1):
        return  "    _SendDouble((double*)&"+namee+","+ str(Nofdata)+");\n"
    elif(typee=="float64"  and Nofdata!=1):
        return  "    _SendDouble("+namee+","+ str(Nofdata)+");\n"    
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
    # print(id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,Nofdata)
    listVoid=strVoid(nameofTopic,dataType,dataName,Nofdata)
    create_hFile(listVoid,id_mcu)
    create_cppFile(listVoid,id_mcu,id_topic,dataType,dataName,Nofdata)
 
def checkArgs():
    flagargs=0
    try:
        input = sys.argv[1]
        if(input == "arduino" or input ==  "stm32" or "esp"):
            flagargs=1
        else:
            print("*************************************************")
            print('******  Input argv Only ["arduino","stm32","esp"]  ******')
    except:
        print('******  Please input argv ["arduino","stm32","esp"]  ******')

    if(flagargs and sys.argv[1]== "stm32"):
        try:
            input = sys.argv[2]
        except:    
            flagargs=0
            print('******  Please input argv [module_Name.h]  ******')

    if(flagargs):
        return 1
    else:
        return 0 

def main():
    if(checkArgs()):
        try:
            gen()
            print("*******Create library arduino complete*******")
        except:
            print("*******Create library arduino failed*******")
if __name__ == '__main__':
    main()