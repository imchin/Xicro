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
    # print("\n\n\n\nDatatype :",dataType)
    # print("\n\n\n\nDataName :",dataName)
    # print("\n\n\n\nNofdata :",NofData)
    # print("\n\n\n\ninterfacefile :",interfacefile)
    # print("\n\n\n\ninterfacefileIn :",interfacein)
    for i in range(0,len(dataType)):
        for j in range(0,len(dataType[i])):
            if(checkSubmsg(dataType[i][j]) == 0):   
                # print("On : ",dataType[i][j])
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
                # print(addtype,addName,addinterfacein)
            
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
    # print(TempType,TempName)
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
    return id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData,interfacein
def setupvarforcreatelibPub():
    id_mcu=0
    id_topic=[]
    nameofTopic=[]
    interfacefile=[]
    interfacepkg=[]
    dataType=[]
    dataName=[]
    NofData=[]
    interfacein=[]
    try:
        id_mcu=get_params("Idmcu")
        Setup_Pub=get_params("Setup_Publisher")
        for i in range(0,len(Setup_Pub)):
            id_topic.append(Setup_Pub[i][0])
            nameofTopic.append(Setup_Pub[i][1])
            interfacefile.append(Setup_Pub[i][2])
        for i in range (0,len(interfacefile)):
            tempinterfacein=[]
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
                    tempinterfacein.append(interfacefile[i].split("/")[0])
                
            NofData.append(tempN)
            dataType.append(tempType)
            dataName.append(tempName)
            interfacein.append(tempinterfacein)
        for i in range(0,10):
            id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData,interfacein=expandSub(id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData,interfacein)
        

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
    interfacein=[]
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
            tempinterfacein=[]
            path = os.path.join(get_package_share_directory( interfacefile[i].split("/")[0]),'msg',  interfacefile[i].split("/")[1])
            msg = open(path, 'r').read().splitlines()
            for j in range(0,len(msg)):
                line=msg[j].split()
                if(len(line)!=0 and line[0]!="#" ):
                    tempType.append(line[0])
                    tempName.append(line[1]),NofData
                    tempdatagrab.append(0)
                    tempN.append(checkNofdata(line[0]))
                    tempinterfacein.append(interfacefile[i].split("/")[0])
            NofData.append(tempN)
            dataType.append(tempType)
            dataName.append(tempName)
            interfacein.append(tempinterfacein)
        for i in range(0,10):
            id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData,interfacein=expandSub(id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData,interfacein)
       
    except:
        print("Error setup variable.")

    return id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData

def normalSt(st,anI,datatype,Nofdata,structName):
    st=st+"        struct{\r"
    for i in range(0,len(anI)):
       
        if(anI[i][len(anI[i])-2]==structName):
            if(Nofdata[0]==1):
                if(convertdatatype(datatype[0])!="String" and convertdatatype(datatype[0])!="std::string"):
                    st=st+"            "+convertdatatype(datatype[0])+" "+anI[i][len(anI[i])-1]+"= 0;\r"  
                else:
                    st=st+"            "+convertdatatype(datatype[0])+" "+anI[i][len(anI[i])-1]+"= \"\";\r"
            else:
                if(convertdatatype(datatype[0])!="String" and convertdatatype(datatype[0])!="std::string"):
                    st=st+"            "+convertdatatype(datatype[0])+" "+anI[i][len(anI[i])-1]+"["+str(Nofdata[0])+"]={0};\r"
                else:
                    st=st+"            "+convertdatatype(datatype[0])+" "+anI[i][len(anI[i])-1]+"["+str(Nofdata[0])+"]={"
                    for k in range(0,Nofdata[0]-1):
                        st=st+"\"\","
                    st=st+"\"\"};\r"

            anI[i].pop(len(anI[i])-1)
            anI[i].pop(len(anI[i])-1)
            Nofdata.pop(0)
            datatype.pop(0)
    st=st+"        } "+structName+";\r"
    return st
def normal_closeSt(st,anI,datatype,Nofdata,structName,maxlen):
   
    for i in range(0,len(anI)):
       
        if(len(anI[i])>=2 and anI[i][len(anI[i])-2]==structName):
            if(Nofdata[0]==1):
                if(convertdatatype(datatype[0])!="String" and convertdatatype(datatype[0])!="std::string"):
                    st=st+"            "+convertdatatype(datatype[0])+" "+anI[i][len(anI[i])-1]+"= 0;\r"  
                else:
                    st=st+"            "+convertdatatype(datatype[0])+" "+anI[i][len(anI[i])-1]+"= \"\";\r"
            else:
                if(convertdatatype(datatype[0])!="String" and convertdatatype(datatype[0])!="std::string"):
                    st=st+"            "+convertdatatype(datatype[0])+" "+anI[i][len(anI[i])-1]+"["+str(Nofdata[0])+"]={0};\r"
                else:
                    st=st+"            "+convertdatatype(datatype[0])+" "+anI[i][len(anI[i])-1]+"["+str(Nofdata[0])+"]={"
                    for k in range(0,Nofdata[0]-1):
                        st=st+"\"\","
                    st=st+"\"\"};\r"
            anI[i].pop(len(anI[i])-1)
            Nofdata.pop(0)
            datatype.pop(0)
    for i in range(0,len(anI)):
        if(anI[i][len(anI[i])-1]==structName):
            anI[i].pop(len(anI[i])-1)
   
    st="        struct{\r"+st
    st=st+"        } "+structName+";\r"
    return st
