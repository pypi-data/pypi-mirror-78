import os
from unittest import TestCase
from unittest.mock import patch, call, Mock, ANY

from ipaconnector.connector import IpaConnector
from python_freeipa.exceptions import Unauthorized, DuplicateEntry, NotFound

from abc import ABC, abstractmethod

from ipaconnector.jdbc import Hive
from ipaconnector.klass import User


class FunctionalTestCase(ABC):
    def make_ut(self):
        with patch('ipaconnector.connector.ClientMeta') as self._Client_mock:
            self.ut = IpaConnector('ipa.server.net')
            self._client_mock = self._Client_mock()
            self.ut.connect(kerberos=True)

    @abstractmethod
    def test_add_users(self):
        raise NotImplementedError

    @abstractmethod
    def test_delete_users(self):
        raise NotImplementedError

    @abstractmethod
    def test_add_group(self):
        raise NotImplementedError

    @abstractmethod
    def test_group_add_member(self):
        raise NotImplementedError

    @abstractmethod
    def test_group_delete_member(self):
        raise NotImplementedError

    @abstractmethod
    def test_group_delete(self):
        raise NotImplementedError

    @abstractmethod
    def test_keytab_creations(self):
        raise NotImplementedError


class TestFunctionalCreations(FunctionalTestCase, TestCase):
    @patch("ipaconnector.connector.ELARA")
    @patch("ipaconnector.connector.Shell")
    @patch("ipaconnector.connector.SSHConn")
    @patch("ipaconnector.connector.socket")
    @patch("ipaconnector.connector.getpass")
    def setUp(self, getpass, socket, ssh, shell, cluster):
        self.jdbc_mock = Mock()
        self.hive_mock = Mock(spec_set=Hive(self.jdbc_mock))
        cluster.get_hive_interface.return_value = self.hive_mock
        cluster.HOST = "elara-edgeg-u1-n01"
        getpass.getuser.return_value = "runuser"
        socket.gethostname.return_value = "elara-edgeg-u1-n01"
        self.ssh = ssh
        self.shell = shell
        self.make_ut()
        self.ut.run(os.path.join(os.path.dirname(__file__), 'delta_test_creations.json'))

    def test_add_users(self):
        self._client_mock.user_add.assert_has_calls([
            call("user_test1", "Test1", "User", "Test1 User", o_homedirectory="/data01/user_test1/",
                 o_mail="user_test1@bouyguestelecom.fr",
                 o_gecos="FR/C//BYTEL/Test1 User", o_ou="Bouygues Telecom"),
            call("user_test2", "Test2", "User", "Test2 User", o_homedirectory="/data01/user_test2/",
                 o_mail="user_test2@bouyguestelecom.fr",
                 o_gecos="FR/C//BYTEL/Test2 User", o_ou="Bouygues Telecom"),
            call("elaint_test1", "Application", "elaint_test1", "Application elaint_test1",
                 o_homedirectory="/data01/elaint_test1/",
                 o_mail="", o_gecos="FR/C//BYTEL/Test app user 1", o_ou="Bouygues Telecom"),
            call("elaint_test2", "Application", "elaint_test2", "Application elaint_test2",
                 o_homedirectory="/data01/elaint_test2/",
                 o_mail="", o_gecos="FR/C//BYTEL/Test app user 2", o_ou="Bouygues Telecom"),
        ])

    def test_delete_users(self):
        self._client_mock.user_del.assert_not_called()

    def test_add_group(self):
        self._client_mock.group_add.assert_has_calls([
            call('user_test1', o_description="Singleton associé à user_test1"),
            call('user_test2', o_description="Singleton associé à user_test2"),
            call('group_test1', o_description="Test group 1"),
            call('app_elaint_test', o_description="Test app user group"),
            call('elaint_test1',
                 o_description="Groupe singleton associé au compte applicatif elaint_test1"),
            call('elaint_test2',
                 o_description="Groupe singleton associé au compte applicatif elaint_test2"),
        ], any_order=True)

    def test_group_add_member(self):
        self._client_mock.group_add_member.assert_has_calls([
            call(a_cn='user_test1', o_user='user_test1'),
            call(a_cn='user_test2', o_user='user_test2'),
            call(a_cn='group_test1', o_user='user_test1'),
            call(a_cn='app_elaint_test', o_user='elaint_test1'),
            call(a_cn='app_elaint_test', o_user='elaint_test2'),
            call(a_cn='group_test1', o_user='user_test2'),
            call(a_cn='dss_user', o_user='user_test2'),
            call(a_cn='elaint_test1', o_user='elaint_test1'),
            call(a_cn='elaint_test2', o_user='elaint_test2'),
        ], any_order=True)

    def test_group_delete_member(self):
        self._client_mock.group_member_del.assert_not_called()

    def test_group_delete(self):
        self._client_mock.group_del.assert_not_called()

    def test_keytab_creations(self):
        self.shell.assert_called_once_with(user="runuser")
        self.shell.return_value.kinit.assert_called_once_with()
        expected_cmd = [
            'ipa service-add user_test1/$(hostname -f)',
            'ipa-getkeytab -p user_test1/$(hostname -f) -k user_test1.keytab',
            'sudo chown user_test1. user_test1.keytab',
            'sudo mkhomedir_helper user_test1 0027',
            'sudo mv user_test1.keytab /data01/user_test1/'
        ]
        self.shell.return_value.execute.assert_called_once_with(cmd_list=expected_cmd)

    def test_hive_dbs(self):
        self.hive_mock.create_database.assert_has_calls([
            call('dev_zi00_adm', description='Dev test base for automation', uri='/data/dev/zi00/adm'),
            call('dev_zi00_source', description='Dev test base for automation', uri='/data/dev/zi00/source'),
            call('dev_zi00_trv', description='Dev test base for automation', uri='/data/dev/zi00/trv'),
            call('dev_zi00_socle', description='Dev test base for automation', uri='/data/dev/zi00/socle'),
            call('dev_zi00_metier', description='Dev test base for automation', uri='/data/dev/zi00/metier'),
            call('dev_zi00_extr', description='Dev test base for automation', uri='/data/dev/zi00/extr'),
            call('prv_tes_zi00_usr', description="Données nécessaires aux cas d'usages métiers",
                 uri='/data/prv_tes/zi00/usr'),
            call('prv_tes_zi01_usr', description="Données nécessaires aux cas d'usages métiers",
                 uri='/data/prv_tes/zi01/usr'),
            call('dev_c00_zi03_adm', description="Données nécessaires aux cas d'usages métiers",
                 uri='/data/dev_c00/zi03/adm'),
            call('dev_c00_zi03_source', description="Données nécessaires aux cas d'usages métiers",
                 uri='/data/dev_c00/zi03/source'),
            call('dev_c00_zi03_trv', description="Données nécessaires aux cas d'usages métiers",
                 uri='/data/dev_c00/zi03/trv'),
            call('dev_c00_zi03_socle', description="Données nécessaires aux cas d'usages métiers",
                 uri='/data/dev_c00/zi03/socle'),
            call('dev_c00_zi03_metier', description="Données nécessaires aux cas d'usages métiers",
                 uri='/data/dev_c00/zi03/metier'),
            call('dev_c00_zi03_extr', description="Données nécessaires aux cas d'usages métiers",
                 uri='/data/dev_c00/zi03/extr')
        ])


