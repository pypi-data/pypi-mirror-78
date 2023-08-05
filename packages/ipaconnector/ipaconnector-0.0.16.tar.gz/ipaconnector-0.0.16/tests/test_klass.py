import os
import json
from unittest import TestCase
from unittest.mock import Mock, call

from ipaconnector.jdbc import Hive, JdbcDriver, PrivateZone
from ipaconnector.klass import User, AppUser


def get_sample(sample='./sample.json'):
    sample_path = os.path.join(os.path.dirname(__file__), sample)
    with open(sample_path) as _file:
        output = json.load(_file)
    return output


class TestUser(TestCase):
    def test_user(self):
        data = get_sample()['CREATIONS']['HumanUser'][0]
        ut = User(data)
        self.assertEqual(ut.login, 'jdoe')
        self.assertEqual(ut.full_name, 'John Doe')
        self.assertEqual(ut.email, 'jdoe@companyone.xyz')
        self.assertEqual(ut.homedir, '/data01/jdoe/')
        self.assertEqual(ut.gecos, 'FR/C//BYTEL/John Doe')

    def test_user_with_missing_info_should_create_with_none(self):
        data = \
            {"firstname": {"newValue": "John"
                           }, "keytab": {"newValue": "true"
                                         }, "company": {"newValue": "company one"
                                                        }, "team": {"newValue": "MOE"
                                                                    }, "login": {"newValue": "jdoe"
                                                                                 }, "primaryKey": {"login": "jdoe"}}
        ut = User(data)
        self.assertEqual(ut.login, 'jdoe')
        self.assertEqual(ut.full_name, 'John ')
        self.assertEqual(ut.email, None)
        self.assertEqual(ut.homedir, '/data01/jdoe/')
        self.assertEqual(ut.gecos, 'FR/C//BYTEL/John ')


class TestAppUser(TestCase):
    def test_user(self):
        data = get_sample("./delta_test_creations.json")['CREATIONS']['AppUser'][0]
        ut = AppUser(data)
        self.assertEqual('elaint_test1', ut.login)
        self.assertEqual('Application elaint_test1', ut.full_name)
        self.assertEqual('', ut.email)
        self.assertEqual('/data01/elaint_test1/', ut.homedir)
        self.assertEqual('FR/C//BYTEL/Test app user 1', ut.gecos)


