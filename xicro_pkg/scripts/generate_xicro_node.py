#!/usr/bin/python3
from math import ceil
import os
import yaml
from ament_index_python.packages import get_package_share_directory
import sys
def gPath(q): # q=1 is install config q=0 is ws/ src pkg
    if(q):
        w=os.popen("ros2 pkg prefix xicro_pkg").read()
        w=w[0:len(w)-1]
        return w+'/share'+'/xicro_pkg'+'/config'
    else:   
        w=os.popen(     "ros2 pkg prefix xicro_pkg").read()
        w=w[0:w.find("/install")]+"/src/Xicro/xicro_pkg"
        return w
def interfacePath():
    w=os.popen("ros2 pkg prefix xicro_interfaces").read()
    w=w[0:len(w)-1]
    return w+'/share'+'/xicro_interfaces'
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

def get_params(q):
    try:
       
        path = os.path.join(gPath(1), 'setup_xicro.yaml')
        with open(path,'r') as f:
            yml_dict = yaml.safe_load(f)
            ans = yml_dict.get(q)
        print('Get '+q+' Done.')
        return  ans
    except:
        print('Get '+q+' Failed'+'Something went wrong when opening YAML.')
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

    # for i in range(0,len(dataName)): #Rename . to _of_
    #     q=[]
    #     for j in range(0,len(dataName[i])):
    #         dataName[i][j]=dataName[i][j].replace(".","__of__")
    
    # print("Datatype :",dataType)
    # print("DataName :",dataName)
    # print("Nofdata :",NofData)
    return id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData,interfacein
def setup_var_protocol():
    setup_pub=get_params('Setup_Publisher')
    Idmsg=[]
    nametopic=[]
    interfacetopic=[]
    interfacein=[]
    for i in range(0,len(setup_pub)):
        Idmsg.append(setup_pub[i][0])
        nametopic.append(setup_pub[i][1])
        interfacetopic.append(setup_pub[i][2])
    print('Done load YAML pub.')
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
    # print(Idmsg,nametopic,interfacetopic,dataType,dataName,datagrab,NofData,datatypeProtocol,bytetograb)
    print('Generate variable from msg Done.')

    
    # return 0,0,0,0,0,0,0,0,0
    for i in range(0,10):
            Idmsg,id_topic,nametopic,interfacetopic,dataType,dataName,NofData,interfacein=expandSub(Idmsg,[],nametopic,interfacetopic,dataType,dataName,NofData,interfacein)
    for i in range(0,len(dataType)): # bias float64 to float32
        for j in range(0,len(dataType[i])):
            if(dataType[i][j].split("[")[0] == "float64" and (sys.argv[1]=="arduino" or sys.argv[1]=="esp") ):
                dataType[i][j]="float32"
                
    # cal  [ byte to grab , dataProtocol , datagrab   ] dataTyperemove_index 
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

# print(setup_var_protocol())
# while(1):
#     1

def cal(baud_rate,byteGrab,Nofdata,NameToppic):
    bytePerS=baud_rate/10.00
    Sumbyte=0
    for i in range(0,len(byteGrab)):
        byte_T= 4 + 1 + 1 # start + sign + id 
        for j in range(0,len(byteGrab[i])):
            byte_T=byte_T + 1 # bit data type
            if(byteGrab[i][j]==888): # string
                byte_T=byte_T+1+2   #asumtion 1 char and stop string 2 byte
                
            elif(byteGrab[i][j]==88): # bool
                if(ceil(Nofdata[i][j]/8.00)>1):
                    byte_T=byte_T + ceil(Nofdata[i][j]/8.00) 
                else:
                    byte_T=byte_T + 0   #1 bool is auto continue or auto stop
            else: #normal var
                byte_T=byte_T+( byteGrab[i][j]*Nofdata[i][j])
            if(Nofdata[i][j]>1):  
                byte_T=byte_T+1 # Bit show Nofdata  

        byte_T=byte_T + ((len(byteGrab[i])-1)*2)  + 2 + 1  #  continue + stop + Crc
        print("Topic >>> ",NameToppic[i] , "Use : " ,byte_T ,"bytes")
        print("Max_frequency On Topic ",NameToppic[i]," is : ",bytePerS/byte_T ," Hz.")
        print("******Calculate Only 1 Topic per Second******")
        Sumbyte=Sumbyte+byte_T

    print("All topic average is : ",bytePerS/Sumbyte," Hz.")
    

    return 0
    
