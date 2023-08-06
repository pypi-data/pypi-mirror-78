import unittest
import json
import datetime
import tests.helper as hlp
from aws_saving.ec2 import Ec2

class Ec2Client():
    di = None
    dt = None
    dia = None
    def __init__(self):
        with open('tests/ec2-describe-instances.json') as json_file:
            self.di = json.load(json_file)
        with open('tests/ec2-describe-tags.json') as json_file:
            self.dt = json.load(json_file)
        with open('tests/ec2-describe-instance-attribute.json') as json_file:
            self.dia = json.load(json_file)
    def describe_instances(self):
        return self.di
    def describe_tags(self, Filters):
        return self.dt
    def describe_instance_attribute(self, Attribute, InstanceId):
        if isinstance(Attribute, str) and isinstance(InstanceId, str):
            return self.dia
        raise ValueError
    def stop_instances(self, InstanceIds):
        if isinstance(InstanceIds, list):
            return
        raise ValueError
    def start_instances(self, InstanceIds):
        if isinstance(InstanceIds, list):
            return
        raise ValueError
    def modify_instance_attribute(self, DisableApiTermination, InstanceId):
        if isinstance(DisableApiTermination, bool) and isinstance(InstanceId, str):
            return
        raise ValueError
    def terminate_instances(self, InstanceIds):
        if isinstance(InstanceIds, list):
            return
        raise ValueError

class TestService(unittest.TestCase, Ec2):
    s = None

    def __init__(self, *args, **kwargs):
        self.s = Ec2({})
        unittest.TestCase.__init__(self, *args, **kwargs)

    def get_output(self, event = {}):
        with hlp.captured_output() as (out, err):
            self.s.run(event)
        return out.getvalue().strip()

    def test_get_instances(self):
        self.s.ec2 = Ec2Client()
        instances = self.s.get_instances()
        self.assertEqual(instances[0]['InstanceId'], 'i-01234567890')
        self.assertEqual(instances[1]['InstanceId'], 'i-01234567891')

    def test_run(self):
        self.s.ec2 = Ec2Client()
        now = datetime.datetime.now()

        for ec2 in self.s.ec2.di['Reservations'][0]['Instances']:
            ec2['State']['Name'] = 'running'
        test = now.replace(hour=18, minute=00, day=6)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "i-01234567890\nStopping i-01234567890\ni-01234567891\nStopping i-01234567891")
        test = now.replace(hour=18, minute=00, day=16)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "i-01234567890\ni-01234567891")

        for ec2 in self.s.ec2.di['Reservations'][0]['Instances']:
            ec2['State']['Name'] = 'stopped'
        test = now.replace(hour=8, minute=00, day=6)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "i-01234567890\nStarting i-01234567890\ni-01234567891\nStarting i-01234567891")
        test = now.replace(hour=8, minute=00, day=16)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "i-01234567890\ni-01234567891")

        self.s.ec2.dia['DisableApiTermination']['Value'] = False
        for ec2 in self.s.ec2.di['Reservations'][0]['Instances']:
            ec2['Tags'][0]['Key'] = 'Delete'
        test = now.replace(hour=8, minute=00, day=6)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "i-01234567890\nDeleting i-01234567890\ni-01234567891\nDeleting i-01234567891")
        test = now.replace(hour=8, minute=00, day=16)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "i-01234567890\ni-01234567891")

        self.s.ec2.dia['DisableApiTermination']['Value'] = True
        test = now.replace(hour=8, minute=00, day=6)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "i-01234567890\nWarning: modify the DisableApiTermination value to false for deleting i-01234567890\ni-01234567891\nWarning: modify the DisableApiTermination value to false for deleting i-01234567891")
        test = now.replace(hour=8, minute=00, day=16)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "i-01234567890\ni-01234567891")

        test = now.replace(hour=8, minute=00, day=6)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output({"force":["i-01234567890","i-01234567891"]}), "i-01234567890\nEnabled Api Termination for i-01234567890\nDeleting i-01234567890\ni-01234567891\nEnabled Api Termination for i-01234567891\nDeleting i-01234567891")
        test = now.replace(hour=8, minute=00, day=16)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output({"force":["i-01234567890","i-01234567891"]}), "i-01234567890\ni-01234567891")

if __name__ == '__main__':
    unittest.main()