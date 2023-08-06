"""The class extends the class named Service and it manages the saving for the Amazon EC2 service

The class accepts a dict with the follow properties:
    'force' (list): list of services identifier that they have to be forced for deleting
    'timezone' (str): Timezone string name, default is Etc/GMT

Here's an example:

    >>> import aws_saving.ec2 as mainClass
    >>> arguments = {}
    >>> arguments['force'] = ['i-01234567890']
    >>> arguments['timezone'] = ['Europe/Rome']
    >>> saving = mainclass.Ec2(arguments)
    >>> saving.run(arguments)

# license MIT
# author Alessandra Bilardi <alessandra.bilardi@gmail.com>
# see https://github.com/bilardi/aws-saving for details
"""

import boto3
from .service import Service

class Ec2(Service):
    ec2 = None
    date_tuple = None

    def __init__(self, event):
        self.ec2 = boto3.client('ec2')
        Service.__init__(self, event)

    def get_instances(self):
        """
        gets the ec2 details
            Returns:
                A dictionary of the ec2 instances details
        """
        instances_list = self.ec2.describe_instances()
        instances = []
        for instance in instances_list['Reservations'][0]['Instances']:
            disable_api_termination = self.ec2.describe_instance_attribute(Attribute='disableApiTermination',InstanceId=instance['InstanceId'])
            tag_list = self.ec2.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [instance['InstanceId']]}])
            saving = self.get_value(tag_list['Tags'], 'saving')
            if saving and saving.lower() == 'enabled':
                instance['Tags'] = tag_list['Tags']
                instance['DisableApiTermination'] = disable_api_termination['DisableApiTermination']['Value']
                instance['InstanceStatus'] = instance['State']['Name']
                instances.append(instance)
        return instances

    def run(self, event):
        """
        runs the schedulation
            Args:
                event (dictionary): aws details
                    'force' (list): list of services identifier that they have to be forced for deleting
        """
        instances = self.get_instances()
        for instance in instances:
            print(instance['InstanceId'])
            if self.is_time_to_act(instance['Tags'], 'stop') and instance['InstanceStatus'] == 'running':
                print('Stopping ' + instance['InstanceId'])
                self.ec2.stop_instances(InstanceIds=[instance['InstanceId']])
            if self.is_time_to_act(instance['Tags'], 'start') and instance['InstanceStatus'] == 'stopped':
                print('Starting ' + instance['InstanceId'])
                self.ec2.start_instances(InstanceIds=[instance['InstanceId']])
            if self.is_time_to_act(instance['Tags'], 'delete') and not instance['InstanceStatus'].startswith('delete'):
                if self.is_to_be_deleted(event, instance, 'InstanceId', 'DisableApiTermination', False):
                    if 'DisableApiTermination' in instance and instance['DisableApiTermination'] is True:
                        self.ec2.modify_instance_attribute(DisableApiTermination=False, InstanceId=instance['InstanceId'])
                        print('Enabled Api Termination for ' + instance['InstanceId'])
                    print('Deleting ' + instance['InstanceId'])
                    self.ec2.terminate_instances(InstanceIds=[instance['InstanceId']])
                else:
                    print('Warning: modify the DisableApiTermination value to false for deleting ' + instance['InstanceId'])

def main(event, context):
    saving = Ec2(event)
    saving.run(event)

if __name__ == '__main__':
    main([], None)