def checkNofdata(dataType):
    S=dataType.find("[")
    F= dataType.find("]")
    if(S!=-1 and F!=-1):
        return int(dataType[S+1:F])
    else:
        return 1


def setupvarforcreatelib():
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
            tempinterfacein=[]
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
def getbeforedot(q):
    qq=""
    for i in range (0,len(q)):
        if(q[i]=="."):
            break
        else:
            qq=qq+q[i]
    return qq

def getafterdot(q):
    qq=""
    flag=0
    for i in range (0,len(q)):
        if(flag):
            qq=qq+q[i]
        if(q[i]=="."):
            flag=1
    return qq

def genSub(fw,nameofTopic,interfacefile):
    try:
        callback=[]
        fw.write("\r\r        #gen\r")
        for i in range (0,len(nameofTopic)):
            q="        self.subscription_"
            q=q+nameofTopic[i]
            w=" = self.create_subscription("
            w=w+getbeforedot(interfacefile[i].split("/")[1])+",'"+nameofTopic[i]+"'," 
            e="self.callback_"+nameofTopic[i]
            w=w+e+",10)"
            callback.append(e)
            fw.write(q+w+"\r")
            fw.write("        "+e+"\r")
        fw.write("\r\r\r\r")
        print("gennerate Sub Done.")
    except:
        print("gennerate Sub Fail.")
    return callback

def typetofunc(typee,namee,Nofdata,cond):
    if(typee.find("[")!=-1):
        typee=typee[0:typee.find("[")]
    # print(Nofdata,typee)    
    try:
        if(typee=="uint8"):
            return  "        self.xicro_instruction._SendUint8(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="uint16"):
            return  "        self.xicro_instruction._SendUint16(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="uint32"):
            return  "        self.xicro_instruction._SendUint32(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="uint64"):
            return  "        self.xicro_instruction._SendUint64(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="int8"):
            return  "        self.xicro_instruction._SendInt8(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="int16"):
            return  "        self.xicro_instruction._SendInt16(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="int32"):
            return  "        self.xicro_instruction._SendInt32(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="int64"):
            return  "        self.xicro_instruction._SendInt64(msg."+namee+","+str(Nofdata)+ ")\n"  
        elif(typee=="float32"):
            return  "        self.xicro_instruction._SendFloat32(msg."+namee+","+str(Nofdata)+ ")\n"  
        elif(typee=="string"):
            return  "        self.xicro_instruction._SendString(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="bool" and Nofdata==1):
            return  "        self.xicro_instruction._SendBool(msg."+namee+",1,"+str(cond)+ ")\n"
        elif(typee=="bool" and Nofdata!=1):
            return  "        self.xicro_instruction._SendBool(msg."+namee+","+str(Nofdata)+","+str(cond)+ ")\n"
        elif(typee=="float64" and ( sys.argv[1] =="arduino" or sys.argv[1] =="esp" )):
            return  "        self.xicro_instruction._SendFloat32(msg."+namee+","+str(Nofdata)+ ")\n"    
        elif(typee=="float64"):
            return  "        self.xicro_instruction._SendFloat64(msg."+namee+","+str(Nofdata)+ ")\n"
        else:
            print("ErorType : ",typee)
            return "1"
    except:
        print("Format .msg wrong")
    return "0"
