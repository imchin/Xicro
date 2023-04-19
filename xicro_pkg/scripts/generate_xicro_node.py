#!/usr/bin/python3
from math import ceil
import os
import yaml
from ament_index_python.packages import get_package_share_directory
import argparse

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

def get_params(qq):
    try:
        q=qq
        path = os.path.join(gPath(1), 'setup_xicro.yaml')
        with open(path,'r') as f:
            yml_dict = yaml.safe_load(f)
            q=q.split(".")
            ans = yml_dict.get(q[0])
            for i in range(1,len(q)):
                ans = ans.get(q[i])
        print('Get '+qq+' Done.')
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
    setup_pub=get_params('ros.publisher')
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
            if(dataType[i][j].split("[")[0] == "float64" and (input.mcu_type=="arduino" or input.mcu_type=="esp") ):
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
                
            elif(byteGrab[i][j]==999): # bool
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
        id_mcu=get_params("microcontroller.idmcu")
        Setup_Sub=get_params("ros.subscriber")
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

def genSrv_server(fw,namesrv,interfacefile,i):
    try:
        callback=""
        q="        self.srv_server_"
        q=q+namesrv[i]
        w=" = self.create_service("
        w=w+getbeforedot(interfacefile[i].split("/")[1])+",'"+namesrv[i]+"'," 
        e="self.srv_server_callback_"+namesrv[i]
        w=w+e+")"
        callback=e
        fw.write(q+w+"\r")
            # fw.write("        "+e+"\r")
        fw.write("\r\r\r\r")
        print("gennerate Srv_server Done.")
    except:
        print("gennerate Srv_server Fail.")
    return callback
def genAction_server(fw,nameaction,interfacefile,i):
    try:
        callback=""
        q="        self.action_server_"
        q=q+nameaction[i]
        w=" = ActionServer(self,"
        w=w+getbeforedot(interfacefile[i].split("/")[1])+",'"+nameaction[i]+"'," 
        e="self.action_server_callback_"+nameaction[i]
        w=w+e+")"
        callback=e
        fw.write(q+w+"\r")
            # fw.write("        "+e+"\r")
        fw.write("\r\r\r\r")
        print("gennerate Action_server Done.")
    except:
        print("gennerate Action_server Fail.")
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
        elif(typee=="float64" and ( input.mcu_type =="arduino" or input.mcu_type =="esp" )):
            return  "        self.xicro_instruction._SendFloat32(msg."+namee+","+str(Nofdata)+ ")\n"    
        elif(typee=="float64"):
            return  "        self.xicro_instruction._SendFloat64(msg."+namee+","+str(Nofdata)+ ")\n"
        else:
            print("ErorType : ",typee)
            return "1"
    except:
        print("Format .msg wrong")
    return "0"
def typetofunc_strr(typee,namee,Nofdata,cond,strr):
    if(typee.find("[")!=-1):
        typee=typee[0:typee.find("[")]
    # print(Nofdata,typee)    
    try:
        if(typee=="uint8"):
            return  "        self.xicro_instruction._SendUint8("+strr+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="uint16"):
            return  "        self.xicro_instruction._SendUint16("+strr+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="uint32"):
            return  "        self.xicro_instruction._SendUint32("+strr+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="uint64"):
            return  "        self.xicro_instruction._SendUint64("+strr+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="int8"):
            return  "        self.xicro_instruction._SendInt8("+strr+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="int16"):
            return  "        self.xicro_instruction._SendInt16("+strr+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="int32"):
            return  "        self.xicro_instruction._SendInt32("+strr+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="int64"):
            return  "        self.xicro_instruction._SendInt64("+strr+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="float32"):
            return  "        self.xicro_instruction._SendFloat32("+strr+namee+","+str(Nofdata)+ ")\n"  
        elif(typee=="string"):
            return  "        self.xicro_instruction._SendString("+strr+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="bool" and Nofdata==1):
            return  "        self.xicro_instruction._SendBool("+strr+namee+",1,"+str(cond)+ ")\n"
        elif(typee=="bool" and Nofdata!=1):
            return  "        self.xicro_instruction._SendBool("+strr+namee+","+str(Nofdata)+","+str(cond)+ ")\n"
        elif(typee=="float64" and ( input.mcu_type =="arduino" or input.mcu_type =="esp" )):
            return  "        self.xicro_instruction._SendFloat32("+strr+namee+","+str(Nofdata)+ ")\n"    
        elif(typee=="float64"):
            return  "        self.xicro_instruction._SendFloat64("+strr+namee+","+str(Nofdata)+ ")\n"
        else:
            print("ErorType "+strr+": ",typee)
            return "1"
    except:
        print("Format "+strr+" wrong")
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

