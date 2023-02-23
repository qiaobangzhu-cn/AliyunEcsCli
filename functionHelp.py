# -*- coding:utf-8 -*-
import os
import sys
import traceback
import logs
import gblvar


class functionHelp():
    def __init__(self):
        self.parm={}
        self.parm=gblvar.ecsParameters

        self.CMD_LIST={}
        self.CMD_LIST['config'] = self.getHelp_config
        self.CMD_LIST['CreateSecurityGroup'] = self.getHelp_createSecurityGroup
        self.CMD_LIST['AuthorizeSecurityGroup'] = self.getHelp_authorizeSecurityGroup
        self.CMD_LIST['DescribeSecurityGroupAttribute'] = self.getHelp_describeSecurityGroupAttribute
        self.CMD_LIST['DescribeSecurityGroups'] = self.getHelp_describeSecurityGroups
        self.CMD_LIST['RevokeSecurityGroup'] = self.getHelp_revokeSecurityGroup
        self.CMD_LIST['DeleteSecurityGroup'] = self.getHelp_deleteSecurityGroup

        self.CMD_LIST['ModifyInstanceAttribute'] = self.getHelp_modifyInstanceAttribute
        self.CMD_LIST['DescribeInstanceStatus'] = self.getHelp_describeInstanceStatus
        self.CMD_LIST['DescribeInstanceAttribute'] = self.getHelp_describeInstanceAttribute

        self.CMD_LIST['DescribeRegions'] = self.getHelp_describeRegions
        self.CMD_LIST['DescribeZones'] = self.getHelp_describeZones

        self.CMD_LIST['CreateImage'] = self.getHelp_createImage
        self.CMD_LIST['DeleteImage'] = self.getHelp_deleteImage
        self.CMD_LIST['DescribeImages'] = self.getHelp_describeImages

        self.CMD_LIST['DescribeInstanceDisks'] = self.getHelp_describeInstanceDisks
        self.CMD_LIST['DeleteDisk'] = self.getHelp_deleteDisk
        self.CMD_LIST['AddDisk'] = self.getHelp_addDisk
        self.CMD_LIST['AllocatePublicIpAddress'] = self.getHelp_allocatePublicIpAddress
        self.CMD_LIST['ReleasePublicIpAddress'] = self.getHelp_releasePublicIpAddress
        #创建实例
        self.CMD_LIST['CreateInstance'] = self.getHelp_createInstance
        self.CMD_LIST['StartInstance'] = self.getHelp_startInstance
        self.CMD_LIST['StopInstance'] = self.getHelp_stopInstance
        self.CMD_LIST['RebootInstance'] = self.getHelp_rebootInstance
        self.CMD_LIST['ResetInstance'] = self.getHelp_resetInstance
        self.CMD_LIST['DeleteInstance'] = self.getHelp_deleteInstance
        self.CMD_LIST['ModifyInstanceSpec'] = self.getHelp_modifyInstanceSpec

        self.CMD_LIST['CreateSnapshot'] = self.getHelp_createSnapshot
        self.CMD_LIST['DeleteSnapshot'] = self.getHelp_deleteSnapshot
        self.CMD_LIST['DescribeSnapshots'] = self.getHelp_describeSnapshots
        self.CMD_LIST['DescribeSnapshotAttribute'] = self.getHelp_describeSnapshotAttribute
        self.CMD_LIST['RollbackSnapshot'] = self.getHelp_rollbackSnapshot

        self.CMD_LIST['DescribeInstanceTypes'] = self.getHelp_describeInstanceTypes

        #lwc add 2014-8-25
        self.CMD_LIST['AddUser'] = self.getHelp_addUser
        self.CMD_LIST['PutUserPolicy'] = self.getHelp_putUserPolicy

        self.CMD_LIST['JoinSecurityGroup'] = self.getHelp_joinSecurityGroup
        self.CMD_LIST['LeaveSecurityGroup'] = self.getHelp_leaveSecurityGroup
        self.CMD_LIST['CreateDisk'] = self.getHelp_createDisk
        self.CMD_LIST['DescribeDisks'] = self.getHelp_describeDisks
        self.CMD_LIST['AttachDisk'] = self.getHelp_attachDisk
        self.CMD_LIST['DetachDisk'] = self.getHelp_detachDisk
        self.CMD_LIST['ModifyDiskAttribute'] = self.getHelp_modifyDiskAttribute
        self.CMD_LIST['ReInitDisk'] = self.getHelp_reInitDisk
        self.CMD_LIST['ResetDisk'] = self.getHelp_resetDisk
        self.CMD_LIST['ReplaceSystemDisk'] = self.getHelp_replaceSystemDisk

        self.CMD_LIST['ModifyAutoSnapshotPolicy'] = self.getHelp_modifyAutoSnapshotPolicy
        self.CMD_LIST['DescribeAutoSnapshotPolicy'] = self.getHelp_describeAutoSnapshotPolicy

        self.CMD_LIST['DescribeInstanceMonitorData'] = self.getHelp_describeInstanceMonitorData
        self.CMD_LIST['DeleteUserPolicy'] = self.getHelp_deleteUserPolicy
        return

    #def setup_cmdlist(self):


    def changeCN(self,content):
        content.encode('gbk')
        return content

    def printHelpInfo(self,keyList,parameters):
        try:
            if len(keyList)>0:
                for key in keyList:
                    if key=="Optional parameters":
                        print ""
                        print  key
                    else:
                        showKey=key.replace("_",".")
                        print "--"+showKey + "        " + parameters[key]
        except:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    def checkActionParm(self,actionName,csList):
        try:
            clDict={}
            for o in self.CMD_LIST.keys():
                clDict[o.lower()]=o
            if actionName in clDict.keys():
                (parameters,RequiredList,OptionalList)=self.CMD_LIST[clDict[actionName]]()
            else:
                print "The '"+actionName+"' is an invalid operation."
                sys.exit(1)
            list1=RequiredList+OptionalList
            list2=[]
            for o in list1:
                list2.append(o.lower())
            for o in csList:
                clStr=o.replace('.','_').lower()
                if clStr not in list2:
                    return o
            return None
        except Exception,e:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)


    def getHelp(self,ActionName):
        parK={}
        try:
            clDict={}
            for o in self.CMD_LIST.keys():
                clDict[o.lower()]=o
            if not ActionName in clDict.keys():
                print "The '"+ActionName+"' is an invalid operation."
                sys.exit(1)
            (parameters,RequiredList,OptionalList)=self.CMD_LIST[clDict[ActionName]]()

            return (RequiredList,OptionalList)

        except Exception,e:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    """
    def getHelp(self,ActionName):
        parK={}
        try:
            clDict={}
            for o in self.CMD_LIST.keys():
                clDict[o.lower()]=o
            if not ActionName in clDict.keys():
                print "The '"+ActionName+"' is an invalid operation."
                sys.exit(1)
            (parameters,RequiredList,OptionalList)=self.CMD_LIST[clDict[ActionName]]()

            if len(RequiredList)>0:
                print "Required"
                self.printHelpInfo(RequiredList,parameters)
            if len(OptionalList)>0:
                print "Optional parameters"
                self.printHelpInfo(OptionalList,parameters)
        except Exception,e:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
    """

    def getParmDict(self,bxList=[],kxList=[]):
        try:
            parameters={}
            if len(bxList)>0:
                for o in bxList:
                    parameters[o] =self.parm[o]
            if len(kxList)>0:
                parameters["Optional parameters"]="Optional parameters"
                for o in kxList:
                    parameters[o] =self.parm[o]
            return parameters
        except Exception,e:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)



    def getHelp_config(self):
        try:
            parameters={}
            #可选
            OptionalList=['output','outputfile','showurl','RegionId','ZoneId']
            #必选
            RequiredList=['Actions','id','key']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception,e:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    def getHelp_createSecurityGroup(self):
        try:
            parameters={}
            #可选
            OptionalList=['ResourceOwnerAccount','ClientToken']
            #必选
            RequiredList=['Actions','RegionId','Description']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception,e:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #AuthorizeSecurityGroup (授权安全组权限)
    def getHelp_authorizeSecurityGroup(self):
        try:
            parameters={}
            #必选
            RequiredList=['SecurityGroupId', 'RegionId', 'IpProtocol', 'PortRange']
            #可选
            OptionalList=['SourceCidrIp', 'SourceGroupId', 'ResourceOwnerAccount', 'SourceCidrIp', 'SourceGroupId', 'Policy', 'NicType']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
        #global parameters


    #DescribeSecurityGroupAttribute (查询安全组规则)
    def getHelp_describeSecurityGroupAttribute(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DescribeSecurityGroupAttribute'
            #必选
            RequiredList=['SecurityGroupId', 'RegionId']
            #可选
            OptionalList=['ResourceOwnerAccount', 'NicType']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #DescribeSecurityGroups (查询安全组列表)
    def getHelp_describeSecurityGroups(self):
        try:
            parameters={}
            #parameters['Actions'] = self.parm['DescribeSecurityGroups']
            #必选
            RequiredList=['RegionId']
            #可选
            OptionalList=['ResourceOwnerAccount', 'PageNumber', 'PageSize']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
    #RevokeSecurityGroup (撤销安全组规则)
    def getHelp_revokeSecurityGroup(self):
        try:
            parameters={}
            #parameters['Actions'] = 'RevokeSecurityGroup'

            #必选
            RequiredList=['SecurityGroupId', 'RegionId', 'IpProtocol', 'PortRange']
            #可选
            OptionalList=['ResourceOwnerAccount', 'SourceCidrIp', 'SourceCidrIp', 'SourceGroupId', 'Policy', 'NicType']
            parameters=self.getParmDict(RequiredList,OptionalList)

            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #DeleteSecurityGroup (删除安全组)
    def getHelp_deleteSecurityGroup(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DeleteSecurityGroup'
            #必选
            RequiredList=['RegionId', 'RegionId', 'SecurityGroupId']
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
    #ModifyInstanceAttribute 修改实例属性(可修改主机名、密码、所属安全组)
    def getHelp_modifyInstanceAttribute(self):
        try:
            parameters={}
            #parameters['Actions'] = 'ModifyInstanceAttribute'
            #必选
            RequiredList=['InstanceId']
            #可选
            OptionalList=['ResourceOwnerAccount', 'InstanceName', 'Description', 'SecurityGroupId', 'HostName', 'Password']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #DescribeInstanceStatus 查询实例状态(查询实例列表)
    def getHelp_describeInstanceStatus(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DescribeInstanceStatus'
            #必选
            RequiredList=['RegionId']
            #可选
            OptionalList=['ResourceOwnerAccount', 'ZoneId', 'PageNumber', 'PageSize']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
    #DescribeInstanceAttribute查询实例信息
    def getHelp_describeInstanceAttribute(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DescribeInstanceAttribute'
            #必选
            RequiredList=['InstanceId']
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)

            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #DescribeRegions查询可用数据中心
    def getHelp_describeRegions(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DescribeRegions'
            #必选
            RequiredList=[]
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #DescribeZones查询指定Region下的Zone列表
    def getHelp_describeZones(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DescribeZones'
            #必选
            RequiredList=['RegionId']
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #cmd_describeInstanceMonitorData 查看云服务器实例的监控信息
    def getHelp_describeInstanceMonitorData(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DescribeInstanceMonitorData'
            #必选
            RequiredList=['InstanceId', 'StartTime', 'EndTime']
            #可选
            OptionalList=['ResourceOwnerAccount', 'Period']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)


    #CreateInstance创建实例
    def getHelp_createInstance(self):
        try:
            parameters={}
            #parameters['Actions'] = 'CreateInstance'

            #必选
            RequiredList=['RegionId', 'ImageId', 'InstanceType', 'SecurityGroupId']
            #可选
            OptionalList=['ResourceOwnerAccount', 'ZoneId', 'InstanceName',\
                          'Description', 'InternetChargeType', 'InternetMaxBandwidthIn',\
                          'InternetMaxBandwidthOut', 'HostName', 'Password',\
                          'SystemDisk_Category', 'SystemDisk_DiskName', 'SystemDisk_Description',\
                          'DataDisk_1_Category', 'DataDisk_1_SnapshotId', 'DataDisk_1_DiskName', 'DataDisk_1_Description', 'DataDisk_1_Device',\
                          'DataDisk_2_Category', 'DataDisk_2_SnapshotId', 'DataDisk_2_DiskName', 'DataDisk_2_Description', 'DataDisk_2_Device',\
                          'DataDisk_3_Category', 'DataDisk_3_SnapshotId', 'DataDisk_3_DiskName', 'DataDisk_3_Description', 'DataDisk_3_Device',\
                          'DataDisk_4_Category', 'DataDisk_4_SnapshotId', 'DataDisk_4_DiskName', 'DataDisk_4_Description', 'DataDisk_4_Device',\
                          'ClientToken']

            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            #sys.exit(1)
            sys.exit()

    #StartInstance启动实例
    def getHelp_startInstance(self):
        try:
            parameters={}
            #parameters['Actions'] = 'StartInstance'
            #必选
            RequiredList=['InstanceId']
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception,e:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #StopInstance停止实例
    def getHelp_stopInstance(self):
        try:
            parameters={}
            #parameters['Actions'] = 'StopInstance'

            #必选
            RequiredList=['InstanceId']
            #可选
            OptionalList=['ResourceOwnerAccount', 'ForceStop']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
    #RebootInstance重启实例
    def getHelp_rebootInstance(self):
        try:
            parameters={}
            #parameters['Actions'] = 'RebootInstance'
            #必选
            RequiredList=['InstanceId']
            #可选
            OptionalList=['ResourceOwnerAccount', 'ForceStop']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
    #ResetInstance重置实例
    def getHelp_resetInstance(self):
        try:
            parameters={}
            #parameters['Actions'] = 'ResetInstance'
            #必选
            RequiredList=['InstanceId','ImageId','DiskType']
            #可选
            OptionalList=[]
            parameters=self.getParmDict(RequiredList,OptionalList)

            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #DeleteInstance删除实例
    def getHelp_deleteInstance(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DeleteInstance'
            #必选
            RequiredList=['InstanceId']
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
    #将实例加入安全组
    def getHelp_joinSecurityGroup(self):
        try:
            parameters={}
            #parameters['Actions'] = 'JoinSecurityGroup'
            #必选
            RequiredList=['InstanceId', 'SecurityGroupId']
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #将实例移除安全组
    def getHelp_leaveSecurityGroup(self):
        try:
            parameters={}
            #parameters['Actions'] = 'LeaveSecurityGroup'
            #必选
            RequiredList=['InstanceId', 'SecurityGroupId']
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)

            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
    #cmd_createdisk创建磁盘  该处的Size和SnapshotId必须至少选择一项
    def getHelp_createDisk(self):
        try:
            parameters={}
            #parameters['Actions'] = 'CreateDisk'
            #必选
            RequiredList=['RegionId', 'ZoneId']
            #可选
            OptionalList=['ResourceOwnerAccount', 'Size', 'SnapshotId', 'DiskName', 'Description', 'ClientToken']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #cmd_describedisks查询磁盘   此处参数的格式需要注意
    def getHelp_describeDisks(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DescribeDisks'
            #必选
            RequiredList=['RegionId']
            #可选
            OptionalList=['ResourceOwnerAccount', 'ZoneId', 'DiskIds', 'InstanceId', 'DiskType', 'Category', 'Status', 'SnapshotId', 'Portable', 'DeleteWithInstance', 'DeleteAutoSnapshot', 'PageNumber', 'PageSize']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
    #cmd_attachdisk挂载磁盘
    def getHelp_attachDisk(self):
        try:
            parameters={}
            #parameters['Actions'] = 'AttachDisk'
            #必选
            RequiredList=['InstanceId', 'DiskId']
            #可选
            OptionalList=['ResourceOwnerAccount', 'Device', 'DeleteWithInstance']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #cmd_detachDisk卸载磁盘
    def getHelp_detachDisk(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DetachDisk'
            #必选
            RequiredList=['InstanceId', 'DiskId']
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #cmd_modifyDiskAttribute 修改磁盘属性
    def getHelp_modifyDiskAttribute(self):
        try:
            parameters={}
            #parameters['Actions'] = 'ModifyDiskAttribute'
            #必选
            RequiredList=['DiskId']
            #可选
            OptionalList=['ResourceOwnerAccount', 'DiskName', 'Description', 'DeleteWithInstance']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #cmd_reInitDisk 重新初始化磁盘
    def getHelp_reInitDisk(self):
        try:
            parameters={}
            #parameters['Actions'] = 'ReInitDisk'
            #必选
            RequiredList=['DiskId']
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #cmd_resetDisk回滚磁盘
    def getHelp_resetDisk(self):
        try:
            parameters={}
            #parameters['Actions'] = 'ResetDisk'
            #必选
            RequiredList=['DiskId','SnapshotId']
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)

            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
    #cmd_replaceSystemDisk 更换系统盘
    def getHelp_replaceSystemDisk(self):
        try:
            parameters={}
            #parameters['Actions'] = 'ReplaceSystemDisk'
            #必选
            RequiredList=['InstanceId','ImageId']
            #可选
            OptionalList=['ResourceOwnerAccount','ClientToken']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)


    #CreateSnapshot创建快照
    def getHelp_createSnapshot(self):
        try:
            parameters={}
            #parameters['Actions'] = 'CreateSnapshot'
            #必选
            RequiredList=['DiskId']
            #可选
            OptionalList=['ResourceOwnerAccount', 'SnapshotName', 'Description', 'ClientToken']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #DeleteSnapshot删除快照
    def getHelp_deleteSnapshot(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DeleteSnapshot'
            #必选
            RequiredList=['SnapshotId']
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #DescribeSnapshots查询磁盘设备的快照列表
    def getHelp_describeSnapshots(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DescribeSnapshots'
            #必选
            RequiredList=['RegionId']
            #可选
            OptionalList=['ResourceOwnerAccount', 'InstanceId', 'DiskId', 'SnapshotIds', 'PageNumber', 'PageSize']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #cmd_modifyAutoSnapshotPolicy设置自动快照策略
    def getHelp_modifyAutoSnapshotPolicy(self):
        try:
            parameters={}
            #parameters['Actions'] = 'ModifyAutoSnapshotPolicy'
            #必选
            RequiredList=[]
            #可选
            OptionalList=['ResourceOwnerAccount', 'SystemDiskPolicyEnabled',\
                          'SystemDiskPolicyTimePeriod', 'SystemDiskPolicyRetentionDays',\
                          'SystemDiskPolicyRetentionLastWeek', 'DataDiskPolicyTimePeriod',\
                          'DataDiskPolicyRetentionDays', 'DataDiskPolicyRetentionLastWeek',\
                          'DataDiskPolicyEnabled']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #cmd_describeAutoSnapshotPolicy 查询自动快照策略
    def getHelp_describeAutoSnapshotPolicy(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DescribeAutoSnapshotPolicy'
            #必选
            RequiredList=[]
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #DescribeSnapshotAttribute查询快照详情
    def getHelp_describeSnapshotAttribute(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DescribeSnapshotAttribute'
            #必选
            RequiredList=['RegionId','SnapshotId']
            #可选
            OptionalList=[]
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #RollbackSnapshot回滚快照
    def getHelp_rollbackSnapshot(self):
        try:
            parameters={}
            #parameters['Actions'] = 'RollbackSnapshot'
            #必选
            RequiredList=['InstanceId', 'SnapshotId', 'DiskId']
            #可选
            OptionalList=[]
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #cmd_describeImages查询可用镜像
    def getHelp_describeImages(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DescribeImages'
            #必选
            RequiredList=['RegionId']
            #可选
            OptionalList=['ResourceOwnerAccount', 'PageNumber', 'PageSize', 'SnapshotId', 'ImageName', 'ImageOwnerAlias']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #CreateImage创建自定义镜像
    def getHelp_createImage(self):
        try:
            parameters={}
            #parameters['Actions'] = 'CreateImage'
            #必选
            RequiredList=['SnapshotId', 'RegionId']
            #可选
            OptionalList=['ResourceOwnerAccount', 'ImageName', 'ImageVersion', 'Description', 'ClientToken']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #DeleteImage删除自定义镜像
    def getHelp_deleteImage(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DeleteImage'
            #必选
            RequiredList=['RegionId', 'ImageId']
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #DescribeInstanceDisks查询实例磁盘列表
    def getHelp_describeInstanceDisks(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DescribeInstanceDisks'
            #必选
            RequiredList=['InstanceId']
            #可选
            OptionalList=[]
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #DeleteDisk删除磁盘
    def getHelp_deleteDisk(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DeleteDisk'
            #必选
            RequiredList=['DiskId']
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #AddDisk为实例增加磁盘设备
    def getHelp_addDisk(self):
        try:
            parameters={}
            #parameters['Actions'] = 'AddDisk'
            #必选
            RequiredList=['InstanceId', 'SnapshotId', 'Size']
            #可选
            OptionalList=[]
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #AllocatePublicIpAddress分配公网ip地址
    def getHelp_allocatePublicIpAddress(self):
        try:
            parameters={}
            #parameters['Actions'] = 'AllocatePublicIpAddress'
            #必选
            RequiredList=['InstanceId']
            #可选
            OptionalList=[]
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #ReleasePublicIpAddress释放公网IP地址
    def getHelp_releasePublicIpAddress(self):
        try:
            parameters={}
            #parameters['Actions'] = 'ReleasePublicIpAddress'
            #必选
            RequiredList=['PublicIpAddress']
            #可选
            OptionalList=[]
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    #ModifyInstanceSpec修改实例规格(实例升级)
    def getHelp_modifyInstanceSpec(self):
        try:
            parameters={}
            #parameters['Actions'] = 'ModifyInstanceSpec'
            #必选
            RequiredList=['InstanceId', 'InstanceType', 'InternetMaxBandwidthIn', 'InternetMaxBandwidthOut']
            #可选
            OptionalList=[]
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    def getHelp_describeInstanceTypes(self):
        try:
            parameters={}
            #parameters['Actions'] = 'DescribeInstanceTypes'
            #必选
            RequiredList=[]
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
    #lwc add 2014-8-25 以下代码为后来添加
    #AddUser (创建安全组)
    def getHelp_addUser(self):
        try:
            parameters={}
            #parameters['Actions'] = 'AddUser'
            #必选
            RequiredList=['UserName', 'Version']
            #可选
            OptionalList=['ResourceOwnerAccount']
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)
    # cmd_PutUserPolicy 为被授权用户设置Policy
    def getHelp_putUserPolicy(self):
        try:
            parameters={}
            #parameters['Actions'] = 'PutUserPolicy'
            #必选
            RequiredList=['UserName', 'PolicyName', 'PolicyDocument']
            #可选
            OptionalList=[]
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)

    def getPolicyDocument(self):
        parameters={}
        #parameters['Actions']=self.parm['Actions']
        #必选
        RequiredList=[]
        #可选
        OptionalList=['Regionid', 'DiskId', 'SecurityGroupId', 'InstanceId', 'SnapshotId', 'ImageId', 'DataDisk_1_SnapshotId', 'DataDisk_2_SnapshotId', 'DataDisk_3_SnapshotId', 'DataDisk_4_SnapshotId', 'PolicyDocument']
        parameters=self.getParmDict(RequiredList,OptionalList)
        return (parameters,RequiredList,OptionalList)

    def getHelp_deleteUserPolicy(self):
        try:
            parameters={}
            #必选
            RequiredList=['UserName', 'PolicyName']
            #可选
            OptionalList=[]
            parameters=self.getParmDict(RequiredList,OptionalList)
            return (parameters,RequiredList,OptionalList)
        except Exception:
            info = traceback.format_exc()
            CustomInfo="Error function '"+sys._getframe().f_code.co_name+"', please check the log file!"
            logs.logs(info,CustomInfo).getECSLogger()
            sys.exit(1)