# -*- coding:utf-8 -*-
import sys
import urllib, urllib2
import base64
import hmac
import hashlib
from hashlib import sha1
import time
import uuid
import gblvar
import logs
import contotable
import contoText
import json
import os
import traceback
import config
import getQueryData
import contoxml
import authorizationInfo
import platform

#用于传入action调用哪个函数
CMD_LIST = {}

#标志位用于函数
mark = None

# ISO8601规范，注意使用GMT时间
timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
parameters = { \
        # 公共参数
        'Format'        : 'json', \
        'Version'       : '2014-05-26', \
        'SignatureVersion'  : '1.0', \
        'SignatureMethod'   : 'HMAC-SHA1', \
        'SignatureNonce'    : str(uuid.uuid1()), \
        'TimeStamp'         : timestamp, \
\
        # 接口参数
        #'Action'            : 'DescribeZones', \
        #'RegionId'          : 'cn-hangzhou-dg-a01', \
}


def setup_cmdlist():
    #lwc add 2014-8-25
    CMD_LIST['adduser'] = cmd_addUser
    CMD_LIST['removeuser']=cmd_RemoveUser
    CMD_LIST['putuserpolicy'] = cmd_putUserPolicy
    CMD_LIST['deleteuserpolicy'] = cmd_deleteUserPolicy
    CMD_LIST['listuserpolicies'] = cmd_listUserPolicies
    CMD_LIST['listusers'] = cmd_ListUsers




def getParmGblvarOptions():
    parmGblvarOptions={}
    jsonStr=str(gblvar.options)
    strDict=eval(jsonStr)
    for key in strDict.keys():
        if strDict[key]!=None:
            parmGblvarOptions[key]=strDict[key]
    return parmGblvarOptions

def percent_encode(str):
    try:
        # 使用urllib.quote编码后，将几个字符做替换即满足ECS API规定的编码规范
        res = urllib.quote(str.decode(sys.stdin.encoding).encode('utf8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res
    except Exception:
        info = traceback.format_exc()
        CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)

def compute_signature(parameters):
    try:
        # 将参数按Key的字典顺序排序
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        # 生成规范化请求字符串
        canonicalizedQueryString = ''
        for (k,v) in sortedParameters:
            canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)
        # 生成用于计算签名的字符串 stringToSign
        stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])
        # 计算签名，注意accessKeySecret后面要加上字符'&'
        h = hmac.new(gblvar.KEY + "&", stringToSign, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature
    except Exception:
        info = traceback.format_exc()
        CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)


def conServer():
    if gblvar.options.OwnerId!=None:
        parameters['OwnerId'] =gblvar.options.OwnerId
    parameters['AccessKeyId'] = gblvar.ID
    #lwc add 2014-8-25
    if gblvar.options.Format=="table" or gblvar.options.Format=="text" or gblvar.options.Format=="xml":
        checkNotNone("json" , 'Format')
    else:
        checkNotNone(gblvar.options.Format , 'Format')
    # 计算签名并把签名结果加入请求参数
    signature = compute_signature(parameters)
    parameters['Signature'] = signature
    # 发送请求
    url = gblvar.ECS_HOST + "/?" + urllib.urlencode(parameters)
    if gblvar.options.showURL=='true':print "url-->",url
    request = urllib2.Request(url)

    #如果指定了outputfile,则检查文件是否创建，否则outputfile=None
    if gblvar.options.outputfile !=None  and gblvar.options.outputfile!="":
        outputfile=config.config().changeFilePath(gblvar.options.outputfile)
        config.config().checkFile(outputfile)
    else:
        outputfile=None
    try:
        conn = urllib2.urlopen(request)
        response = conn.read()
        if outputfile!=None:
            f = file(outputfile, 'w')
            f.write(response)
            f.close()
        #根据Query参数，对response数据进行检索
        dictObj=getQueryRS(response,parameters["Format"],gblvar.options.Query)
        #控制输出格式
        rSetOutPutInfo(dictObj,gblvar.options.Format,None,outputfile)
    except urllib2.HTTPError, e:
        error_msg = e.read().strip()
        if outputfile!=None:
            f = file(outputfile, 'w')
            f.write(error_msg)
            f.close()
        rSetOutPutInfo(json.loads(error_msg),gblvar.options.Format,None,outputfile)
    except IOError:
        info = traceback.format_exc()
        CustomInfo="No permission to write to the file"
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)