class TestFunctionalUpdates(FunctionalTestCase, TestCase):
    @patch("ipaconnector.connector.ELARA")
    @patch("ipaconnector.connector.Shell")
    @patch("ipaconnector.connector.SSHConn")
    @patch("ipaconnector.connector.socket")
    @patch("ipaconnector.connector.getpass")
    def setUp(self, getpass, socket, ssh, shell, cluster):
        self.jdbc_mock = Mock()
        self.hive_mock = Mock(spec_set=Hive(self.jdbc_mock))
        cluster.get_hive_interface.return_value = self.hive_mock
        cluster.HOST = "elara-edgeg-u1-n01"
        getpass.getuser.return_value = "runuser"
        socket.gethostname.return_value = "elara-edgeg-u1-n01"
        self.ssh = ssh
        self.shell = shell
        self.make_ut()
        self.ut.run(os.path.join(os.path.dirname(__file__), 'delta_test_updates.json'))

    def test_add_users(self):
        self._client_mock.user_add.assert_not_called()

    def test_delete_users(self):
        self._client_mock.user_del.assert_not_called()

    def test_add_group(self):
        self._client_mock.group_add.assert_not_called()

    def test_group_add_member(self):
        actual_call_list = self._client_mock.group_add_member._mock_call_args_list
        self.assertIn(call(a_cn='user_test1', o_user='elaint_test1'), actual_call_list)
        self.assertIn(call(a_cn='user_test1', o_user='elaint_test1'), actual_call_list)
        self.assertIn(call(a_cn='user_test1', o_user='elaint_test1'), actual_call_list)
        self.assertIn(call(a_cn='DSI_GDA_BIGDATA_MOE_PREPROD',
                           o_user='elaint_test1'), actual_call_list)
        self.assertIn(call(a_cn='DSI_GDA_BIGDATA_MOE_PREPROD',
                           o_user='elaint_test1'), actual_call_list)
        self.assertIn(call(a_cn='elaint_test1', o_user='elaint_test1'), actual_call_list)
        self.assertIn(call(a_cn='dss_user', o_user='user_test1'), actual_call_list)
        # ], any_order=True)

    def test_group_delete_member(self):
        actual_call_list = self._client_mock.group_remove_member._mock_call_args_list
        self.assertIn(call(a_cn='app_elaint_test', o_user='elaint_test1'), actual_call_list)
        self.assertIn(call(a_cn='app_elaint_test', o_user='elaint_test1'), actual_call_list)
        self.assertIn(call(a_cn='group_test1', o_user='elaint_test1'), actual_call_list)
        self.assertIn(call(a_cn='app_elaint_test', o_user='elaint_test1'), actual_call_list)
        self.assertIn(call(a_cn='group_test1', o_user='elaint_test1'), actual_call_list)
        self.assertIn(call(a_cn='DSI_GDA_BIGDATA_MOE_DEV', o_user='elaint_test1'), actual_call_list)
        self.assertIn(call(a_cn='DSI_GDA_BIGDATA_MOE_DEV', o_user='elaint_test1'), actual_call_list)
        self.assertIn(call(a_cn='dss_user', o_user='user_test2'), actual_call_list)
        self.assertIn(call(a_cn='group_test1', o_user='user_test2'), actual_call_list)

    def test_group_delete(self):
        self._client_mock.group_del.assert_not_called()

    def test_keytab_creations(self):
        self.shell.assert_called_once_with(user="runuser")
        self.shell.return_value.kinit.assert_called_once_with()
        expected_cmd = [
            'ipa service-add user_test2/$(hostname -f)',
            'ipa-getkeytab -p user_test2/$(hostname -f) -k user_test2.keytab',
            'sudo chown user_test2. user_test2.keytab',
            'sudo mkhomedir_helper user_test2 0027',
            'sudo mv user_test2.keytab /data01/user_test2/'
        ]
        self.shell.return_value.execute.assert_called_once_with(cmd_list=expected_cmd)