def gencallback_srv_server(fw,callback_srv,id_mcu,Idsrv,dataType_srv_req,dataName_srv_req,NofData_srv_req,dataType_srv_res,dataName_srv_res,NofData_srv_res,i):
    try:
        # fw.write("    # gen service_server callback\r")
        
        fw.write("    def "+getafterdot(callback_srv)+"(self,request, response):\r")
        fw.write("        st_index=self.Obj_uart.index.value\r")
        fw.write("        self.xicro_instruction._Reset_Buff()\r")
        fw.write("        self.xicro_instruction._Reset_CRC()\r")
        fw.write("        self.xicro_instruction._SendStart()\r")
        fw.write("        self.xicro_instruction._SendSignature("+str(id_mcu)+","+"13)\r")
        fw.write("        self.xicro_instruction._SendIdsrv("+str(Idsrv[i])+")\r")
        for j in range (0,len(dataType_srv_req[i])):
            cond=j<len(dataType_srv_req[i])-1 #check flag continue or stop
            fw.write(typetofunc_strr(dataType_srv_req[i][j],dataName_srv_req[i][j],NofData_srv_req[i][j],cond,"request."))
            if(dataType_srv_req[i][j]=="bool" and NofData_srv_req[i][j]==1 ):
                fw.write("# auto by 1 bool\n")
            elif(cond):
                fw.write("        self.xicro_instruction._SendContinue()\r")
            else:
                fw.write("        self.xicro_instruction._SendStop()\r")
                
        fw.write("        self.xicro_instruction._SendCRC()\r")
        fw.write("        self.xicro_instruction._To_Send()\r\r")
            
        fw.write("        mana = mp.Manager()\n")
        fw.write("        sh_res = mana.list()\n")
        fw.write("        p = mp.Process(target=Protocol_XicroToRos_spin,args=(self.Obj_uart,2,"+str(Idsrv[i])+",sh_res,st_index,888,))\n")
        fw.write("        p.start()\n")
        fw.write("        st=time.time()\n")
        fw.write("        while(1):\n")
        fw.write("            if(len(sh_res)==self.maxlen_response):\n")   
        fw.write("                p.join()\n")
        # gen exec response
        for j in range (0,len(dataName_srv_res[i])):
            if(dataName_srv_res[i]!="xxicro_Empty"):
                fw.write("                response."+dataName_srv_res[i][j]+"=sh_res["+str(j)+"]\n")
        fw.write("                return response\n\n")
        fw.write("            elif((time.time()-st>=self.timeout)):\n")
        fw.write("                p.terminate()\n")
        fw.write("                break\n\n")
        fw.write("        return response\n\n")
      
            # fw.write("\r        return 1\r\r\r\r")
        print("gennerate Callback_srv_Server Done.")
        return 1
    except:
        print("gennerate Callback_srv_Server Fail.")
    return 0
