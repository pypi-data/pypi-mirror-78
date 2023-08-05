from unittest.mock import Mock, patch, call
from unittest import TestCase

from ipaconnector.jdbc import JdbcDriver, Hive


class TestHive(TestCase):
    def setUp(self) -> None:
        jdbc = Mock(spec=JdbcDriver, spec_set=JdbcDriver)
        self.jdbc = jdbc('xd')
        self.ut = Hive(self.jdbc)

    def test_show_databases(self):
        op = [('default',), ('dev_c00_zi00_adm',), ('dev_c00_zi00_extr',), ('dev_c00_zi00_metier',),
              ('dev_c00_zi00_socle',), ('dev_c00_zi00_source',), ('dev_c00_zi00_trv',)]
        self.jdbc.query.return_value = op
        dbs = self.ut.show_databases()
        self.jdbc.query.assert_called_once_with("show databases")
        expected_dbs = ['default', 'dev_c00_zi00_adm', 'dev_c00_zi00_extr', 'dev_c00_zi00_metier',
                        'dev_c00_zi00_socle', 'dev_c00_zi00_source', 'dev_c00_zi00_trv']
        self.assertListEqual(dbs, expected_dbs)

    def test_show_grant_role(self):
        op = [('prv_moe_zi20_usr', '', '', '', 'user_access_rw_prv_moe_zi20_usr',
               'ROLE', '*', False, 1582126727000, '--'),
              ('hdfs://elara-ha/data/prv_moe/zi20/usr', '', '', '', 'user_access_rw_prv_moe_zi20_usr',
               'ROLE', '*', False, 1582126717000, '--')]
        self.jdbc.query.return_value = op
        role_grant = self.ut.show_grant_role("custom_role")
        self.jdbc.query.assert_called_once_with("SHOW GRANT ROLE `custom_role`")
        expected_grants = ['prv_moe_zi20_usr', 'hdfs://elara-ha/data/prv_moe/zi20/usr']
        self.assertListEqual(expected_grants, role_grant)

    def test_show_role_grant_group(self):
        op = [('acces applicatifs rw dev_cin_zi00', False, 0, '--'),
              ('acces personnes rw dev_c00_zi00', False, 0, '--'),
              ('user_access_rw_prv_dtk_zi00_usr', False, 0, '--'),
              ('user_access_rw_prv_moe_zi11_usr', False, 0, '--'),
              ('user_access_rw_prv_moe_zi20_usr', False, 0, '--'),
              ('user_access_rw_prv_moe_zi43_usr', False, 0, '--')]
        self.jdbc.query.return_value = op
        role_grant = self.ut.show_role_grant_group("custom_group")
        self.jdbc.query.assert_called_once_with("SHOW ROLE GRANT GROUP `custom_group`")
        expected_grants = ['acces applicatifs rw dev_cin_zi00',
                           'acces personnes rw dev_c00_zi00',
                           'user_access_rw_prv_dtk_zi00_usr',
                           'user_access_rw_prv_moe_zi11_usr',
                           'user_access_rw_prv_moe_zi20_usr',
                           'user_access_rw_prv_moe_zi43_usr',
                           ]
        self.assertListEqual(expected_grants, role_grant)

    def test_create_database_without_uri(self):
        self.ut.create_database("prv_moa_zi43_usr", uri="/data/prv_moa/zi43/usr")
        self.jdbc.query.assert_has_calls([
            call('DROP DATABASE IF EXISTS prv_moa_zi43_usr CASCADE'),
            call('CREATE DATABASE `prv_moa_zi43_usr` COMMENT "DB created automatically"'
                 ' LOCATION "/data/prv_moa/zi43/usr"')])

    def test_create_database_with_comment(self):
        self.ut.create_database("prv_moa_zi43_usr", description="This is database description",
                                uri="/data/prv_moa/zi43/usr")
        self.jdbc.query.assert_has_calls([
            call('DROP DATABASE IF EXISTS prv_moa_zi43_usr CASCADE'),
            call('CREATE DATABASE `prv_moa_zi43_usr` COMMENT '
                 '"This is database description" '
                 'LOCATION "/data/prv_moa/zi43/usr"')])

    def test_create_role(self):
        self.ut.create_role("usr_role_name")
        self.jdbc.query.assert_called_once_with("CREATE ROLE `usr_role_name`")

    def test_grant_access_to_db(self):
        self.ut.grant_access_to_db("prv_moa_zi43_usr", "/data/prv_moa/zi43/usr", 'usr_role_name', 'elara')
        self.jdbc.query.assert_has_calls([
            call("GRANT ALL ON DATABASE `prv_moa_zi43_usr` TO ROLE `usr_role_name`"),
            call("GRANT ALL ON URI 'hdfs://elara-ha/data/prv_moa/zi43/usr' TO ROLE `usr_role_name`"),
        ])

    def test_grant_access_to_db_create_select(self):
        self.ut.grant_access_to_db("prv_moa_zi43_usr",
                                   "/data/prv_moa/zi43/usr",
                                   'usr_role_name',
                                   'elara',
                                   'CREATE,SELECT',
                                   )

        self.jdbc.query.assert_has_calls([
            call("GRANT CREATE,SELECT ON DATABASE `prv_moa_zi43_usr` TO ROLE `usr_role_name`"),
            call("GRANT ALL ON URI 'hdfs://elara-ha/data/prv_moa/zi43/usr' TO ROLE `usr_role_name`"),
        ])

    def test_grant_access_to_db_read_only_should_not_grant_all_on_uri(self):
        self.ut.grant_access_to_db("prv_moa_zi43_usr",
                                   "/data/prv_moa/zi43/usr",
                                   'usr_role_name',
                                   "elara",
                                   'SELECT')
        self.jdbc.query.assert_called_once_with("GRANT SELECT ON DATABASE `prv_moa_zi43_usr` TO ROLE `usr_role_name`")

    def test_add_group_to_role(self):
        self.ut.add_group_to_role(group="test_group", role="test_role")
        self.jdbc.query.assert_called_once_with("GRANT ROLE `test_role` TO GROUP `test_group`")

    def test_drop_old_role_should_not_reovke(self):
        self.ut.drop_old_role("some_old_role")
        self.jdbc.query.assert_called_once_with("DROP ROLE `some_old_role`")


class TestJdbcDriver(TestCase):
    def setUp(self) -> None:
        self.ut = JdbcDriver("some.server", port=10001, principal="hive/_HOST@some.server")

    @patch("ipaconnector.jdbc.jaydebeapi")
    def test_connect_context_manager(self, jdba):
        with self.ut:
            pass
        jdba.connect.assert_called_once_with("org.apache.hive.jdbc.HiveDriver",
                                             "jdbc:hive2://some.server:10001/default;"
                                             "principal=hive/_HOST@some.server;ssl=true")
        jdba.connect.return_value.cursor.assert_called_once_with()
        jdba.connect.return_value.cursor.return_value.close.assert_called_once_with()
        jdba.connect.return_value.close.assert_called_once_with()

    @patch("ipaconnector.jdbc.jaydebeapi")
    def test_query(self, jdba):
        jdba.connect.return_value.cursor.return_value.fetchall.return_value = [('default',), ('dev_c00_zi00_adm',)]
        with self.ut:
            output = self.ut.query("show databases")
        jdba.connect.return_value.cursor.return_value.execute.assert_called_once_with("show databases")
        jdba.connect.return_value.cursor.return_value.fetchall.assert_called_once_with()
        self.assertEqual(output, [('default',), ('dev_c00_zi00_adm',)])