class TestFunctionalDeletions(FunctionalTestCase, TestCase):
    @patch("ipaconnector.connector.ELARA")
    @patch("ipaconnector.connector.Shell")
    @patch("ipaconnector.connector.SSHConn")
    @patch("ipaconnector.connector.socket")
    @patch("ipaconnector.connector.getpass")
    def setUp(self, getpass, socket, ssh, shell, cluster):
        self.jdbc_mock = Mock()
        self.hive_mock = Mock(spec_set=Hive(self.jdbc_mock))
        cluster.get_hive_interface.return_value = self.hive_mock
        cluster.HOST = "elara-edgeg-u1-n01"
        getpass.getuser.return_value = "runuser"
        socket.gethostname.return_value = "elara-edgeg-u1-n01"
        self.make_ut()
        self.ut.run(os.path.join(os.path.dirname(__file__), 'delta_test_deletions.json'))

    def test_add_users(self):
        self._client_mock.user_add.assert_not_called()

    def test_delete_users(self):
        self._client_mock.user_del.assert_has_calls([
            call('user_test1'),
            call('user_test2'),
            call('elaint_test1'),
            call('elaint_test2'),
        ], any_order=True)

    def test_add_group(self):
        self._client_mock.group_add.assert_not_called()

    def test_group_add_member(self):
        self._client_mock.group_add_member.assert_not_called()

    def test_group_delete_member(self):
        self._client_mock.group_remove_member.assert_has_calls([
            call(a_cn='dss_user', o_user='user_test1')
        ])

    def test_group_delete(self):
        self._client_mock.group_del.assert_has_calls([
            call('app_elaint_test'),
            call('elaint_test1'),
            call('elaint_test2'),
            call('user_test1'),
            call('user_test2'),
            call('group_test1'),
        ], any_order=True)

    def test_keytab_creations(self):
        pass


