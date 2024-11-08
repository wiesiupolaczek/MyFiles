import boto3
from botocore.exceptions import ClientError

def launch_ec2_instance():
  ec2_client = boto3.client('ec2', region_name='us-east-1')  # Replace with your desired region

  try:
      # Launch an EC2 instance
      response = ec2_client.run_instances(
          ImageId='ami-0866a3c8686eaeeba',    # Replace with a valid AMI ID
          InstanceType='t2.micro',            # Instance type
          KeyName='1st',              # Replace with your key pair name
          MinCount=1,
          MaxCount=1,
          SecurityGroupIds=['sg-06b4b3c8491e3a68d'],  # Replace with your security group ID(s)
          SubnetId='subnet-0e8f6b0c8e6b89f9b',        # Replace with your subnet ID
          TagSpecifications=[
              {
                  'ResourceType': 'instance',
                  'Tags': [
                      {'Key': 'Name', 'Value': 'MyEC2Instance'}
                  ]
              },
          ]
      )

      instance = response['Instances'][0]
      instance_id = instance['InstanceId']
      print(f'Launched EC2 instance {instance_id}')

  except ClientError as e:
      print(f'An error occurred: {e}')

if __name__ == '__main__':
  launch_ec2_instance()