def structOnly_close(st,anI,structName):
    st="        struct{\r"+st
    st=st+"        } "+structName+";\r"
    for i in range(0,len(anI)):
        if(anI[i][len(anI[i])-1]==structName):
            anI[i].pop(len(anI[i])-1)
    return st
def exStruct(st,anI,datatype,Nofdata):
    # q=0
    while(len(anI[0])>0):
       
        # print("\n\n\n\nOn:",anI,"\n\n\n\n")
        maxlen=len(anI[0])
        #select struct name 
        if(len(anI[1])>= 2 and anI[0][len(anI[0])-1]==anI[1][len(anI[1])-1]):
            structName=anI[0][len(anI[0])-2]
            # print("case struct only close\n")
            # print("structnameOn :",structName,"\n\n")
            st=structOnly_close(st,anI,structName)
        elif(anI[0][len(anI[0])-1]!=anI[1][len(anI[1])-1] and  anI[0][maxlen-2]==anI[1][maxlen-2] and len(anI[0])!= len(anI[1])):  #maxlen=len(anI[0])
            structName=anI[0][len(anI[0])-2]
            # print("case normal close struct\n")
            # print("structnameOn :",structName,"\n\n")
            st=normal_closeSt(st,anI,datatype,Nofdata,structName,maxlen)
        else:
            structName=anI[0][len(anI[0])-2]
            # print("case normal struct\n")
            # print("structnameOn :",structName,"\n\n")
            st=normalSt(st,anI,datatype,Nofdata,structName)
        anI.sort(reverse=True,key=funS)
        # q=q+1
        # if(q>=4):
        #     break

    return st
def funS(e):
  return len(e)
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

      
        # for ii in range(0,len(an)):
        #     print("\n\n\n")
        #     print("------------------------------------------")
        #     print(an[ii])
        #     print("------------------------------------------")
        #     print("\n\n\n")
        for k in range(0,len(an)):
            st=""
            st=exStruct(st,an[k],nn,NN) # st ,an[k] , Type, Nofdata
            q=q+st
              
        q=q+"        } Sub_"+nameofTopic[i]+";\r\r"
        public_struct.append(q)
        fw.write(q)
   
    return public_struct
    
