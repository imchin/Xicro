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

    # for i in range(0,len(dataName)): #Rename . to _of_
    #     q=[]
    #     for j in range(0,len(dataName[i])):
    #         dataName[i][j]=dataName[i][j].replace(".","__of__")
    
    
    # print("Datatype :",dataType)
    # print("DataName :",dataName)
    # print("Nofdata :",NofData)
    return id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,NofData
def setup_var_protocol():
    setup_pub=get_params('Setup_Publisher')
    Idmsg=[]
    nametopic=[]
    interfacetopic=[]
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
        NofData.append(tempN)
        dataType.append(tempType)
        dataName.append(tempName)
    # print(Idmsg,nametopic,interfacetopic,dataType,dataName,datagrab,NofData,datatypeProtocol,bytetograb)
    print('Generate variable from msg Done.')

    print('Generate variable from msg Failed.')
    # return 0,0,0,0,0,0,0,0,0
    for i in range(0,10):
            Idmsg,id_topic,nametopic,interfacetopic,dataType,dataName,NofData=expandSub(Idmsg,[],nametopic,interfacetopic,dataType,dataName,NofData)

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

def cal(buad_rate,byteGrab,Nofdata,NameToppic):
    bytePerS=buad_rate/10.00
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
            return    "            self._SendUint8(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="uint16"):
            return  "            self._SendUint16(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="uint32"):
            return  "            self._SendUint32(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="uint64"):
            return  "            self._SendUint64(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="int8"):
            return  "            self._SendInt8(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="int16"):
            return  "            self._SendInt16(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="int32"):
            return  "            self._SendInt32(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="int64"):
            return  "            self._SendInt64(msg."+namee+","+str(Nofdata)+ ")\n"  
        elif(typee=="float32"):
            return  "            self._SendFloat32(msg."+namee+","+str(Nofdata)+ ")\n"  
        elif(typee=="string"):
            return  "            self._SendString(msg."+namee+","+str(Nofdata)+ ")\n"
        elif(typee=="bool" and Nofdata==1):
            return  "            self._SendBool(msg."+namee+",1,"+str(cond)+ ")\n"
        elif(typee=="bool" and Nofdata!=1):
            return  "            self._SendBool(msg."+namee+","+str(Nofdata)+","+str(cond)+ ")\n"
        elif(typee=="float64" and ( sys.argv[1] =="arduino" or sys.argv[1] =="esp" )):
            return  "            self._SendFloat32(msg."+namee+","+str(Nofdata)+ ")\n"    
        elif(typee=="float64"):
            return  "            self._SendFloat64(msg."+namee+","+str(Nofdata)+ ")\n"
        else:
            print("ErorType : ",typee)
            return "1"
    except:
        print("Format .msg wrong")
    return "0"
def gencallback(fw,callback,id_mcu,id_topic,dataType,dataName,Nofdata):
    try:
        fw.write("    # gen\r")
        for i in range(len(callback)):
            fw.write("    def "+getafterdot(callback[i])+"(self,msg):\r")
            fw.write("        try:\r\r")
            fw.write("            self.CRC=0\r")
            fw.write("            self._SendStart()\r")
            fw.write("            self._SendSignature("+str(id_mcu)+","+"2)\r")
            fw.write("            self._SendIdtopic("+str(id_topic[i])+")\r")
            for j in range (0,len(dataType[i])):
                cond=j<len(dataType[i])-1 #check flag continue or stop
                fw.write(typetofunc(dataType[i][j],dataName[i][j],Nofdata[i][j],cond))
                if(dataType[i][j]=="bool" and Nofdata[i][j]==1 ):
                    fw.write("# auto by 1 bool\n")
                elif(cond):
                    fw.write("            self._SendContinue()\r")
                else:
                    fw.write("            self._SendStop()\r")
                    
            fw.write("            self._SendCRC()\r")
            fw.write("        except:\r            1\r\r")
            fw.write("\r        return 1\r\r\r\r")
        print("gennerate Callback Done.")
        return 1
    except:
        print("gennerate Callback Fail.")
    return 0
def genImport(fw):
    interfacemsg=[]
    try:
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
        fw.write("\r\r")
        print("Generate Import Interface Done.")
    except:
        print("Generate Import Interface Fail.")


    return 1
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
        if(c==157):
            callback=genSub(fw,nameofTopic,interfacefile)
        elif(c==405):
            gencallback(fw,callback,id_mcu,id_topic,dataType,dataName,Nofdata)
        elif(c==75):
            fw.write("\r\rdef setup_var_protocol():\r\r")
            Idmsgg,nametopicc,interfacetopicc,dataTypee,dataNamee,datagrabb,NofDataa,datatypeProtocoll,bytetograbb=setup_var_protocol()
            fw.write("    return "+str(Idmsgg)+","+str(nametopicc)+","+str(interfacetopicc)+","+str(dataTypee)+","+str(dataNamee)+","+str(datagrabb)+","+str(NofDataa)+","+str(datatypeProtocoll)+","+str(bytetograbb))
            fw.write("\r\r")
        elif(c==439):
            fw.write("    Idmcu = "+str(id_mcu)+"\n")
        elif(c==10):
            fw.write("#gen\r")
            genImport(fw)
        elif(c==799):
            b=get_params("Buadrate")
            f=0
            fw.write("            ser = serial.Serial(Port,"+ str(get_params("Buadrate"))+", timeout=1000 ,stopbits=1)\n")    
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