class TestFunctionalFgase(FunctionalTestCase, TestCase):
    @patch("ipaconnector.connector.CALLISTO")
    @patch("ipaconnector.connector.ELARA")
    @patch("ipaconnector.connector.Shell")
    @patch("ipaconnector.connector.SSHConn")
    @patch("ipaconnector.connector.socket")
    @patch("ipaconnector.connector.getpass")
    def setUp(self, getpass, socket, ssh, shell, elara, callisto):
        self.jdbc_mock = Mock()
        self.hive_mock_elara = Mock(spec_set=Hive(self.jdbc_mock))
        self.hive_mock_callisto = Mock(spec_set=Hive(self.jdbc_mock))
        callisto.get_hive_interface.return_value = self.hive_mock_callisto
        elara.get_hive_interface.return_value = self.hive_mock_elara
        elara.HOST = "elara-edgeg-u1-n01"
        callisto.HOST = "callisto-edgeg-u1-n01"
        getpass.getuser.return_value = "runuser"
        socket.gethostname.return_value = "elara-edgeg-u1-n01"
        self.ssh = ssh
        self.shell = shell
        self.make_ut()
        self.ut.run(os.path.join(os.path.dirname(__file__), 'fgase.json'))

    def test_add_users(self):
        self._client_mock.user_add.assert_has_calls([
            call("fgase", "Florent", "GASE", "Florent GASE", o_homedirectory="/data01/fgase/",
                 o_mail="fgase@bouyguestelecom.fr",
                 o_gecos="FR/C//BYTEL/Florent GASE", o_ou="Bouygues Telecom"),

        ])

    def test_delete_users(self):
        self._client_mock.user_del.assert_not_called()

    def test_add_group(self):
        self._client_mock.group_add.assert_has_calls([
            call('fgase', o_description="Singleton associé à fgase"),
        ], any_order=True)

    def test_group_add_member(self):
        self._client_mock.group_add_member.assert_has_calls([
            call(a_cn='fgase', o_user='fgase'),
            call(a_cn='moe_signaletique', o_user='fgase')
        ], any_order=True)

    def test_group_delete_member(self):
        self._client_mock.group_member_del.assert_not_called()

    def test_group_delete(self):
        self._client_mock.group_del.assert_not_called()

    def test_keytab_creations(self):
        self.shell.assert_called_once_with(user="runuser")
        self.shell.return_value.kinit.assert_called_once_with()
        expected_cmd = [
            'ipa service-add fgase/$(hostname -f)',
            'ipa-getkeytab -p fgase/$(hostname -f) -k fgase.keytab',
            'sudo chown fgase. fgase.keytab',
            'sudo mkhomedir_helper fgase 0027',
            'sudo mv fgase.keytab /data01/fgase/'
        ]
        self.shell.return_value.execute.assert_called_once_with(cmd_list=expected_cmd)

    def test_hive_dbs(self):
        self.hive_mock_elara.create_database.assert_called()
        self.hive_mock_callisto.create_database.assert_not_called()
        print(self.jdbc_mock.__dict__)


class TestFunctionalFgaseCallisto(FunctionalTestCase, TestCase):
    def make_ut(self):
        with patch("ipaconnector.connector.socket.gethostname") as gethostname:
            with patch('ipaconnector.connector.ClientMeta') as self._Client_mock:
                gethostname.return_value = 'callisto-edgeg-u1-n01'
                self.ut = IpaConnector('ipa.server.net')
                self._client_mock = self._Client_mock()
                self.ut.connect(kerberos=True)

    @patch("ipaconnector.connector.CALLISTO")
    @patch("ipaconnector.connector.ELARA")
    @patch("ipaconnector.connector.Shell")
    @patch("ipaconnector.connector.SSHConn")
    @patch("ipaconnector.connector.socket")
    @patch("ipaconnector.connector.getpass")
    def setUp(self, getpass, socket, ssh, shell, elara, callisto):
        self.jdbc_mock = Mock()
        self.hive_mock_elara = Mock(spec_set=Hive(self.jdbc_mock))
        self.hive_mock_callisto = Mock(spec_set=Hive(self.jdbc_mock))
        callisto.get_hive_interface.return_value = self.hive_mock_callisto
        elara.get_hive_interface.return_value = self.hive_mock_elara
        callisto.HOST = 'callisto-edgeg-u1-n01'
        getpass.getuser.return_value = "runuser"
        socket.gethostname.return_value = 'callisto-edgeg-u1-n01'
        self.ssh = ssh
        self.shell = shell
        self.make_ut()
        self.ut.run(os.path.join(os.path.dirname(__file__), 'fgase.json'))

    def test_add_users(self):
        self._client_mock.user_add.assert_has_calls([
            call("fgase", "Florent", "GASE", "Florent GASE", o_homedirectory="/data01/fgase/",
                 o_mail="fgase@bouyguestelecom.fr",
                 o_gecos="FR/C//BYTEL/Florent GASE", o_ou="Bouygues Telecom"),

        ])

    def test_delete_users(self):
        self._client_mock.user_del.assert_not_called()

    def test_add_group(self):
        self._client_mock.group_add.assert_has_calls([
            call('fgase', o_description="Singleton associé à fgase"),
        ], any_order=True)

    def test_group_add_member(self):
        self._client_mock.group_add_member.assert_has_calls([
            call(a_cn='fgase', o_user='fgase'),
            call(a_cn='moe_signaletique', o_user='fgase')
        ], any_order=True)

    def test_group_delete_member(self):
        self._client_mock.group_member_del.assert_not_called()

    def test_group_delete(self):
        self._client_mock.group_del.assert_not_called()

    def test_keytab_creations(self):
        self.shell.assert_called_once_with(user="runuser")
        self.shell.return_value.kinit.assert_called_once_with()
        expected_cmd = [
            'ipa service-add fgase/$(hostname -f)',
            'ipa-getkeytab -p fgase/$(hostname -f) -k fgase.keytab',
            'sudo chown fgase. fgase.keytab',
            'sudo mkhomedir_helper fgase 0027',
            'sudo mv fgase.keytab /data01/fgase/'
        ]
        self.shell.return_value.execute.assert_called_once_with(cmd_list=expected_cmd)

    def test_hive_dbs(self):
        self.hive_mock_elara.create_database.assert_not_called()
        self.hive_mock_callisto.create_database.assert_called()


