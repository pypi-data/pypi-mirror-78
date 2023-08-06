"""The class extended by each class that implements an AWS service

The class accepts a dict with the follow properties:
    'force' (list): list of services identifier that they have to be forced for deleting
    'timezone' (str): Timezone string name, default is Etc/GMT

This class is an interface, it contains some methods not implemented.
The methods implemented define if it is the time that the object will be to start, stop, delete.

# license MIT
# author Alessandra Bilardi <alessandra.bilardi@gmail.com>
# see https://github.com/bilardi/aws-saving for details
"""

import re
import pytz
import boto3
import cronex
import datetime

class Service():
    date_tuple = None

    def __init__(self, event):
        """
        initializes variables
            Args:
                event (list): aws details
                    'timezone' (str): Timezone string name, default is Etc/GMT
        """
        if not 'timezone' in event:
            event['timezone'] = 'Etc/GMT'
        now = datetime.datetime.now(pytz.timezone(event['timezone']))
        self.date_tuple = (now.year, now.month, now.day, now.hour, now.minute)

    def get_value(self, list, label):
        """
        gets the value of the tag requested
            Args:
                list (dictionary): list of tags
                label (string): label of the Key of the tag requested
            Returns:
                A string value of the variable named label
        """
        for tag in list:
            if tag['Key'].lower() == label:
                return tag['Value']
        return None

    def is_time_to_act(self, list, action):
        """
        checks if the schedulation and date overlap
            Args:
                list (dictionary): tag list
                action (string): label of the action
            Returns:
                A boolean True if it is time to act
        """
        value = self.get_value(list, action)
        crontab_format = re.compile('[0-9\.\-]* [0-9\.\-]* [0-9\.\-]* [0-9\.\-]* [0-9\.\-]*')
        if value and crontab_format.match(value):
            crontab = value.replace('.', '*')
            if cronex.CronExpression(crontab).check_trigger(self.date_tuple):
                return True
        return False

    def is_to_be_deleted(self, event, instance, id_label, protected_key, protected_value):
        """
        checks if the instance is to be deleted
            Args:
                event (dictionary): the element named force contains the instances list have to be deleted
                id_label (string): name of element for getting the id of instance to check
                protected_key (string): name of element for getting if the instance is protected from deletion
                protected_value (boolean): value of element for getting if the instance is protected from deletion
            Returns:
                A boolean True if it is to be deleted
        """
        if id_label in instance and ((protected_key in instance and instance[protected_key] is protected_value or not protected_key in instance) or (event and 'force' in event and instance[id_label] in event['force'])):
            return True
        return False

    def get_instances(self) -> dict:
        """
        gets the objects details
            Returns:
                A dictionary of the objects details
            Raises:
                NotImplementedError
        """
        raise NotImplementedError

    def already_exists(self, name) -> bool:
        """
        checks if the instance exists
            Args:
                name (string): the instance identifier
            Returns:
                A boolean True if it exists
            Raises:
                NotImplementedError
        """
        raise NotImplementedError

    def run(self, event):
        """
        runs the schedulation
            Args:
                event (dictionary): aws details
                    'force' (list): list of services identifier that they have to be forced for deleting
            Raises:
                NotImplementedError
        """
        raise NotImplementedError