def gencallback_action_server(fw,callback_action,id_mcu,Idaction_server,nameaction_server,interfaceaction_server,dataType_action_server_req,dataName_action_server_req,datagrab_action_server_req,NofData_action_server_req,datatypeProtocol_action_server_req,bytetograb_action_server_req,dataType_action_server_res,dataName_action_server_res,datagrab_action_server_res,NofData_action_server_res,datatypeProtocol_action_server_res,bytetograb_action_server_res,dataType_action_server_feed,dataName_action_server_feed,datagrab_action_server_feed,NofData_action_server_feed,datatypeProtocol_action_server_feed,bytetograb_action_server_feed,timeOut_action_server,i):
    try:
        fw.write("    def "+getafterdot(callback_action)+"(self, goal_handle):\r")
        fw.write("        st_index=self.Obj_uart.index.value\r")
        fw.write("        self.xicro_instruction._Reset_Buff()\r")
        fw.write("        self.xicro_instruction._Reset_CRC()\r")
        fw.write("        self.xicro_instruction._SendStart()\r")
        fw.write("        self.xicro_instruction._SendSignature("+str(id_mcu)+","+"8)\r")
        fw.write("        self.xicro_instruction._SendIdaction("+str(Idaction_server[i])+")\r")
        for j in range (0,len(dataType_action_server_req[i])):
            cond=j<len(dataType_action_server_req[i])-1 #check flag continue or stop
            fw.write(typetofunc_strr(dataType_action_server_req[i][j],dataName_action_server_req[i][j],NofData_action_server_req[i][j],cond,"goal_handle.request."))
            if(dataType_action_server_req[i][j]=="bool" and NofData_action_server_req[i][j]==1 ):
                fw.write("# auto by 1 bool\n")
            elif(cond):
                fw.write("        self.xicro_instruction._SendContinue()\r")
            else:
                fw.write("        self.xicro_instruction._SendStop()\r")
                
        fw.write("        self.xicro_instruction._SendCRC()\r")
        fw.write("        self.xicro_instruction._To_Send()\r\r")
        fw.write("        mana = mp.Manager()\n")
        fw.write("        sh_res = mana.list()\n")
        fw.write("        sh_res_2 = mana.list()\n")
        fw.write("        p = mp.Process(target=Protocol_XicroToRos_spin,args=(self.Obj_uart,4,"+str(Idaction_server[i])+",sh_res,st_index,sh_res_2,))\n")
        fw.write("        p.start()\n")
        fw.write("        st=time.time()\n")
        fw.write("        feedback_msg = "+getbeforedot(interfaceaction_server[i].split("/")[1])+".Feedback()\n")
        fw.write("        result = "+getbeforedot(interfaceaction_server[i].split("/")[1])+".Result()\n")
        fw.write("        while(1):\n")
        fw.write("            if(len(sh_res)!= 0):\n")
        fw.write("                feed=sh_res[0]\n")
        fw.write("                sh_res.pop(0)\n")
        for j in range (0,len(dataName_action_server_feed[i])):
            if(dataName_action_server_feed[i]!="xxicro_Empty"):
                fw.write("                feedback_msg."+dataName_action_server_feed[i][j]+"=feed["+str(j)+"]\n")
        fw.write("                goal_handle.publish_feedback(feedback_msg)\n")
        fw.write("\n            elif(len(sh_res_2)!= 0):\n")
        fw.write("                p.join()\n")
        fw.write("                goal_handle.succeed()\n")
        fw.write("                resu=sh_res_2[0]\n")
        for j in range (0,len(dataName_action_server_res[i])):
            if(dataName_action_server_res[i]!="xxicro_Empty"):
                fw.write("                result."+dataName_action_server_res[i][j]+"=resu["+str(j)+"]\n")
        fw.write("                return result\n\n")
        fw.write("            elif((time.time()-st>=self.timeout)):\n")
        fw.write("                p.terminate()\n")
        fw.write("                print('timeout Action server IdOn : "+str(Idaction_server[i])+"')\n")
        fw.write("                goal_handle.abort()\n")
        fw.write("                break\n")
        fw.write("        return result\n")
        print("gennerate Callback_action_Server Done.")
        return 1
    except:
        print("gennerate Callback_action_Server Fail.")
    
    
    return 1

def genImport(fw):
    try:
        fw.write("\r# gen import msg\r")
        interfacemsg=[]
        Setup_Sub=get_params("ros.subscriber")
        for i in range(0,len(Setup_Sub)):
            interfacemsg.append(Setup_Sub[i][2])
        Setup_Pub=get_params("ros.publisher")
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
        fw.write("\r\r# gen import srv client\r")

        interfacesrv=[]
        Setup_Srv=get_params("ros.srv_client")
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

        fw.write("\r\r# gen import srv server\r")

        interfacesrv=[]
        Setup_Srv=get_params("ros.srv_server")
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


        fw.write("\r\r# gen import action client\r")

        interfaceSetup_Action_client=[]
        Setup_Action_client=get_params("ros.action_client")
        for i in range(0,len(Setup_Action_client)):
            interfaceSetup_Action_client.append(Setup_Action_client[i][2])  
        tt=[]
        for i in range(0,len(interfaceSetup_Action_client)):
            s=0
            for j in range(0,len(tt)):
                if(interfaceSetup_Action_client[i] == tt[j]):
                    s=s+1
            if(s==0):
                tt.append(interfaceSetup_Action_client[i])
        interfaceSetup_Action_client=tt.copy()
        for i in range(0,len(interfaceSetup_Action_client)):
            fw.write("from "+interfaceSetup_Action_client[i].split("/")[0]+".action import "+interfaceSetup_Action_client[i].split("/")[1].split(".")[0] + "\r")
        fw.write("\r\r")


        fw.write("\r\r# gen import action server\r")

        interfaceAction_server=[]
        Setup_Action_server=get_params("ros.action_server")
        for i in range(0,len(Setup_Action_server)):
            interfaceAction_server.append(Setup_Action_server[i][2])  
        tt=[]
        for i in range(0,len(interfaceAction_server)):
            s=0
            for j in range(0,len(tt)):
                if(interfaceAction_server[i] == tt[j]):
                    s=s+1
            if(s==0):
                tt.append(interfaceAction_server[i])
        interfaceAction_server=tt.copy()
        for i in range(0,len(interfaceAction_server)):
            fw.write("from "+interfaceAction_server[i].split("/")[0]+".action import "+interfaceAction_server[i].split("/")[1].split(".")[0] + "\r")
        fw.write("\r\r")


        print("Generate Import Interface Done.")
    except:
        print("Generate Import Interface Fail.")


    return 1

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



