# -*- coding:utf-8 -*-

##author : ruijie.qiao
##email  : ruijie.qiao@gmail.com
##date   : 2013-8-18
##modify : 2013-8-22

import gblvar
import apimethod
import config
import parameter
import sys
import logs

import traceback
import platform


def getQueryStr(lsList):
    try:
        list1=[]
        starStr=""
        for obj in lsList:
            yclList=obj.split('=')
            if yclList[0].lower()=='--query':
                 list1.append(obj[len('--query='):])
        """
        for obj in lsList:
            if '--Query=' in obj:
                list1.append(obj[len('--Query='):])
        """
        if len(list1)>1:
            obj1=list1[0].split(".")
            obj2=list1[1].split(".")
            starStr=obj1[0]
            for i in range(1,len(obj1)):
                if obj1[i]==obj2[i]:
                    starStr=starStr+"."+obj1[i]
                else:
                    break
            starStr=starStr+"."
            lastStr=""
            n=len(starStr)
            for obj in list1:
                lastStr=lastStr+ ","+obj[n:]
            Query=starStr+'{'+lastStr[1:]+'}'
            return Query
        return None
    except Exception:
        info = traceback.format_exc()
        CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)


def isGetHelp(paramDict):
    # --key=value 类型参数，将小写key和原始key保存到字典中------>lower(key):key
    keyKEYdict=paramDict['keyKEYdict']
    # --key=value类型参数，以字典方式保存，且，key全部小写------->key:value
    keyVALUEdict=paramDict['keyVALUEdict']
    # --key 类型参数, 以列表方式保存, 且，key全部小写----------->lower(key)
    keylist=paramDict['keylist']
    #短命令参数集合，以小写方式存储
    shortList=paramDict['shortList']
    # action 类型数据，以列表方式保存，且 action全部小写
    acList=paramDict['acList']

    try:
        list2=[]
        #排除判断的公共参数
        notPDList=['output','query','outputfile','help','showurl']
        actions=""
        #if 'config' in acList: return False
        if len(keylist)>0:
            lspd=False
            CustomInfo="Parameter format error, please check the parameters: "
            for o in keylist:
                if o!="help":
                    lspd=True
                    CustomInfo=CustomInfo+"--"+o+","
            if lspd:
                logs.logs(CustomInfo,CustomInfo).getECSLogger()
                return True

        if len(shortList)>0:
            lspd=False
            CustomInfo="Parameter format error, please check the parameters:"
            for o in shortList:
                if o!='-h':
                    lspd=True
                    CustomInfo=CustomInfo+o+","
            if lspd:
                logs.logs(CustomInfo,CustomInfo).getECSLogger()
                return True


        if len(acList)>0:
            for o in acList:
                fdindex=o.find('.py')
                if fdindex==-1:
                    actions=o
                    break
        else:
            actions=""

        #判断参数中是不是有 --help
        helpX=False
        for tsParm in notPDList:
            if tsParm in keylist:
                keylist.remove(tsParm)
                if tsParm=='help':
                    helpX=True

        if len(shortList)>0:
            for o in shortList:
                if o.lower()=='-h':
                    helpX=True

        #如果没有操作名，且有--help参数,则进入分页显示help，并退出程序
        if actions=="" and helpX:
            getAllHelp(paramDict,[],[])
            sys.exit(1)
            """
            getAllHelp(paramDict,[],[])
            sys.exit(1)
            """

        if helpX:
            if actions!="":
                """
                if actions.lower()=='actions':
                    getAllHelp(paramDict,[],[])
                    return True
                """
                acNameList=gblvar.ACTION_Dict.keys()
                for acName in acNameList:
                    if acName.lower()==actions.lower():
                        acDict=gblvar.ACTION_Dict[acName]
                        mustList=acDict['MustParameters']
                        optionalList=acDict['OptionalParameters']
                        getAllHelp(paramDict,mustList,optionalList)
                        return True
                print "Operation not supported: '"+ actions + "'"
                return True
        return False
    except Exception:
        info = traceback.format_exc()
        CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)


