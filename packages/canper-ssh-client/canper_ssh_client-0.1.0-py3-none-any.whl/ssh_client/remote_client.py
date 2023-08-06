"""Client to handle connections and actions executed against a remote host."""
import logging
from os import system

from paramiko import SSHClient, AutoAddPolicy, RSAKey, SFTPClient, Transport
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException




class RemoteClient:
    """Client to interact with a remote host via SSH & SCP."""

    def __init__(self, host, user, password):
    # def __init__(self, host, user, password, remote_path):
        self.host = host
        self.user = user
        self.password = password
        self.client = None  # connection objection
        self.scp = None  #  handles connections for transferring files
        self.conn = None

    def connect(self):
        """Open connection to remote host."""
        if self.conn is None:
            try:
                self.client = SSHClient()
                self.client.set_missing_host_key_policy(AutoAddPolicy())
                self.client.connect(
                    self.host,
                    username=self.user,
                    password=self.password,
                )
                self.scp = SCPClient(self.client.get_transport())
            except AuthenticationException as error:
                logging.error(f'Authentication failed: \
                    did you remember to create an SSH key? {error}')
                raise error
        return self.client

    def disconnect(self):
        """Close ssh connection."""
        if self.client:
            self.client.close()
        if self.scp:
            self.scp.close()

    def execute_commands(self, commands):
        """
        Execute multiple commands in succession.

        :param commands: List of commands as strings.
        :type commands: List[str]
        """
        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            for line in stdout.read().splitlines():
                logging.info(f'INPUT: {cmd} | OUTPUT: {line}')
                print(f'INPUT: {cmd} | OUTPUT: {line}')


    def upload_single_file(self, local_file_path, remote_file_path):
        """Upload a single file to a remote directory."""

        try:
            self.scp.putfo(
                local_file_path,
                remote_file_path
            )
            logging.info(f'Uploaded {local_file_path} to {remote_file_path} on {self.host}')
        except SCPException as error:
            logging.error(error)
            raise error

    def download_file(self, local_file_path, remote_file_path):
        """Download file from remote host."""
        self.scp.get(
            remote_file_path,
            local_file_path
            )