def genclassSrv_server(fw,id_mcu):
    Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res,timeOut=setup_srv_server_protocol()
    srv_server=[]
    for i in range(0,len(Idsrv)):
        srv_server.append("Srv_server_"+namesrv[i]+"_node")
        fw.write("\nclass Srv_server_"+namesrv[i]+"_node(Node):\r")
        fw.write("    def __init__(self,Obj_uart):\n")
        fw.write("        super().__init__('xicro_"+get_params("microcontroller.namespace").lower()+"_"+srv_server[i].lower()+"')\n")
        fw.write("        self.Obj_uart=Obj_uart\n")
        fw.write("        self.xicro_instruction = Xicro_instruction(self.Obj_uart)\n")
        fw.write("        self.timeout = "+str(timeOut[i])+"\n")
        fw.write("        self.maxlen_response = "+str(len(datagrab_srv_res[i]))+"\n\n")
        callback_srv=genSrv_server(fw,namesrv,interfacesrv,i)
        fw.write("\n\n    # gen service_server callback\n")
        gencallback_srv_server(fw,callback_srv,id_mcu,Idsrv,dataType_srv_req,dataName_srv_req,NofData_srv_req,dataType_srv_res,dataName_srv_res,NofData_srv_res,i)
    return srv_server
def genclassAction_server(fw,id_mcu):
    Idaction_server,nameaction_server,interfaceaction_server,dataType_action_server_req,dataName_action_server_req,datagrab_action_server_req,NofData_action_server_req,datatypeProtocol_action_server_req,bytetograb_action_server_req,dataType_action_server_res,dataName_action_server_res,datagrab_action_server_res,NofData_action_server_res,datatypeProtocol_action_server_res,bytetograb_action_server_res,dataType_action_server_feed,dataName_action_server_feed,datagrab_action_server_feed,NofData_action_server_feed,datatypeProtocol_action_server_feed,bytetograb_action_server_feed,timeOut_action_server = setup_action_server_protocol()
    action_server=[]
    for i in range(0,len(Idaction_server)):
        action_server.append("Action_server_"+nameaction_server[i]+"_node")
        fw.write("\nclass Action_server_"+nameaction_server[i]+"_node(Node):\r")
        fw.write("    def __init__(self,Obj_uart):\n")
        fw.write("        super().__init__('xicro_"+get_params("microcontroller.namespace").lower()+"_"+nameaction_server[i].lower()+"_node')\n")
        fw.write("        self.Obj_uart=Obj_uart\n")
        fw.write("        self.xicro_instruction = Xicro_instruction(self.Obj_uart)\n")
        fw.write("        self.timeout = "+str(timeOut_action_server[i])+"\n")
        callback_action=genAction_server(fw,nameaction_server,interfaceaction_server,i)
        fw.write("\n\n    # gen action_server callback\n")
        gencallback_action_server(fw,callback_action,id_mcu,Idaction_server,nameaction_server,interfaceaction_server,dataType_action_server_req,dataName_action_server_req,datagrab_action_server_req,NofData_action_server_req,datatypeProtocol_action_server_req,bytetograb_action_server_req,dataType_action_server_res,dataName_action_server_res,datagrab_action_server_res,NofData_action_server_res,datatypeProtocol_action_server_res,bytetograb_action_server_res,dataType_action_server_feed,dataName_action_server_feed,datagrab_action_server_feed,NofData_action_server_feed,datatypeProtocol_action_server_feed,bytetograb_action_server_feed,timeOut_action_server,i)
    return action_server
