# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2018 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Fabric library for Rattail itself
"""

from __future__ import unicode_literals, absolute_import

import os

from rattail_fabric2 import postgresql, make_deploy, make_system_user, mkdir


deploy = make_deploy(__file__)


def bootstrap_rattail(c, home='/var/lib/rattail', uid=None, shell='/bin/bash'):
    """
    Bootstrap a basic Rattail software environment.
    """
    make_system_user(c, 'rattail', home=home, uid=uid, shell=shell)
    mkdir(c, os.path.join(home, '.ssh'), owner='rattail:', mode='0700', use_sudo=True)

    mkdir(c, '/etc/rattail', use_sudo=True)
    mkdir(c, '/srv/rattail', use_sudo=True)
    mkdir(c, '/var/log/rattail', owner='rattail:rattail', mode='0775', use_sudo=True)

    mkdir(c, '/srv/rattail/init', use_sudo=True)
    deploy(c, 'daemon', '/srv/rattail/init/daemon', use_sudo=True)
    deploy(c, 'check-rattail-daemon', '/usr/local/bin/check-rattail-daemon', use_sudo=True)
    deploy(c, 'check-supervisor-process', '/usr/local/bin/check-supervisor-process', use_sudo=True)
    deploy(c, 'check-systemd-service', '/usr/local/bin/check-systemd-service', use_sudo=True)
    deploy(c, 'luigid', '/srv/rattail/init/luigid', use_sudo=True)
    deploy(c, 'soffice', '/srv/rattail/init/soffice', use_sudo=True)
    # TODO: deprecate / remove these
    deploy(c, 'bouncer', '/srv/rattail/init/bouncer', use_sudo=True)
    deploy(c, 'datasync', '/srv/rattail/init/datasync', use_sudo=True)
    deploy(c, 'filemon', '/srv/rattail/init/filemon', use_sudo=True)


def deploy_machine_conf(c, timezone='America/Chicago'):
    """
    Deploy the standard machine-wide ``rattail.conf`` file.
    """
    mkdir(c, '/etc/rattail', use_sudo=True)
    deploy(c, 'rattail/rattail.conf.mako', '/etc/rattail/rattail.conf', use_sudo=True,
           context={'timezone': timezone})


def delete_email_recipients(c, dbname):
    """
    Purge all email recipient settings for the given database.
    """
    postgresql.sql(c, "delete from setting where name like 'rattail.mail.%.to';", database=dbname)
    postgresql.sql(c, "delete from setting where name like 'rattail.mail.%.cc';", database=dbname)
    postgresql.sql(c, "delete from setting where name like 'rattail.mail.%.bcc';", database=dbname)


def disable_emails(c, dbname):
    """
    Disable all emails for the given database.
    """
    postgresql.sql(c, "update setting set value = 'false' where name like 'rattail.mail.%.enabled';", database=dbname)
