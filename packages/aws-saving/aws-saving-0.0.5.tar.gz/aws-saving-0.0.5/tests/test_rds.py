import unittest
import json
import datetime
import tests.helper as hlp
from aws_saving.rds import Rds

class RdsClient():
    ddi = None
    ltfr = None
    ne = False
    def __init__(self):
        with open('tests/rds-describe-db-instances.json') as json_file:
            self.ddi = json.load(json_file)
        with open('tests/rds-list-tags-for-resource.json') as json_file:
            self.ltfr = json.load(json_file)
    def describe_db_instances(self, DBInstanceIdentifier=None):
        if DBInstanceIdentifier is None or self.ne is False:
            return self.ddi
        raise ValueError
    def list_tags_for_resource(self, ResourceName):
        if isinstance(ResourceName, str):
            return self.ltfr
        raise ValueError
    def stop_db_cluster(self, DBClusterIdentifier):
        if isinstance(DBClusterIdentifier, str):
            return
        raise ValueError
    def stop_db_instance(self, DBInstanceIdentifier):
        if isinstance(DBInstanceIdentifier, str):
            return
        raise ValueError
    def start_db_cluster(self, DBClusterIdentifier):
        if isinstance(DBClusterIdentifier, str):
            return
        raise ValueError
    def start_db_instance(self, DBInstanceIdentifier):
        if isinstance(DBInstanceIdentifier, str):
            return
        raise ValueError
    def modify_db_cluster(self, DeletionProtection, DBClusterIdentifier):
        if isinstance(DeletionProtection, bool) and isinstance(DBClusterIdentifier, str):
            return
        raise ValueError
    def modify_db_instance(self, DeletionProtection, DBInstanceIdentifier):
        if isinstance(DeletionProtection, bool) and isinstance(DBInstanceIdentifier, str):
            return
        raise ValueError
    def delete_db_cluster(self, DBClusterIdentifier, SkipFinalSnapshot):
        if isinstance(SkipFinalSnapshot, bool) and isinstance(DBClusterIdentifier, str):
            return
        raise ValueError
    def delete_db_instance(self, DBInstanceIdentifier, SkipFinalSnapshot, DeleteAutomatedBackups):
        if isinstance(SkipFinalSnapshot, bool) and isinstance(DeleteAutomatedBackups, bool) and isinstance(DBInstanceIdentifier, str):
            return
        raise ValueError
    def set_not_exists_simulation(self, boolean):
        self.ne = boolean

class TestService(unittest.TestCase, Rds):
    s = None

    def __init__(self, *args, **kwargs):
        self.s = Rds({})
        self.s.rds = RdsClient()
        unittest.TestCase.__init__(self, *args, **kwargs)

    def get_output(self, event = {}):
        with hlp.captured_output() as (out, err):
            self.s.run(event)
        return out.getvalue().strip()

    def test_get_instances(self):
        instances = self.s.get_instances()
        self.assertEqual(instances[0]['DBIdentifier'], 'aurora-cluster')
        self.assertEqual(instances[1]['DBIdentifier'], 'rds-1')

    def test_already_exists(self):
        self.s.rds.set_not_exists_simulation(False)
        self.assertTrue(self.s.already_exists('aurora-cluster'))
        self.s.rds.set_not_exists_simulation(True)
        with hlp.captured_output() as (out, err):
            self.assertFalse(self.s.already_exists('aurora-cluster'))
        self.assertEqual(out.getvalue().strip(), "The RDS instance named aurora-cluster not exists")

    def test_run(self):
        now = datetime.datetime.now()

        for rds in self.s.rds.ddi['DBInstances']:
            rds['DBInstanceStatus'] = 'available'
        test = now.replace(hour=18, minute=00, day=6)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "aurora-cluster\nStopping aurora-cluster\nrds-1\nStopping rds-1")
        test = now.replace(hour=18, minute=00, day=16)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "aurora-cluster\nrds-1")

        for rds in self.s.rds.ddi['DBInstances']:
            rds['DBInstanceStatus'] = 'stopped'
        test = now.replace(hour=8, minute=00, day=6)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "aurora-cluster\nStarting aurora-cluster\nrds-1\nStarting rds-1")
        test = now.replace(hour=8, minute=00, day=16)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "aurora-cluster\nrds-1")

        self.s.rds.ltfr['TagList'][0]['Key'] = 'Delete'
        for rds in self.s.rds.ddi['DBInstances']:
            rds['DeletionProtection'] = False
        test = now.replace(hour=8, minute=00, day=6)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "aurora-cluster\nDeleting aurora-cluster\nrds-1\nDeleting rds-1")
        test = now.replace(hour=8, minute=00, day=16)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "aurora-cluster\nrds-1")

        for rds in self.s.rds.ddi['DBInstances']:
            rds['DeletionProtection'] = True
        test = now.replace(hour=8, minute=00, day=6)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "aurora-cluster\nWarning: modify the DeletionProtection value to false for deleting aurora-cluster\nrds-1\nWarning: modify the DeletionProtection value to false for deleting rds-1")
        test = now.replace(hour=8, minute=00, day=16)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output(), "aurora-cluster\nrds-1")

        test = now.replace(hour=8, minute=00, day=6)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output({"force":["aurora-cluster","rds-1"]}), "aurora-cluster\nDisabled Deletion Protection for aurora-cluster\nDeleting aurora-cluster\nrds-1\nDisabled Deletion Protection for rds-1\nDeleting rds-1")
        test = now.replace(hour=8, minute=00, day=16)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertEqual(self.get_output({"force":["aurora-cluster","rds-1"]}), "aurora-cluster\nrds-1")

if __name__ == '__main__':
    unittest.main()