def getAllHelp(paramDict,MustParameters=[],OptionalParameters=[]):

    # --key=value 类型参数，将小写key和原始key保存到字典中------>lower(key):key
    keyKEYdict=paramDict['keyKEYdict']
    # --key=value类型参数，以字典方式保存，且，key全部小写------->key:value
    keyVALUEdict=paramDict['keyVALUEdict']
    # --key 类型参数, 以列表方式保存, 且，key全部小写----------->lower(key)
    keylist=paramDict['keylist']
    #短命令参数集合，以小写方式存储
    shortList=paramDict['shortList']
    # action 类型数据，以列表方式保存，且 action全部小写
    acList=paramDict['acList']

    #判断是否列出Actions
    boolPd=False

    #必须按参数 MustParameters
    #可选参数OptionalParameters

    #需要显示的参数名列表
    parmKeyList=[]
    #当存在可选参数和必须参数时，记录可选参数和必须按参数的第一个值
    titleList=["",""]

    try:
        if 'pagenumber' in keyVALUEdict.keys():
            PageNumber=int(keyVALUEdict['pagenumber'])
        else:
            PageNumber=1
        if 'pagesize' in keyVALUEdict.keys():
            PageSize=int(keyVALUEdict['pagesize'])
        else:
            PageSize=10
    except:
        print 'Parameters of the PageNumber or PageSize value is not an integer'
        sys.exit(1)
    if PageNumber<=0:PageNumber=1
    if PageSize<=0:PageSize=10


    if len(acList)==1:
        parmKeyList=gblvar.ACTION_List.keys()
        parmKeyList.sort()
        boolPd=True
        parmKeyList.sort()
    else:
        if len(MustParameters)>0:
            #parmKeyList.append('Must Parameters')
            MustParameters.sort()
            titleList[0]=MustParameters[0]
            parmKeyList=parmKeyList+MustParameters

        if len(OptionalParameters)>0:
            #parmKeyList.append('Optional Parameters')
            OptionalParameters.sort()
            titleList[1]=OptionalParameters[0]
            parmKeyList=parmKeyList+OptionalParameters

    #总参数个数
    parameterCount=len(parmKeyList)

    #计算总页数
    countPage=parameterCount/PageSize
    if parameterCount % PageSize >0:
        countPage=countPage+1

    endNum=PageNumber*PageSize
    if endNum>parameterCount:
        #结束位置
        endNum=parameterCount
        #页数
        PageNumber=countPage
    #开始位置
    starNum=(PageNumber-1)*PageSize
    if boolPd:
        print ""
        print "Actions List"
        for n in range(starNum,endNum):
            key=parmKeyList[n]
            kbStr=" " * (40-len(key))
            key2=key.replace("_",".")
            print key2 + kbStr + gblvar.ACTION_List[key]
    else:
        for n in range(starNum,endNum):
            key=parmKeyList[n]
            if key==titleList[0]:
                print ""
                print "Must Parameters"
            if key==titleList[1]:
                print ""
                print "Optional Parameters"
            kbStr=" " * (40-len(key))
            key2=key.replace("_",".")

            print '--'+ key2 + kbStr + gblvar.ecsParameters[key]


    print "PageNumber:",PageNumber,'        ','PageSize:',endNum-starNum,'        ','parameterCount:',parameterCount,'      ','pageCount:',countPage



def getParm():
    # --key=value 类型参数，将小写key和原始key保存到字典中------>lower(key):key
    keyKEYdict={}
    # --key=value类型参数，以字典方式保存，且，key全部小写------->key:value
    keyVALUEdict={}
    # --key 类型参数, 以列表方式保存, 且，key全部小写----------->lower(key)
    keylist=[]
    #短命令参数集合，以小写方式存储
    shortList=[]
    # action 类型数据，以列表方式保存，且 action全部小写
    acList=[]
    for o in sys.argv:
        if o[0:2]=='--':
            indexD=o.find('=')
            if indexD!=-1:
                keyKEYdict[o[2:indexD].lower()]=o[2:indexD]
                keyVALUEdict[o[2:indexD].lower()]=o[indexD+1:]
            else:
                keylist.append(o[2:].lower())
        elif o[0:1]=='-':
            shortList.append(o.lower())
            #shortList.append(o[0:2].lower())
        else:
            acList.append(o.lower())
    paramDict={}
    paramDict['keyKEYdict']=keyKEYdict
    paramDict['keyVALUEdict']=keyVALUEdict
    paramDict['keylist']=keylist
    paramDict['shortList']=shortList
    paramDict['acList']=acList
    return paramDict


if __name__ == '__main__':
    #(clDict,clList,clList2)=getParm()
    paramDict=getParm()
    if len(paramDict['keyKEYdict'].keys())==0:
        if len(paramDict['keylist'])==0 and len(paramDict['shortList'])==0:
            if len(paramDict['acList'])==1:
                message='The lack of the operation name and parameters.'
                logs.logs(None,message).getCustom_Log().error(message)
                sys.exit()
    pd=False
    pd=isGetHelp(paramDict)
    if pd:
        sys.exit()
    apimethod.setup_cmdlist()
    parmt = parameter.inputParameter(paramDict['keyKEYdict'])
    (gblvar.options, gblvar.args) = parmt.reParameter()

    sysstr = platform.system()
    if(sysstr =="Windows"):
        pass
    elif(sysstr == "Linux"):
        oo=getQueryStr(sys.argv)
        if oo!=None:
            gblvar.options.Query=oo
    else:
        oo=getQueryStr(sys.argv)
        if oo!=None:
            gblvar.options.Query=oo

    if gblvar.options.config_file is not None:
        CONFIGFILE = gblvar.options.config_file

    if len(gblvar.args) < 1:
        message='Please input Action!'
        logs.logs(None,message).getCustom_Log().error(message)
        sys.exit(1)

    if gblvar.args[0].lower() != 'config':
        config.config().get_configure()
    else:
        config.config().set_configure()
        sys.exit(1)


    #if gblvar.args[0].lower() not in apimethod.CMD_LIST.keys():
    if gblvar.args[0].lower() not in gblvar.ActionKeyDict.keys():
        message="unsupported command : %s " % gblvar.args[0]
        logs.logs(None,message).getCustom_Log().error(message)
        #print "unsupported command : %s " % gblvar.args[0]
        sys.exit(1)
    cmd = gblvar.args[0].lower()

    #res = apimethod.CMD_LIST[cmd]()
    res = apimethod.ExecuteTheCommand(cmd)