class TestFunctional(TestCase):
    def setUp(self):
        self.sample = os.path.join(os.path.dirname(__file__), 'sample.json')
        with patch('ipaconnector.connector.ClientMeta') as self._Client_mock:
            self.ut = IpaConnector('ipa.server.net')
            self._client_mock = self._Client_mock()
            self.ut.connect(kerberos=True)

    @patch("ipaconnector.connector.Shell")
    @patch("ipaconnector.connector.SSHConn")
    @patch("ipaconnector.connector.socket")
    @patch("ipaconnector.connector.getpass")
    def test_case_sample_two(self, getpass, socket, ssh, shell):
        getpass.getuser.return_value = "runuser"
        socket.gethostname.return_value = "elara-edgeg-u1-n01"
        self.ut.run(os.path.join(os.path.dirname(__file__), 'sample_two.json'))
        self._client_mock.user_add.assert_called_once_with('user_one',
                                                           'user_one',
                                                           'user_one_name',
                                                           'user_one user_one_name',
                                                           o_gecos='FR/C//BYTEL/user_one user_one_name',
                                                           o_homedirectory='/data01/user_one/',
                                                           o_mail='some@mail.com',
                                                           o_ou='company_one')
        self._client_mock.user_del.assert_not_called()
        self._client_mock.group_add.assert_not_called()
        self._client_mock.group_del.assert_not_called()
        self._client_mock.group_member_add.assert_not_called()
        self._client_mock.group_member_del.assert_not_called()

    def test_case_sample_three(self):
        self.ut.run(os.path.join(os.path.dirname(__file__), 'sample_three.json'))
        self._client_mock.user_add.assert_not_called()
        self._client_mock.user_del.assert_called_once_with('user_one')
        self._client_mock.group_add.assert_not_called()
        self._client_mock.group_del.assert_not_called()
        self._client_mock.group_member_add.assert_not_called()
        self._client_mock.group_member_del.assert_not_called()


