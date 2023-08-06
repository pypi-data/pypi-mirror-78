import unittest
import re
import cronex
import datetime
from aws_saving.service import Service

class TestService(unittest.TestCase, Service):
    no_act_list = [{"Key":"Saving", "Value":"Enabled"}]
    perfect_list = [{"Key":"Saving", "Value":"Enabled"},{"Key":"Stop", "Value":"0 18 . . ."},{"Key":"Start", "Value":"0 6 . . ."}]
    alternative_list = [{"Key":"saving", "Value":"enabled"},{"Key":"stop", "Value":"0 19 . . ."},{"Key":"start", "Value":"0 7 . . ."}]
    s = None

    def __init__(self, *args, **kwargs):
        self.s = Service({})
        unittest.TestCase.__init__(self, *args, **kwargs)

    def test_get_value(self):
        self.assertEqual(self.s.get_value(self.perfect_list, 'stop'), '0 18 . . .');
        self.assertEqual(self.s.get_value(self.alternative_list, 'stop'), '0 19 . . .');
        self.assertEqual(self.s.get_value(self.no_act_list, 'saving'), 'Enabled');
        self.assertNotEqual(self.s.get_value(self.no_act_list, 'saving'), 'enabled');
        self.assertEqual(self.s.get_value(self.no_act_list, 'stop'), None);

    def test_is_time_to_act(self):
        now = datetime.datetime.now()
        test = now.replace(hour=18, minute=00)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertTrue(self.s.is_time_to_act(self.perfect_list, 'stop'));
        self.assertFalse(self.s.is_time_to_act(self.alternative_list, 'stop'));
        test = now.replace(hour=19, minute=00)
        self.s.date_tuple = (test.year, test.month, test.day, test.hour, test.minute)
        self.assertTrue(self.s.is_time_to_act(self.alternative_list, 'stop'));
        self.assertFalse(self.s.is_time_to_act(self.no_act_list, 'saving'));
        self.assertFalse(self.s.is_time_to_act(self.no_act_list, 'stop'));

    def test_get_instances(self):
        with self.assertRaises(NotImplementedError):
            self.s.get_instances()
    
    def test_already_exists(self):
        with self.assertRaises(NotImplementedError):
            self.s.already_exists('instance-name')
    
    def test_run(self):
        with self.assertRaises(NotImplementedError):
            self.s.run({})

if __name__ == '__main__':
    unittest.main()