class TestHiveDb(TestCase):
    def setUp(self) -> None:
        jdbc = JdbcDriver(host="somehost", principal="some_princ")
        self.jdbc = Mock(spec_set=jdbc)
        hive = Hive(self.jdbc)
        self.hive = Mock(spec_set=hive)
        self.real_hive = hive

    def test_hive_table_dev_zone_0(self):
        data = get_sample("./delta_test_creations.json")['CREATIONS']['DevZone'][0]
        ut = PrivateZone(data)
        self.assertEqual(ut.tech_name, "dev_c00_zi03_*")
        self.assertEqual(ut.cluster, "elara")
        self.assertEqual(ut.description, "Données nécessaires aux cas d'usages métiers")
        self.assertEqual(ut.rw_groups, ["group_test1"])
        self.assertEqual(ut.ro_groups, ["app_elaint_test"])

    def test_hive_table_private_zone_0(self):
        data = get_sample("./delta_test_creations.json")['CREATIONS']['PrivateZone'][0]
        ut = PrivateZone(data)
        self.assertEqual(ut.tech_name, "prv_tes_zi00_usr")
        self.assertEqual(ut.cluster, "elara")
        self.assertEqual(ut.description, "Données nécessaires aux cas d'usages métiers")
        self.assertEqual(ut.rw_groups, ["user_test1"])
        self.assertEqual(ut.ro_groups, [])

    def test_hive_table_private_zone_1(self):
        data = get_sample("./delta_test_creations.json")['CREATIONS']['PrivateZone'][1]
        ut = PrivateZone(data)
        self.assertEqual(ut.tech_name, "prv_tes_zi01_usr")
        self.assertEqual(ut.cluster, "elara")
        self.assertEqual(ut.description, "Données nécessaires aux cas d'usages métiers")
        self.assertEqual(ut.rw_groups, ["user_test2", "dssuser"])
        self.assertEqual(ut.ro_groups, [])

    def test_hive_table_exploited_zone_0(self):
        data = get_sample("./delta_test_creations.json")['CREATIONS']['ExploitedZone'][0]
        ut = PrivateZone(data)
        self.assertEqual(ut.tech_name, "dev_zi00_*")
        self.assertEqual(ut.cluster, "elara")
        self.assertEqual(ut.description, "Dev test base for automation")
        self.assertEqual(ut.rw_groups, ["app_elaint_test"])
        self.assertEqual(ut.ro_groups, ["group_test1"])

    def test_hive_add_db(self):
        data = get_sample("./delta_test_creations.json")['CREATIONS']['PrivateZone'][0]
        ut = PrivateZone(data)
        ut.add_new_database(self.hive)
        self.hive.create_database.assert_called_once_with("prv_tes_zi00_usr",
                                                          description="Données nécessaires "
                                                                      "aux cas d'usages métiers",
                                                          uri="/data/prv_tes/zi00/usr")

    def test_hive_add_dbxd(self):
        data = get_sample("./delta_test_creations.json")['CREATIONS']['PrivateZone'][0]
        ut = PrivateZone(data)
        ut.add_new_database(self.real_hive)
        _func = "usr"
        expected_calls = list()
        expected_calls.append(call(f'CREATE DATABASE `prv_tes_zi00_{_func}` COMMENT "Données nécessaires aux '
                                   f'cas d\'usages métiers" LOCATION "/data/prv_tes/zi00/{_func}"'))
        expected_calls.append(call(f"DROP ROLE `user_access_rw_prv_tes_zi00_{_func}`"))
        expected_calls.append(call(f"DROP ROLE `user_access_r_prv_tes_zi00_{_func}`"))
        expected_calls.append(call(f"CREATE ROLE `user_access_rw_prv_tes_zi00_{_func}`"))
        expected_calls.append(call(f"GRANT ROLE `user_access_rw_prv_tes_zi00_{_func}` TO "
                                   f"GROUP `user_test1`"))
        expected_calls.append(
            call(f"GRANT ALL ON DATABASE `prv_tes_zi00_{_func}` TO ROLE "
                 f"`user_access_rw_prv_tes_zi00_{_func}`"))
        expected_calls.append(
            call(f"GRANT ALL ON URI 'hdfs://elara-ha/data/prv_tes/zi00/{_func}' TO ROLE "
                 f"`user_access_rw_prv_tes_zi00_{_func}`"))
        self.jdbc.query.assert_has_calls(expected_calls)

    def test_hive_add_db_exploited_zone_0(self):
        data = get_sample("./delta_test_creations.json")['CREATIONS']['ExploitedZone'][0]
        ut = PrivateZone(data)
        ut.add_new_database(self.real_hive)
        expected_calls = []
        _functions = ['adm', 'source', 'trv', 'socle', 'metier', 'extr']
        for _func in _functions:
            expected_calls.append(call(f'DROP DATABASE IF EXISTS dev_zi00_{_func} CASCADE'))
            expected_calls.append(call(f'CREATE DATABASE `dev_zi00_{_func}` COMMENT "Dev test base for automation"'
                                       f' LOCATION "/data/dev/zi00/{_func}"'))
            expected_calls.append(call(f"DROP ROLE `user_access_rw_dev_zi00_{_func}`"))
            expected_calls.append(call(f"DROP ROLE `user_access_r_dev_zi00_{_func}`"))
            expected_calls.append(call(f"CREATE ROLE `user_access_r_dev_zi00_{_func}`"))
            expected_calls.append(call(f"GRANT ROLE `user_access_r_dev_zi00_{_func}` TO GROUP"
                                       f" `group_test1`"))
            expected_calls.append(call(f"GRANT SELECT ON DATABASE `dev_zi00_{_func}` TO ROLE "
                                       f"`user_access_r_dev_zi00_{_func}`"))
            expected_calls.append(call(f"CREATE ROLE `user_access_rw_dev_zi00_{_func}`"))
            expected_calls.append(call(f"GRANT ROLE `user_access_rw_dev_zi00_{_func}` TO GROUP"
                                       f" `app_elaint_test`"))
            expected_calls.append(call(f"GRANT ALL ON DATABASE `dev_zi00_{_func}` TO ROLE "
                                       f"`user_access_rw_dev_zi00_{_func}`"))
            expected_calls.append(call(f"GRANT ALL ON URI 'hdfs://elara-ha/data/dev/zi00/{_func}'"
                                       f" TO ROLE `user_access_rw_dev_zi00_{_func}`"))
        self.jdbc.query.assert_has_calls(expected_calls)
