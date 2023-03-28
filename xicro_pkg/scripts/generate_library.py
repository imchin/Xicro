#!/usr/bin/python3
import os
import argparse
import yaml
from ament_index_python.packages import get_package_share_directory

def get_params(qq):
    try:
        q=qq
        path = os.path.join(get_package_share_directory('xicro_pkg'),'config', 'setup_xicro.yaml')
        with open(path,'r') as f:
            yml_dict = yaml.safe_load(f)
            q=q.split(".")
            ans = yml_dict.get(q[0])
            for i in range(1,len(q)):
                ans = ans.get(q[i])
        print('Get '+qq+' Done.')
        return  ans
    except:
        print('Get '+qq+' Fail'+'Something went wrong when opening YAML.')


    return 0
def mkdir():
    path="Fail"
    try:
        path = get_params("microcontroller.generate_library_Path")
        ns= get_params("microcontroller.namespace")
        id = get_params("microcontroller.idmcu")
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
        id_mcu=get_params("microcontroller.idmcu")
        Setup_Pub=get_params("ros.publisher")
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
        # print(id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData)
        for i in range(0,10):
            id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData,interfacein=expandSub(id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData,interfacein)
        # print(id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData)

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
        id_mcu=get_params("microcontroller.idmcu")
        Setup_Sub=get_params("ros.subscriber")
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
       
        # print("\n\n\n\nOn:",anI,len(anI),"\n\n\n\n")
        maxlen=len(anI[0])
        #select struct name 
        if(len(anI)>1 and len(anI[1])>= 2 and anI[0][len(anI[0])-1]==anI[1][len(anI[1])-1]):
            structName=anI[0][len(anI[0])-2]
            # print("case struct only close\n")
            # print("structnameOn :",structName,"\n\n")
            st=structOnly_close(st,anI,structName)
        elif(len(anI)>1 and anI[0][len(anI[0])-1]!=anI[1][len(anI[1])-1] and  anI[0][maxlen-2]==anI[1][maxlen-2] and len(anI[0])!= len(anI[1])):  #maxlen=len(anI[0])
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
def create_hstruct_pub(fw):
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData=setupvarforcreatelibPub()
    public_struct=[]
    fw.write("\r\r\r        // gen pub struct\r")
    for i in range (0,len(dataType)):
        nn=[] #name
        ss=[] # list sub in sub
        NN=[] #N of data 
        q="        struct{\r"
        q=q+"            struct{\r"
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
        q=q+"            } message; \r"
        q=q+"        } Publisher_"+nameofTopic[i]+";\r\r"
        public_struct.append(q)
        fw.write(q)
   
    return public_struct

    
def create_hstruct(fw):
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData=setupvarforcreatelibSub()
    public_struct=[]
    fw.write("\r\r\r        // gen Sub struct\r")
    for i in range (0,len(dataType)):
        nn=[] #name
        ss=[] # list sub in sub
        NN=[] #N of data 
        q="        struct{\r"
        q=q+"            struct{\r"
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
        q=q+"            } message; \r"
        q=q+"        } Subscription_"+nameofTopic[i]+";\r\r"
        public_struct.append(q)
        fw.write(q)
   
    return public_struct
    
