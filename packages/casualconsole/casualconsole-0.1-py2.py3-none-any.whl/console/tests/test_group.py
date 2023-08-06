import unittest
import json
import os


import console.state.group as group_info

basedir = os.path.dirname(__file__)


class TestGroup(unittest.TestCase):

    def setUp(self):
        self.domain = self.get_domain()
        self.groups = self.domain['groups']
        self.servers = self.domain['servers']
        self.executables = self.domain['executables']

    def get_domain(self):
        with open(os.path.join(basedir, 'domain_state.json')) as state:
            domain = json.load(state)
            return domain['result']

    def test_get_group_by_name(self):
        name = '.casual.master'
        group = group_info.get_group_by_name(self.groups, name)
        self.assertIsNotNone(group['name'])
        self.assertEqual(group['name'], name)

    def test_get_group_ny_name_not_found(self):
        name = 'bogus.group.name'
        group = group_info.get_group_by_name(self.groups, name)
        self.assertIsNone(group)

    def test_group_member_count_only_servers(self):
        name = '.casual.master'
        group = group_info.get_group_by_name(self.groups, name)
        group = group_info.get_group_members([group], self.servers, self.executables)[0]
        self.assertIsNotNone(group['membercount'])
        self.assertEqual(group['membercount'], 2)

    def test_group_member_count_including_executables(self):
        name = '.global'
        group = group_info.get_group_by_name(self.groups, name)
        group = group_info.get_group_members([group], self.servers, self.executables)[0]
        self.assertIsNotNone(group['membercount'])
        self.assertEqual(group['membercount'], 3)


if __name__ == '__main__':
    unittest.main()
