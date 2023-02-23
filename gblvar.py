# -*- coding:utf-8 -*-
import os

#程序默认配置
CONFIG='.config'

#输出文本路径可被用户更改
#OUTPUTFILE=os.path.expanduser('~')+'/.ecs/response.txt'
OUTPUTFILE=os.path.expanduser('~')+ os.path.sep +'.ecs'+os.path.sep+'response.txt'

#保存id和key的文本路径
#CONFIGFILE = os.path.expanduser('~') + '/.osscredentials'
ConfigML=os.path.expanduser('~') + os.path.sep +'.ecs'
#CONFIGFILE = os.path.expanduser('~') + '/.ecs/config'
CONFIGFILE = os.path.expanduser('~') + os.path.sep +'.ecs'+os.path.sep+'config'
LOGFILE=os.path.expanduser('~')+os.path.sep+'.ecs'+os.path.sep+'ecs.log'



#保存id和key的文本中的section
CONFIGSECTION ='user'
#配置中的默认config
DEFAULTCONFIG="config"
#默认连接阿里云OSS的服务器地址
ECS_HOST = "http://ecs.aliyuncs.com"
RAM_HOST = "https://ram.aliyuncs.com"

#AccessId
ID = ""

#AccessKey
KEY = ""

options = None
args = None