def gencallback(fw,callback,id_mcu,id_topic,dataType,dataName,Nofdata):
    try:
        fw.write("    # gen callback Sub\r")
        for i in range(len(callback)):
            fw.write("    def "+getafterdot(callback[i])+"(self,msg):\r")
            fw.write("        self.xicro_instruction._Reset_Buff()\r")
            fw.write("        self.xicro_instruction._Reset_CRC()\r")
            fw.write("        self.xicro_instruction._SendStart()\r")
            fw.write("        self.xicro_instruction._SendSignature("+str(id_mcu)+","+"2)\r")
            fw.write("        self.xicro_instruction._SendIdtopic("+str(id_topic[i])+")\r")
            for j in range (0,len(dataType[i])):
                cond=j<len(dataType[i])-1 #check flag continue or stop
                fw.write(typetofunc(dataType[i][j],dataName[i][j],Nofdata[i][j],cond))
                if(dataType[i][j]=="bool" and Nofdata[i][j]==1 ):
                    fw.write("# auto by 1 bool\n")
                elif(cond):
                    fw.write("        self.xicro_instruction._SendContinue()\r")
                else:
                    fw.write("        self.xicro_instruction._SendStop()\r")
                    
            fw.write("        self.xicro_instruction._SendCRC()\r")
            fw.write("        self.xicro_instruction._To_Send()\r")
            fw.write("\r        return 1\r\r\r\r")
        print("gennerate Callback Done.")
        return 1
    except:
        print("gennerate Callback Fail.")
    return 0
def genImport(fw):
    try:
        fw.write("\r# gen import msg\r")
        interfacemsg=[]
        Setup_Sub=get_params("Setup_Subscriber")
        for i in range(0,len(Setup_Sub)):
            interfacemsg.append(Setup_Sub[i][2])
        Setup_Pub=get_params("Setup_Publisher")
        for i in range(0,len(Setup_Pub)):
            interfacemsg.append(Setup_Pub[i][2])  
            
        # print("interfacemsg",interfacemsg)
        tt=[]
        for i in range(0,len(interfacemsg)):
            s=0
            for j in range(0,len(tt)):
                if(interfacemsg[i] == tt[j]):
                    s=s+1
            if(s==0):
                tt.append(interfacemsg[i])
        interfacemsg=tt.copy()
        for i in range(0,len(interfacemsg)):
            fw.write("from "+interfacemsg[i].split("/")[0]+".msg import "+interfacemsg[i].split("/")[1].split(".")[0] + "\r")
        fw.write("\r\r# gen import srv\r")

        interfacesrv=[]
        Setup_Srv=get_params("Setup_Srv_client")
        for i in range(0,len(Setup_Srv)):
            interfacesrv.append(Setup_Srv[i][2])  
        tt=[]
        for i in range(0,len(interfacesrv)):
            s=0
            for j in range(0,len(tt)):
                if(interfacesrv[i] == tt[j]):
                    s=s+1
            if(s==0):
                tt.append(interfacesrv[i])
        interfacesrv=tt.copy()
        for i in range(0,len(interfacesrv)):
            fw.write("from "+interfacesrv[i].split("/")[0]+".srv import "+interfacesrv[i].split("/")[1].split(".")[0] + "\r")
        fw.write("\r\r")


        print("Generate Import Interface Done.")
    except:
        print("Generate Import Interface Fail.")


    return 1

def setup_srv_protocol():
    setup_srv=get_params('Setup_Srv_client')
    Idmcu=get_params("Idmcu")
    Idsrv=[]
    namesrv=[]
    interfacesrv=[]
    timeOut=[]
    for i in range(0,len(setup_srv)):
        Idsrv.append(setup_srv[i][0])
        namesrv.append(setup_srv[i][1])
        interfacesrv.append(setup_srv[i][2])
        timeOut.append(setup_srv[i][3])
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


