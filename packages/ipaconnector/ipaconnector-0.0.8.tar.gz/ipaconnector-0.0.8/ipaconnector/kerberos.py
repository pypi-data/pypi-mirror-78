import subprocess
import ipaconnector.config as config


class Kerberos:
    def __init__(self):
        self._init_command = f"kinit -kt {config.keytab_path} {config.user}/{config.hostname}".split()

    def acquire_tgt(self):
        """
        Renew TGT ticket by kinit command
        """
        process = subprocess.Popen(self._init_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if err:
            raise RuntimeError(err)