#存储Parameters信息
ecsParameters={}
ecsParameters["id"]='The user ID'
ecsParameters["key"]='The user key'
ecsParameters["host"]='The host'
ecsParameters["showURL"]='Whether to display the URL submission'
ecsParameters["RegionId"]='Instance belongs to region ID'
ecsParameters["Description"]='Example description'
ecsParameters["Comments"]='Additional comments'
ecsParameters["config"]='Save ID and KEY'
ecsParameters["ColWidth"]='Control the number of table columns, on duty more than the number of columns in the data itself, invalid'
ecsParameters["outputfile"]='Returns the data output path'
ecsParameters["configfile"]='Configuration file path'
#ecsParameters["AliasName"]='Account alias'
ecsParameters["output"]='Control the format of the data returned:xml/json/table/text'
ecsParameters["Query"]='Query'
ecsParameters["StartTime"]='Specify a start time'
ecsParameters["EndTime"]='The specified end time'
ecsParameters["DiskIds"]='The content of DiskId in the list, do more than 100'
ecsParameters["IpProtocol"]='IP protocol, value: tcp|udp|icmp|gre|all; all says it supports four kinds of protocol'
ecsParameters["PortRange"]='The specified end time'
ecsParameters["SourceGroupId"]='Source security code security group'
ecsParameters["SourceCidrIp"]='The source IP range of security groups'
ecsParameters["SecurityGroupId"]='The security group code'
ecsParameters["Policy"]='Authorization strategy'
ecsParameters["NicType"]='Network type, value: internet/intranet; the default value is Internet'
ecsParameters["PageNumber"]='The current page number. The initial value is 1, the default value is 1'
ecsParameters["PageSize"]='Set pagination query time lines per page, in 50 lines maximum, the default is 10 for'
ecsParameters["InstanceId"]='Examples of ID'
ecsParameters["ZoneId"]='Instance belongs to the available area ID'
ecsParameters["ImageId"]='Mirror image ID'
ecsParameters["InstanceType"]='Examples of resource specifications'
ecsParameters["InternetMaxBandwidthIn"]='The public into the maximum bandwidth value'
ecsParameters["InternetMaxBandwidthOut"]='Network bandwidth maximum'
ecsParameters["HostName"]='Examples of machine name'
ecsParameters["Password"]='Examples of machine code'
ecsParameters["ClientToken"]='Request for idempotence guarantee'
ecsParameters["DiskId"]='Disk ID'
ecsParameters["Size"]='The disk size'
ecsParameters["SnapshotId"]='Create a snapshot data disk use'
ecsParameters["PublicIpAddress"]='Examples of public IP'
ecsParameters["DiskType"]='The source disk properties, System|Data'
ecsParameters["ForceStop"]='Whether forced shutdown restart the instance; False: said go normal shutdown process; True: represents the forced shutdown'
ecsParameters["SnapshotName"]='Snapshots of the display name [2128] in English or in character, must be based on the size of letters or Chinese at the beginning, may contain numbers, "_" or "-", and cannot start with auto (snapshot name at the beginning of the auto are reserved for automatic snapshot). Soon as display name will be displayed in the console. Not with http:// and https:// at the beginning.'
ecsParameters["ImageVersion"]='Mirroring the version number'
ecsParameters["Visibility"]=''
ecsParameters["config_file"]='the file which stores id-key pair'
ecsParameters["Version"]='The API version number'
ecsParameters["UserName"]='RAM authorization authorized account name'
ecsParameters["PolicyName"]='The authorized human Policy name'
ecsParameters["PolicyDocument"]='RAM authorization information'
ecsParameters["ResourceOwnerAccount"]='Authorization rules in the authorized account'
ecsParameters["InstanceName"]='The example shows the name'
ecsParameters["InternetChargeType"]='Network accounting type'
ecsParameters["DiskName"]='Disk name'
ecsParameters["DeleteAutoSnapshot"]='Remove the disk whether also delete snapshots, True deletes the automatic snapshot, False expressed reservations automatic snapshot'
ecsParameters["DeleteWithInstance"]='Whether the disk with instance release: True says that the Instance is released, the disk with the Instance release; False indicates that the Instance is released, the disk retention does not release'
ecsParameters["Portable"]='True represent independent cloud disk, False represents the non independent cloud disk'
ecsParameters["Status"]='Examples of state'
ecsParameters["Category"]='Disk type optional values: cloud: cloud ephemeral: disk, temporary disk'
ecsParameters["Device"]='Air is represented by the system default distribution, /dev/xvdb began to /dev/xvdz the default value: empty'
ecsParameters["SnapshotIds"]='Snapshot list'
ecsParameters["Period"]='Monitoring data acquisition accuracy, the default 60 seconds, only to multiples of 60'
ecsParameters["MonitorData"]='A collection of monitoring data instances of InstanceMonitorDataType consisting of'
ecsParameters["SystemDiskPolicyEnabled"]='The system disk automatic snapshot policy switch: True: the disk properties disk play automatic snapshot, False: does not play the automatic snapshot,'
ecsParameters["SystemDiskPolicyTimePeriod"]='Time period system disk automatic snapshot strategy: 4 time periods (1:00-7:00, 1), (2) 7:00-13:00, (3) 13:00-19:00, 19:00-1:00 (4): no default value, expressed reservations current value'
ecsParameters["SystemDiskPolicyRetentionDays"]='The number of days to retain the system disk automatic snapshot strategy: 1|2|3'
ecsParameters["SystemDiskPolicyRetentionLastWeek"]='Keep the system disk automatic snapshot strategy last Sunday options: True: reserves last Sunday snapshot, False: does not preserve'
ecsParameters["DataDiskPolicyTimePeriod"]='Time data disc automatic snapshot strategy: 4 time periods, (1).00-7:00'
ecsParameters["DataDiskPolicyRetentionDays"]='The number of days to retain automatic snapshot, 1|2|3,'
ecsParameters["DataDiskPolicyRetentionLastWeek"]='The retention data disc automatic snapshot strategy options: False: True: on Sunday snapshot representative reserves on Sunday not to retain'
ecsParameters["ImageName"]='Image name'
ecsParameters["ImageOwnerAlias"]='Mirror owners alias valid values: System - system of public image; custom image self - user; others - other users to open mirror; mirror image marketplace- Market'
ecsParameters["SystemDisk_Category"]='The system disk disk type: cloud- cloud disk; ephemeral- temporary disk; the default value: cloud'
ecsParameters["SystemDisk_DiskName"]='The corresponding disk display name'
ecsParameters["SystemDisk_Description"]='The description of the corresponding disk'
ecsParameters["DataDisk_1_Category"]='The system disk disk type: cloud- cloud disk; ephemeral- temporary disk; the default value: cloud'
ecsParameters["DataDisk_1_SnapshotId"]='Snapshot while creating disk'
ecsParameters["DataDisk_1_DiskName"]='The corresponding disk display name'
ecsParameters["DataDisk_1_Description"]='The description of the corresponding disk'
ecsParameters["DataDisk_1_Device"]='Air is represented by the system default distribution, /dev/xvdb began to /dev/xvdz the default value: empty'
ecsParameters["DataDisk_2_Category"]='The system disk disk type: cloud- cloud disk; ephemeral- temporary disk; the default value: cloud'
ecsParameters["DataDisk_2_SnapshotId"]='Snapshot while creating disk'
ecsParameters["DataDisk_2_DiskName"]='The corresponding disk display name'
ecsParameters["DataDisk_2_Description"]='The description of the corresponding disk'
ecsParameters["DataDisk_2_Device"]='Air is represented by the system default distribution, /dev/xvdb began to /dev/xvdz the default value: empty'
ecsParameters["DataDisk_3_Category"]='The system disk disk type: cloud- cloud disk; ephemeral- temporary disk; the default value: cloud'
ecsParameters["DataDisk_3_SnapshotId"]='Snapshot while creating disk'
ecsParameters["DataDisk_3_DiskName"]='The corresponding disk display name'
ecsParameters["DataDisk_3_Description"]='The description of the corresponding disk'
ecsParameters["DataDisk_3_Device"]='Air is represented by the system default distribution, /dev/xvdb began to /dev/xvdz the default value: empty'
ecsParameters["DataDisk_4_Category"]='The system disk disk type: cloud- cloud disk; ephemeral- temporary disk; the default value: cloud'
ecsParameters["DataDisk_4_SnapshotId"]='Snapshot while creating disk'
ecsParameters["DataDisk_4_DiskName"]='The corresponding disk display name'
ecsParameters["DataDisk_4_Description"]='The description of the corresponding disk'
ecsParameters["DataDisk_4_Device"]='Air is represented by the system default distribution, /dev/xvdb began to /dev/xvdz the default value: empty'
ecsParameters["DataDiskPolicyEnabled"]='Data disk automatic snapshot policy switch: True: the disk properties disk play automatic snapshot False: does not play the automatic snapshot'
ecsParameters["Action"]=''
ecsParameters["logfile"]=''
ecsParameters["CidrBlock"]=''
ecsParameters["VpcName"]=''
ecsParameters["OwnerId"]=''
ecsParameters["VpcId"]=''
ecsParameters["VSwitchId"]=''
ecsParameters["PrivateIpAddress"]=''
ecsParameters["VSwitchName"]=''
ecsParameters["NextHopId"]=''
ecsParameters["DestinationCidrBlock"]=''
ecsParameters["RouteTableId"]=''
ecsParameters["VRouterId"]=''
ecsParameters["VRouterName"]=''
ecsParameters["Time"]=''
ecsParameters["EipAddress"]=''
ecsParameters["AllocationId"]=''
ecsParameters["Bandwidth"]=''






