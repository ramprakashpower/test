import json
import boto3
import time
import sys

def lambda_handler(event, context):
    clientcode=event["clientCode"]
    bucketname=event["bucketName"]
    command0 = "rm -rf /home/ssm-user/talend_pipeline/"+clientcode+"/"
    command1 = "aws s3 sync s3://"+bucketname+"/talendpipeline/"+clientcode+"/ /home/ssm-user/talend_pipeline/"+clientcode+"/"
    command2 = "unzip -o /home/ssm-user/talend_pipeline/"+clientcode+"/deploy/*.zip -d /home/ssm-user/talend_pipeline/"+clientcode+"/"
    command3 = "aws s3 sync  s3://"+bucketname+"/talendpipeline/talend_centralized/ /home/ssm-user/talend_pipeline/"+clientcode+"/deploy/"
    command4 ="chmod +x /home/ssm-user/talend_pipeline/"+clientcode+"/"+clientcode+"/"+clientcode+"_master/"+clientcode+"_master_run.sh"
    command5 = "./home/ssm-user/talend_pipeline/"+clientcode+"/"+clientcode+"/"+clientcode+"_master/"+clientcode+"_master_run.sh"
    # Talend pipeline machine id
    Instance_Id = "i-0f4fa2433b773b0e7"
    ssmc = boto3.client('ssm')
    def ssmcrun(c_in,Instance_Id,test,workdir,long_running):
        newcommandrun = ssmc.send_command(
            InstanceIds=[
                Instance_Id
            ],
            DocumentName='AWS-RunShellScript',
            TimeoutSeconds=86400,
            Parameters={
                    "executionTimeout": [
                        "86400"
                    ],
                    "workingDirectory": [
                        workdir
                    ],
                    "commands": [
                        c_in
                    ]        },
        CloudWatchOutputConfig={
            'CloudWatchLogGroupName': 'ssm_talend_execution/'+clientcode+'/',
            'CloudWatchOutputEnabled': True})
        f = ['Cancelling','Failed','TimedOut','Cancelled']
        #p =['Pending','InProgress','Delayed']
        if long_running == False:
            while True:
                time.sleep(5)
                #print("executing")
                status = ssmc.get_command_invocation(CommandId=(newcommandrun["Command"]["CommandId"]),InstanceId=Instance_Id)
                if (status['Status']) == "Success":
                    if test is False:
                        print("success")
                    break
                elif (status['Status']) in f:
                    if test is False:
                        print(status['Status'])
                    break
    workdir = "/"
    ssmcrun(command0,Instance_Id,True,workdir,False)
    ssmcrun(command1,Instance_Id,True,workdir,False)
    ssmcrun(command2,Instance_Id,True,workdir,False)
    ssmcrun(command3,Instance_Id,True,workdir,False)
    ssmcrun(command4,Instance_Id,True,workdir,False)
    ssmcrun(command5,Instance_Id,True,workdir,True)