def create_hstruct_srv_client(fw):
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res = setup_srv_protocol()
    public_struct=[]
    fw.write("\r\r\r        // gen struct srv client res\r")
    for i in range (0,len(dataType_srv_res)):
        nn=[] #name
        ss=[] # list sub in sub
        NN=[] #N of data 
        q="        struct{\r"
        for j in range (0,len(dataType_srv_res[i])):
            if(dataName_srv_res[i][j].find("__of__")==-1):  # normal struct
                if(NofData_srv_res[i][j]==1):
                    if(convertdatatype(dataType_srv_res[i][j])!="String" and convertdatatype(dataType_srv_res[i][j])!="std::string"):
                        q=q+"            "+convertdatatype(dataType_srv_res[i][j])+" "+dataName_srv_res[i][j]+"= 0;\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_srv_res[i][j])+" "+dataName_srv_res[i][j]+"= \"\";\r"
                else:
                    if(convertdatatype(dataType_srv_res[i][j])!="String" and convertdatatype(dataType_srv_res[i][j])!="std::string"):
                        q=q+"            "+convertdatatype(dataType_srv_res[i][j])+" "+dataName_srv_res[i][j]+"["+str(NofData_srv_res[i][j])+"]={0};\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_srv_res[i][j])+" "+dataName_srv_res[i][j]+"["+str(NofData_srv_res[i][j])+"]={"
                        for k in range(0,NofData_srv_res[i][j]-1):
                            q=q+"\"\","
                        q=q+"\"\"};\r"
            else:
                ss.append(dataName_srv_res[i][j].split("__of__")   )    
                NN.append(NofData_srv_res[i][j])
                nn.append(dataType_srv_res[i][j])
                  
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
        for k in range(0,len(an)):
            st=""
            st=exStruct(st,an[k],nn,NN) # st ,an[k] , Type, Nofdata
            q=q+st
        q=q+"        } Client_res_"+namesrv[i]+";\r\r"
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
def typetoProtocol_2(typee,Nofdata):
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
    elif(typee=="float64" and ( sys.argv[1] =="arduino" or sys.argv[1] =="esp" )): # force float64 to float32
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
    elif(typee=="xxicro_Empty"):
        t=254
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
def setup_srv_protocol():
    setup_srv=get_params('Setup_Srv_client')
    Idmcu=get_params("Idmcu")
    Idsrv=[]
    namesrv=[]
    interfacesrv=[]
    for i in range(0,len(setup_srv)):
        Idsrv.append(setup_srv[i][0])
        namesrv.append(setup_srv[i][1])
        interfacesrv.append(setup_srv[i][2])
    print('Done load YAML srv_client.')
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
            if(dataType_srv_req[i][j].split("[")[0] == "float64" and (sys.argv[1]=="arduino" or sys.argv[1]=="esp") ):
                dataType_srv_req[i][j]="float32"
    for i in range(0,len(dataType_srv_res)): # bias float64 to float32
        for j in range(0,len(dataType_srv_res[i])):
            if(dataType_srv_res[i][j].split("[")[0] == "float64" and (sys.argv[1]=="arduino" or sys.argv[1]=="esp") ):
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
                a,b=typetoProtocol_2(dataType[i][j],NofData[i][j])
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
    return Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res

def genstate_srv(fw):
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res = setup_srv_protocol()
    fw.write("\r\r\r        // gen state_srv_action\r")
    fw.write("\r        struct{\r")
    for i in range(0,len(namesrv)):
        fw.write("            uint8_t Srv_"+namesrv[i]+ " = 0;\r")
    fw.write("\r        } State;\r")
def genResclient(fw):
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res = setup_srv_protocol()
    1
def create_hFile(listVoid,Idmcu,listVoid_client_req):
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
        public_struct_client_Res=[]
        c=0
        for line in fr:
            c=c+1
            if(c==8):
                try:
                    fw.write("\r\r\r        // gen public pub void\r")
                    for i in range(0,len(listVoid)):
                        fw.write(listVoid[i])
                        fw.write("\n")
                    print("gen voidPub Done")
                    public_struct=create_hstruct(fw)
                    print("gen public_struct Done")
                    genstate_srv(fw)
                    print("gen state_srv Done")
                    public_struct_client_Res=create_hstruct_srv_client(fw)
                    genResclient(fw)
                    print("gen client_res_struct Done")
                    fw.write("\r\r\r        // gen service call void\r")
                    for i in range(0,len(listVoid_client_req)):
                        fw.write(listVoid_client_req[i])
                        fw.write("\n")

                except:
                    print("gen public_struct or voidPub Fail.")
            elif(c==57):
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
def genvoidService_call(fw,listVoid_client_req,id_mcu):
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res = setup_srv_protocol()
    for i in range(0,len(listVoid_client_req)):
        # print(listVoid[i][8:12])
        fw.write(listVoid_client_req[i][8:12]+" Xicro::"+listVoid_client_req[i][13:len(listVoid_client_req[i])-1])
        fw.write(("{\n"))
        fw.write("    _crc=0;\r")
        fw.write("    _Sendstart();\n")
        fw.write("    _SendSignature("+str(id_mcu)+",11);\n")
        fw.write("    _SendIdTopic("+str(Idsrv[i])+");\n")
        for j in range(0,len(dataType_srv_req[i])):
            cond=j<len(dataType_srv_req[i])-1 #check flag continue or stop
            fw.write(typetoVoid(dataType_srv_req[i][j],dataName_srv_req[i][j],NofData_srv_req[i][j],cond))
            if(dataType_srv_req[i][j]=="bool" and NofData_srv_req[i][j]==1 ):
                fw.write("// auto by 1 bool\n")
            elif(cond):
                fw.write("    _Sendcontinue();\n")
            else:
                fw.write("    _Sendstop();\n")
        fw.write("    _Sendcrc();\r")
        fw.write("}\n")
def create_cppFile(listVoid,id_mcu,id_topic,dataType,dataName,Nofdata,listVoid_client_req):
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
                    fw.write("\r\r\r// gen publish void\r")
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
                    fw.write("\r\r\r// gen service call void\r")
                    genvoidService_call(fw,listVoid_client_req,id_mcu)
                    print("gen service call void Done.")
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
    elif(typee=="xxicro_Empty" and Nofdata==1):
        return  "    _SendEmpty();\n"
    else:

        print(typee )
        return "1"

def strVoid(nameofTopic,dataType,dataName,Nofdata):
    # print(nameofTopic,dataType,dataName,Nofdata)
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
def strVoid_srv_req():
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res = setup_srv_protocol()
    temp=[]
    for i in range(0,len(namesrv)):
        t="        "
        t=t+"void service_call_"+namesrv[i]+"("
        if(dataType_srv_req[i][0]!="xxicro_Empty"):
            for j in range(0,len(dataType_srv_req[i])):
                t=t+convertdatatype(dataType_srv_req[i][j])+" "
                if(NofData_srv_req[i][j]!=1):
                    t=t+"*"
                t=t+dataName_srv_req[i][j]+" "
                if(j>=0 and j<len(dataType_srv_req[i])-1):
                    t=t+","
        t=t+");"
        temp.append(t)
    # print(temp)
    return temp


def gen():
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,Nofdata=setupvarforcreatelibPub()
    # print(id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,Nofdata)
    listVoid=strVoid(nameofTopic,dataType,dataName,Nofdata)
    listVoid_client_req=strVoid_srv_req()
    create_hFile(listVoid,id_mcu,listVoid_client_req)
    create_cppFile(listVoid,id_mcu,id_topic,dataType,dataName,Nofdata,listVoid_client_req)
 
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