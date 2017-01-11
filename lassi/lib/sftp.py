import md5
import sys
import logging
import traceback

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

class SFTPConnection(object):

    def __init__(self, hostname, username, password):
        """
        Initializes a SFTPConnection object
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
            transport = paramiko.Transport((self.hostname, 22))
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            try:
                transport.close()
            except:
                pass
            sys.exit(1)
        return sftp

    def transfer(self, src, dest, transferred = 0):
        """
        Transfers a file from source on localhost to
        destination on remote host
        """
        try:
            sftp = self.connect()
        except Exception as e:
            print('Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            sys.exit(1)

        try:
            if sftp.stat(dest):
                local_data = open(src, 'r').read()
                remote_data = sftp.open(dest, 'r').read()
                local_md5sum = md5.new(local_data).digest()
                remote_md5sum = md5.new(remote_data).digest()
                if local_md5sum == remote_md5sum:
                    logging.debug("[%s] Remote file is upto-date with local copy" % (self.hostname))
                else:
                    logging.debug("[%s] Remote file is not upto-date with local copy, updating it" % (self.hostname))
                    sftp.put(src, dest)
                    transferred = 1
                return transferred
        except IOError:
            logging.debug("[%s] Remote file is unavailable, pushing the file" % (self.hostname))
            sftp.put(src, dest)
            transferred = 1
            return transferred
        except Exception as e:
            print('Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            sys.exit(1)