class TestIpaConnector(TestCase):
    def setUp(self):

        self.sample = os.path.join(os.path.dirname(__file__), 'sample.json')
        with patch('ipaconnector.connector.ClientMeta') as self._Client_mock:
            self.ut = IpaConnector('ipa.server.net')
            self._client_mock = self._Client_mock()

    @patch('ipaconnector.connector.ClientMeta')
    def test_init(self, client):
        ut = IpaConnector('ipa.server.net')
        ut.connect(kerberos=True)
        client.return_value.login_kerberos.assert_called_once_with()

    @patch('ipaconnector.connector.ClientMeta')
    @patch('ipaconnector.connector.Kerberos')
    @patch('ipaconnector.sshwrapper.subprocess')
    @patch('ipaconnector.connector.getpass')
    def test_keytab_creations_local(self, gp, sp, krb, client):
        gp.getuser.return_value = "runuser"
        mockuser = Mock(spec=User)
        mockuser.login = "test"
        self.ut._keytab_creations = [mockuser]

        with patch("ipaconnector.connector.socket") as socket:
            socket.gethostname.return_value = "elara-edgeg-u1-n01"
            self.ut.create_keytabs()
        sp.run.assert_has_calls([
            call("kinit -kt /home/runuser/runuser.keytab runuser/$(hostname -f)",
                 shell=True, stdout=ANY),
            call("ipa service-add test/$(hostname -f)", shell=True, stdout=ANY),
            ANY,  # call().stdout.__str__(),
            call("ipa-getkeytab -p test/$(hostname -f) -k test.keytab", shell=True, stdout=ANY),
            ANY,
            call("sudo chown test. test.keytab", shell=True, stdout=ANY),
            ANY,
            call("sudo mkhomedir_helper test 0027", shell=True, stdout=ANY),
            ANY,
            call("sudo mv test.keytab /data01/test/", shell=True, stdout=ANY),
            ANY,
        ])

    @patch('ipaconnector.connector.ClientMeta')
    @patch('ipaconnector.connector.Kerberos')
    def test_init_without_tgt_should_kinit_and_retry(self, krb, client):
        client.return_value.login_kerberos.side_effect = Unauthorized, None
        ut = IpaConnector('ipa.server.net')
        ut.connect(kerberos=True)
        krb.return_value.acquire_tgt.assert_called_once_with()
        client.return_value.assert_has_calls([call.login_kerberos(),
                                              call.login_kerberos()])

    @patch('ipaconnector.connector.ClientMeta')
    @patch('ipaconnector.connector.Kerberos')
    def test_init_without_tgt_kinit_fails_should_raise_error(self, krb, client):
        client.return_value.login_kerberos.side_effect = Unauthorized
        with self.assertRaises(Unauthorized):
            ut = IpaConnector('ipa.server.net')
            ut.connect(kerberos=True)

    @patch('ipaconnector.connector.ClientMeta')
    def test_init_login_with_creds(self, client):
        ut = IpaConnector('ipa.server.net')
        ut.connect("user", "password")
        client.return_value.login.assert_called_once_with('user', 'password')
        client.return_value.login_kerberos.assert_not_called()

    @patch('ipaconnector.connector.ClientMeta')
    def test_init_login_with_kerberos(self, client):
        ut = IpaConnector('ipa.server.net')
        ut.connect(kerberos=True)
        client.return_value.login_kerberos.assert_called_once_with()
        client.return_value.login.assert_not_called()

    def test_read_data_should_return_three_tuples_of_lists(self):
        to_add, to_update, to_delete = self.ut.read_input(self.sample)
        self.assertTrue(list, type(to_add))
        self.assertTrue(list, type(to_update))
        self.assertTrue(list, type(to_delete))

    def test_read_data_should_not_be_empty(self):
        to_add, to_update, to_delete = self.ut.read_input(self.sample)
        self.assertFalse(0, len(to_add))
        self.assertFalse(0, len(to_update))
        self.assertFalse(0, len(to_delete))

    def test_read_data_to_add_if_data_correct_with_sample_json(self):
        to_add, _, _ = self.ut.read_input(self.sample)
        self.assertEqual(to_add['HumanUser'][0]['primaryKey']['login'], 'jdoe')

    @patch("ipaconnector.connector.ELARA")
    def test_sample_add_user(self, cluster):
        hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = hive_mock
        to_add, _, _ = self.ut.read_input(self.sample)
        self.ut.to_add = to_add
        self.ut.make_add()
        self._client_mock.user_add.assert_called_once_with(
            "jdoe",
            "John",
            "Doe",
            "John Doe",
            o_homedirectory="/data01/jdoe/",
            o_mail="jdoe@companyone.xyz",
            o_gecos="FR/C//BYTEL/John Doe",
            o_ou="company one")

    @patch("ipaconnector.connector.ELARA")
    def test_sample_add_two_users(self, cluster):
        hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = hive_mock
        new_user = {
            "firstname": {"newValue": "new"},
            "name": {"newValue": "user"},
            "keytab": {"newValue": "true"},
            "company": {"newValue": "company one"},
            "team": {"newValue": "oem"},
            "login": {"newValue": "newuser"},
            "email": {"newValue": "new@user.com"},
            "primaryKey": {"login": "newuser"}}
        to_add, _, _ = self.ut.read_input(self.sample)
        to_add['HumanUser'].append(new_user)
        self.ut.to_add = to_add
        self.ut.make_add()
        self._client_mock.user_add.assert_has_calls([call(
            "jdoe",
            "John",
            "Doe",
            "John Doe",
            o_homedirectory="/data01/jdoe/",
            o_mail="jdoe@companyone.xyz",
            o_gecos="FR/C//BYTEL/John Doe",
            o_ou="company one"),
            call(
                "newuser",
                "new",
                "user",
                "new user",
                o_homedirectory="/data01/newuser/",
                o_mail="new@user.com",
                o_gecos="FR/C//BYTEL/new user",
                o_ou="company one")
        ])

    def test_add_no_users_to_add_should_do_nothing(self):
        self.ut.to_add = {}
        self.ut.make_add()
        self._client_mock.user_add.assert_not_called()

    @patch("ipaconnector.connector.ELARA")
    def test_sample_add_two_users_first_exists_should_continue(self, cluster):
        hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = hive_mock

        new_user = {
            "firstname": {"newValue": "new"},
            "name": {"newValue": "user"},
            "keytab": {"newValue": "true"},
            "company": {"newValue": "company one"},
            "team": {"newValue": "oem"},
            "login": {"newValue": "newuser"},
            "email": {"newValue": "new@user.com"},
            "primaryKey": {"login": "newuser"}}
        to_add, _, _ = self.ut.read_input(self.sample)
        to_add['HumanUser'].append(new_user)
        self._client_mock.user_add.side_effect = DuplicateEntry, Mock()
        self.ut.to_add = to_add
        self.ut.make_add()
        self._client_mock.user_add.assert_has_calls([call(
            "jdoe",
            "John",
            "Doe",
            "John Doe",
            o_homedirectory="/data01/jdoe/",
            o_mail="jdoe@companyone.xyz",
            o_gecos="FR/C//BYTEL/John Doe",
            o_ou="company one"),
            call(
                "newuser",
                "new",
                "user",
                "new user",
                o_homedirectory="/data01/newuser/",
                o_mail="new@user.com",
                o_gecos="FR/C//BYTEL/new user",
                o_ou="company one")
        ])

    def test_delete_one_user_only_login_provided(self):
        _, _, to_delete = self.ut.read_input(self.sample)
        self.ut.to_delete = to_delete
        self.ut.make_delete()
        self._client_mock.user_del.assert_called_once_with("deleteThisUser")

    def test_delete_nothing_to_delete_should_do_nothing(self):
        self.ut.to_delete = {}
        self.ut.make_delete()
        self._client_mock.user_del.assert_not_called()

    @patch("ipaconnector.connector.ELARA")
    def test_delete_should_delete_user_and_group(self, cluster):
        hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = hive_mock
        _, _, to_delete = self.ut.read_input(self.sample)
        self.ut.to_delete = to_delete
        self.ut.make_delete()
        self._client_mock.user_del.assert_called_once_with("deleteThisUser")
        self._client_mock.group_del.assert_called_once_with("group_delete")

    @patch("ipaconnector.connector.ELARA")
    def test_delete_two_users_only_login_provided(self, cluster):
        hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = hive_mock
        _, _, to_delete = self.ut.read_input(self.sample)
        new_user = {"login": {"newValue": "anotherDeleteUser"}}
        to_delete['HumanUser'].append(new_user)
        self.ut.to_delete = to_delete
        self.ut.make_delete()
        self._client_mock.user_del.assert_has_calls([call("deleteThisUser"),
                                                     call("anotherDeleteUser")])

    @patch("ipaconnector.connector.ELARA")
    def test_delete_no_users_to_delete_should_do_nothing(self, cluster):
        hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = hive_mock
        self.ut.to_delete = {}
        self.ut.make_delete()
        self._client_mock.user_del.assert_not_called()

    @patch("ipaconnector.connector.ELARA")
    def test_sample_add_no_users_to_add(self, cluster):
        hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = hive_mock
        to_add, _, _ = self.ut.read_input(self.sample)
        to_add['HumanUser'] = []
        self.ut.to_add = to_add
        self.ut.make_add()
        self._client_mock.user_add.assert_not_called()

    @patch("ipaconnector.connector.ELARA")
    def test_sample_add_no_group_to_add(self, cluster):
        hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = hive_mock
        to_add, _, _ = self.ut.read_input(self.sample)
        to_add['UserGroup'] = []
        self.ut.to_add = to_add
        self.ut.make_add()
        self._client_mock.group_add.assert_not_called()

    @patch("ipaconnector.connector.ELARA")
    def test_sample_add_should_add_one_group_and_one_member(self, cluster):
        hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = hive_mock
        to_add, _, _ = self.ut.read_input(self.sample)
        self.ut.to_add = to_add
        self.ut.make_add()
        self._client_mock.group_add.assert_called_once_with('TestGroup',
                                                            o_description="Description of TestGroup")
        self._client_mock.group_add_member.assert_called_once_with(a_cn='TestGroup',
                                                                   o_user='testUser')

    @patch("ipaconnector.connector.ELARA")
    def test_sample_add_should_add_two_groups_multiple_members(self, cluster):
        hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = hive_mock
        to_add, _, _ = self.ut.read_input(self.sample)
        new_group = {
            "members": {"add": ['user1', 'user2']},
            "name": {"newValue": "newGroup"},
            "description": {"newValue": "description of newGroup"}
        }
        to_add['UserGroup'].append(new_group)
        self.ut.to_add = to_add
        self.ut.make_add()
        self._client_mock.group_add.assert_has_calls([
            call('TestGroup', o_description="Description of TestGroup"),
            call('newGroup', o_description="description of newGroup")
        ])

        self._client_mock.group_add_member.assert_has_calls([
            call(a_cn='TestGroup', o_user='testUser'),
            call(a_cn='newGroup', o_user='user1'),
            call(a_cn='newGroup', o_user='user2')])

    @patch("ipaconnector.connector.ELARA")
    def test_sample_add_should_add_two_groups_without_members(self, cluster):
        hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = hive_mock
        to_add, _, _ = self.ut.read_input(self.sample)
        new_group = {
            "members": {"add": []},
            "name": {"newValue": "newGroup"},
            "description": {"newValue": "description of newGroup"}
        }
        to_add['UserGroup'] = [new_group]
        self.ut.to_add = to_add
        self.ut.make_add()
        self._client_mock.group_add.assert_called_once_with('newGroup',
                                                            o_description="description of newGroup")
        self._client_mock.group_add_member.assert_not_called()

    @patch("ipaconnector.connector.ELARA")
    def test_sample_add_should_add_two_groups_without_members_defined(self, cluster):
        hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = hive_mock
        to_add, _, _ = self.ut.read_input(self.sample)
        new_group = {
            "name": {"newValue": "newGroup"},
            "description": {"newValue": "description of newGroup"}
        }
        to_add['UserGroup'] = [new_group]
        self.ut.to_add = to_add
        self.ut.make_add()
        self._client_mock.group_add.assert_called_once_with('newGroup',
                                                            o_description="description of newGroup")
        self._client_mock.group_add_member.assert_not_called()

    @patch("ipaconnector.connector.ELARA")
    def test_update_user_group_add_new_members(self, cluster):
        hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = hive_mock
        _, to_update, _ = self.ut.read_input(self.sample)
        print(to_update)
        self.ut.to_update = to_update
        self.ut.make_update()
        self._client_mock.group_add.assert_not_called()
        self._client_mock.group_add_member.assert_called_once_with(a_cn='dss_user',
                                                                   o_user='newuser')

    @patch("ipaconnector.connector.ELARA")
    def test_update_user_group__two_groups_first_non_exists_should_continue(self, cluster):
        hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = hive_mock
        _, to_update, _ = self.ut.read_input(self.sample)
        self._client_mock.group_add_member.side_effect = NotFound, None
        new = {'members': {'add': ['newuser'], 'remove': []}, 'primaryKey': {'name': 'nogroup'}}
        to_update['UserGroup'].insert(0, new)
        self.ut.to_update = to_update
        self.ut.make_update()
        self._client_mock.group_add.assert_not_called()
        self._client_mock.group_add_member.assert_has_calls([
            call(a_cn='nogroup', o_user='newuser'),
            call(a_cn='dss_user', o_user='newuser')])

    @patch("ipaconnector.connector.ELARA")
    def test_update_user_group_remove_two_members_add_one(self, cluster):
        hive_mock = Mock(spec_set=Hive(Mock()))
        cluster.get_hive_interface.return_value = hive_mock
        _, to_update, _ = self.ut.read_input(self.sample)
        to_update['UserGroup'][0]['members']['remove'] = ['removeUser1', 'removeUser2']
        self.ut.to_update = to_update
        self.ut.make_update()
        self._client_mock.group_add.assert_not_called()
        self._client_mock.group_add_member.assert_called_once_with(a_cn='dss_user',
                                                                   o_user='newuser')
        self._client_mock.group_remove_member.assert_has_calls([
            call(a_cn='dss_user', o_user='removeUser1'),
            call(a_cn='dss_user', o_user='removeUser2')])
