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
import queryResult
import getQueryData


class authorizationInfo():
    def __init__(self):
        self.sq_Action = {}
        self.setup_sqlist()
        return
    def setup_sqlist(self):
        self.sq_Action['CreateSecurityGroup'] = self.cmd_createSecurityGroup
        self.sq_Action['AuthorizeSecurityGroup'] = self.cmd_authorizeSecurityGroup
        self.sq_Action['DescribeSecurityGroupAttribute'] = self.cmd_describeSecurityGroupAttribute
        self.sq_Action['DescribeSecurityGroups'] = self.cmd_describeSecurityGroups

        self.sq_Action['RevokeSecurityGroup'] = self.cmd_revokeSecurityGroup
        self.sq_Action['DeleteSecurityGroup'] = self.cmd_deleteSecurityGroup

        self.sq_Action['ModifyInstanceAttribute'] = self.cmd_modifyInstanceAttribute
        self.sq_Action['DescribeInstanceStatus'] = self.cmd_describeInstanceStatus
        self.sq_Action['DescribeInstanceAttribute'] = self.cmd_describeInstanceAttribute

        self.sq_Action['DescribeRegions'] = self.cmd_describeRegions
        self.sq_Action['DescribeZones'] = self.cmd_describeZones

        self.sq_Action['CreateImage'] = self.cmd_createImage
        self.sq_Action['DeleteImage'] = self.cmd_deleteImage
        self.sq_Action['DescribeImages'] = self.cmd_describeImages

        self.sq_Action['DeleteDisk'] = self.cmd_deleteDisk
        #创建实例
        self.sq_Action['CreateInstance'] = self.cmd_createInstance
        self.sq_Action['StartInstance'] = self.cmd_startInstance
        self.sq_Action['StopInstance'] = self.cmd_stopInstance
        self.sq_Action['RebootInstance'] = self.cmd_rebootInstance
        self.sq_Action['DeleteInstance'] = self.cmd_deleteInstance

        self.sq_Action['CreateSnapshot'] = self.cmd_createSnapshot
        self.sq_Action['DeleteSnapshot'] = self.cmd_deleteSnapshot
        self.sq_Action['DescribeSnapshots'] = self.cmd_describeSnapshots

        self.sq_Action['DescribeInstanceTypes'] = self.cmd_describeInstanceTypes


        self.sq_Action['JoinSecurityGroup'] = self.cmd_joinSecurityGroup
        self.sq_Action['LeaveSecurityGroup'] = self.cmd_leaveSecurityGroup
        self.sq_Action['CreateDisk'] = self.cmd_createDisk
        self.sq_Action['DescribeDisks'] = self.cmd_describeDisks
        self.sq_Action['AttachDisk'] = self.cmd_attachDisk
        self.sq_Action['DetachDisk'] = self.cmd_detachDisk
        self.sq_Action['ModifyDiskAttribute'] = self.cmd_modifyDiskAttribute
        self.sq_Action['ReInitDisk'] = self.cmd_reInitDisk
        self.sq_Action['ResetDisk'] = self.cmd_resetDisk
        self.sq_Action['ReplaceSystemDisk'] = self.cmd_replaceSystemDisk

        self.sq_Action['ModifyAutoSnapshotPolicy'] = self.cmd_modifyAutoSnapshotPolicy
        self.sq_Action['DescribeAutoSnapshotPolicy'] = self.cmd_describeAutoSnapshotPolicy

        self.sq_Action['DescribeInstanceMonitorData'] = self.cmd_describeInstanceMonitorData


    #验证为空，则退出程序。不为空，则赋值参数。
    def checkNone(self,parName,dictInfo):
        if parName in dictInfo.keys():
            return dictInfo[parName]
        else:
            info='Command parameter "'+parName+'" is missing'
            logs.logs(None,info).getCustom_Log().error(info)
            sys.exit(1)
    #验证为空，则退出程序。不为空，则赋值参数。
    def checkNotNone(self,parName,dictInfo):
        if parName in dictInfo.keys():
            return dictInfo[parName]
        else:
            return None

    def cmd_createSecurityGroup(self,dictParm):
        RegionId=self.checkNone("RegionId",dictParm)
        return "acs:ecs:"+RegionId+":securitygroup/*"


    def cmd_createSecurityGroup(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            returnStr='"acs:ecs:%s:securitygroup/*"'   % RegionId
            return returnStr

        except Exception,e:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_authorizeSecurityGroup(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            SecurityGroupId=self.checkNone("SecurityGroupId",dictParm)
            #非必须参数
            SourceGroupId=self.checkNotNone("SourceGroupId",dictParm)

            if SourceGroupId==None:
                returnStr='"acs:ecs:%s:securitygroup/%s"'   %(RegionId,SecurityGroupId)
            else:
                returnStr='"acs:ecs:%s:securitygroup/%s and acs:ecs:%s:securitygroup/%s"'  %(RegionId,SecurityGroupId,RegionId,SourceGroupId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)


    def cmd_describeSecurityGroupAttribute(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            SecurityGroupId=self.checkNone("SecurityGroupId",dictParm)
            returnStr='"acs:ecs:%s:securitygroup/%s"'   %(RegionId,SecurityGroupId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_describeSecurityGroups(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            SecurityGroupId=self.checkNone("SecurityGroupId",dictParm)
            returnStr='"acs:ecs:%s:securitygroup/%s"'   %(RegionId,SecurityGroupId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)
    def cmd_revokeSecurityGroup(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            SecurityGroupId=self.checkNone("SecurityGroupId",dictParm)
            returnStr='"acs:ecs:%s:securitygroup/%s"'   %(RegionId,SecurityGroupId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_deleteSecurityGroup(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            SecurityGroupId=self.checkNone("SecurityGroupId",dictParm)
            returnStr='"acs:ecs:%s:securitygroup/%s"'   %(RegionId,SecurityGroupId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)
    def cmd_modifyInstanceAttribute(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            InstanceId=self.checkNone("InstanceId",dictParm)
            returnStr='"acs:ecs:%s:instance/%s"'   %(RegionId,InstanceId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_describeInstanceStatus(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            InstanceId=self.checkNone("InstanceId",dictParm)
            returnStr='"acs:ecs:%s:instance/%s"'   %(RegionId,InstanceId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_describeInstanceAttribute(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            InstanceId=self.checkNone("InstanceId",dictParm)
            returnStr='"acs:ecs:%s:instance/%s"'   %(RegionId,InstanceId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_describeRegions(self,dictParm):
        try:
            returnStr=""
            returnStr='"acs:ecs:*:*"'
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)


    def cmd_describeZones(self,dictParm):
        try:
            returnStr=""
            returnStr='"acs:ecs:*:*"'
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)


    def cmd_describeInstanceMonitorData(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            InstanceId=self.checkNone("InstanceId",dictParm)
            returnStr='"acs:ecs:%s:instance/%s"'   %(RegionId,InstanceId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)



    def cmd_createInstance(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            InstanceId=self.checkNone("InstanceId",dictParm)
            SecurityGroupId=self.checkNone("SecurityGroupId",dictParm)
            ImageId=self.checkNone("ImageId",dictParm)
            returnStr='"acs:ecs:%s:instance/%s"'   %(RegionId,InstanceId)

            returnStr='acs:ecs:%s:instance/* and acs:ecs:%s:securitygroup/%s and acs:ecs:%s:image/%s' %(RegionId,RegionId,SecurityGroupId,RegionId,ImageId)

            DataDisk_1_SnapshotId=self.checkNotNone("DataDisk_1_SnapshotId",dictParm)
            DataDisk_2_SnapshotId=self.checkNotNone("DataDisk_2_SnapshotId",dictParm)
            DataDisk_3_SnapshotId=self.checkNotNone("DataDisk_3_SnapshotId",dictParm)
            DataDisk_4_SnapshotId=self.checkNotNone("DataDisk_4_SnapshotId",dictParm)

            if DataDisk_1_SnapshotId!=None:
                returnStr=returnStr+'and acs:ecs:%s:snapshot/%s' %(RegionId,DataDisk_1_SnapshotId)
            if DataDisk_2_SnapshotId!=None:
                returnStr=returnStr+'and acs:ecs:%s:snapshot/%s' %(RegionId,DataDisk_2_SnapshotId)
            if DataDisk_3_SnapshotId!=None:
                returnStr=returnStr+'and acs:ecs:%s:snapshot/%s' %(RegionId,DataDisk_3_SnapshotId)
            if DataDisk_4_SnapshotId!=None:
                returnStr=returnStr+'and acs:ecs:%s:snapshot/%s' %(RegionId,DataDisk_4_SnapshotId)

            returnStr='"'+returnStr+'"'
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)


    def cmd_startInstance(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            InstanceId=self.checkNone("InstanceId",dictParm)
            returnStr='"acs:ecs:%s:instance/%s"'   %(RegionId,InstanceId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)


    def cmd_stopInstance(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            InstanceId=self.checkNone("InstanceId",dictParm)
            returnStr='"acs:ecs:%s:instance/%s"'   %(RegionId,InstanceId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_rebootInstance(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            InstanceId=self.checkNone("InstanceId",dictParm)
            returnStr='"acs:ecs:%s:instance/%s"'   %(RegionId,InstanceId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)


    def cmd_deleteInstance(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            InstanceId=self.checkNone("InstanceId",dictParm)
            returnStr='"acs:ecs:%s:instance/%s"'   %(RegionId,InstanceId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_joinSecurityGroup(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            InstanceId=self.checkNone("InstanceId",dictParm)
            SecurityGroupId=self.checkNone("SecurityGroupId",dictParm)
            returnStr='"acs:ecs:%s:instance/%s and acs:ecs:%s:securitygroup/%s"'   %(RegionId,InstanceId,RegionId,SecurityGroupId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)


    def cmd_leaveSecurityGroup(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            InstanceId=self.checkNone("InstanceId",dictParm)
            SecurityGroupId=self.checkNone("SecurityGroupId",dictParm)
            returnStr='"acs:ecs:%s:instance/%s and acs:ecs:%s:securitygroup/%s"'   %(RegionId,InstanceId,RegionId,SecurityGroupId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_createDisk(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            SnapshotId=self.checkNotNone("SnapshotId",dictParm)
            if SnapshotId==None:
                returnStr='"acs:ecs:%s:disk/*"'   % RegionId
            else:
                returnStr='"acs:ecs:%s:disk/* and acs:ecs:%s:snapshot/%s"'   %(RegionId,RegionId,SnapshotId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)


    def cmd_describeDisks(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            DiskId=self.checkNone("DiskId",dictParm)
            returnStr='"acs:ecs:%s:disk/%s"'   %(RegionId,DiskId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_attachDisk(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            DiskId=self.checkNone("DiskId",dictParm)
            InstanceId=self.checkNone("InstanceId",dictParm)
            returnStr='"acs:ecs:%s:disk/%s and acs:ecs:%s:instance/%s"'   %(RegionId,DiskId,RegionId,InstanceId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)


    def cmd_detachDisk(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            DiskId=self.checkNone("DiskId",dictParm)
            InstanceId=self.checkNone("InstanceId",dictParm)
            returnStr='"acs:ecs:%s:disk/%s and acs:ecs:%s:instance/%s"'   %(RegionId,DiskId,RegionId,InstanceId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_modifyDiskAttribute(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            DiskId=self.checkNone("DiskId",dictParm)
            returnStr='"acs:ecs:%s:disk/%s"'   %(RegionId,DiskId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_reInitDisk(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            DiskId=self.checkNone("DiskId",dictParm)
            returnStr='"acs:ecs:%s:disk/%s"'   %(RegionId,DiskId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)


    def cmd_resetDisk(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            SnapshotId=self.checkNone("SnapshotId",dictParm)
            DiskId=self.checkNone("DiskId",dictParm)
            returnStr='"acs:ecs:%s:snapshot/%s and acs:ecs:%s:disk/%s"'   %(RegionId,SnapshotId,RegionId,DiskId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_replaceSystemDisk(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            InstanceId=self.checkNone("InstanceId",dictParm)
            ImageId=self.checkNotNone("ImageId",dictParm)
            if ImageId==None:
                returnStr='"acs:ecs:%s:instance/%s"'   %(RegionId,InstanceId)
            else:
                returnStr='"acs:ecs:%s:instance/%s and acs:ecs:%s:image/%s"'   %(RegionId,InstanceId,RegionId,ImageId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)


    def cmd_createSnapshot(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            DiskId=self.checkNone("DiskId",dictParm)
            returnStr='"acs:ecs:%s:disk/%s and acs:ecs:%s:snapshot/*"'   %(RegionId,DiskId,RegionId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_deleteSnapshot(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            SnapshotId=self.checkNone("SnapshotId",dictParm)
            returnStr='"acs:ecs:%s:snapshot/%s"'   %(RegionId,SnapshotId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_describeSnapshots(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            SnapshotId=self.checkNone("SnapshotId",dictParm)
            returnStr='"acs:ecs:%s:snapshot/%s"'   %(RegionId,SnapshotId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)


    def cmd_modifyAutoSnapshotPolicy(self,dictParm):
        try:
            returnStr=""
            returnStr='"acs:ecs:*:snapshot/*"'
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)


    def cmd_describeAutoSnapshotPolicy(self,dictParm):
        try:
            returnStr=""
            returnStr='"acs:ecs:*:snapshot/*"'
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_describeImages(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            ImageId=self.checkNone("ImageId",dictParm)
            returnStr='"acs:ecs:%s:image/%s"'   %(RegionId,ImageId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)



    def cmd_createImage(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            SnapshotId=self.checkNone("SnapshotId",dictParm)
            returnStr='"acs:ecs:%s:image/* and acs:ecs:%s:snapshot/%s"'   %(RegionId,RegionId,SnapshotId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def cmd_deleteImage(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            ImageId=self.checkNone("ImageId",dictParm)
            returnStr='"acs:ecs:%s:image/%s"'   %(RegionId,ImageId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)


    def cmd_deleteDisk(self,dictParm):
        try:
            returnStr=""
            RegionId=self.checkNone("RegionId",dictParm)
            DiskId=self.checkNone("DiskId",dictParm)
            returnStr='"acs:ecs:%s:disk/%s"'   %(RegionId,DiskId)
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)


    def cmd_describeInstanceTypes(self,dictParm):
        try:
            returnStr=""
            returnStr='"acs:ecs:*:*"'
            return returnStr
        except Exception:
            info = traceback.format_exc()
            logs.logs(info,'error').getECSLogger()
            sys.exit(1)

    def getPolicyDocument(self,parm):
        actionLS=parm["Actions"].split(",")
        ResourceList=[]
        ActionList=[]
        RsStr=""
        AsStr=""
        for Action in actionLS:
            Resource=self.sq_Action[Action](parm)
            if Resource in ResourceList:
                pass
            else:
                ResourceList.append(Resource)
                RsStr=RsStr+Resource+","
            actionStr='"ecs:'+Action+'"'
            ActionList.append(actionStr)
            AsStr=AsStr+actionStr+","
        RsStr=RsStr[:len(RsStr)-1]
        AsStr=AsStr[:len(AsStr)-1]
        print AsStr
        print RsStr
        jsonStr='{"Version": "1","Statement":[{"Effect": "Allow","Action": ['+AsStr+'],"Resource":['+RsStr+']}]}'
        return jsonStr