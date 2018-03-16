import boto3
import time
import json

print('Loading function')

def lambda_handler(event, context):
    
    ssm = boto3.client('ssm')
    message = event['Records'][0]['Sns']['Message']
    documentName = 'AWS-RunShellScript'
    commandopen = ['iptables -I INPUT -p tcp --dport 81 -j ACCEPT']
    commandclose  = ['iptables -I INPUT -p tcp --dport 81 -j DROP']

    if message.lower() == 'start':
        print("SNS message is: " + message)
        ssmCommand = ssm.send_command(
            DocumentName=documentName,
		    Parameters={'commands': commandopen},
		    Targets =[
		        {
                   "Key": "tag:Name",
                   "Values":[
                       "Prince_POC",
                       ]
               },
           ],
           TimeoutSeconds = 240,
		   Comment = 'nginx service start'
		)
    elif message.lower() == 'stop':
        print("SNS message is: " + message)
        ssmCommand = ssm.send_command(
            DocumentName=documentName,
            Parameters={'commands': commandclose},
            Targets =[
               {
                   "Key": "tag:Name",
                   "Values":[
                       "Prince_POC",
                       ]
               },
           ],
           TimeoutSeconds = 240,
		   Comment = 'nginx service stop'
		)
    else:
        print('Invalid Input')