def getQueryRS(strContent,strType,query):
    """
    根据返回的结果，对其进行Query查询
    :param strContent:
    :param strType:
    :param query:
    :return:  目前全部以json 的格式反回
    """
    returnStr=strContent
    try:
        if query==None or query=="":
            return strContent
        else:
            try:
                query=query.decode('utf-8')
            except:
                #query=query.decode('gbk').encode('utf-8')
                query=query.decode('gbk')
            #query=query.decode('utf-8').encode('utf-8')
            x=getQueryData.getQueryData(strContent,None,query)
            return x.getQueryData()
    except Exception,e:
        info = traceback.format_exc()
        CustomInfo="Query failed. Please check the log."
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)

def rSetOutPutInfo(response,outputFormat,filePath=None,fileName=None):
    """
    对服务器反悔的参数进行Table/Text格式化
    :param response:
    :param outputFormat:
    :param filePath:
    :param fileName:
    :return:
    """
    try:
        dictinfo=response
        if not isinstance(response,dict):
            response=response.decode('utf-8')
            dictinfo=json.loads(response)
        if outputFormat=="table":
            converterTable=contotable.contotable(dictinfo,filePath,fileName)
            if gblvar.options.ColWidth!=None:
                converterTable.getTableData(gblvar.options.ColWidth)
            else:
                converterTable.getTableData(4)
        elif outputFormat=="text":
            converterText=contoText.contoText(dictinfo,filePath,fileName)
            converterText.getTextData()
        elif outputFormat=="xml":
            encod='utf-8'
            contoxml.contoXML().getDictToXml(dictinfo,fileName)
        elif outputFormat=="json":
            #此处将response转换成json格式，编码格式转换为 unicode
            jsoninfo = json.dumps(dictinfo,sort_keys=True,indent=2,ensure_ascii=False)
            #此处将 unicode 编码转换为 utf-8  保存到文件
            jsoninfo=jsoninfo.encode('utf-8')
            #控制台输出显示的编码格式改为 gbk    控制台输出
            sysType=platform.system()
            if sysType=="Windows":
                jsoninfo_print=jsoninfo.decode('utf-8').encode('gbk')
            else:
                jsoninfo_print=jsoninfo.decode('utf-8')
            if fileName!=None:
                file1=open(fileName,"w")
                file1.writelines(jsoninfo)
                file1.close()
            print jsoninfo_print
    except IOError:
        info = traceback.format_exc()
        CustomInfo="No permission to write to the file"
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)
    except Exception,e:
        info = traceback.format_exc()
        CustomInfo="functionName'"+sys._getframe().f_code.co_name+"'. The query result format failure. Please check the log"
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)


