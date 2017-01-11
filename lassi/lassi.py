#!/usr/bin/env python

import sys
import json
import logging

from .lib import file, package, service, sftp

def read_config(config):
    """
    Reads the configuration for each host
    and applies them one by one.
    """
    try:
        with open(config) as config_file:
            config_data = json.load(config_file)
        return config_data
    except IOError:
        logging.error("Configuration file unavailable")
        sys.exit(1)

def install_packages(hostname, username, password, packages=[]):
    """
    Installs the list of packages
    """
    for pack in packages:
        installer = package.Package(pack["name"], hostname, username, password)
        if "ensure" in pack and pack["ensure"] == "absent":
            logging.info("[%s] Removing package: %s" % (hostname, pack["name"]))
            installer.remove()
        else:
            if installer.check_installation() == 0:
                logging.info("[%s] Already installed package: %s" % (hostname, pack["name"]))
                pass
            else:
                logging.info("[%s] Installing package: %s" % (hostname, pack["name"]))
                installer.update()
                installer.install()
                if "notify" in pack:
                    for serv in pack["notify"]:
                        logging.info("[%s] Reloading service: %s" % (hostname, serv))
                        supervisor = service.Service(serv, hostname, username, password)
                        supervisor.reload()

def ensure_services(hostname, username, password, services=[]):
    """
    Ensure the services are running
    """
    for serv in services:
        logging.info("[%s] Ensuring service: %s to be running" % (hostname, serv))
        supervisor = service.Service(serv, hostname, username, password)
        supervisor.start()

def push_files(hostname, username, password, files=[]):
    """
    Push configuration files
    """
    for f in files:
        connection = sftp.SFTPConnection(hostname, username, password)
        logging.info("[%s] Pushing file: %s at %s" % (hostname, f["source"], f["destination"]))
        transferred = connection.transfer(f["source"], f["destination"])
        fd = file.File(f["destination"], hostname, username, password)
        if "owner" in f:
            logging.info("[%s] Changing the ownership of file: %s to %s" % (hostname, f["destination"], f["owner"]))
            fd.set_owner(f["owner"])
        if "group" in f:
            logging.info("[%s] Changing the group ownership of file: %s to %s" % (hostname, f["destination"], f["group"]))
            fd.set_group(f["group"])
        if "permissions" in f:
            logging.info("[%s] Changing the permissions of file: %s to %s" % (hostname, f["destination"], f["permissions"]))
            fd.set_permissions(f["permissions"])
        if transferred == 1 and "notify" in f:
            for serv in f["notify"]:
                logging.info("[%s] Reloading service: %s" % (hostname, serv))
                supervisor = service.Service(serv, hostname, username, password)
                supervisor.reload()

def main():
    """
    Configuration Management Tool
    """
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    config = read_config("/etc/lassi.config")

    for conf in config:
        hostname = conf["hostname"]
        username = conf["username"]
        password = conf["password"]

        # Install required packages
        install_packages(hostname, username, password, conf["package"])

        # Ensure services are up
        ensure_services(hostname, username, password, conf["service"])

        # Serve files
        push_files(hostname, username, password, conf["file"])

if __name__ == "__main__":
    sys.exit(main())
