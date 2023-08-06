# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2019 Lance Edgar
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
Fabric library for CORE-POS (IS4C)
"""

from __future__ import unicode_literals, absolute_import

import os

from rattail_fabric2 import mysql, exists, mkdir


def install_fannie(c, rootdir, user='www-data', branch='version-2.10',
                   mysql_user='is4c', mysql_pass='is4c'):
    """
    Install the Fannie app to the given location.

    Please note, this assumes composer is already installed and available.
    """
    mkdir(c, rootdir, owner=user, use_sudo=True)

    # fannie source
    is4c = os.path.join(rootdir, 'IS4C')
    if not exists(c, is4c):
        c.sudo('git clone https://github.com/CORE-POS/IS4C.git {}'.format(is4c), user=user)
        c.sudo("bash -c 'cd {}; git checkout {}'".format(is4c, branch), user=user)
        c.sudo("bash -c 'cd {}; git pull'".format(is4c), user=user)

    # fannie dependencies
    mkdir(c, [os.path.join(is4c, 'vendor'),
              os.path.join(is4c, 'fannie/src/javascript/composer-components')],
          owner=user, use_sudo=True)
    c.sudo("bash -c 'cd {}; composer.phar install'".format(is4c), user=user)

    # shadowread
    # TODO: check first; only 'make' if necessary
    c.sudo("bash -c 'cd {}/fannie/auth/shadowread; make'".format(is4c), user=user)
    c.sudo("bash -c 'cd {}/fannie/auth/shadowread; make install'".format(is4c)) # as root!

    # fannie logging
    c.sudo("bash -c 'cd {}/fannie/logs; touch fannie.log debug_fannie.log queries.log php-errors.log dayend.log'".format(is4c), user=user)

    # fannie databases
    mysql.create_user(c, mysql_user, host='%', password=mysql_pass)
    mysql.create_db(c, 'core_op', user="{}@'%'".format(mysql_user))
    mysql.create_db(c, 'core_trans', user="{}@'%'".format(mysql_user))
    mysql.create_db(c, 'trans_archive', user="{}@'%'".format(mysql_user))