def create_hstruct_srv_client(fw):
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res = setup_srv_protocol()
    public_struct=[]
    fw.write("\r\r\r        // gen struct srv client \r") 
    for i in range (0,len(namesrv)):
        nn=[] #name
        ss=[] # list sub in sub
        NN=[] #N of data 
        q="        struct{\r"

        q=q+"            struct{\r"
        for j in range (0,len(dataType_srv_req[i])):
            if(dataName_srv_req[i][j].find("__of__")==-1):  # normal struct
                if(NofData_srv_req[i][j]==1):
                    if(convertdatatype(dataType_srv_req[i][j])!="String" and convertdatatype(dataType_srv_req[i][j])!="std::string" ):
                        q=q+"            "+convertdatatype(dataType_srv_req[i][j])+" "+dataName_srv_req[i][j]+"= 0;\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_srv_req[i][j])+" "+dataName_srv_req[i][j]+"= \"\";\r"
                else:
                    if(convertdatatype(dataType_srv_req[i][j])!="String" and convertdatatype(dataType_srv_req[i][j])!="std::string" ):
                        q=q+"            "+convertdatatype(dataType_srv_req[i][j])+" "+dataName_srv_req[i][j]+"["+str(NofData_srv_req[i][j])+"]={0};\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_srv_req[i][j])+" "+dataName_srv_req[i][j]+"["+str(NofData_srv_req[i][j])+"]={"
                        for k in range(0,NofData_srv_req[i][j]-1):
                            q=q+"\"\","
                        q=q+"\"\"};\r"
            else:
                ss.append(dataName_srv_req[i][j].split("__of__")   )    
                NN.append(NofData_srv_req[i][j])
                nn.append(dataType_srv_req[i][j])
                  
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
        q=q+"            } request;\r\r"

        # end req
        q=q+"            struct{\r"
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
        q=q+"            } response;\r\r"
        # end res
        
        q=q+"            uint8_t state = 0;\r"

        q=q+"        } Service_client_"+namesrv[i]+";\r\r"
        # bias empty gen nothing
        while(q.find("xxicro_Empty xxicro_Empty= 0;")!=-1):
            qq=q.split("xxicro_Empty xxicro_Empty= 0;")
            q=""
            for ii in range(0,len(qq)):
                q=q+qq[ii] 
        public_struct.append(q)        
        fw.write(q)
    return public_struct

def create_hstruct_action_client(fw):
    Idaction_client,nameaction_client,interfaceaction_client,dataType_action_client_req,dataName_action_client_req,datagrab_action_client_req,NofData_action_client_req,datatypeProtocol_action_client_req,bytetograb_action_client_req,dataType_action_client_res,dataName_action_client_res,datagrab_action_client_res,NofData_action_client_res,datatypeProtocol_action_client_res,bytetograb_action_client_res,dataType_action_client_feed,dataName_action_client_feed,datagrab_action_client_feed,NofData_action_client_feed,datatypeProtocol_action_client_feed,bytetograb_action_client_feed,timeOut_action_client = setup_action_client_protocol()
    public_struct=[]
    fw.write("\r\r\r        // gen struct action client \r") 
    for i in range (0,len(nameaction_client)):
        nn=[] #name
        ss=[] # list sub in sub
        NN=[] #N of data 
        q="        struct{\r"

        q=q+"            struct{\r"
        for j in range (0,len(dataType_action_client_req[i])):
            if(dataName_action_client_req[i][j].find("__of__")==-1):  # normal struct
                if(NofData_action_client_req[i][j]==1):
                    if(convertdatatype(dataType_action_client_req[i][j])!="String" and convertdatatype(dataType_action_client_req[i][j])!="std::string" ):
                        q=q+"            "+convertdatatype(dataType_action_client_req[i][j])+" "+dataName_action_client_req[i][j]+"= 0;\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_action_client_req[i][j])+" "+dataName_action_client_req[i][j]+"= \"\";\r"
                else:
                    if(convertdatatype(dataType_action_client_req[i][j])!="String" and convertdatatype(dataType_action_client_req[i][j])!="std::string" ):
                        q=q+"            "+convertdatatype(dataType_action_client_req[i][j])+" "+dataName_action_client_req[i][j]+"["+str(NofData_action_client_req[i][j])+"]={0};\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_action_client_req[i][j])+" "+dataName_action_client_req[i][j]+"["+str(NofData_action_client_req[i][j])+"]={"
                        for k in range(0,NofData_action_client_req[i][j]-1):
                            q=q+"\"\","
                        q=q+"\"\"};\r"
            else:
                ss.append(dataName_action_client_req[i][j].split("__of__")   )    
                NN.append(NofData_action_client_req[i][j])
                nn.append(dataType_action_client_req[i][j])
                  
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
        q=q+"            } request;\r\r"

        # end req
        q=q+"            struct{\r"
        for j in range (0,len(dataType_action_client_res[i])):
            if(dataName_action_client_res[i][j].find("__of__")==-1):  # normal struct
                if(NofData_action_client_res[i][j]==1):
                    if(convertdatatype(dataType_action_client_res[i][j])!="String" and convertdatatype(dataType_action_client_res[i][j])!="std::string"):
                        q=q+"            "+convertdatatype(dataType_action_client_res[i][j])+" "+dataName_action_client_res[i][j]+"= 0;\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_action_client_res[i][j])+" "+dataName_action_client_res[i][j]+"= \"\";\r"
                else:
                    if(convertdatatype(dataType_action_client_res[i][j])!="String" and convertdatatype(dataType_action_client_res[i][j])!="std::string"):
                        q=q+"            "+convertdatatype(dataType_action_client_res[i][j])+" "+dataName_action_client_res[i][j]+"["+str(NofData_action_client_res[i][j])+"]={0};\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_action_client_res[i][j])+" "+dataName_action_client_res[i][j]+"["+str(NofData_action_client_res[i][j])+"]={"
                        for k in range(0,NofData_action_client_res[i][j]-1):
                            q=q+"\"\","
                        q=q+"\"\"};\r"
            else:
                ss.append(dataName_action_client_res[i][j].split("__of__")   )    
                NN.append(NofData_action_client_res[i][j])
                nn.append(dataType_action_client_res[i][j])
                  
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
        q=q+"            } result;\r\r"
        # end res
        

        q=q+"            struct{\r"
        for j in range (0,len(dataType_action_client_feed[i])):
            if(dataName_action_client_feed[i][j].find("__of__")==-1):  # normal struct
                if(NofData_action_client_feed[i][j]==1):
                    if(convertdatatype(dataType_action_client_feed[i][j])!="String" and convertdatatype(dataType_action_client_feed[i][j])!="std::string"):
                        q=q+"            "+convertdatatype(dataType_action_client_feed[i][j])+" "+dataName_action_client_feed[i][j]+"= 0;\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_action_client_feed[i][j])+" "+dataName_action_client_feed[i][j]+"= \"\";\r"
                else:
                    if(convertdatatype(dataType_action_client_feed[i][j])!="String" and convertdatatype(dataType_action_client_feed[i][j])!="std::string"):
                        q=q+"            "+convertdatatype(dataType_action_client_feed[i][j])+" "+dataName_action_client_feed[i][j]+"["+str(NofData_action_client_feed[i][j])+"]={0};\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_action_client_feed[i][j])+" "+dataName_action_client_feed[i][j]+"["+str(NofData_action_client_feed[i][j])+"]={"
                        for k in range(0,NofData_action_client_feed[i][j]-1):
                            q=q+"\"\","
                        q=q+"\"\"};\r"
            else:
                ss.append(dataName_action_client_feed[i][j].split("__of__")   )    
                NN.append(NofData_action_client_feed[i][j])
                nn.append(dataType_action_client_feed[i][j])
                  
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
        q=q+"            } feedback;\r\r"  
        # end feed



        q=q+"            uint8_t state = 0;\r"

        q=q+"        } Action_client_"+nameaction_client[i]+";\r\r"
        # bias empty gen nothing
        while(q.find("xxicro_Empty xxicro_Empty= 0;")!=-1):
            qq=q.split("xxicro_Empty xxicro_Empty= 0;")
            q=""
            for ii in range(0,len(qq)):
                q=q+qq[ii] 
        public_struct.append(q)        
        fw.write(q)
    return public_struct

def create_hstruct_action_server(fw):
    Idaction_server,nameaction_server,interfaceaction_server,dataType_action_server_req,dataName_action_server_req,datagrab_action_server_req,NofData_action_server_req,datatypeProtocol_action_server_req,bytetograb_action_server_req,dataType_action_server_res,dataName_action_server_res,datagrab_action_server_res,NofData_action_server_res,datatypeProtocol_action_server_res,bytetograb_action_server_res,dataType_action_server_feed,dataName_action_server_feed,datagrab_action_server_feed,NofData_action_server_feed,datatypeProtocol_action_server_feed,bytetograb_action_server_feed,timeOut_action_server = setup_action_server_protocol()
    public_struct=[]
    fw.write("\r\r\r        // gen struct action server \r") 
    for i in range (0,len(nameaction_server)):
        nn=[] #name
        ss=[] # list sub in sub
        NN=[] #N of data 
        q="        struct{\r"

        q=q+"            struct{\r"
        for j in range (0,len(dataType_action_server_req[i])):
            if(dataName_action_server_req[i][j].find("__of__")==-1):  # normal struct
                if(NofData_action_server_req[i][j]==1):
                    if(convertdatatype(dataType_action_server_req[i][j])!="String" and convertdatatype(dataType_action_server_req[i][j])!="std::string" ):
                        q=q+"            "+convertdatatype(dataType_action_server_req[i][j])+" "+dataName_action_server_req[i][j]+"= 0;\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_action_server_req[i][j])+" "+dataName_action_server_req[i][j]+"= \"\";\r"
                else:
                    if(convertdatatype(dataType_action_server_req[i][j])!="String" and convertdatatype(dataType_action_server_req[i][j])!="std::string" ):
                        q=q+"            "+convertdatatype(dataType_action_server_req[i][j])+" "+dataName_action_server_req[i][j]+"["+str(NofData_action_server_req[i][j])+"]={0};\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_action_server_req[i][j])+" "+dataName_action_server_req[i][j]+"["+str(NofData_action_server_req[i][j])+"]={"
                        for k in range(0,NofData_action_server_req[i][j]-1):
                            q=q+"\"\","
                        q=q+"\"\"};\r"
            else:
                ss.append(dataName_action_server_req[i][j].split("__of__")   )    
                NN.append(NofData_action_server_req[i][j])
                nn.append(dataType_action_server_req[i][j])
                  
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
        q=q+"            } request;\r\r"

        # end req
        q=q+"            struct{\r"
        for j in range (0,len(dataType_action_server_res[i])):
            if(dataName_action_server_res[i][j].find("__of__")==-1):  # normal struct
                if(NofData_action_server_res[i][j]==1):
                    if(convertdatatype(dataType_action_server_res[i][j])!="String" and convertdatatype(dataType_action_server_res[i][j])!="std::string"):
                        q=q+"            "+convertdatatype(dataType_action_server_res[i][j])+" "+dataName_action_server_res[i][j]+"= 0;\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_action_server_res[i][j])+" "+dataName_action_server_res[i][j]+"= \"\";\r"
                else:
                    if(convertdatatype(dataType_action_server_res[i][j])!="String" and convertdatatype(dataType_action_server_res[i][j])!="std::string"):
                        q=q+"            "+convertdatatype(dataType_action_server_res[i][j])+" "+dataName_action_server_res[i][j]+"["+str(NofData_action_server_res[i][j])+"]={0};\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_action_server_res[i][j])+" "+dataName_action_server_res[i][j]+"["+str(NofData_action_server_res[i][j])+"]={"
                        for k in range(0,NofData_action_server_res[i][j]-1):
                            q=q+"\"\","
                        q=q+"\"\"};\r"
            else:
                ss.append(dataName_action_server_res[i][j].split("__of__")   )    
                NN.append(NofData_action_server_res[i][j])
                nn.append(dataType_action_server_res[i][j])
                  
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
        q=q+"            } result;\r\r"
        # end res
        

        q=q+"            struct{\r"
        for j in range (0,len(dataType_action_server_feed[i])):
            if(dataName_action_server_feed[i][j].find("__of__")==-1):  # normal struct
                if(NofData_action_server_feed[i][j]==1):
                    if(convertdatatype(dataType_action_server_feed[i][j])!="String" and convertdatatype(dataType_action_server_feed[i][j])!="std::string"):
                        q=q+"            "+convertdatatype(dataType_action_server_feed[i][j])+" "+dataName_action_server_feed[i][j]+"= 0;\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_action_server_feed[i][j])+" "+dataName_action_server_feed[i][j]+"= \"\";\r"
                else:
                    if(convertdatatype(dataType_action_server_feed[i][j])!="String" and convertdatatype(dataType_action_server_feed[i][j])!="std::string"):
                        q=q+"            "+convertdatatype(dataType_action_server_feed[i][j])+" "+dataName_action_server_feed[i][j]+"["+str(NofData_action_server_feed[i][j])+"]={0};\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_action_server_feed[i][j])+" "+dataName_action_server_feed[i][j]+"["+str(NofData_action_server_feed[i][j])+"]={"
                        for k in range(0,NofData_action_server_feed[i][j]-1):
                            q=q+"\"\","
                        q=q+"\"\"};\r"
            else:
                ss.append(dataName_action_server_feed[i][j].split("__of__")   )    
                NN.append(NofData_action_server_feed[i][j])
                nn.append(dataType_action_server_feed[i][j])
                  
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
        q=q+"            } feedback;\r\r"  
        # end feed


        
        q=q+"            uint8_t state = 0;\r"

        q=q+"        } Action_server_"+nameaction_server[i]+";\r\r"
        # bias empty gen nothing
        while(q.find("xxicro_Empty xxicro_Empty= 0;")!=-1):
            qq=q.split("xxicro_Empty xxicro_Empty= 0;")
            q=""
            for ii in range(0,len(qq)):
                q=q+qq[ii] 
        public_struct.append(q)        
        fw.write(q)
    return public_struct

def create_hstruct_srv_server(fw):
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res = setup_srv_server_protocol()
    public_struct=[]
    fw.write("\r\r\r        // gen struct srv server\r") 
    for i in range (0,len(namesrv)):
        nn=[] #name
        ss=[] # list sub in sub
        NN=[] #N of data 
        q="        struct{\r"

        q=q+"            struct{\r"
        for j in range (0,len(dataType_srv_req[i])):
            if(dataName_srv_req[i][j].find("__of__")==-1):  # normal struct
                if(NofData_srv_req[i][j]==1):
                    if(convertdatatype(dataType_srv_req[i][j])!="String" and convertdatatype(dataType_srv_req[i][j])!="std::string" ):
                        q=q+"            "+convertdatatype(dataType_srv_req[i][j])+" "+dataName_srv_req[i][j]+"= 0;\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_srv_req[i][j])+" "+dataName_srv_req[i][j]+"= \"\";\r"
                else:
                    if(convertdatatype(dataType_srv_req[i][j])!="String" and convertdatatype(dataType_srv_req[i][j])!="std::string" ):
                        q=q+"            "+convertdatatype(dataType_srv_req[i][j])+" "+dataName_srv_req[i][j]+"["+str(NofData_srv_req[i][j])+"]={0};\r"
                    else:
                        q=q+"            "+convertdatatype(dataType_srv_req[i][j])+" "+dataName_srv_req[i][j]+"["+str(NofData_srv_req[i][j])+"]={"
                        for k in range(0,NofData_srv_req[i][j]-1):
                            q=q+"\"\","
                        q=q+"\"\"};\r"
            else:
                ss.append(dataName_srv_req[i][j].split("__of__")   )    
                NN.append(NofData_srv_req[i][j])
                nn.append(dataType_srv_req[i][j])
                  
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
        q=q+"            } request;\r\r"

        # end req
        q=q+"            struct{\r"
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
        q=q+"            } response;\r\r"
        # end res
        
        q=q+"            uint8_t state = 0;\r"

        q=q+"        } Service_server_"+namesrv[i]+";\r\r"
        # bias empty gen nothing
        while(q.find("xxicro_Empty xxicro_Empty= 0;")!=-1):
            qq=q.split("xxicro_Empty xxicro_Empty= 0;")
            q=""
            for ii in range(0,len(qq)):
                q=q+qq[ii] 
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
    elif(typee=="float64" and input.mcu_type=="stm32"):
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
    fw.write("\r\r\r        // gen Sub\r")
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
def gen_privateStruct_srv_client_res(fw):
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res=setup_srv_protocol()
    # print(Nofdata)
    fw.write("\r\r\r        // gen client res\r")
    q="        void* _nonverify_srv_client_res["+str(len(Idsrv))+"]["+str(getMaxNdata(dataType_srv_res))+"]["+str(getMaxofArray(NofData_srv_res))+"];\r"
    q=q+"        void* _verify_srv_client_res["+str(len(Idsrv))+"]["+str(getMaxNdata(dataType_srv_res))+"]["+str(getMaxofArray(NofData_srv_res))+"];\r"
    q=q+"        uint8_t _Idsrv_client["+str(len(Idsrv))+"]={"
    for i in range (0,len(Idsrv)):
        if(i<len(Idsrv)-1):
            q=q+str(Idsrv[i])+","
        else:
            q=q+str(Idsrv[i])
    q=q+"};\r"
    q=q+"        uint8_t _Srv_client_res_Type["+str(len(Idsrv))+"]["+str(getMaxNdata(dataType_srv_res))+"]="+Arraymaptype(dataType_srv_res)
    q=q+"        uint8_t _Totalvar_srv_client_res["+str(len(Idsrv))+"]="+ArraytotalVar(dataType_srv_res)
    q=q+"        uint8_t _Nofdata_srv_client_res["+str(len(Idsrv))+"]["+str(getMaxNdata(dataType_srv_res))+"]="+str(NofData_srv_res).replace("[","{").replace("]","}")+";\r"
    q=q+"        void* _nonverify_srv_client_state["+str(len(Idsrv))+"];\r"
    q=q+"        void* _verify_srv_client_state["+str(len(Idsrv))+"];\r"
    fw.write(q)
    return 1
def gen_privateStruct_action_client(fw):
    Idaction_client,nameaction_client,interfaceaction_client,dataType_action_client_req,dataName_action_client_req,datagrab_action_client_req,NofData_action_client_req,datatypeProtocol_action_client_req,bytetograb_action_client_req,dataType_action_client_res,dataName_action_client_res,datagrab_action_client_res,NofData_action_client_res,datatypeProtocol_action_client_res,bytetograb_action_client_res,dataType_action_client_feed,dataName_action_client_feed,datagrab_action_client_feed,NofData_action_client_feed,datatypeProtocol_action_client_feed,bytetograb_action_client_feed,timeOut_action_client = setup_action_client_protocol()
    fw.write("\r\r\r        // gen action client feed res\r")
    q="        void* _nonverify_action_client_res["+str(len(Idaction_client))+"]["+str(getMaxNdata(dataType_action_client_res))+"]["+str(getMaxofArray(NofData_action_client_res))+"];\r"
    q=q+"        void* _verify_action_client_res["+str(len(Idaction_client))+"]["+str(getMaxNdata(dataType_action_client_res))+"]["+str(getMaxofArray(NofData_action_client_res))+"];\r"
    q=q+"        uint8_t _Idaction_client["+str(len(Idaction_client))+"]={"
    for i in range (0,len(Idaction_client)):
        if(i<len(Idaction_client)-1):
            q=q+str(Idaction_client[i])+","
        else:
            q=q+str(Idaction_client[i])
    q=q+"};\r"
    q=q+"        uint8_t _Action_client_res_Type["+str(len(Idaction_client))+"]["+str(getMaxNdata(dataType_action_client_res))+"]="+Arraymaptype(dataType_action_client_res)
    q=q+"        uint8_t _Totalvar_action_client_res["+str(len(Idaction_client))+"]="+ArraytotalVar(dataType_action_client_res)
    q=q+"        uint8_t _Nofdata_action_client_res["+str(len(Idaction_client))+"]["+str(getMaxNdata(dataType_action_client_res))+"]="+str(NofData_action_client_res).replace("[","{").replace("]","}")+";\r"
  
    q=q+"        void* _nonverify_action_client_feed["+str(len(Idaction_client))+"]["+str(getMaxNdata(dataType_action_client_feed))+"]["+str(getMaxofArray(NofData_action_client_feed))+"];\r"
    q=q+"        void* _verify_action_client_feed["+str(len(Idaction_client))+"]["+str(getMaxNdata(dataType_action_client_feed))+"]["+str(getMaxofArray(NofData_action_client_feed))+"];\r"
    q=q+"        uint8_t _Action_client_feed_Type["+str(len(Idaction_client))+"]["+str(getMaxNdata(dataType_action_client_feed))+"]="+Arraymaptype(dataType_action_client_feed)
    q=q+"        uint8_t _Totalvar_action_client_feed["+str(len(Idaction_client))+"]="+ArraytotalVar(dataType_action_client_feed)
    q=q+"        uint8_t _Nofdata_action_client_feed["+str(len(Idaction_client))+"]["+str(getMaxNdata(dataType_action_client_feed))+"]="+str(NofData_action_client_feed).replace("[","{").replace("]","}")+";\r"

    
    q=q+"        void* _nonverify_action_client_state["+str(len(Idaction_client))+"];\r"
    q=q+"        void* _verify_action_client_state["+str(len(Idaction_client))+"];\r"
    fw.write(q)
    return 1

def gen_privateStruct_action_server(fw):
    Idaction_server,nameaction_server,interfaceaction_server,dataType_action_server_req,dataName_action_server_req,datagrab_action_server_req,NofData_action_server_req,datatypeProtocol_action_server_req,bytetograb_action_server_req,dataType_action_server_res,dataName_action_server_res,datagrab_action_server_res,NofData_action_server_res,datatypeProtocol_action_server_res,bytetograb_action_server_res,dataType_action_server_feed,dataName_action_server_feed,datagrab_action_server_feed,NofData_action_server_feed,datatypeProtocol_action_server_feed,bytetograb_action_server_feed,timeOut_action_server = setup_action_server_protocol()
    fw.write("\r\r\r        // gen action server goal\r")
    q="        void* _nonverify_action_server_req["+str(len(Idaction_server))+"]["+str(getMaxNdata(dataType_action_server_req))+"]["+str(getMaxofArray(NofData_action_server_req))+"];\r"
    q=q+"        void* _verify_action_server_req["+str(len(Idaction_server))+"]["+str(getMaxNdata(dataType_action_server_req))+"]["+str(getMaxofArray(NofData_action_server_req))+"];\r"
    q=q+"        uint8_t _Idaction_server["+str(len(Idaction_server))+"]={"
    for i in range (0,len(Idaction_server)):
        if(i<len(Idaction_server)-1):
            q=q+str(Idaction_server[i])+","
        else:
            q=q+str(Idaction_server[i])
    q=q+"};\r"
    q=q+"        uint8_t _Action_server_req_Type["+str(len(Idaction_server))+"]["+str(getMaxNdata(dataType_action_server_req))+"]="+Arraymaptype(dataType_action_server_req)
    q=q+"        uint8_t _Totalvar_action_server_req["+str(len(Idaction_server))+"]="+ArraytotalVar(dataType_action_server_req)
    q=q+"        uint8_t _Nofdata_action_server_req["+str(len(Idaction_server))+"]["+str(getMaxNdata(dataType_action_server_req))+"]="+str(NofData_action_server_req).replace("[","{").replace("]","}")+";\r"
    
    q=q+"        void* _nonverify_action_server_state["+str(len(Idaction_server))+"];\r"
    q=q+"        void* _verify_action_server_state["+str(len(Idaction_server))+"];\r"
    fw.write(q)
    return 1
def gen_privateStruct_srv_server_req(fw):
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res=setup_srv_server_protocol()
    # print(Nofdata)
    fw.write("\r\r\r        // gen server req\r")
    q="        void* _nonverify_srv_server_req["+str(len(Idsrv))+"]["+str(getMaxNdata(dataType_srv_req))+"]["+str(getMaxofArray(NofData_srv_req))+"];\r"
    q=q+"        void* _verify_srv_server_req["+str(len(Idsrv))+"]["+str(getMaxNdata(dataType_srv_req))+"]["+str(getMaxofArray(NofData_srv_req))+"];\r"
    q=q+"        uint8_t _Idsrv_server["+str(len(Idsrv))+"]={"
    for i in range (0,len(Idsrv)):
        if(i<len(Idsrv)-1):
            q=q+str(Idsrv[i])+","
        else:
            q=q+str(Idsrv[i])
    q=q+"};\r"
    q=q+"        uint8_t _Srv_server_req_Type["+str(len(Idsrv))+"]["+str(getMaxNdata(dataType_srv_req))+"]="+Arraymaptype(dataType_srv_req)
    q=q+"        uint8_t _Totalvar_srv_server_req["+str(len(Idsrv))+"]="+ArraytotalVar(dataType_srv_req)
    q=q+"        uint8_t _Nofdata_srv_server_req["+str(len(Idsrv))+"]["+str(getMaxNdata(dataType_srv_req))+"]="+str(NofData_srv_req).replace("[","{").replace("]","}")+";\r"
    q=q+"        void* _nonverify_srv_server_state["+str(len(Idsrv))+"];\r"
    q=q+"        void* _verify_srv_server_state["+str(len(Idsrv))+"];\r"
    fw.write(q)
    return 1
def publicStructToprivateStruct(fw,q):
    w=""
    tt=1
    fw.write("\r\r\r        // gen private struct sub\r")
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

def  publicStructToprivateStruct_srv(fw,q):
    w=""
    tt=1
    fw.write("\r\r\r        // gen private struct srv\r")
    for i in range(0,len(q)):
        e=""
        for j in range(0,len(q[i])):
            if(q[i][j]=="}" and q[i][j+1]!=";" and q[i][j+2]=="S" and q[i][j+3]=="e" and q[i][j+4]=="r"):
                e=e+"}_"
                tt=0
            elif(tt):
                e=e+q[i][j]
            else:
                tt=1
        w=w+e
    fw.write(w)
    return 1

def publicStructToprivateStruct_action(fw,q):
    w=""
    tt=1
    fw.write("\r\r\r        // gen private struct action\r")
    for i in range(0,len(q)):
        e=""
        for j in range(0,len(q[i])):
            if(q[i][j]=="}" and q[i][j+1]!=";" and q[i][j+2]=="A" and q[i][j+3]=="c" and q[i][j+4]=="t"):
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
    setup_srv=get_params('ros.srv_client')
    Idmcu=get_params("microcontroller.idmcu")
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

def setup_srv_server_protocol():
    setup_srv=get_params('ros.srv_server')
    Idmcu=get_params("microcontroller.idmcu")
    Idsrv=[]
    namesrv=[]
    interfacesrv=[]
    for i in range(0,len(setup_srv)):
        Idsrv.append(setup_srv[i][0])
        namesrv.append(setup_srv[i][1])
        interfacesrv.append(setup_srv[i][2])
    print('Done load YAML srv_server.')
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
    print('Done load YAML action client.')
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
                a,b=typetoProtocol_2(dataType[i][j],NofData[i][j])
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
    print('Done load YAML action server.')
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
                a,b=typetoProtocol_2(dataType[i][j],NofData[i][j])
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




def genvoid_begin_srv_server_h(fw):
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res = setup_srv_server_protocol()
    fw.write("\r\r\r        // gen void begin srv server\r")
    if(len(namesrv)>0):
        fw.write("        void begin_service_server(")
    for i in range(0,len(namesrv)):
        fw.write("void* server_"+namesrv[i])
        if(i<len(namesrv)-1):
            fw.write(",")
        else:
            fw.write(");\r")
    return 1
def genvoid_begin_action_server_h(fw):
    Idaction_server,nameaction_server,interfaceaction_server,dataType_action_server_req,dataName_action_server_req,datagrab_action_server_req,NofData_action_server_req,datatypeProtocol_action_server_req,bytetograb_action_server_req,dataType_action_server_res,dataName_action_server_res,datagrab_action_server_res,NofData_action_server_res,datatypeProtocol_action_server_res,bytetograb_action_server_res,dataType_action_server_feed,dataName_action_server_feed,datagrab_action_server_feed,NofData_action_server_feed,datatypeProtocol_action_server_feed,bytetograb_action_server_feed,timeOut_action_server = setup_action_server_protocol()
    fw.write("\r\r\r        // gen void begin action server\r")
    if(len(nameaction_server)>0):
        fw.write("        void begin_action_server(")
    for i in range(0,len(nameaction_server)):
        fw.write("void* server_"+nameaction_server[i])
        if(i<len(nameaction_server)-1):
            fw.write(",")
        else:
            fw.write(");\r")
    return 1
def genvoid_begin_srv_server_cpp(fw):
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res = setup_srv_server_protocol()
    fw.write("\r\r\r// gen void begin srv server\r")
    if(len(namesrv)>0):
        fw.write("void Xicro::begin_service_server(")
    for i in range(0,len(namesrv)):
        fw.write("void* server_"+namesrv[i])
        if(i<len(namesrv)-1):
            fw.write(",")
        else:
            fw.write("){\r")
            for i in range(0,len(namesrv)):
                fw.write("    _service_server["+str(i)+"]=server_"+namesrv[i]+";\r")
            fw.write("\r}\r")
    return 1
def genvoid_begin_action_server_cpp(fw):
    Idaction_server,nameaction_server,interfaceaction_server,dataType_action_server_req,dataName_action_server_req,datagrab_action_server_req,NofData_action_server_req,datatypeProtocol_action_server_req,bytetograb_action_server_req,dataType_action_server_res,dataName_action_server_res,datagrab_action_server_res,NofData_action_server_res,datatypeProtocol_action_server_res,bytetograb_action_server_res,dataType_action_server_feed,dataName_action_server_feed,datagrab_action_server_feed,NofData_action_server_feed,datatypeProtocol_action_server_feed,bytetograb_action_server_feed,timeOut_action_server = setup_action_server_protocol()
    fw.write("\r\r\r// gen void begin action server\r")
    if(len(nameaction_server)>0):
        fw.write("void Xicro::begin_action_server(")
    for i in range(0,len(nameaction_server)):
        fw.write("void* server_"+nameaction_server[i])
        if(i<len(nameaction_server)-1):
            fw.write(",")
        else:
            fw.write("){\r")
            for i in range(0,len(nameaction_server)):
                fw.write("    _action_server["+str(i)+"]=server_"+nameaction_server[i]+";\r")
            fw.write("\r}\r")
    return 1
def genpointer_srv_server(fw):
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res = setup_srv_server_protocol()
    fw.write("\r\r        // gen pointer srv server void\r")
    fw.write("        void* _service_server["+str(len(namesrv))+"];\r\r\r")
    return 1
def genpointer_action_server(fw):
    Idaction_server,nameaction_server,interfaceaction_server,dataType_action_server_req,dataName_action_server_req,datagrab_action_server_req,NofData_action_server_req,datatypeProtocol_action_server_req,bytetograb_action_server_req,dataType_action_server_res,dataName_action_server_res,datagrab_action_server_res,NofData_action_server_res,datatypeProtocol_action_server_res,bytetograb_action_server_res,dataType_action_server_feed,dataName_action_server_feed,datagrab_action_server_feed,NofData_action_server_feed,datatypeProtocol_action_server_feed,bytetograb_action_server_feed,timeOut_action_server = setup_action_server_protocol()
    fw.write("\r\r        // gen pointer srv server void\r")
    fw.write("        void* _action_server["+str(len(nameaction_server))+"];\r\r\r")
    return 1
def create_hFile(listVoid,Idmcu,listVoid_client_req,listVoid_server_res,listVoid_action_client_req,listVoid_action_server_feed,listVoid_action_server_res):
    try:
        path = mkdir()
        path = path +"/Xicro_"+get_params("microcontroller.namespace")+"_ID_"+str(Idmcu)+".h"
       
        fw  = open(path, "w+")
        # if(input.mcu_type=="stm32"):
        #     pathr = os.path.join(get_package_share_directory('xicro_pkg'),'config', '.stm32_h_preSetup.txt')
        # else:
        #     pathr = os.path.join(get_package_share_directory('xicro_pkg'),'config', '.arduino_h_preSetup.txt')
        pathr = os.path.join(get_package_share_directory('xicro_pkg'),'config', '.library_h_preSetup.xicro')
        fr=open(pathr, 'r') 
        fw.write("// ***************************************************************************************************************************************************\r")
        fw.write("//      |              This script was auto-generated by generate_library.py which received parameters from setup_xicro.yaml                   |\r")
        fw.write("//      |                                         EDITING THIS FILE BY HAND IS NOT RECOMMENDED                                                 |\r")
        fw.write("// ***************************************************************************************************************************************************\r\r")
        fw.write("\r\r#ifndef "+path[1:len(path)-2].split("/")[-1].upper()+"_H\r")
        fw.write("#define "+path[1:len(path)-2].split("/")[-1].upper()+"_H\r")
        public_struct=[]
        public_struct_srv_client=[]
        public_struct_srv_server=[]
        public_struct_action_client=[]
        public_struct_action_server=[]
        c=0
        for line in fr:
            c=c+1
            if(line=="!#@ gen_struct\n"):
                try:
                    fw.write("\r\r\r        // gen public pub void\r")
                    for i in range(0,len(listVoid)):
                        fw.write(listVoid[i])
                        fw.write("\n")
                    print("gen voidPub Done")
                    create_hstruct_pub(fw)
                    public_struct=create_hstruct(fw)
                    print("gen public_struct srv client Done")
                    public_struct_srv_client=create_hstruct_srv_client(fw)
                    print("gen client_struct Done")
                    fw.write("\r\r\r        // gen service call void\r")
                    for i in range(0,len(listVoid_client_req)):
                        fw.write(listVoid_client_req[i])
                        fw.write("\n")
                    fw.write("\r\r")
                    public_struct_srv_server=create_hstruct_srv_server(fw)
                    print("gen public_struct srv server Done")
                    genvoid_begin_srv_server_h(fw)
                    print("gen begin srv server Done.")
                    fw.write("\r\r\r        // gen service server response void\r")
                    for i in range(0,len(listVoid_server_res)):
                        fw.write(listVoid_server_res[i])
                        fw.write("\n")
                    print("gen service server response Done")    
                    fw.write("\r\r\r        // gen action client call void\r")
                    for i in range(0,len(listVoid_action_client_req)):
                        fw.write(listVoid_action_client_req[i])
                        fw.write("\n")
                    print("gen action call void Done")
                    public_struct_action_client=create_hstruct_action_client(fw)
                    public_struct_action_server=create_hstruct_action_server(fw)
                    genvoid_begin_action_server_h(fw)
                    fw.write("\r\r\r        // gen action server feedback void\r")
                    for i in range(0,len(listVoid_action_server_feed)):
                        fw.write(listVoid_action_server_feed[i])
                        fw.write("\n")
                    print("gen action server feedback void Done")
                    fw.write("\r\r\r        // gen action server response void\r")
                    for i in range(0,len(listVoid_action_server_res)):
                        fw.write(listVoid_action_server_res[i])
                        fw.write("\n")
                    print("gen action server response void Done")

                    print("gen public_struct action client Done")
                except:
                    print("gen public_struct or voidPub Fail.")
            elif(line=="!#@ gen_private_struct\n"):
                try:
                    gen_privateStruct(fw)
                    gen_privateStruct_srv_client_res(fw)
                    gen_privateStruct_srv_server_req(fw)
                    publicStructToprivateStruct(fw,public_struct)
                    publicStructToprivateStruct_srv(fw,public_struct_srv_client)
                    publicStructToprivateStruct_srv(fw,public_struct_srv_server)
                    publicStructToprivateStruct_action(fw,public_struct_action_client)
                    publicStructToprivateStruct_action(fw,public_struct_action_server)
                    genpointer_srv_server(fw)
                    gen_privateStruct_action_client(fw)
                    genpointer_action_server(fw)
                    gen_privateStruct_action_server(fw)

                    print("gen private_struct Done")
                except:
                    print("gen private_struct Fail")
            elif(line=="!#@ gendefine_Idmcu\n"):
                fw.write("        uint8_t _Idmcu=" +str(Idmcu)+";\n\r")
            elif(line=="!#@ gen_type\n" and input.mcu_type=="stm32"):
                fw.write("#include "+'"' + input.module_name+'"\r')
                fw.write("#include \"string\"\r")
                fw.write("#include \"string.h\"\r")
                fw.write("#include \"math.h\"\r")
                fw.write("#include \"stdbool.h\"\r")
                fw.write("#define __UART_TYPE UART_HandleTypeDef\n")
                fw.write("#define __STR_TYPE std::string\n\n")
            elif(line=="!#@ gen_type\n" and (input.mcu_type=="arduino" or input.mcu_type=="esp")):
                fw.write('\n\n#include "Arduino.h" \n')
                if(get_params("microcontroller.connection.type") == "UART"):
                    fw.write("#define __UART_TYPE Stream\n")
                elif(get_params("microcontroller.connection.type") == "UDP"):
                    fw.write("#include <WiFiUdp.h>\n#define __UART_TYPE WiFiUDP\n")
                fw.write("#define __STR_TYPE String\n\n")
            elif(line=="!#@ gen_double\n"and input.mcu_type=="stm32"):
                fw.write("        void _SendDouble(double *data,uint8_t len);\n")
            elif((line=="!#@ gen_double\n" or line=="!#@ gen_uart_buff_dma\n")and (input.mcu_type=="arduino" or input.mcu_type=="esp")):
                pass
            elif(line=="!#@ gen_uart_buff_dma\n" and input.mcu_type=="stm32"):
                fw.write("\n        uint8_t _UartBuff[64]={0};\n")
                fw.write("        uint8_t _Posdata=0;\n")
                fw.write("        uint8_t _Posdatapre=0;\n\n")
            elif(line=="!#@ gen_void_begin_h\n" and get_params("microcontroller.connection.type") == "UART"):
                fw.write("        void begin(__UART_TYPE *SerialObject);\n")
            elif(line=="!#@ gen_void_begin_h\n" and get_params("microcontroller.connection.type") == "UDP"):
                fw.write("        void begin(__UART_TYPE *SerialObject,char *udpAddress,int udpPort);\n")
                fw.write("        char * _udpAddress;\n        int _udpPort;\n")
            elif(line=="!#@ gen_udp_buff\n" and get_params("microcontroller.connection.type") == "UART" ):
                pass
            elif(line=="!#@ gen_udp_buff\n" and get_params("microcontroller.connection.type") == "UDP" ):
                fw.write("        uint8_t _buffer_udp[1000]={0};\n        uint16_t _num_udp=0;\n")
                fw.write("        uint8_t _buff[1000]={0};\n")
                fw.write("        uint16_t _Posdata=0;\n        uint16_t _Posdatapre=0;\n")
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
    fw.write("\r    // gen pointer sub\r")
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
                    q=q+"    _nonverify["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Subscription_"+nameofTopic[i]+".message."+dataName[i][j]+";\r"
                    w=w+"    _verify["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Subscription_"+nameofTopic[i]+".message."+dataName[i][j]+";\r"
                else:
                    q=q+"    _nonverify["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Subscription_"+nameofTopic[i]+".message."+dataName[i][j]+"["+str(k) +"];\r"
                    w=w+"    _verify["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Subscription_"+nameofTopic[i]+".message."+dataName[i][j]+"["+str(k) +"];\r"
    q=q+"\r\r"
    q=q+w
    fw.write(q)
    fw.write("\r\r\r")
    return 1

def genPointer_srv_client_res(fw):
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res=setup_srv_protocol()
    fw.write("\r    // gen pointer srv client res\r")
    q=""
    w=""
    for i in range(0,len(Idsrv)):
        for j in range(0,len(dataName_srv_res[i])):
            if(dataName_srv_res[i][j].find("__of__")!=-1):
                dataName_srv_res[i][j]=dataName_srv_res[i][j].replace("__of__",".")
    for i in range(0,len(Idsrv)):
        for j in range(0,len(dataName_srv_res[i])):
            for k in range(0,NofData_srv_res[i][j]):
                if(NofData_srv_res[i][j]==1 and  dataName_srv_res[i][j]=="xxicro_Empty"):
                    q=q+"    _nonverify_srv_client_res["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Service_client_"+namesrv[i]+".response"+";\r"
                    w=w+"    _verify_srv_client_res["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Service_client_"+namesrv[i]+".response"+";\r"
                elif(NofData_srv_res[i][j]==1):
                    q=q+"    _nonverify_srv_client_res["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Service_client_"+namesrv[i]+".response."+dataName_srv_res[i][j]+";\r"
                    w=w+"    _verify_srv_client_res["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Service_client_"+namesrv[i]+".response."+dataName_srv_res[i][j]+";\r"
                else:
                    q=q+"    _nonverify_srv_client_res["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Service_client_"+namesrv[i]+".response."+dataName_srv_res[i][j]+"["+str(k) +"];\r"
                    w=w+"    _verify_srv_client_res["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Service_client_"+namesrv[i]+".response."+dataName_srv_res[i][j]+"["+str(k) +"];\r"
        q=q+"    _nonverify_srv_client_state["+str(i)+"]=&_Service_client_"+namesrv[i]+".state"+";\r"
        w=w+"    _verify_srv_client_state["+str(i)+"]=&Service_client_"+namesrv[i]+".state"+";\r"
    q=q+"\r\r"
    q=q+w
    fw.write(q)
    fw.write("\r\r\r")
    return 1
def genPointer_action_client(fw):
    Idaction_client,nameaction_client,interfaceaction_client,dataType_action_client_req,dataName_action_client_req,datagrab_action_client_req,NofData_action_client_req,datatypeProtocol_action_client_req,bytetograb_action_client_req,dataType_action_client_res,dataName_action_client_res,datagrab_action_client_res,NofData_action_client_res,datatypeProtocol_action_client_res,bytetograb_action_client_res,dataType_action_client_feed,dataName_action_client_feed,datagrab_action_client_feed,NofData_action_client_feed,datatypeProtocol_action_client_feed,bytetograb_action_client_feed,timeOut_action_client = setup_action_client_protocol()
    fw.write("\r    // gen pointer action client feed\r")
    q=""
    w=""
    for i in range(0,len(Idaction_client)):
        for j in range(0,len(dataName_action_client_feed[i])):
            if(dataName_action_client_feed[i][j].find("__of__")!=-1):
                dataName_action_client_feed[i][j]=dataName_action_client_feed[i][j].replace("__of__",".")
    for i in range(0,len(Idaction_client)):
        for j in range(0,len(dataName_action_client_feed[i])):
            for k in range(0,NofData_action_client_feed[i][j]):
                if(NofData_action_client_feed[i][j]==1 and  dataName_action_client_feed[i][j]=="xxicro_Empty"):
                    q=q+"    _nonverify_action_client_feed["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Action_client_"+nameaction_client[i]+".feedback"+";\r"
                    w=w+"    _verify_action_client_feed["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Action_client_"+nameaction_client[i]+".feedback"+";\r"
                elif(NofData_action_client_feed[i][j]==1):
                    q=q+"    _nonverify_action_client_feed["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Action_client_"+nameaction_client[i]+".feedback."+dataName_action_client_feed[i][j]+";\r"
                    w=w+"    _verify_action_client_feed["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Action_client_"+nameaction_client[i]+".feedback."+dataName_action_client_feed[i][j]+";\r"
                else:
                    q=q+"    _nonverify_action_client_feed["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Action_client_"+nameaction_client[i]+".feedback."+dataName_action_client_feed[i][j]+"["+str(k) +"];\r"
                    w=w+"    _verify_action_client_feed["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Action_client_"+nameaction_client[i]+".feedback."+dataName_action_client_feed[i][j]+"["+str(k) +"];\r"
       
    for i in range(0,len(Idaction_client)):
        for j in range(0,len(dataName_action_client_res[i])):
            if(dataName_action_client_res[i][j].find("__of__")!=-1):
                dataName_action_client_res[i][j]=dataName_action_client_res[i][j].replace("__of__",".")
    for i in range(0,len(Idaction_client)):
        for j in range(0,len(dataName_action_client_res[i])):
            for k in range(0,NofData_action_client_res[i][j]):
                if(NofData_action_client_res[i][j]==1 and  dataName_action_client_res[i][j]=="xxicro_Empty"):
                    q=q+"    _nonverify_action_client_res["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Action_client_"+nameaction_client[i]+".result"+";\r"
                    w=w+"    _verify_action_client_res["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Action_client_"+nameaction_client[i]+".result"+";\r"
                elif(NofData_action_client_res[i][j]==1):
                    q=q+"    _nonverify_action_client_res["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Action_client_"+nameaction_client[i]+".result."+dataName_action_client_res[i][j]+";\r"
                    w=w+"    _verify_action_client_res["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Action_client_"+nameaction_client[i]+".result."+dataName_action_client_res[i][j]+";\r"
                else:
                    q=q+"    _nonverify_action_client_res["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Action_client_"+nameaction_client[i]+".result."+dataName_action_client_res[i][j]+"["+str(k) +"];\r"
                    w=w+"    _verify_action_client_res["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Action_client_"+nameaction_client[i]+".result."+dataName_action_client_res[i][j]+"["+str(k) +"];\r"


        q=q+"    _nonverify_action_client_state["+str(i)+"]=&_Action_client_"+nameaction_client[i]+".state"+";\r"
        w=w+"    _verify_action_client_state["+str(i)+"]=&Action_client_"+nameaction_client[i]+".state"+";\r"
    q=q+"\r\r"
    q=q+w
    fw.write(q)
    fw.write("\r\r\r")

    return 1
def genPointer_action_server(fw):
    Idaction_server,nameaction_server,interfaceaction_server,dataType_action_server_req,dataName_action_server_req,datagrab_action_server_req,NofData_action_server_req,datatypeProtocol_action_server_req,bytetograb_action_server_req,dataType_action_server_res,dataName_action_server_res,datagrab_action_server_res,NofData_action_server_res,datatypeProtocol_action_server_res,bytetograb_action_server_res,dataType_action_server_feed,dataName_action_server_feed,datagrab_action_server_feed,NofData_action_server_feed,datatypeProtocol_action_server_feed,bytetograb_action_server_feed,timeOut_action_server = setup_action_server_protocol()
    fw.write("\r    // gen pointer action server req\r")
    q=""
    w=""
    for i in range(0,len(Idaction_server)):
        for j in range(0,len(dataName_action_server_req[i])):
            if(dataName_action_server_req[i][j].find("__of__")!=-1):
                dataName_action_server_req[i][j]=dataName_action_server_req[i][j].replace("__of__",".")
    for i in range(0,len(Idaction_server)):
        for j in range(0,len(dataName_action_server_req[i])):
            for k in range(0,NofData_action_server_req[i][j]):
                if(NofData_action_server_req[i][j]==1 and  dataName_action_server_req[i][j]=="xxicro_Empty"):
                    q=q+"    _nonverify_action_server_req["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Action_server"+nameaction_server[i]+".request"+";\r"
                    w=w+"    _verify_action_server_req["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Action_server_"+nameaction_server[i]+".request"+";\r"
                elif(NofData_action_server_req[i][j]==1):
                    q=q+"    _nonverify_action_server_req["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Action_server_"+nameaction_server[i]+".request."+dataName_action_server_req[i][j]+";\r"
                    w=w+"    _verify_action_server_req["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Action_server_"+nameaction_server[i]+".request."+dataName_action_server_req[i][j]+";\r"
                else:
                    q=q+"    _nonverify_action_server_req["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Action_server_"+nameaction_server[i]+".request."+dataName_action_server_req[i][j]+"["+str(k) +"];\r"
                    w=w+"    _verify_action_server_req["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Action_server_"+nameaction_server[i]+".request."+dataName_action_server_req[i][j]+"["+str(k) +"];\r"
        q=q+"    _nonverify_action_server_state["+str(i)+"]=&_Action_server_"+nameaction_server[i]+".state"+";\r"
        w=w+"    _verify_action_server_state["+str(i)+"]=&Action_server_"+nameaction_server[i]+".state"+";\r"
    q=q+"\r\r"
    q=q+w
    fw.write(q)
    fw.write("\r\r\r")
    return 1
def genPointer_srv_server_req(fw):
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res=setup_srv_server_protocol()
    fw.write("\r    // gen pointer srv server req\r")
    q=""
    w=""
    for i in range(0,len(Idsrv)):
        for j in range(0,len(dataName_srv_req[i])):
            if(dataName_srv_req[i][j].find("__of__")!=-1):
                dataName_srv_req[i][j]=dataName_srv_req[i][j].replace("__of__",".")
    for i in range(0,len(Idsrv)):
        for j in range(0,len(dataName_srv_req[i])):
            for k in range(0,NofData_srv_req[i][j]):
                if(NofData_srv_req[i][j]==1 and  dataName_srv_req[i][j]=="xxicro_Empty"):
                    q=q+"    _nonverify_srv_server_req["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Service_server"+namesrv[i]+".request"+";\r"
                    w=w+"    _verify_srv_server_req["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Service_server_"+namesrv[i]+".request"+";\r"
                elif(NofData_srv_req[i][j]==1):
                    q=q+"    _nonverify_srv_server_req["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Service_server_"+namesrv[i]+".request."+dataName_srv_req[i][j]+";\r"
                    w=w+"    _verify_srv_server_req["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Service_server_"+namesrv[i]+".request."+dataName_srv_req[i][j]+";\r"
                else:
                    q=q+"    _nonverify_srv_server_req["+str(i)+"]["+str(j)+"]["+ str(k) +"]=&_Service_server_"+namesrv[i]+".request."+dataName_srv_req[i][j]+"["+str(k) +"];\r"
                    w=w+"    _verify_srv_server_req["+str(i)+"]["+str(j)+"]["+str(k) +"]=&Service_server_"+namesrv[i]+".request."+dataName_srv_req[i][j]+"["+str(k) +"];\r"
        q=q+"    _nonverify_srv_server_state["+str(i)+"]=&_Service_server_"+namesrv[i]+".state"+";\r"
        w=w+"    _verify_srv_server_state["+str(i)+"]=&Service_server_"+namesrv[i]+".state"+";\r"
    q=q+"\r\r"
    q=q+w
    fw.write(q)
    fw.write("\r\r\r")
    return 1

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
            cond=j<len(dataType_srv_req[i]) -1 #check flag continue or stop
            # print(dataType_srv_req[i][j],dataName_srv_req[i][j],NofData_srv_req[i][j],cond)
            fw.write(typetoVoid(dataType_srv_req[i][j],dataName_srv_req[i][j],NofData_srv_req[i][j],cond,"Service_client_"+namesrv[i]+".request"))
            if(dataType_srv_req[i][j]=="bool" and NofData_srv_req[i][j]==1 ):
                fw.write("// auto by 1 bool\n")
            elif(cond):
                fw.write("    _Sendcontinue();\n")
            else:
                fw.write("    _Sendstop();\n")
        fw.write("    _Sendcrc();\r")
        fw.write("}\n")

def genvoidAction_call(fw,listVoid_action_client_req,id_mcu):
    Idaction_client,nameaction_client,interfaceaction_client,dataType_action_client_req,dataName_action_client_req,datagrab_action_client_req,NofData_action_client_req,datatypeProtocol_action_client_req,bytetograb_action_client_req,dataType_action_client_res,dataName_action_client_res,datagrab_action_client_res,NofData_action_client_res,datatypeProtocol_action_client_res,bytetograb_action_client_res,dataType_action_client_feed,dataName_action_client_feed,datagrab_action_client_feed,NofData_action_client_feed,datatypeProtocol_action_client_feed,bytetograb_action_client_feed,timeOut_action_client = setup_action_client_protocol()
    for i in range(0,len(listVoid_action_client_req)):
        # print(listVoid[i][8:12])
        fw.write(listVoid_action_client_req[i][8:12]+" Xicro::"+listVoid_action_client_req[i][13:len(listVoid_action_client_req[i])-1])
        fw.write(("{\n"))
        fw.write("    _crc=0;\r")
        fw.write("    _Sendstart();\n")
        fw.write("    _SendSignature("+str(id_mcu)+",5);\n")
        fw.write("    _SendIdTopic("+str(Idaction_client[i])+");\n")
        for j in range(0,len(dataType_action_client_req[i])):
            cond=j<len(dataType_action_client_req[i]) -1 #check flag continue or stop
            # print(dataType_srv_req[i][j],dataName_srv_req[i][j],NofData_srv_req[i][j],cond)
            fw.write(typetoVoid(dataType_action_client_req[i][j],dataName_action_client_req[i][j],NofData_action_client_req[i][j],cond,"Action_client_"+nameaction_client[i]+".request"))
            if(dataType_action_client_req[i][j]=="bool" and NofData_action_client_req[i][j]==1 ):
                fw.write("// auto by 1 bool\n")
            elif(cond):
                fw.write("    _Sendcontinue();\n")
            else:
                fw.write("    _Sendstop();\n")
        fw.write("    _Sendcrc();\r")
        fw.write("}\n")
    return 1
def genvoidAction_server_feed(fw,listVoid_action_server_feed,id_mcu):
    Idaction_server,nameaction_server,interfaceaction_server,dataType_action_server_req,dataName_action_server_req,datagrab_action_server_req,NofData_action_server_req,datatypeProtocol_action_server_req,bytetograb_action_server_req,dataType_action_server_res,dataName_action_server_res,datagrab_action_server_res,NofData_action_server_res,datatypeProtocol_action_server_res,bytetograb_action_server_res,dataType_action_server_feed,dataName_action_server_feed,datagrab_action_server_feed,NofData_action_server_feed,datatypeProtocol_action_server_feed,bytetograb_action_server_feed,timeOut_action_server = setup_action_server_protocol()
    for i in range(0,len(listVoid_action_server_feed)):
        # print(listVoid[i][8:12])
        fw.write(listVoid_action_server_feed[i][8:12]+" Xicro::"+listVoid_action_server_feed[i][13:len(listVoid_action_server_feed[i])-1])
        fw.write(("{\n"))
        fw.write("    _crc=0;\r")
        fw.write("    _Sendstart();\n")
        fw.write("    _SendSignature("+str(id_mcu)+",9);\n")
        fw.write("    _SendIdTopic("+str(Idaction_server[i])+");\n")
        for j in range(0,len(dataType_action_server_feed[i])):
            cond=j<len(dataType_action_server_feed[i]) -1 #check flag continue or stop
            # print(dataType_srv_req[i][j],dataName_srv_req[i][j],NofData_srv_req[i][j],cond)
            fw.write(typetoVoid(dataType_action_server_feed[i][j],dataName_action_server_feed[i][j],NofData_action_server_feed[i][j],cond,"Action_server_"+nameaction_server[i]+".feedback"))
            if(dataType_action_server_feed[i][j]=="bool" and NofData_action_server_feed[i][j]==1 ):
                fw.write("// auto by 1 bool\n")
            elif(cond):
                fw.write("    _Sendcontinue();\n")
            else:
                fw.write("    _Sendstop();\n")
        fw.write("    _Sendcrc();\r")
        fw.write("}\n")
    return 1

def genvoidAction_server_res(fw,listVoid_action_server_res,id_mcu):
    Idaction_server,nameaction_server,interfaceaction_server,dataType_action_server_req,dataName_action_server_req,datagrab_action_server_req,NofData_action_server_req,datatypeProtocol_action_server_req,bytetograb_action_server_req,dataType_action_server_res,dataName_action_server_res,datagrab_action_server_res,NofData_action_server_res,datatypeProtocol_action_server_res,bytetograb_action_server_res,dataType_action_server_feed,dataName_action_server_feed,datagrab_action_server_feed,NofData_action_server_feed,datatypeProtocol_action_server_feed,bytetograb_action_server_feed,timeOut_action_server = setup_action_server_protocol()
    for i in range(0,len(listVoid_action_server_res)):
        # print(listVoid[i][8:12])
        fw.write(listVoid_action_server_res[i][8:12]+" Xicro::"+listVoid_action_server_res[i][13:len(listVoid_action_server_res[i])-1])
        fw.write(("{\n"))
        fw.write("    _crc=0;\r")
        fw.write("    _Sendstart();\n")
        fw.write("    _SendSignature("+str(id_mcu)+",10);\n")
        fw.write("    _SendIdTopic("+str(Idaction_server[i])+");\n")
        for j in range(0,len(dataType_action_server_res[i])):
            cond=j<len(dataType_action_server_res[i]) -1 #check flag continue or stop
            # print(dataType_srv_req[i][j],dataName_srv_req[i][j],NofData_srv_req[i][j],cond)
            fw.write(typetoVoid(dataType_action_server_res[i][j],dataName_action_server_res[i][j],NofData_action_server_res[i][j],cond,"Action_server_"+nameaction_server[i]+".result"))
            if(dataType_action_server_res[i][j]=="bool" and NofData_action_server_res[i][j]==1 ):
                fw.write("// auto by 1 bool\n")
            elif(cond):
                fw.write("    _Sendcontinue();\n")
            else:
                fw.write("    _Sendstop();\n")
        fw.write("    _Sendcrc();\r")
        fw.write("}\n")
    return 1
def genvoidService_server_send_response(fw,listVoid_server_res,id_mcu):
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res=setup_srv_server_protocol()
    fw.write("\r\r\r// gen service server callback void\r")
    for i in range(0,len(listVoid_server_res)):
        # print(listVoid[i][8:12])
        fw.write(listVoid_server_res[i][8:12]+" Xicro::"+listVoid_server_res[i][13:len(listVoid_server_res[i])-1])
        fw.write(("{\n"))
        fw.write("    _crc=0;\r")
        fw.write("    _Sendstart();\n")
        fw.write("    _SendSignature("+str(id_mcu)+",14);\n")
        fw.write("    _SendIdTopic("+str(Idsrv[i])+");\n")
        for j in range(0,len(dataType_srv_res[i])):
            cond=j<len(dataType_srv_res[i])-1 #check flag continue or stop
            fw.write(typetoVoid(dataType_srv_res[i][j],dataName_srv_res[i][j],NofData_srv_res[i][j],cond,"Service_server_"+namesrv[i]+".response"))
            if(dataType_srv_res[i][j]=="bool" and NofData_srv_res[i][j]==1 ):
                fw.write("// auto by 1 bool\n")
            elif(cond):
                fw.write("    _Sendcontinue();\n")
            else:
                fw.write("    _Sendstop();\n")
        fw.write("    _Sendcrc();\r")
        fw.write("    Service_server_"+namesrv[i]+".state = 2;\n")
        fw.write("}\n")
    print("gen service server callback Done.")
    return 1
def gen_head_state_udp(fw):
    fw.write("    _serial->parsePacket();\n    _num_udp=_serial->read(_buffer_udp, 999);\n")
    fw.write("    if(_num_udp>0){\n        for(int ii=0;ii<_num_udp;ii++){\n            _buff[_Posdata]=(uint8_t)_buffer_udp[ii];\n")
    fw.write("            _Posdata=(_Posdata+1 )%1000;\n        }\n    }\n")
    fw.write("    if(_Posdata!=_Posdatapre ){\n")
    fw.write("        _datain[0] =_buff[_Posdatapre];\n\n")
def create_cppFile(listVoid,id_mcu,id_topic,dataType,dataName,Nofdata,listVoid_client_req,listVoid_server_res,listVoid_action_client_req,listVoid_action_server_feed,listVoid_action_server_res):
    try:
        # print(listVoid,id_mcu,id_topic,dataType,dataName,Nofdata)
        path = mkdir()
        path = path +"/Xicro_"+get_params("microcontroller.namespace")+"_ID_"+str(id_mcu)+".cpp"
        fw  = open(path, "w+") 
        # if(input.mcu_type=="stm32"):
        #     pathr = os.path.join(get_package_share_directory('xicro_pkg'),'config', '.stm32_cpp_preSetup.txt')
        # else:
        #     pathr = os.path.join(get_package_share_directory('xicro_pkg'),'config', '.arduino_cpp_preSetup.txt')
        pathr = os.path.join(get_package_share_directory('xicro_pkg'),'config', '.library_cpp_preSetup.xicro')
        fr=open(pathr, 'r') 
        fw.write("// ***************************************************************************************************************************************************\r")
        fw.write("//      |              This script was auto-generated by generate_arduino_lib.py which received parameters from setup_xicro.yaml               |\r")
        fw.write("//      |                                         EDITING THIS FILE BY HAND IS NOT RECOMMENDED                                                 |\r")
        fw.write("// ***************************************************************************************************************************************************\r\r")
        fw.write("\r\n#include \""+"Xicro_"+get_params("microcontroller.namespace")+"_ID_"+str(id_mcu)+".h\"\r\n")
        c=0
        for line in fr:        
            c=c+1
            if(line=="!#@ gen_void\n"): 
                try:
                    p,p,nameofTopic,p,p,p,p=setupvarforcreatelibPub()
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
                            fw.write(typetoVoid(dataType[i][j],dataName[i][j],Nofdata[i][j],cond,"Publisher_"+nameofTopic[i]+".message"))
                            if(dataType[i][j]=="bool" and Nofdata[i][j]==1 ):
                                fw.write("// auto by 1 bool\n")
                            elif(cond):
                                fw.write("    _Sendcontinue();\n")
                            else:
                                fw.write("    _Sendstop();\n")
                        fw.write("    _Sendcrc();\r")
                        fw.write("}\n")
                    print("gen functionPub Done.")
                    fw.write("\r\r\r// gen service client call void\r")
                    genvoidService_call(fw,listVoid_client_req,id_mcu)
                    print("gen service client call void Done.")
                    genvoid_begin_srv_server_cpp(fw)
                    print("gen service client call void Done.")
                    genvoidService_server_send_response(fw,listVoid_server_res,id_mcu)
                    print("gen void service server response Done.")
                    fw.write("\r\r\r// gen action client call void\r")
                    genvoidAction_call(fw,listVoid_action_client_req,id_mcu)
                    genvoid_begin_action_server_cpp(fw)
                    fw.write("\r\r\r// gen action server feedback void\r")
                    genvoidAction_server_feed(fw,listVoid_action_server_feed,id_mcu)
                    print("gen action server feedback void Done.")
                    fw.write("\r\r\r// gen action server response void\r")
                    genvoidAction_server_res(fw,listVoid_action_server_res,id_mcu)
                    print("gen action server response void Done.")
                    print("gen function call Done.")
                except:
                    print("gen function call Fail.")
            elif(line=="!#@ gen_void_begin\n"):
                try:
                    if(input.mcu_type== "stm32"):
                        fw.write("\n    HAL_UART_Receive_DMA(_serial, _UartBuff, 64);\n\n\n\n")
                    genPointer(fw)
                    genPointer_srv_client_res(fw)
                    genPointer_srv_server_req(fw)
                    genPointer_action_client(fw)
                    genPointer_action_server(fw)
                    print("gen pointer Done.")
                except:
                    print("gen pointer Fail.")
            elif(line=="!#@ gen_define\n"and ((input.mcu_type== "arduino" )or (input.mcu_type== "esp"))):
                fw.write("\n#define __SEND_UART(x,y) _serial->write(x,y);\n\n")
            elif(line=="!#@ gen_define\n"and input.mcu_type== "stm32"):
                fw.write("\n#define __SEND_UART(x,y) HAL_UART_Transmit(_serial, x, y, 1000);\n\n")
            elif(line=="!#@ gen_head_state\n"and ((input.mcu_type== "arduino" )or (input.mcu_type== "esp")) and get_params("microcontroller.connection.type") == "UART" ):
                fw.write("\n\n    if(_serial->available() > 0){\n")
                fw.write("        _serial->readBytes(_datain,1);\n\n")
            elif(line=="!#@ gen_head_state\n"and get_params("microcontroller.connection.type") == "UDP" ):
                gen_head_state_udp(fw)
            elif(line=="!#@ gen_count_buffer\n" and get_params("microcontroller.connection.type") == "UDP"):
                fw.write("        _Posdatapre=(_Posdatapre+1) %1000;\n")
            elif(line=="!#@ gen_count_buffer\n" and get_params("microcontroller.connection.type") == "UART" and ((input.mcu_type== "arduino" )or (input.mcu_type== "esp"))):
                pass
            elif(line=="!#@ gen_count_buffer\n" and input.mcu_type== "stm32" ):
                fw.write("        _Posdatapre=(_Posdatapre+1) %64;\n")
            elif(line=="!#@ gen_head_state\n"and input.mcu_type== "stm32"):
                fw.write("\n\n    _Posdata=((UART_HandleTypeDef)*_serial).RxXferSize-__HAL_DMA_GET_COUNTER(((UART_HandleTypeDef)*_serial).hdmarx);\n")
                fw.write("    if(_Posdata!=_Posdatapre ){\n")
                fw.write("        _datain[0] = _UartBuff[_Posdatapre];\n\n")
            elif(line=="!#@ gen_void_head_begin_cpp\n" and get_params("microcontroller.connection.type") == "UART"):
                fw.write("void Xicro::begin(__UART_TYPE *SerialObject){\n")
            elif(line=="!#@ gen_void_head_begin_cpp\n" and get_params("microcontroller.connection.type") == "UDP"):
                fw.write("void Xicro::begin(__UART_TYPE *SerialObject,char *udpAddress,int udpPort){\n")
                fw.write("    _udpAddress=udpAddress;\n    _udpPort=udpPort;\n")
            elif((line=="!#@ gen_start_pack_udp\n" or line=="!#@ gen_stop_pack_udp\n") and get_params("microcontroller.connection.type") == "UART"):
                pass
            elif(line=="!#@ gen_start_pack_udp\n" and get_params("microcontroller.connection.type") == "UDP"):
                fw.write("    _serial->beginPacket(_udpAddress,_udpPort);\n")
            elif(line=="!#@ gen_stop_pack_udp\n" and get_params("microcontroller.connection.type") == "UDP"):
                fw.write("    _serial->endPacket();\n")    
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
    elif(strr=="float32" or (strr=="float64" and input.mcu_type!="stm32") ):
        return "float"
    elif(strr=="float64"):
        return "double"
    elif(strr=="string" and input.mcu_type!="stm32"):
        return "String"
    elif(strr=="string" ):
        return "std::string"
    elif(strr== "bool"):
        return "bool"
    elif(strr=="xxicro_Empty"):
        return "xxicro_Empty"
    else:
        return "ERRORTYPE"

    


    
def typetoVoid(typee,namee,Nofdata,cond,nameString):
    # print(typee,namee,Nofdata,cond,nameString)
    namee=nameString+"."+namee
    # for i in range(0,10): # bias __of__ to .
    #     if(namee.find("__of__")==-1):
    #         break
    #     else:
    namee=namee.replace("__of__",".")
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
    elif( (typee=="float32" or (typee=="float64" and input.mcu_type!="stm32")  ) and Nofdata==1):
        return  "    _SendFloat32((float*)&"+namee+","+ str(Nofdata)+");\n"
    elif( (typee=="float32" or (typee=="float64" and input.mcu_type!="stm32")  ) and Nofdata!=1):
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
        return  "    _SendBool((bool*)"+namee+","+ str(Nofdata)+","+str(int(cond))+");\n"
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
        # for j in range(0,len(dataType[i])):
        #     t=t+convertdatatype(dataType[i][j])+" "
        #     if(Nofdata[i][j]!=1):
        #         t=t+"*"
        #     t=t+dataName[i][j]+" "
        #     if(j>=0 and j<len(dataType[i])-1):
        #         t=t+","
        t=t+");"
        temp.append(t)
    # print(temp)
    return temp
def strVoid_srv_req():
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res = setup_srv_protocol()
    temp=[]
    for i in range(0,len(namesrv)):
        t="        "
        t=t+"void service_client_call_"+namesrv[i]+"("
        # if(dataType_srv_req[i][0]!="xxicro_Empty"):
        #     for j in range(0,len(dataType_srv_req[i])):
        #         t=t+convertdatatype(dataType_srv_req[i][j])+" "
        #         if(NofData_srv_req[i][j]!=1):
        #             t=t+"*"
        #         t=t+dataName_srv_req[i][j]+" "
        #         if(j>=0 and j<len(dataType_srv_req[i])-1):
        #             t=t+","
        t=t+");"
        temp.append(t)
    # print(temp)
    return temp
def strVoid_srv_res():
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res = setup_srv_server_protocol()
    temp=[]
    for i in range(0,len(namesrv)):
        t="        "
        t=t+"void service_server_response_"+namesrv[i]+"("
        # if(dataType_srv_req[i][0]!="xxicro_Empty"):
        #     for j in range(0,len(dataType_srv_req[i])):
        #         t=t+convertdatatype(dataType_srv_req[i][j])+" "
        #         if(NofData_srv_req[i][j]!=1):
        #             t=t+"*"
        #         t=t+dataName_srv_req[i][j]+" "
        #         if(j>=0 and j<len(dataType_srv_req[i])-1):
        #             t=t+","
        t=t+");"
        temp.append(t)
    # print(temp)
    return temp
def strVoid_action_req():
    Idaction_client,nameaction_client,interfaceaction_client,dataType_action_client_req,dataName_action_client_req,datagrab_action_client_req,NofData_action_client_req,datatypeProtocol_action_client_req,bytetograb_action_client_req,dataType_action_client_res,dataName_action_client_res,datagrab_action_client_res,NofData_action_client_res,datatypeProtocol_action_client_res,bytetograb_action_client_res,dataType_action_client_feed,dataName_action_client_feed,datagrab_action_client_feed,NofData_action_client_feed,datatypeProtocol_action_client_feed,bytetograb_action_client_feed,timeOut_action_client = setup_action_client_protocol()
    temp=[]
    for i in range(0,len(nameaction_client)):
        t="        "
        t=t+"void action_client_call_"+nameaction_client[i]+"("
        # if(dataType_srv_req[i][0]!="xxicro_Empty"):
        #     for j in range(0,len(dataType_srv_req[i])):
        #         t=t+convertdatatype(dataType_srv_req[i][j])+" "
        #         if(NofData_srv_req[i][j]!=1):
        #             t=t+"*"
        #         t=t+dataName_srv_req[i][j]+" "
        #         if(j>=0 and j<len(dataType_srv_req[i])-1):
        #             t=t+","
        t=t+");"
        temp.append(t)
    # print(temp)
    return temp
def strVoid_action__server_feed():
    Idaction_server,nameaction_server,interfaceaction_server,dataType_action_server_req,dataName_action_server_req,datagrab_action_server_req,NofData_action_server_req,datatypeProtocol_action_server_req,bytetograb_action_server_req,dataType_action_server_res,dataName_action_server_res,datagrab_action_server_res,NofData_action_server_res,datatypeProtocol_action_server_res,bytetograb_action_server_res,dataType_action_server_feed,dataName_action_server_feed,datagrab_action_server_feed,NofData_action_server_feed,datatypeProtocol_action_server_feed,bytetograb_action_server_feed,timeOut_action_server = setup_action_server_protocol()
    temp=[]
    for i in range(0,len(nameaction_server)):
        t="        "
        t=t+"void action_server_send_feedback_"+nameaction_server[i]+"("
        # if(dataType_srv_req[i][0]!="xxicro_Empty"):
        #     for j in range(0,len(dataType_srv_req[i])):
        #         t=t+convertdatatype(dataType_srv_req[i][j])+" "
        #         if(NofData_srv_req[i][j]!=1):
        #             t=t+"*"
        #         t=t+dataName_srv_req[i][j]+" "
        #         if(j>=0 and j<len(dataType_srv_req[i])-1):
        #             t=t+","
        t=t+");"
        temp.append(t)
    # print(temp)
    return temp
def strVoid_action_server_res():
    Idaction_server,nameaction_server,interfaceaction_server,dataType_action_server_req,dataName_action_server_req,datagrab_action_server_req,NofData_action_server_req,datatypeProtocol_action_server_req,bytetograb_action_server_req,dataType_action_server_res,dataName_action_server_res,datagrab_action_server_res,NofData_action_server_res,datatypeProtocol_action_server_res,bytetograb_action_server_res,dataType_action_server_feed,dataName_action_server_feed,datagrab_action_server_feed,NofData_action_server_feed,datatypeProtocol_action_server_feed,bytetograb_action_server_feed,timeOut_action_server = setup_action_server_protocol()
    temp=[]
    for i in range(0,len(nameaction_server)):
        t="        "
        t=t+"void action_server_send_result_"+nameaction_server[i]+"("
        # if(dataType_srv_req[i][0]!="xxicro_Empty"):
        #     for j in range(0,len(dataType_srv_req[i])):
        #         t=t+convertdatatype(dataType_srv_req[i][j])+" "
        #         if(NofData_srv_req[i][j]!=1):
        #             t=t+"*"
        #         t=t+dataName_srv_req[i][j]+" "
        #         if(j>=0 and j<len(dataType_srv_req[i])-1):
        #             t=t+","
        t=t+");"
        temp.append(t)
    # print(temp)
    return temp
def gen():
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,Nofdata=setupvarforcreatelibPub()
    # print(id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,Nofdata)
    listVoid=strVoid(nameofTopic,dataType,dataName,Nofdata)
    listVoid_client_req=strVoid_srv_req()
    listVoid_server_res=strVoid_srv_res()
    listVoid_action_client_req=strVoid_action_req()
    listVoid_action_server_feed=strVoid_action__server_feed()
    listVoid_action_server_res=strVoid_action_server_res()
    create_hFile(listVoid,id_mcu,listVoid_client_req,listVoid_server_res,listVoid_action_client_req,listVoid_action_server_feed,listVoid_action_server_res)
    create_cppFile(listVoid,id_mcu,id_topic,dataType,dataName,Nofdata,listVoid_client_req,listVoid_server_res,listVoid_action_client_req,listVoid_action_server_feed,listVoid_action_server_res)
 
def checkArgs():
    flagargs=0
    try:
        global input 
        input = argparse.ArgumentParser()
        input.add_argument("-mcu_type", help="type of microcontroller",choices=["arduino","esp","stm32"],type=str,required=1)
        input.add_argument("-module_name",help="include module for microcontroller \nexample 'stm32f4xx_hal.h','Arduino.h' ",type=str)
        input = input.parse_args()
        if(input.mcu_type == "arduino" or input.mcu_type ==  "stm32" or input.mcu_type == "esp"):
            flagargs=1
    except:
        print('******  Please input argv [-mcu_type]  ******')

    if(flagargs and input.mcu_type== "stm32"):
        if(input.module_name == None):
            flagargs=0
            print('******  Please input argv [-module_name]  ******')

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