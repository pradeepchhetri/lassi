import sys
import logging
import traceback

from ssh import SSHConnection

class Service(object):

    def __init__(self, service, hostname, username, password):
        """
        Initializes a Service object
        """
        self.service = service
        self.hostname = hostname
        self.sshconnection = SSHConnection(hostname, username, password)

    def start(self):
        """
        Starts a service
        """
        try:
            stdout, stderr, code = self.sshconnection.execute('service %s start' % self.service)
            if code != 0:
                logging.error("[%s] Error starting service: %s" % (self.hostname, self.service))
                logging.error("%s" % stderr)
                sys.exit(1)
        except Exception as e:
            print('Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            sys.exit(1)

    def stop(self):
        """
        Stops a service
        """
        try:
            stdout, stderr, code = self.sshconnection.execute('service %s stop' % self.service)
            if code != 0:
                logging.error("[%s] Error stopping service: %s" % (self.hostname, self.service))
                logging.error("%s" % stderr)
                sys.exit(1)
        except Exception as e:
            print('Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            sys.exit(1)

    def restart(self):
        """
        Restarts a service
        """
        try:
            stdout, stderr, code = self.sshconnection.execute('service %s restart' % self.service)
            if code != 0:
                logging.error("[%s] Error restarting service: %s" % (self.hostname, self.service))
                logging.error("%s" % stderr)
                sys.exit(1)
        except Exception as e:
            print('Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            sys.exit(1)

    def reload(self):
        """
        Reloads a service
        """
        try:
            stdout, stderr, code = self.sshconnection.execute('service %s reload' % self.service)
            if code != 0:
                logging.error("[%s] Error reloading service: %s" % (self.hostname, self.service))
                logging.error("%s" % stderr)
                sys.exit(1)
        except Exception as e:
            print('Caught exception: %s: %s' % (e.__class__, e))
            traceback.print_exc()
            sys.exit(1)
