#!/usr/bin/python3
import os
import yaml

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
    datagrab=[]
    NofData=[]
    datatypeProtocol=[]
    bytetograb=[]
    try:
        for i in range (0,len(interfacetopic)):
            tempType=[]
            tempName=[]
            tempdatagrab=[]
            tempN=[]
            tempdatatypeProtocol=[]
            tempbytetograb=[]
            path = os.path.join(os.path.expanduser('~'), 'xicro_ws', 'src','xicro_interfaces','msg', interfacetopic[i])
            msg = open(path, 'r').read().splitlines()
            for j in range(0,len(msg)):
                line=msg[j].split()
                tempN.append(checkNofdata(line[0]))
                if(line[0].find("[")!=-1):
                    line[0]=line[0][0:line[0].find("[")]
                tempType.append(line[0])
                tempName.append(line[1])
                a,b=typetoProtocol(line[0],tempN[j])
                tempdatatypeProtocol.append(a)
                tempbytetograb.append(b)
                if(tempN[j]!=1):
                    tt=[]
                    for k in range(0,tempN[j]):
                        if(line[0]=="string"):
                            tt.append("")
                        elif(line[0]=="float32" or line[0]=="float64"):
                            tt.append(0.0)
                        elif(line[0]=="bool"):
                            tt.append(False)   
                        else:
                            tt.append(0)
                    tempdatagrab.append(tt)
                else:
                    if(line[0]=="string"):
                        tempdatagrab.append("")
                    elif(line[0]=="float32" or line[0]=="float64"):
                        tempdatagrab.append(0.0)
                    elif(line[0]=="bool"):
                        tempdatagrab.append(False)
                    else:
                        tempdatagrab.append(0)
            bytetograb.append(tempbytetograb)
            datatypeProtocol.append(tempdatatypeProtocol)
            NofData.append(tempN)
            dataType.append(tempType)
            dataName.append(tempName)
            datagrab.append(tempdatagrab)
        print('Generate variable from msg Done.')
    except:
        print('Generate variable from msg Failed.')
        return 0,0,0,0,0,0
   
    return Idmsg,nametopic,interfacetopic,dataType,dataName,datagrab,NofData,datatypeProtocol,bytetograb

def get_params(q):
    try:
        path = os.path.join(os.path.expanduser('~'), 'xicro_ws', 'src','xicro_pkg','config', 'setup_xicro.yaml')
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
            path = os.path.join(os.path.expanduser('~'), 'xicro_ws', 'src','xicro_interfaces','msg',  interfacefile[i])
            msg = open(path, 'r').read().splitlines()
            for j in range(0,len(msg)):
                line=msg[j].split()
                tempType.append(line[0])
                tempName.append(line[1])
                tempdatagrab.append(0)
                tempN.append(checkNofdata(line[0]))
            NofData.append(tempN)
            dataType.append(tempType)
            dataName.append(tempName)
           
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
            w=w+getbeforedot(interfacefile[i])+",'"+nameofTopic[i]+"'," 
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
        else:
            print(typee)
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
def gennerate(): 
    
    id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,Nofdata=setupvarforcreatelib()
    # print(id_mcu,id_topic,nameofTopic,interfacefile,dataType,dataName,Nofdata)
    pathr= os.path.join(os.path.expanduser('~'), 'xicro_ws', 'src','xicro_pkg','scripts', '.Xicro_node_preSetup.txt')
    pathw= os.path.join(os.path.expanduser('~'), 'xicro_ws', 'src','xicro_pkg','scripts', 'xicro_node_'+get_params("Namespace")+"_ID_"+str(id_mcu)+'.py')
    fr=open(pathr, 'r') 
    fw=open(pathw, 'w+') 
    fw.write("#!/usr/bin/python3\r\n")
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
        elif(c==440):
            fw.write("    Idmcu = "+str(id_mcu))
        else:
            fw.write(line)
    return 1
def addentrypoint():
    pathr= os.path.join(os.path.expanduser('~'), 'xicro_ws', 'src','xicro_pkg', 'CMakeLists.txt')
    f=open(pathr, 'r+') 
    entryp=[]
   
    for line in f:
        entryp.append(line)
      
    # entryString="        \t\"xicro_node_"+get_params("Namespace")+"_ID_"+str(get_params("Idmcu"))+" = scripts."+"xicro_node_"+get_params("Namespace")+"_ID_"+str(get_params("Idmcu"))+":main\",\n"
    # stopP=0
    # h=0
    # for i in range(0,len(entryp)):
    #     if(entryp[i]==entryString):
    #         h=1
    #     if(entryp[i]=='#1orcix\n'):
    #         stopP=i
    # if(not h):
    #     entryp.insert(stopP,entryString)
    # print(entryp)
    # moduString="        \"scripts.xicro_node_"+get_params("Namespace")+"_ID_"+str(get_params("Idmcu"))+"\",\n"

    # stopP=0
    # h=0
    # for i in range(0,len(entryp)):
    #     if(entryp[i]==moduString):
    #         h=1
    #     if(entryp[i]=='#2orcix\n'):
    #         stopP=i
    # if(not h):
    #     entryp.insert(stopP,moduString)

    entrystring="  scripts/"+"xicro_node_"+get_params("Namespace")+"_ID_"+str(get_params("Idmcu"))+".py\n"
    stopP=0
    h=0
    for i in range(0,len(entryp)):
        if(entryp[i]==entrystring):
            h=1
        if(entryp[i]=='#orcix\n'):
            stopP=i
    if(not h):
        entryp.insert(stopP,entrystring)
    pathw= os.path.join(os.path.expanduser('~'), 'xicro_ws', 'src','xicro_pkg', 'CMakeLists.txt')
    fw=open(pathw, 'w')
    for i in range(0,len(entryp)):
        fw.write(entryp[i])


    return 1

    
def main():
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