from unittest.mock import Mock, patch, call
from unittest import TestCase

from ipaconnector.sshwrapper import SSHConn


class TestSSHConn(TestCase):
    def setUp(self) -> None:
        self.ut = SSHConn("192.168.1.1", 'user', 'password')

    @patch("ipaconnector.sshwrapper.paramiko")
    def test_context_manager(self, paramiko):
        ssh_client = paramiko.SSHClient.return_value
        with self.ut as xd:
            pass
        ssh_client.connect.assert_called_once_with('192.168.1.1',
                                                   username='user',
                                                   password='password')
        ssh_client.close.assert_called_once_with()

    @patch("ipaconnector.sshwrapper.paramiko")
    def test_single_cmd(self, paramiko):
        ssh_client = paramiko.SSHClient.return_value
        stdout_mock = Mock()
        stdout_mock.readlines.return_value = "listofiles"
        ssh_client.exec_command.return_value = [Mock(), stdout_mock, Mock()]
        with self.ut as xd:
            output = self.ut.execute("ls -l")
        ssh_client.connect.assert_called_once_with('192.168.1.1',
                                                   username='user',
                                                   password='password')
        ssh_client.exec_command.assert_called_once_with('ls -l')
        ssh_client.close.assert_called_once_with()
        self.assertEqual(output, ["listofiles"])

    @patch("ipaconnector.sshwrapper.paramiko")
    def test_multiple_cmd(self, paramiko):
        ssh_client = paramiko.SSHClient.return_value
        stdout_mock = Mock()
        stdout_mock.readlines.side_effect = ["listofiles", "othercmd"]
        ssh_client.exec_command.return_value = [Mock(), stdout_mock, Mock()]
        with self.ut:
            output = self.ut.execute(cmd_list=["ls -l", "rm -rf"])
        ssh_client.connect.assert_called_once_with('192.168.1.1',
                                                   username='user',
                                                   password='password')
        ssh_client.exec_command.assert_has_calls([
            call('ls -l'),
            call('rm -rf'),
        ])
        ssh_client.close.assert_called_once_with()
        self.assertEqual(output, ["listofiles", "othercmd"])
