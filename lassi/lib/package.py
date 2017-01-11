import sys
import logging
import traceback

from ssh import SSHConnection

class Package(object):

    def __init__(self, package, hostname, username, password):
        """
        Initializes a Package object
        """
        self.package = package
        self.hostname = hostname
        self.sshconnection = SSHConnection(hostname, username, password)

    def check_installation(self):
        """
        Checks whether the package is already installed
        """
        try:
            return self.sshconnection.execute('dpkg-query -l %s' % (self.package))[2]
        except Exception as e:
            print('Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            sys.exit(1)

    def update(self):
        """
        Updates the local dpkg cache
        """
        try:
            stdout, stderr, code = self.sshconnection.execute('apt-get update -y')
            if code != 0:
                logging.error("[%s] Error updating apt local cache" % (self.hostname))
                logging.error("%s" % stderr)
                sys.exit(1)
        except Exception as e:
            print('Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            sys.exit(1)

    def install(self):
        """
        Installs the package on remote host
        """
        try:
            stdout, stderr, code = self.sshconnection.execute('apt-get install -y %s' % (self.package))
            if code != 0:
                logging.error("[%s] Error installing package: %s" % (self.hostname, self.package))
                logging.error("%s" % stderr)
                sys.exit(1)
        except Exception as e:
            print('Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            sys.exit(1)

    def remove(self):
        """
        Removes the package on remote host
        """
        try:
            stdout, stderr, code = self.sshconnection.execute('apt-get purge -y %s' % (self.package))
            if code != 0:
                logging.error("[%s] Error removing package: %s" % (self.hostname, self.package))
                logging.error("%s" % stderr)
                sys.exit(1)
        except Exception as e:
            print('Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            sys.exit(1)
