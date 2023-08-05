import subprocess
import paramiko

from ipaconnector.constans import ELARA
from ipaconnector.klass import LoggingClass


class Shell(LoggingClass):
    def __init__(self, server='localhost', user=None):
        self.server = server
        self.user = user

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def kinit(self, keytab_path=None, cluster=ELARA):
        """
        :param cluster: CLuster
        :param str keytab_path: path to keytab file. Default /home/<user>/<user>.keytab.
        """
        if not keytab_path:
            keytab_path = f"/home/{self.user}/{self.user}.keytab"
        self._cmd_exec(f"kinit -kt {keytab_path} {self.user}/{cluster.DOMAIN}")

    def execute(self, cmd=None, cmd_list=None):
        """
        :param cmd: str Command to execute
        :param cmd_list: List of commands to execute
        :return: response as list
        """
        to_exec = []
        output = []
        if cmd:
            to_exec.append(cmd)
        if cmd_list:
            to_exec.extend(cmd_list)
        for cmd in to_exec:
            self._log.debug(f"[{self.server}] SSH CMD: {cmd}")
            _cmd_output = self._cmd_exec(cmd)
            self._log.debug(f"[{self.server}] OUTPUT: {_cmd_output}")
            output.append(_cmd_output)
        return output

    def _cmd_exec(self, cmd):
        self._log.debug(cmd)
        output = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
        return output.stdout


class SSHConn(Shell, LoggingClass):
    def __init__(self, server, user, passwd):
        super(SSHConn, self).__init__(server, user)
        self.passwd = passwd
        self._connection = None

    def _cmd_exec(self, cmd):
        stdin, stdout, stderr = self._connection.exec_command(cmd)
        stdout.channel.recv_exit_status()
        response = stdout.readlines()
        return response

    def __enter__(self):
        self._log.info(f"SSH connect to {self.user}@{self.server}")
        self._connection = client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.server, username=self.user, password=self.passwd)
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._log.info(f"Disconnecting from {self.server}")
        self._connection.close()
        self._connection = None