def gennerate(): 
    
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,Nofdata=setupvarforcreatelib()
    # print(id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,Nofdata)
    pathr= os.path.join(gPath(1)+'/.Xicro_node_preSetup.txt')
    
    pathw= os.path.join(gPath(0)+ '/scripts/xicro_node_'+get_params("Namespace")+"_ID_"+str(id_mcu)+'_'+sys.argv[1]+'.py')
    os.popen("code " + pathw)

    # print(gPath(0)+ '/scripts/xicro_node_'+get_params("Namespace")+"_ID_"+str(id_mcu)+'.py')
    fr=open(pathr, 'r') 
    fw=open(pathw, 'w') 
    fw.write("#!/usr/bin/python3\r\r\r\r")
    fw.write("# ***************************************************************************************************************************************************\r")
    fw.write("#      |          This script was auto-generated by generate_Xicro_node.py which received parameters from setup_xicro.yaml                    |\r")
    fw.write("#      |                                         EDITING THIS FILE BY HAND IS NOT RECOMMENDED                                                 |\r")
    fw.write("# ***************************************************************************************************************************************************\r\r")
    c=0
    callback=[]
    for line in fr:
        c=c+1
        if(c==407):
            callback=genSub(fw,nameofTopic,interfacefile)
        elif(c==410):
            gencallback(fw,callback,id_mcu,id_topic,dataType,dataName,Nofdata)
        elif(c==79):
            fw.write("\r\rdef setup_var_protocol():\r\r")
            Idmsgg,nametopicc,interfacetopicc,dataTypee,dataNamee,datagrabb,NofDataa,datatypeProtocoll,bytetograbb=setup_var_protocol()
            cal(get_params("Baudrate"),bytetograbb,NofDataa,nametopicc)
            fw.write("    return "+str(Idmsgg)+","+str(nametopicc)+","+str(interfacetopicc)+","+str(dataTypee)+","+str(dataNamee)+","+str(datagrabb)+","+str(NofDataa)+","+str(datatypeProtocoll)+","+str(bytetograbb))
            fw.write("\r\r")
            Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res,timeOut=setup_srv_protocol()
            fw.write("\r\rdef setup_srv_protocol():\r\r")
            fw.write("    return "+str(Idsrv)+","+str(namesrv)+","+str(interfacesrv)+","+str(dataType_srv_req)+","+str(dataName_srv_req)+","+str(datagrab_srv_req)+","+str(NofData_srv_req)+","+str(datatypeProtocol_srv_req)+","+str(bytetograb_srv_req)+","+str(dataType_srv_res)+","+str(dataName_srv_res)+","+str(datagrab_srv_res)+","+str(NofData_srv_res)+","+str(datatypeProtocol_srv_res)+","+str(bytetograb_srv_res)+","+str(timeOut))
            fw.write("\r\r")
        elif(c==458):
            fw.write("    Idmcu = "+str(id_mcu)+"\n")
        elif(c==10):
            fw.write("# gen Import interfaces\r")
            genImport(fw)
        elif(c==872):
            fw.write("        self.Idmcu = "+str(id_mcu)+"\n")
        elif(c==846):
            fw.write("            ser = serial.Serial(Port,"+ str(get_params("Baudrate"))+", timeout=1000 ,stopbits=1)\n")    
        else:
            fw.write(line)
    return 1
def addentrypoint():
    pathr= os.path.join(gPath(0), 'CMakeLists.txt')
    f=open(pathr, 'r+') 
    entryp=[]
   
    for line in f:
        entryp.append(line)
    


    entrystring="  scripts/"+"xicro_node_"+get_params("Namespace")+"_ID_"+str(get_params("Idmcu"))+'_'+sys.argv[1]+'.py\n'
    stopP=0
    h=0
    for i in range(0,len(entryp)):
        if(entryp[i]==entrystring):
            h=1
        if(entryp[i]=='#orcix\n'):
            stopP=i
    if(not h):
        entryp.insert(stopP,entrystring)
    pathw= os.path.join(gPath(0), 'CMakeLists.txt')
    fw=open(pathw, 'w')
    for i in range(0,len(entryp)):
        fw.write(entryp[i])


    return 1

        
def main():
    flagargs=0
    try:
        input = sys.argv[1]
        if(input == "arduino" or input ==  "stm32" or "esp"):
            flagargs=1
        else:
            print("*************************************************")
            print('******  Input argv Only ["arduino","stm32","esp"]  ******')
    except:
        print('******  Please argv ["arduino","stm32","esp"]  ******')
    if(flagargs):
        try:
            gennerate()
            print("----------------------generate xicro_node.py Done----------------------")
            try:
                addentrypoint()
                print("----------------------generate Entry_Point Done----------------------")
            except:
                print("----------------------generate Entry_Point Fail----------------------")
        except:
            print("----------------------generate xicro_node.py Fail----------------------")
    return 1

if __name__=='__main__':
    main()