def genSrv_server_spin(fw,srv_server):
    for i in range(0,len(srv_server)):
        fw.write("    "+srv_server[i].lower()+"="+srv_server[i]+"(Obj_uart)\n")
    fw.write("\n\n    # gen srv executor\n")
    for i in range(0,len(srv_server)):
        fw.write("    executor.add_node("+srv_server[i].lower()+")\n")
    return 1
def genAction_server_spin(fw,action_server):
    for i in range(0,len(action_server)):
        fw.write("    "+action_server[i].lower()+"="+action_server[i]+"(Obj_uart)\n")
    fw.write("\n\n    # gen action executor\n")
    for i in range(0,len(action_server)):
        fw.write("    executor.add_node("+action_server[i].lower()+")\n")
    return 1
def gen_import_module_connection(fw):
    try:
        con_type = get_params("microcontroller.connection.type")
        if(con_type=="UART"):
            fw.write("import serial\n")
        elif(con_type=="UDP"):
            fw.write("import socket\n")
        print("gennerate import module connection Done.")
        return 1
    except:
        print("gennerate import module connection Fail.")
        return 0 

def gen_def_check_port(fw):
    try:
        con_type = get_params("microcontroller.connection.type")
        if(con_type=="UART"):
            fw.write("    def check_port_open(self):\n")
            fw.write("        try:\n")
            fw.write("            ser = serial.Serial(self.port,self.baudrate, timeout=1000 ,stopbits=1)\n")    
            fw.write("            print(self.port + ': port is Open.')\n")
            fw.write("            return ser\n")
            fw.write("        except:\n")
            fw.write("            print(self.port + ': open port Fail.')\n        return 0\n")
        elif(con_type=="UDP"):
            fw.write("    def check_port_open(self):\n")
            fw.write("        try:\n")
            fw.write("            ser = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)\n")    
            fw.write("            ser.setblocking(1)\n")
            fw.write("            ser.bind(('', self.udp_port_mcu))\n")
            fw.write("            print('UDP open Connection done.')\n")
            fw.write("            return ser\n")
            fw.write("        except:\n")
            fw.write("            print('UDP open Connection fail.')\n        return 0\n")
        print("gennerate def check_port Done.")
        return 1
    except:
        print("gennerate def check_port Fail.")
        return 0 
def gen_input_arg(fw):
    try:
        con_type = get_params("microcontroller.connection.type")
        if(con_type=="UART"):
            fw.write('    input.add_argument("-serial_port", help="new connection port",type=str)\n')
            fw.write('    input.add_argument("-baudrate", help="new baudrate of mcu",type=str)\n')
        elif(con_type=="UDP"):
            fw.write('    input.add_argument("-ip_address_mcu",help="new ip address of microcontroller",type=str)\n')
            fw.write('    input.add_argument("-udp_port_mcu",help="new connection port of microcontroller",type=int)\n')
        print("gennerate input argument Done.")
        return 1
    except:
        print("gennerate input argument Fail.")
        return 0 
def gen_setup_input_arg(fw):
    try:
        con_type = get_params("microcontroller.connection.type")
        if(con_type=="UART"):
            fw.write("        if( input.serial_port != None):\n")
            fw.write("            self.port = input.serial_port\n")
            fw.write('            print("Input new argument uart_port is : "+self.port)\n')
            fw.write("        else:\n")
            fw.write('            self.port = "'+get_params("microcontroller.connection.serial_port")+'"\n')
            fw.write('            print("Input argument Port use is : "+self.port)\n')
            fw.write("        if( input.baudrate != None):\n")
            fw.write("            self.baudrate = input.baudrate\n")
            fw.write('            print("Input new argument baudrate  is : "+str(self.baudrate))\n')
            fw.write("        else:\n")
            fw.write('            self.baudrate = '+str(get_params("microcontroller.connection.baudrate"))+'\n')
            fw.write('            print("Input arg baudrate is : "+str(self.baudrate))\n')
        elif(con_type=="UDP"):
            fw.write("        if( input.ip_address_mcu != None):\n")
            fw.write("            self.ip_address_mcu = input.ip_address_mcu\n")
            fw.write('            print("Input new argument ip_address_mcu is : "+self.ip_address_mcu)\n')
            fw.write("        else:\n")
            fw.write('            self.ip_address_mcu = "'+get_params("microcontroller.connection.ip_address_mcu")+'"\n')
            fw.write('            print("Input argument ip_address_mcu use is : "+self.ip_address_mcu)\n')
            fw.write("        if( input.udp_port_mcu != None):\n")
            fw.write("            self.udp_port_mcu = input.udp_port_mcu\n")
            fw.write('            print("Input new argument udp_port_mcu  is : "+str(self.udp_port_mcu))\n')
            fw.write("        else:\n")
            fw.write('            self.udp_port_mcu = '+str(get_params("microcontroller.connection.udp_port_mcu"))+'\n')
            fw.write('            print("Input arg udp_port_mcu is : "+str(self.udp_port_mcu))\n')
        print("gennerate setup input argument Done.")
        return 1
    except:
        print("gennerate setup input argument Fail.")
        return 0 
