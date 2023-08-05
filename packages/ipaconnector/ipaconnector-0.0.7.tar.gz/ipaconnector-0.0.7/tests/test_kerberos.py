from ipaconnector.kerberos import Kerberos
from unittest import TestCase
from unittest.mock import Mock, patch


class TestKerberos(TestCase):
    def setUp(self):
        self.ut = Kerberos()

    @patch('ipaconnector.kerberos.subprocess')
    def test_acquire_success(self, sp):
        process_mock = Mock()
        process_mock.communicate.return_value = (None, None)
        sp.Popen.return_value = process_mock
        self.ut.acquire_tgt()
        sp.Popen.assert_called_once_with("kinit -kt /path/to/kt.keytab connector/some.hostname".split(),
                                         stdout=sp.PIPE, stderr=sp.PIPE)

    @patch('ipaconnector.kerberos.subprocess')
    def test_acquire_success_failure_should_raise_error(self, sp):
        process_mock = Mock()
        process_mock.communicate.return_value = (None, "some error")
        sp.Popen.return_value = process_mock
        with self.assertRaisesRegex(RuntimeError, "some error"):
            self.ut.acquire_tgt()
        sp.Popen.assert_called_once_with("kinit -kt /path/to/kt.keytab connector/some.hostname".split(),
                                         stdout=sp.PIPE, stderr=sp.PIPE)
