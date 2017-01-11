import os
import sys
import stat
import logging
from ssh import SSHConnection
from sftp import SFTPConnection

class File(object):

    def __init__(self, filename, hostname, username, password):
        """
        Initializes a File object
        """
        self.filename = filename
        self.hostname = hostname
        self.sshconnection = SSHConnection(hostname, username, password)
        self.sftpconnection = SFTPConnection(hostname, username, password).connect()

    def set_permissions(self, permissions):
        """
        Sets the permissions of the remote file
        """
        try:
            if self.sftpconnection.stat(self.filename):
                self.sftpconnection.chmod(self.filename, int(permissions, 8))
        except IOError:
            logging.debug("[%s] Remote file in unavailable" % (self.hostname))

    def set_owner(self, owner):
        """
        Sets the owner of the remote file
        """
        try:
            logging.debug("[%s] Getting the userid for %s" % (self.hostname, owner))
            user_id, stderr, code = self.sshconnection.execute('id -u %s' % (owner))
            if code != 0:
                logging.error("[%s] Error while getting userid:" % (self.hostname))
                logging.error("%s" % stderr)
                sys.exit(1)
            stat = self.sftpconnection.stat(self.filename)
            if stat:
                self.sftpconnection.chown(self.filename, int(user_id.rstrip()), stat.st_gid)
        except IOError:
            logging.debug("[%s] Remote file in unavailable" % (self.hostname))

    def set_group(self, group):
        """
        Sets the group of the remote file
        """
        try:
            logging.debug("[%s] Getting the groupid for %s" % (self.hostname, group))
            group_id, stderr, code = self.sshconnection.execute('id -g %s' % (group))
            if code != 0:
                logging.error("[%s] Error while getting groupid:" % (self.hostname))
                logging.error("%s" % stderr)
                sys.exit(1)
            stat = self.sftpconnection.stat(self.filename)
            if stat:
                self.sftpconnection.chown(self.filename, stat.st_uid, int(group_id.rstrip()))
        except IOError:
            logging.debug("[%s] Remote file in unavailable" % (self.hostname))