def gen_def_receive_uart(fw):
    try:
        con_type = get_params("microcontroller.connection.type")
        if(con_type=="UART"):
            fw.write("def Receive_uart(Obj_uart): #processer 1\n")
            fw.write('    print("Start Receive Xicro_protocol")\n')
            fw.write("    while(1):\n")
            fw.write("        try:\n            s = Obj_uart.ser.read()\n")
            fw.write('            Obj_uart.Buff[Obj_uart.index.value]=(int.from_bytes(s, byteorder="big",signed=0) )\n')
            fw.write("            Obj_uart.index.value = (Obj_uart.index.value + 1 )%1000\n")
            fw.write("        except:\n            Obj_uart.ser = Obj_uart.check_port_open()\n")
        elif(con_type=="UDP"):
            fw.write("def Receive_uart(Obj_uart): #processer 1\n")
            fw.write('    print("Start Receive Xicro_protocol")\n')
            fw.write("    while(1):\n")
            fw.write("        try:\n            datafromWIFI = Obj_uart.ser.recvfrom(1000)\n")
            fw.write("            if(datafromWIFI[1][0]==Obj_uart.ip_address_mcu):\n")
            fw.write('                for i in range(0,len(datafromWIFI[0])):\n')
            fw.write("                    Obj_uart.Buff[Obj_uart.index.value]=datafromWIFI[0][i]\n")
            fw.write("                    Obj_uart.index.value = (Obj_uart.index.value + 1 )%1000\n")
            fw.write("        except:\n            Obj_uart.ser = Obj_uart.check_port_open()\n")
        print("gennerate def receive Done.")
        return 1
    except:
        print("gennerate def receive Fail.")
        return 0 


