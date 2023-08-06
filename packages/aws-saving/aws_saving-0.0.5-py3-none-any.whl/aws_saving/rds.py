"""The class extends the class named Service and it manages the saving for the Amazon RDS and Amazon Aurora services

The class accepts a dict with the follow properties:
    'force' (list): list of services identifier that they have to be forced for deleting
    'timezone' (str): Timezone string name, default is Etc/GMT

Here's an example:

    >>> import aws_saving.rds as mainClass
    >>> arguments = {}
    >>> arguments['force'] = ['aurora-cluster-identifier']
    >>> arguments['timezone'] = ['Europe/Rome']
    >>> saving = mainclass.Rds(arguments)
    >>> saving.run(arguments)

# license MIT
# author Alessandra Bilardi <alessandra.bilardi@gmail.com>
# see https://github.com/bilardi/aws-saving for details
"""

import boto3
from .service import Service

class Rds(Service):
    rds = None
    date_tuple = None

    def __init__(self, event):
        self.rds = boto3.client('rds')
        Service.__init__(self, event)

    def get_instances(self):
        """
        gets the rds details
            Returns:
                A dictionary of the rds instances details
        """
        instances_list = self.rds.describe_db_instances()
        instances = []
        for instance in instances_list['DBInstances']:
            tag_list = self.rds.list_tags_for_resource(ResourceName=instance['DBInstanceArn'])
            saving = self.get_value(tag_list['TagList'], 'saving')
            if saving and saving.lower() == 'enabled':
                instance['DBIdentifier'] = instance['DBClusterIdentifier'] if 'DBClusterIdentifier' in instance else instance['DBInstanceIdentifier']
                instance['Tags'] = tag_list['TagList']
                instances.append(instance)
        return instances

    def already_exists(self, name):
        """
        checks if the rds instance exists
            Args:
                name (string): the rds identifier
            Returns:
                A boolean True if it exists
        """
        try:
            if self.rds.describe_db_instances(DBInstanceIdentifier=name):
                return True
        except:
            print('The RDS instance named ' + str(name) + ' not exists')
        return False

    def run(self, event):
        """
        runs the schedulation
            Args:
                event (dictionary): aws details
                    'force' (list): list of services identifier that they have to be forced for deleting
        """
        instances = self.get_instances()
        for instance in instances:
            print(instance['DBIdentifier'])
            if self.is_time_to_act(instance['Tags'], 'stop') and instance['DBInstanceStatus'] == 'available':
                if 'DBClusterIdentifier' in instance:
                    print('Stopping ' + instance['DBClusterIdentifier'])
                    self.rds.stop_db_cluster(DBClusterIdentifier=instance['DBClusterIdentifier'])
                else:
                    print('Stopping ' + instance['DBInstanceIdentifier'])
                    self.rds.stop_db_instance(DBInstanceIdentifier=instance['DBInstanceIdentifier'])
            if self.is_time_to_act(instance['Tags'], 'start') and instance['DBInstanceStatus'] == 'stopped':
                if 'DBClusterIdentifier' in instance:
                    print('Starting ' + instance['DBClusterIdentifier'])
                    self.rds.start_db_cluster(DBClusterIdentifier=instance['DBClusterIdentifier'])
                else:
                    print('Starting ' + instance['DBInstanceIdentifier'])
                    self.rds.start_db_instance(DBInstanceIdentifier=instance['DBInstanceIdentifier'])
            if self.is_time_to_act(instance['Tags'], 'delete') and not instance['DBInstanceStatus'].startswith('delete'):
                if self.is_to_be_deleted(event, instance, 'DBIdentifier', 'DeletionProtection', False):
                    if 'DeletionProtection' in instance and instance['DeletionProtection'] is True:
                        if 'DBClusterIdentifier' in instance:
                            self.rds.modify_db_cluster(DeletionProtection=False, DBClusterIdentifier=instance['DBClusterIdentifier'])
                        else:
                            self.rds.modify_db_instance(DeletionProtection=False, DBInstanceIdentifier=instance['DBInstanceIdentifier'])
                        print('Disabled Deletion Protection for ' + instance['DBIdentifier'])
                    print('Deleting ' + instance['DBIdentifier'])
                    if 'DBClusterIdentifier' in instance:
                        self.rds.delete_db_instance(DBInstanceIdentifier=instance['DBInstanceIdentifier'], SkipFinalSnapshot=True, DeleteAutomatedBackups=True)
                        self.rds.delete_db_cluster(DBClusterIdentifier=instance['DBClusterIdentifier'], SkipFinalSnapshot=True)
                    else:
                        self.rds.delete_db_instance(DBInstanceIdentifier=instance['DBInstanceIdentifier'], SkipFinalSnapshot=True, DeleteAutomatedBackups=True)
                else:
                    print('Warning: modify the DeletionProtection value to false for deleting ' + instance['DBIdentifier'])

def main(event, context):
    saving = Rds(event)
    saving.run(event)

if __name__ == '__main__':
    main([], None)