def conServerRAM():
    parameters['AccessKeyId'] = gblvar.ID
    #lwc add 2014-8-25
    if gblvar.options.Format=="table" or gblvar.options.Format=="text" or gblvar.options.Format=="xml":
        checkNotNone("json" , 'Format')
    else:
        checkNotNone(gblvar.options.Format , 'Format')
    #RAM 版本为2014-02-14
    parameters['Version'] = "2014-02-14"

    # 计算签名并把签名结果加入请求参数
    signature = compute_signature(parameters)
    parameters['Signature'] = signature
    # 发送请求
    url = gblvar.RAM_HOST + "/?" + urllib.urlencode(parameters)
    if gblvar.options.showURL=='true':print "url-->",url
    request = urllib2.Request(url)

    #如果指定了outputfile,则检查文件是否创建，否则outputfile=None
    if gblvar.options.outputfile !=None  and gblvar.options.outputfile!="":
        outputfile=config.config().changeFilePath(gblvar.options.outputfile)
        config.config().checkFile(outputfile)
    else:
        outputfile=None
    try:
        conn = urllib2.urlopen(request)
        response = conn.read()
        if outputfile!=None:
            f = file(outputfile, 'w')
            f.write(response)
            f.close()
        #根据Query参数，对response数据进行检索
        dictObj=getQueryRS(response,parameters["Format"],gblvar.options.Query)
        #控制输出格式
        rSetOutPutInfo(dictObj,gblvar.options.Format,None,outputfile)
    except urllib2.HTTPError, e:
        error_msg = e.read().strip()
        if outputfile!=None:
            f = file(outputfile, 'w')
            f.write(error_msg)
            f.close()
        rSetOutPutInfo(json.loads(error_msg),gblvar.options.Format,None,outputfile)
    except IOError:
        info = traceback.format_exc()
        CustomInfo="No permission to write to the file"
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)



#验证为空，则退出程序。不为空，则赋值参数。
def checkNone(p,name):
    #global parameters
    if p is None:
        #print 'Please input '+ name + '!'
        info='Please input '+ name + '!'
        logs.logs(None,info).getCustom_Log().error(info)
        sys.exit(1)
    else:
        parameters[name] = p

#验证不为空，则赋值参数。为空，则不处理什么。
def checkNotNone(p,name):
    #global parameters
    if p is not None:
        parameters[name] = p


def ExecuteTheCommand(actionName):
    try:
        ActionDict={}
        ActionDict=gblvar.ACTION_Dict
        #将操作名 以action:ACTION的字典形势存储
        acNameDict={}
        #操作名小写化后，排序的列表,用于判断Action是否存在列表中
        acNameList=[]

        MustParameters=[]
        OptionalParameters=[]

        for o in ActionDict.keys():
            acNameDict[o.lower()]=o
        acNameList=acNameDict.keys()
        acNameList.sort()

        if not actionName.lower() in acNameList:
            print "Unsupported instructions '"+ actionName +"'"
            sys.exit(1)
        setup_cmdlist()
        if 'FunctionName' in ActionDict[acNameDict[actionName]].keys():
            CMD_LIST[actionName]()
        else:
            parameters['Action']=acNameDict[actionName.lower()]
            MustParameters=ActionDict[parameters['Action']]['MustParameters']
            OptionalParameters=ActionDict[parameters['Action']]['OptionalParameters']
            lsList=MustParameters+OptionalParameters
            parmGblvarOptions=getParmGblvarOptions()
            for key in MustParameters:
                #keyName2=getOptions(key)
                if key in parmGblvarOptions.keys():
                    checkNone(parmGblvarOptions[key], key)
                else:
                    checkNone(None, key)

            for key in OptionalParameters:
                if key in parmGblvarOptions.keys():
                    checkNone(parmGblvarOptions[key], key)
                else:
                    checkNotNone(None, key)
            conServer()
    except Exception,e:
        info = traceback.format_exc()
        CustomInfo="functionName'"+sys._getframe().f_code.co_name+"'. Command execution failed, please check the log."
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)


#lwc add 2014-8-25 以下代码为后来添加
#AddUser (创建安全组)
def cmd_addUser():
    try:
        #global parameters
        parameters['Action'] = 'AddUser'
        checkNotNone(gblvar.options.UserName , 'UserName')
        #checkNotNone(gblvar.options.Version , 'Version')
        checkNotNone(gblvar.options.Comments , 'Comments')
        conServerRAM()
    except Exception:
        info = traceback.format_exc()
        CustomInfo="functionName: '"+sys._getframe().f_code.co_name+"'. RAM failed to add, please see the log!"
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)