#存储Action信息
ACTION_Dict={}
ACTION_Dict['config'] ={\
    'MustParameters':[],\
    'OptionalParameters':['id','key','output','outputfile','showURL','RegionId'],\
    'Effect':'Save or modify the configuration information.'\
    }

ACTION_Dict['CreateSecurityGroup'] ={\
    'MustParameters':['RegionId','RegionId'],\
    'OptionalParameters':['ClientToken','VpcId','Description','ResourceOwnerAccount'],\
    'Effect':'Create a security group.'\
    }

ACTION_Dict['AuthorizeSecurityGroup'] ={\
    'MustParameters':['SecurityGroupId','RegionId','SecurityGroupId','IpProtocol','PortRange'],\
    'OptionalParameters':['SourceCidrIp','SourceGroupId','Policy','NicType','ResourceOwnerAccount'],\
    'Effect':'Authorization group permissions'\
    }

ACTION_Dict['DescribeSecurityGroupAttribute'] ={\
    'MustParameters':['SecurityGroupId', 'RegionId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'NicType'],\
    'Effect':'Query the security group rules.'\
    }
ACTION_Dict['DescribeSecurityGroups'] ={\
    'MustParameters':['RegionId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'PageNumber', 'PageSize'],\
    'Effect':'Query security list'\
    }

ACTION_Dict['RevokeSecurityGroup'] ={\
    'MustParameters':['SecurityGroupId', 'RegionId', 'IpProtocol', 'PortRange'],\
    'OptionalParameters':['ResourceOwnerAccount', 'SourceGroupId', 'SourceCidrIp', 'Policy', 'NicType'],\
    'Effect':'Revocation of group rules'\
    }
ACTION_Dict['DeleteSecurityGroup'] ={\
    'MustParameters':['RegionId', 'RegionId', 'SecurityGroupId'],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'Remove the security group'\
    }

ACTION_Dict['ModifyInstanceAttribute'] ={\
    'MustParameters':['InstanceId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'InstanceName', 'Description', 'HostName', 'Password'],\
    'Effect':'Modify instance attributes'\
    }

ACTION_Dict['ModifyInstanceVpcAttribute'] ={\
    'MustParameters':['InstanceId'],\
    'OptionalParameters':['InstanceId', 'VSwitchId', 'PrivateIpAddress'],\
    'Effect':'Modify instance attributes'\
    }


ACTION_Dict['DescribeInstances'] ={\
    'MustParameters':['RegionId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'VpcId', 'VSwitchId', 'ZoneId','InstanceNetworkType','SecurityGroupId','PageNumber','PageSize'],\
    'Effect':'Query (query instance instance state list)'\
    }

ACTION_Dict['DescribeInstanceStatus'] ={\
    'MustParameters':['RegionId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'ZoneId', 'PageNumber', 'PageSize'],\
    'Effect':'Query (query instance instance state list)'\
    }
ACTION_Dict['DescribeInstanceAttribute'] ={\
    'MustParameters':['InstanceId'],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'For details of the specified instance.'\
    }

ACTION_Dict['DescribeRegions'] ={\
    'MustParameters':[],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'Query for available Region list.'\
    }
ACTION_Dict['DescribeZones'] ={\
    'MustParameters':['RegionId'],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'Query the available usable area (Zone) list.'\
    }

ACTION_Dict['CreateImage'] ={\
    'MustParameters':['SnapshotId', 'RegionId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'ImageName', 'ImageVersion', 'Description', 'ClientToken'],\
    'Effect':'Create a custom image by the snapshot, mirror after creation can be used for the new ECS instance.'\
    }
ACTION_Dict['DeleteImage'] ={\
    'MustParameters':['RegionId', 'ImageId'],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'Delete the specified user custom image. The mirror after the deletion will no longer be used to create an instance of ECS, reset.'\
    }
ACTION_Dict['DescribeImages'] ={\
    'MustParameters':['RegionId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'PageNumber', 'PageSize', 'SnapshotId', 'ImageName', 'ImageOwnerAlias'],\
    'Effect':'Query the available image'\
    }

#ACTION_Dict['DescribeInstanceDisks'] ={\
#    'MustParameters':[],\
#    'OptionalParameters':[]\
#    }
ACTION_Dict['DeleteDisk'] ={\
    'MustParameters':['DiskId'],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'When a disk device is no longer in use, can remove the disk. But you can only delete disk independent cloud.'\
    }

ACTION_Dict['AddDisk'] ={\
    'MustParameters':['InstanceId', 'Size'],\
    'OptionalParameters':['SnapshotId']\
    }
ACTION_Dict['AllocatePublicIpAddress'] ={\
    'MustParameters':['InstanceId'],\
    'OptionalParameters':['IpAddress','VlanId'],\
    'Effect':'Allocates an available public IP address to a particular instance of.'\
    }

ACTION_Dict['ReleasePublicIpAddress'] ={\
    'MustParameters':['PublicIpAddress'],\
    'OptionalParameters':[]\
    }
#创建实例
ACTION_Dict['CreateInstance'] ={\
    'MustParameters':['RegionId', 'ImageId', 'InstanceType', 'SecurityGroupId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'ZoneId', 'InstanceName',\
                          'Description', 'InternetChargeType', 'InternetMaxBandwidthIn',\
                          'InternetMaxBandwidthOut', 'HostName', 'Password',\
                          'SystemDisk_Category', 'SystemDisk_DiskName', 'SystemDisk_Description',\
                          'DataDisk_1_Category', 'DataDisk_1_SnapshotId', 'DataDisk_1_DiskName', 'DataDisk_1_Description', 'DataDisk_1_Device',\
                          'DataDisk_2_Category', 'DataDisk_2_SnapshotId', 'DataDisk_2_DiskName', 'DataDisk_2_Description', 'DataDisk_2_Device',\
                          'DataDisk_3_Category', 'DataDisk_3_SnapshotId', 'DataDisk_3_DiskName', 'DataDisk_3_Description', 'DataDisk_3_Device',\
                          'DataDisk_4_Category', 'DataDisk_4_SnapshotId', 'DataDisk_4_DiskName', 'DataDisk_4_Description', 'DataDisk_4_Device',\
                          'ClientToken','VSwitchId','PrivateIpAddress'],\
    'Effect':'Create an instance of'\
    }
ACTION_Dict['StartInstance'] ={\
    'MustParameters':['InstanceId'],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'Start a named instance.'\
    }
ACTION_Dict['StopInstance'] ={\
    'MustParameters':['InstanceId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'ForceStop'],\
    'Effect':'Stop a named instance'\
    }
ACTION_Dict['RebootInstance'] ={\
    'MustParameters':['InstanceId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'ForceStop'],\
    'Effect':'Restart the instance specified.'\
    }
"""
ACTION_Dict['ResetInstance'] ={\
    'MustParameters':['InstanceId','ImageId','DiskType'],\
    'OptionalParameters':[],\
    'Effect':''\
    }
"""
ACTION_Dict['DeleteInstance'] ={\
    'MustParameters':['InstanceId'],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'Delete instances'\
    }

ACTION_Dict['CreateSnapshot'] ={\
    'MustParameters':['DiskId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'SnapshotName', 'Description', 'ClientToken'],\
    'Effect':'Create a snapshot of the specified disk storage device.'\
    }
ACTION_Dict['DeleteSnapshot'] ={\
    'MustParameters':['SnapshotId'],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'Delete the specified instance specified snapshot, disk device.'\
    }
ACTION_Dict['DescribeSnapshots'] ={\
    'MustParameters':['RegionId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'InstanceId', 'DiskId', 'SnapshotIds', 'PageNumber', 'PageSize'],\
    'Effect':'The query for a disk device cloud servers all snapshot list.'\
    }
"""
ACTION_Dict['DescribeSnapshotAttribute'] ={\
    'MustParameters':['RegionId','SnapshotId'],\
    'OptionalParameters':[],\
    'Effect':''\
    }
"""
#ACTION_Dict['RollbackSnapshot'] ={\
#    'MustParameters':['InstanceId', 'SnapshotId', 'DiskId'],\
#    'OptionalParameters':[]\
#    }

ACTION_Dict['DescribeInstanceTypes'] ={\
    'MustParameters':[],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'Query provided by ECS instance resource specification list.'\
    }
ACTION_Dict['JoinSecurityGroup'] ={\
    'MustParameters':['InstanceId', 'SecurityGroupId'],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'The instance is added to the security group specified.'\
    }
ACTION_Dict['LeaveSecurityGroup'] ={\
    'MustParameters':['InstanceId', 'SecurityGroupId'],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'The instance removed from the specified security group.'\
    }
ACTION_Dict['CreateDisk'] = {\
    'MustParameters':['RegionId', 'ZoneId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'Size', 'SnapshotId', 'DiskName', 'Description', 'ClientToken'],\
    'Effect':'Create disk'\
    }
ACTION_Dict['DescribeDisks'] ={\
    'MustParameters':['RegionId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'ZoneId', 'DiskIds', 'InstanceId', 'DiskType', 'Category', 'Status', 'SnapshotId', 'Portable', 'DeleteWithInstance', 'DeleteAutoSnapshot', 'PageNumber', 'PageSize'],\
    'Effect':'Query disk'\
    }
ACTION_Dict['AttachDisk'] ={\
    'MustParameters':['InstanceId', 'DiskId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'Device', 'DeleteWithInstance'],\
    'Effect':'Mount the disk'\
    }
ACTION_Dict['DetachDisk'] = {\
    'MustParameters':['InstanceId', 'DiskId'],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'Unmount disk'\
    }
ACTION_Dict['ModifyDiskAttribute'] = {\
    'MustParameters':['DiskId'],\
    'OptionalParameters':['ResourceOwnerAccount', 'DiskName', 'Description', 'DeleteWithInstance'],\
    'Effect':'Modify disk properties'\
    }
ACTION_Dict['ReInitDisk'] ={\
    'MustParameters':['DiskId'],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'Reinitializes the disk to the initial state'\
    }
ACTION_Dict['ResetDisk'] ={\
    'MustParameters':['DiskId','SnapshotId'],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'Use the specified snapshot rollback disk disk itself.'\
    }

ACTION_Dict['RestoreDisk'] ={\
    'MustParameters':['DiskId','SnapshotId'],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':''\
    }

ACTION_Dict['ReplaceSystemDisk'] ={\
    'MustParameters':['InstanceId','ImageId'],\
    'OptionalParameters':['ResourceOwnerAccount','ClientToken'],\
    'Effect':'Replace the system disk'\
    }

ACTION_Dict['ModifyAutoSnapshotPolicy'] ={\
    'MustParameters':[],\
    'OptionalParameters':['ResourceOwnerAccount', 'SystemDiskPolicyEnabled',\
                          'SystemDiskPolicyTimePeriod', 'SystemDiskPolicyRetentionDays',\
                          'SystemDiskPolicyRetentionLastWeek', 'DataDiskPolicyTimePeriod',\
                          'DataDiskPolicyRetentionDays', 'DataDiskPolicyRetentionLastWeek',\
                          'DataDiskPolicyEnabled'],\
    'Effect':'Set up automatic snapshot strategy'\
    }
ACTION_Dict['DescribeAutoSnapshotPolicy'] ={\
    'MustParameters':[],\
    'OptionalParameters':['ResourceOwnerAccount'],\
    'Effect':'The automatic snapshot query strategy'\
    }

ACTION_Dict['DescribeInstanceMonitorData'] ={\
    'MustParameters':['InstanceId', 'StartTime', 'EndTime'],\
    'OptionalParameters':['ResourceOwnerAccount', 'Period'],\
    'Effect':'Paging query monitoring information related to all of the users of the cloud server.'\
    }


#2014-11-19号下班前最后添加
ACTION_Dict['AllocateEipAddress'] ={\
    'MustParameters':['RegionId'],\
    'OptionalParameters':['Bandwidth', 'InternetChargeType','ClientToken'],\
    'Effect':''\
    }
ACTION_Dict['AssociateEipAddress'] ={\
    'MustParameters':['AllocationId','InstanceId'],\
    'OptionalParameters':['Bandwidth', 'InternetChargeType','ClientToken'],\
    'Effect':''\
    }


ACTION_Dict['DescribeEipAddresses'] ={\
    'MustParameters':['RegionId'],\
    'OptionalParameters':['Status', 'EipAddress','AllocationId','PageNumber','PageSize'],\
    'Effect':''\
    }

ACTION_Dict['ModifyEipAddressAttribute'] ={\
    'MustParameters':['AllocationId','Bandwidth'],\
    'OptionalParameters':[],\
    'Effect':''\
    }


ACTION_Dict['UnassociateEipAddress'] ={\
    'MustParameters':['AllocationId','Bandwidth'],\
    'OptionalParameters':[],\
    'Effect':''\
    }


ACTION_Dict['ReleaseEipAddress'] ={\
    'MustParameters':['AllocationId'],\
    'OptionalParameters':[],\
    'Effect':''\
    }

ACTION_Dict['ModifyInstanceSpec'] ={\
    'MustParameters':['InstanceId'],\
    'OptionalParameters':['InternetMaxBandwidthOut', 'InternetMaxBandwidthIn'],\
    'Effect':''\
    }


ACTION_Dict['DescribeEipMonitorData'] ={\
    'MustParameters':['AllocationId','StartTime','EndTime'],\
    'OptionalParameters':['Period'],\
    'Effect':''\
    }

ACTION_Dict['CreateVpc'] ={\
    'MustParameters':['RegionId'],\
    'OptionalParameters':['CidrBlock','VpcName','Description','ClientToken'],\
    'Effect':''\
    }



ACTION_Dict['DeleteVpc'] ={\
    'MustParameters':['VpcId'],\
    'OptionalParameters':[],\
    'Effect':''\
    }

ACTION_Dict['DescribeVpcs'] ={\
    'MustParameters':['RegionId'],\
    'OptionalParameters':['VpcId','PageNumber','PageSize'],\
    'Effect':''\
    }

ACTION_Dict['ModifyVpcAttribute'] ={\
    'MustParameters':['VpcId'],\
    'OptionalParameters':['VpcName','Description'],\
    'Effect':''\
    }


ACTION_Dict['DescribeVRouters'] ={\
    'MustParameters':['RegionId'],\
    'OptionalParameters':['VRouterId','PageNumber','PageSize'],\
    'Effect':''\
    }


ACTION_Dict['ModifyVRouterAttribute'] ={\
    'MustParameters':['VRouterId'],\
    'OptionalParameters':['VRouterName','Description'],\
    'Effect':''\
    }



ACTION_Dict['CreateVSwitch'] ={\
    'MustParameters':['ZoneId','CidrBlock','VpcId'],\
    'OptionalParameters':['VSwitchName','Description','ClientToken'],\
    'Effect':''\
    }


ACTION_Dict['ModifyVSwitchAttribute'] ={\
    'MustParameters':['VSwitchId'],\
    'OptionalParameters':['VSwitchName','Description'],\
    'Effect':''\
    }


ACTION_Dict['DeleteVSwitch'] ={\
    'MustParameters':['VSwitchId'],\
    'OptionalParameters':[],\
    'Effect':''\
    }


ACTION_Dict['DescribeVSwitches'] ={\
    'MustParameters':['VpcId'],\
    'OptionalParameters':['VSwitchId','ZoneId','PageNumber','PageSize'],\
    'Effect':''\
    }


ACTION_Dict['CreateRouteEntry'] ={\
    'MustParameters':['RouteTableId','DestinationCidrBlock','NextHopId'],\
    'OptionalParameters':['ClientToken'],\
    'Effect':''\
    }
ACTION_Dict['ModifyRouteEntry'] ={\
    'MustParameters':['RouteTableId','DestinationCidrBlock','InstanceId'],\
    'OptionalParameters':['ClientToken'],\
    'Effect':''\
    }

ACTION_Dict['DeleteRouteEntry'] ={\
    'MustParameters':['RouteTableId','DestinationCidrBlock','NextHopId'],\
    'OptionalParameters':[],\
    'Effect':''\
    }

ACTION_Dict['DescribeRouteTables'] ={\
    'MustParameters':['VRouterId','PageNumber'],\
    'OptionalParameters':['RouteTableId','PageSize'],\
    'Effect':''\
    }

#lwc add 2014-8-25
ACTION_Dict['AddUser'] ={\
    'MustParameters':['UserName'],\
    'OptionalParameters':['Comments'],
    'FunctionName':'AddUser',\
    'Effect':'The specified user permissions will be added to the space.'\
    }

ACTION_Dict['RemoveUser'] ={\
    'MustParameters':['UserName'],\
    'OptionalParameters':[''],
    'FunctionName':'RemoveUser',\
    'Effect':'A user is removed from the authority in space.'\
    }

ACTION_Dict['PutUserPolicy'] ={\
    'MustParameters':['UserName', 'PolicyName','PolicyDocument'],\
    'OptionalParameters':[''],\
    'FunctionName':'PutUserPolicy',\
    'Effect':'Set the Policy to a user'\
    }
ACTION_Dict['DeleteUserPolicy'] ={\
    'MustParameters':['UserName', 'PolicyName'],\
    'OptionalParameters':[],\
    'FunctionName':'DeleteUserPolicy',\
    'Effect':'Delete a user specified under the Policy.'\
    }
ACTION_Dict['ListUserPolicies'] ={\
    'MustParameters':['UserName'],\
    'OptionalParameters':[],\
    'FunctionName':'ListUserPolicies',\
    'Effect':'The name list of all Policy users under the.'\
    }

ACTION_Dict['ListUsers'] ={\
    'MustParameters':[],\
    'OptionalParameters':[],\
    'FunctionName':'ListUsers',\
    'Effect':'A list of all the users.'\
    }


ActionKeyDict={}
ACTION_List={}
for key in ACTION_Dict.keys():
    ActionKeyDict[key.lower()]=key
    if 'Effect' in ACTION_Dict[key].keys():
        ACTION_List[key]=ACTION_Dict[key]['Effect']