def gennerate(): 
    
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,Nofdata=setupvarforcreatelib()
    # print(id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,Nofdata)
    pathr= os.path.join(gPath(1)+'/.Xicro_node_preSetup.xicro')
    pathw= os.path.join(gPath(0)+ '/scripts/xicro_node_'+get_params("microcontroller.namespace")+"_ID_"+str(id_mcu)+'_'+input.mcu_type+'.py')
    # os.popen("code " + pathw)

    # print(gPath(0)+ '/scripts/xicro_node_'+get_params("Namespace")+"_ID_"+str(id_mcu)+'.py')
    fr=open(pathr, 'r') 
    fw=open(pathw, 'w') 
    fw.write("#!/usr/bin/python3\n\n\n\n")
    fw.write("# ***************************************************************************************************************************************************\n")
    fw.write("#      |          This script was auto-generated by generate_Xicro_node.py which received parameters from setup_xicro.yaml                    |\n")
    fw.write("#      |                                         EDITING THIS FILE BY HAND IS NOT RECOMMENDED                                                 |\n")
    fw.write("# ***************************************************************************************************************************************************\n\n")
    c=0
    callback=[]
    srv_server=[]
    action_server=[]
    for line in fr:
        c=c+1
        if(line=="!#@ gen_sub\n"):
            callback=genSub(fw,nameofTopic,interfacefile)
        elif(line=="!#@ gen_callback_sub\n"):
            gencallback(fw,callback,id_mcu,id_topic,dataType,dataName,Nofdata)
        elif(line=="!#@ gen_setup_function\n"):
            fw.write("\n\ndef setup_var_protocol():\n\n")
            Idmsgg,nametopicc,interfacetopicc,dataTypee,dataNamee,datagrabb,NofDataa,datatypeProtocoll,bytetograbb=setup_var_protocol()
            # cal(get_params("Baudrate"),bytetograbb,NofDataa,nametopicc)
            fw.write("    return "+str(Idmsgg)+","+str(nametopicc)+","+str(interfacetopicc)+","+str(dataTypee)+","+str(dataNamee)+","+str(datagrabb)+","+str(NofDataa)+","+str(datatypeProtocoll)+","+str(bytetograbb))
            fw.write("\n\n")
            Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res,timeOut=setup_srv_protocol()
            fw.write("\n\ndef setup_srv_protocol():\r\r")
            fw.write("    return "+str(Idsrv)+","+str(namesrv)+","+str(interfacesrv)+","+str(dataType_srv_req)+","+str(dataName_srv_req)+","+str(datagrab_srv_req)+","+str(NofData_srv_req)+","+str(datatypeProtocol_srv_req)+","+str(bytetograb_srv_req)+","+str(dataType_srv_res)+","+str(dataName_srv_res)+","+str(datagrab_srv_res)+","+str(NofData_srv_res)+","+str(datatypeProtocol_srv_res)+","+str(bytetograb_srv_res)+","+str(timeOut))
            Idsrv,namesrv,interfacesrv,dataType_srv_req,dataName_srv_req,datagrab_srv_req,NofData_srv_req,datatypeProtocol_srv_req,bytetograb_srv_req,dataType_srv_res,dataName_srv_res,datagrab_srv_res,NofData_srv_res,datatypeProtocol_srv_res,bytetograb_srv_res,timeOut=setup_srv_server_protocol()
            fw.write("\n\ndef setup_srv_server_protocol():\r\r")
            fw.write("    return "+str(Idsrv)+","+str(namesrv)+","+str(interfacesrv)+","+str(dataType_srv_req)+","+str(dataName_srv_req)+","+str(datagrab_srv_req)+","+str(NofData_srv_req)+","+str(datatypeProtocol_srv_req)+","+str(bytetograb_srv_req)+","+str(dataType_srv_res)+","+str(dataName_srv_res)+","+str(datagrab_srv_res)+","+str(NofData_srv_res)+","+str(datatypeProtocol_srv_res)+","+str(bytetograb_srv_res)+","+str(timeOut))
            fw.write("\n\n")
            Idaction,nameaction,interfaceaction,dataType_action_req,dataName_action_req,datagrab_action_req,NofData_action_req,datatypeProtocol_action_req,bytetograb_action_req,dataType_action_res,dataName_action_res,datagrab_action_res,NofData_action_res,datatypeProtocol_action_res,bytetograb_action_res,dataType_action_feed,dataName_action_feed,datagrab_action_feed,NofData_action_feed,datatypeProtocol_action_feed,bytetograb_action_feed,timeOut = setup_action_client_protocol()
            fw.write("\n\ndef setup_action_client_protocol():\r\r")
            fw.write("    return "+str(Idaction)+","+str(nameaction)+","+str(interfaceaction)+","+str(dataType_action_req)+","+str(dataName_action_req)+","+str(datagrab_action_req)+","+str(NofData_action_req)+","+str(datatypeProtocol_action_req)+","+str(bytetograb_action_req)+","+str(dataType_action_res)+","+str(dataName_action_res)+","+str(datagrab_action_res)+","+str(NofData_action_res)+","+str(datatypeProtocol_action_res)+","+str(bytetograb_action_res)+","+str(dataType_action_feed)+","+str(dataName_action_feed)+","+str(datagrab_action_feed)+","+str(NofData_action_feed)+","+str(datatypeProtocol_action_feed)+","+str(bytetograb_action_feed)+","+str(timeOut ))
            fw.write("\n\n")
            Idaction,nameaction,interfaceaction,dataType_action_req,dataName_action_req,datagrab_action_req,NofData_action_req,datatypeProtocol_action_req,bytetograb_action_req,dataType_action_res,dataName_action_res,datagrab_action_res,NofData_action_res,datatypeProtocol_action_res,bytetograb_action_res,dataType_action_feed,dataName_action_feed,datagrab_action_feed,NofData_action_feed,datatypeProtocol_action_feed,bytetograb_action_feed,timeOut = setup_action_server_protocol()
            fw.write("\n\ndef setup_action_server_protocol():\r\r")
            fw.write("    return "+str(Idaction)+","+str(nameaction)+","+str(interfaceaction)+","+str(dataType_action_req)+","+str(dataName_action_req)+","+str(datagrab_action_req)+","+str(NofData_action_req)+","+str(datatypeProtocol_action_req)+","+str(bytetograb_action_req)+","+str(dataType_action_res)+","+str(dataName_action_res)+","+str(datagrab_action_res)+","+str(NofData_action_res)+","+str(datatypeProtocol_action_res)+","+str(bytetograb_action_res)+","+str(dataType_action_feed)+","+str(dataName_action_feed)+","+str(datagrab_action_feed)+","+str(NofData_action_feed)+","+str(datatypeProtocol_action_feed)+","+str(bytetograb_action_feed)+","+str(timeOut ))
            fw.write("\n\n")
        elif(line=="!#@ gen_id_mcu\n"):
            fw.write("    Idmcu = "+str(id_mcu)+"\n")
        elif(line=="!#@ gen_import_interface\n"):
            fw.write("# gen Import interfaces\n")
            genImport(fw)
        elif(line=="!#@ gen_self_id_mcu\n"): # 2 
            fw.write("        self.Idmcu = "+str(id_mcu)+"\n")
        elif(line=="!#@ gen_def_check_port_open\n"):
            gen_def_check_port(fw)
        elif(line=="!#@ gen_service_server\n"):
            srv_server=genclassSrv_server(fw,id_mcu)
        elif(line=="!#@ gen_action_server\n"):
            action_server=genclassAction_server(fw,id_mcu)
        elif(line=="!#@ gen_service_server_spin\n"):
            genSrv_server_spin(fw,srv_server)
        elif(line=="!#@ gen_action_server_spin\n"):
            genAction_server_spin(fw,action_server)
        elif(line=="!#@ gen_name_of_publisher_node\n"):
            fw.write("        super().__init__('xicro_publisher_node_"+get_params("microcontroller.namespace").lower()+"')\n" )
        elif(line=="!#@ gen_name_of_subscriber_node\n"):
            fw.write("        super().__init__('xicro_subscriber_node_"+get_params("microcontroller.namespace").lower()+"')\n" )
        elif(line=="!#@ gen_name_of_srv_client_node\n"):
            fw.write("        super().__init__('xicro_service_client_node_"+get_params("microcontroller.namespace").lower()+"_'+str(sequence))")
        elif(line=="!#@ gen_name_of_action_client_node\n"):
            fw.write("        super().__init__('xicro_action_client_node_"+get_params("microcontroller.namespace").lower()+"_'+str(sequence))")
        elif(line=="!#@ gen_mcu_type\n"):
            fw.write('    MCU_TYPE = "'+input.mcu_type+'"\n')
        elif(line=="!#@ gen_input_arg\n"):
            gen_input_arg(fw)
        elif(line=="!#@ gen_setup_arg\n"):
            gen_setup_input_arg(fw)
        elif(line=="!#@ gen_def_receive_uart\n"):
            gen_def_receive_uart(fw)
        elif(line=="!#@ gen_import_module_connection\n"):
            gen_import_module_connection(fw)
        elif(line=="!#@ gen_Tx_type\n" and get_params("microcontroller.connection.type") == "UART"):
            fw.write("                Obj_uart.ser.write(bytearray(Obj_uart.Buff_SSend[0]))\n")
        elif(line=="!#@ gen_Tx_type\n" and get_params("microcontroller.connection.type") == "UDP"):
            fw.write("                Obj_uart.ser.sendto(bytearray(Obj_uart.Buff_SSend[0]), (Obj_uart.ip_address_mcu,Obj_uart.udp_port_mcu))\n")
        else:
            fw.write(line)
    return 1
def addentrypoint():
    pathr= os.path.join(gPath(0), 'CMakeLists.txt')
    f=open(pathr, 'r+') 
    entryp=[]
   
    for line in f:
        entryp.append(line)
    


    entrystring="  scripts/"+"xicro_node_"+get_params("microcontroller.namespace")+"_ID_"+str(get_params("microcontroller.idmcu"))+'_'+input.mcu_type+'.py\n'
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
        global input 
        input = argparse.ArgumentParser()
        input.add_argument("-mcu_type", help="type of microcontroller",choices=["arduino","esp","stm32"],type=str,required=1)
        input = input.parse_args()
        if(input.mcu_type == "arduino" or input.mcu_type ==  "stm32" or "esp"):
            flagargs=1
    
    except:
        print('******  Please input argv [-mcu_type]  ******')
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
