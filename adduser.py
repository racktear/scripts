#!/usr/bin/env python

import sys
import argparse
from fabric.api import *
from fabric.contrib.files import *
from fabric.operations import *

def new_user(host, username, keyfile):
    if not os.path.exists(keyfile):
        sys.exit("key file doesn't exist: %s" % keyfile)

    key = open(keyfile).read()

    with settings(host_string=host):
        userid = ""

        with settings(warn_only=True):
            userid = sudo("id -u %s" % username)

        if not userid.isdigit():
            sudo('adduser -m %s' % username)

        sudo('echo "%s ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/%s' %
             (username, username))
        sudo('mkdir -p /home/%s/.ssh' %
             username)

        keys = ""

        with settings(warn_only=True):
            keys = sudo("cat /home/%s/.ssh/authorized_keys" % username)

        if key not in keys:
            sudo('echo "%s" >> /home/%s/.ssh/authorized_keys' %
                 (key, username))

        sudo('chown -R %s:%s /home/%s/.ssh' % (username, username, username))
        sudo('chmod 700 /home/%s/.ssh' % username)
        sudo('chmod 600 /home/%s/.ssh/authorized_keys' % username)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("user")
    parser.add_argument("keyfile")

    args = parser.parse_args()

    new_user(args.host, args.user, args.keyfile)


if __name__ == "__main__":
    main()
