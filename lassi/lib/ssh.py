import sys
import socket
import logging
import traceback
import StringIO

try:
    import paramiko
    logging.getLogger("paramiko").setLevel(logging.ERROR)
except ImportError, e:
    traceback.print_exc()
    message = """
Error importing the paramiko python module.
Please ensure all dependencies are installed.
""".rstrip()
    sys.stderr.write(msg + '\n')
    sys.exit(1)

class SSHConnection(object):

    def __init__(self, hostname, username, password):
        """
        Initializes a SSHConnection object
        """
        self.hostname = hostname
        self.username = username
        self.password = password

    def connect(self):
        """
        Connects with the host using username &
        password authentication pair
        """
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.hostname, username=self.username, password=self.password)
        except Exception as e:
            print('Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                client.close()
            except:
                pass
            sys.exit(1)
        return client

    def execute(self, cmd):
        """
        Executes a command on the host
        """
        client = self.connect()
        chan = client.get_transport().open_session()
        chan.settimeout(10800)
        try:
            # Execute the given command
            chan.exec_command(cmd)

            # To capture data, need to read the entire buffer to capture output
            output = StringIO.StringIO()
            error = StringIO.StringIO()

            while not chan.exit_status_ready():
                if chan.recv_ready():
                    data = chan.recv(1024)
                    while data:
                        output.write(data)
                        data = chan.recv(1024)

                if chan.recv_stderr_ready():
                    error_buff = chan.recv_stderr(1024)
                    while error_buff:
                        error.write(error_buff)
                        error_buff = chan.recv_stderr(1024)

            exit_status = chan.recv_exit_status()

        except socket.timeout:
            raise socket.timeout

        stdout = output.getvalue()
        stderr = error.getvalue()

        return stdout, stderr, exit_status
