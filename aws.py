import boto3
import botocore
import json
import os

def create_ec2_instance(image_id, instance_type, subnet_id, security_group_ids, user_data):
    try:
        resource_aws = boto3.resource("ec2",
                                      aws_access_key_id=os.getenv('Access key'),
                                      aws_secret_access_key=os.getenv('screat access key'),
                                      region_name="us-east-1")

        instance = resource_aws.create_instances(
            ImageId=image_id,
            InstanceType=instance_type,
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sda1',
                    'Ebs': {
                        'DeleteOnTermination': True,
                    }
                }
            ],
            MaxCount=1,
            MinCount=1,
            KeyName='aws.key.pem',  # Update this with your key name
            SecurityGroupIds=security_group_ids,
            SubnetId=subnet_id,
            UserData=user_data,
            InstanceInitiatedShutdownBehavior='terminate'
        )
        
        return instance[0]  # Assuming you are creating only one instance

    except botocore.exceptions.ClientError as e:
        print("Error creating EC2 instance:", e)
        return None

if app_config.get("RUN_MODE", 'PRODUCTION') == 'PRODUCTION':
    # Assuming 'config_worker', 'access_key', 'secret_access', 'ami', 'instanceType', 'subnet_id', 'security_group_ids' are defined

    app_config_for_worker = json.loads(os.getenv('config_worker'))
    user_data = '''#!/bin/bash
    set -x
    cd /home/ubuntu/worker/app
    sudo -u ubuntu python3 ./main.py work
    shutdown
    '''

    instance1 = create_ec2_instance(os.getenv('ami-04b70fa74e45c3917'),
                                     os.getenv('t2.micro'),
                                     'subnet-091f8243f5859a9dd',  # Update with your subnet ID
                                     ['sg-07de83a88c6199978'],     # Update with your security group IDs
                                     user_data)

    instance2 = create_ec2_instance(os.getenv('ami-04b70fa74e45c3917'),
                                     os.getenv('t2.micro'),
                                     'subnet-0bb109ce2a2e1f094',  # Update with your subnet ID
                                     ['sg-07de83a88c6199978'], # Update with your security group IDs
                                     user_data)

    if instance1:
        print("Instance 1 created successfully with ID:", instance1.id)
    if instance2:
        print("Instance 2 created successfully with ID:", instance2.id)