def cmd_RemoveUser():
    try:
        parameters['Action'] = 'RemoveUser'
        checkNone(gblvar.options.UserName , 'UserName')
        conServerRAM()
    except Exception:
        info = traceback.format_exc()
        CustomInfo="functionName: '"+sys._getframe().f_code.co_name+"'. RAM failed to add, please see the log!"
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)


# cmd_PutUserPolicy 为被授权用户设置Policy
def cmd_putUserPolicy():
    try:
        parameters['Action'] = 'PutUserPolicy'
        checkNone(gblvar.options.UserName , 'UserName')
        checkNone(gblvar.options.PolicyName , 'PolicyName')
        checkNone(gblvar.options.PolicyDocument , 'PolicyDocument')
        """
        PolicyDocument=getPolicyDocument()
        checkNotNone(PolicyDocument , 'PolicyDocument')
        """
        conServerRAM()
    except Exception:
        info = traceback.format_exc()
        CustomInfo="functionName:'"+sys._getframe().f_code.co_name+"', please check the log file!"
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)


getRamParm={'Actions':''}

#验证不为空，则赋值参数。为空，则不处理什么。
def checkRAMNone(p,name):
    #global parameters
    if p is not None:
        getRamParm[name] = p

def getPolicyDocument():
    #jsonStr='{"Version": "1","Statement":[{"Effect": "Allow","Action": ["ecs:RebootInstance","ecs:StopInstance","ecs:DescribeInstanceAttribute"],"Resource":["acs:ecs:*:instance/I-instance1"]}]}'
    parm={}
    checkRAMNone(gblvar.options.Actions,'Actions')
    checkRAMNone(gblvar.options.RegionId,'RegionId')
    checkRAMNone(gblvar.options.DiskId,'DiskId')
    checkRAMNone(gblvar.options.SecurityGroupId,'SecurityGroupId')
    checkRAMNone(gblvar.options.InstanceId,'InstanceId')
    checkRAMNone(gblvar.options.SnapshotId,'SnapshotId')
    checkRAMNone(gblvar.options.ImageId,'ImageId')
    checkRAMNone(gblvar.options.DataDisk_1_SnapshotId,'DataDisk_1_SnapshotId')
    checkRAMNone(gblvar.options.DataDisk_2_SnapshotId,'DataDisk_2_SnapshotId')
    checkRAMNone(gblvar.options.DataDisk_3_SnapshotId,'DataDisk_3_SnapshotId')
    checkRAMNone(gblvar.options.DataDisk_4_SnapshotId,'DataDisk_4_SnapshotId')
    PolicyDocument=authorizationInfo.authorizationInfo().getPolicyDocument(getRamParm)
    return PolicyDocument

def cmd_deleteUserPolicy():
    try:
        #global parameters
        parameters['Action'] = 'DeleteUserPolicy'
        checkNone(gblvar.options.UserName , 'UserName')
        checkNone(gblvar.options.PolicyName , 'PolicyName')
        conServerRAM()
    except Exception:
        info = traceback.format_exc()
        CustomInfo="functionName:'"+sys._getframe().f_code.co_name+"', please check the log file!"
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)

def cmd_listUserPolicies():
    try:
        parameters['Action'] = 'ListUserPolicies'
        checkNotNone(gblvar.options.UserName , 'UserName')
        conServerRAM()
    except Exception:
        info = traceback.format_exc()
        CustomInfo="functionName:'"+sys._getframe().f_code.co_name+"', please check the log file!"
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)

def cmd_ListUsers():
    try:
        parameters['Action'] = 'ListUsers'
        conServerRAM()
    except Exception:
        info = traceback.format_exc()
        CustomInfo="functionName:'"+sys._getframe().f_code.co_name+"', please check the log file!"
        logs.logs(info,CustomInfo).getECSLogger()
        sys.exit(1)
