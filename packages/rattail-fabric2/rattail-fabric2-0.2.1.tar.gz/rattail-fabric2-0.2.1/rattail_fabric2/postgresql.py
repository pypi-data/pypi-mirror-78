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
Fabric Library for PostgreSQL
"""

import os
import re

from rattail_fabric2 import apt


def install(c):
    """
    Install the PostgreSQL database service
    """
    apt.install(c, 'postgresql')


def get_version(c):
    """
    Fetch the version of PostgreSQL running on the target system
    """
    result = c.run('psql --version', warn=True)
    if not result.failed:
        match = re.match(r'^psql \(PostgreSQL\) (\d+\.\d+)(?:\.\d+)?', result.stdout.strip())
        if match:
            return float(match.group(1))

def restart(c):
    """
    Restart the PostgreSQL database service
    """
    c.sudo('systemctl restart postgresql.service')


def reload(c):
    """
    Reload config for the PostgreSQL database service
    """
    c.sudo('systemctl reload postgresql.service')


def sql(c, sql, database='', port=None, **kwargs):
    """
    Execute some SQL as the 'postgres' user.
    """
    cmd = 'psql {port} --tuples-only --no-align --command="{sql}" {database}'.format(
        port='--port={}'.format(port) if port else '',
        sql=sql, database=database)
    return c.sudo(cmd, user='postgres', **kwargs)


def user_exists(c, name, port=None):
    """
    Determine if a given PostgreSQL user exists.
    """
    user = sql(c, "SELECT rolname FROM pg_roles WHERE rolname = '{0}'".format(name), port=port).stdout.strip()
    return bool(user)


def create_user(c, name, password=None, port=None, checkfirst=True, createdb=False):
    """
    Create a PostgreSQL user account.
    """
    if not checkfirst or not user_exists(c, name, port=port):
        cmd = 'createuser {port} {createdb} --no-createrole --no-superuser {name}'.format(
            port='--port={}'.format(port) if port else '',
            createdb='--{}createdb'.format('' if createdb else 'no-'),
            name=name)
        c.sudo(cmd, user='postgres')
        if password:
            set_user_password(c, name, password, port=port)


def set_user_password(c, name, password, port=None):
    """
    Set the password for a PostgreSQL user account
    """
    sql(c, "ALTER USER \\\"{}\\\" PASSWORD '{}';".format(name, password), port=port,
        hide=True, echo=False)


def db_exists(c, name, port=None):
    """
    Determine if a given PostgreSQL database exists.
    """
    db = sql(c, "SELECT datname FROM pg_database WHERE datname = '{0}'".format(name), port=port).stdout.strip()
    return db == name


def create_db(c, name, owner=None, port=None, checkfirst=True):
    """
    Create a PostgreSQL database.
    """
    if not checkfirst or not db_exists(c, name, port=port):
        cmd = 'createdb {port} {owner} {name}'.format(
            port='--port={}'.format(port) if port else '',
            owner='--owner={}'.format(owner) if owner else '',
            name=name)
        c.sudo(cmd, user='postgres')


def create_schema(c, name, dbname, owner='rattail', port=None):
    """
    Create a schema within a PostgreSQL database.
    """
    sql_ = "create schema if not exists {} authorization {}".format(name, owner)
    sql(c, sql_, database=dbname, port=port)


def drop_db(c, name, checkfirst=True):
    """
    Drop a PostgreSQL database.
    """
    if not checkfirst or db_exists(c, name):
        c.sudo('dropdb {}'.format(name), user='postgres')


def download_db(c, name, destination=None, port=None, exclude_tables=None):
    """
    Download a database from the server represented by ``c`` param.
    """
    if destination is None:
        destination = './{}.sql.gz'.format(name)
    c.run('touch {}.sql'.format(name))
    c.run('chmod 0666 {}.sql'.format(name))
    cmd = 'pg_dump {port} {exclude_tables} --file={name}.sql {name}'.format(
        name=name,
        port='--port={}'.format(port) if port else '',
        exclude_tables='--exclude-table-data={}'.format(exclude_tables) if exclude_tables else '')
    c.sudo(cmd, user='postgres')
    c.run('gzip --force {}.sql'.format(name))
    c.get('{}.sql.gz'.format(name), destination)
    c.run('rm {}.sql.gz'.format(name))


def clone_db(c, name, owner, download, user='rattail', force=False, workdir=None):
    """
    Clone a database from a (presumably live) server

    :param name: Name of the database.

    :param owner: Username of the user who is to own the database.

    :param force: Whether the target database should be forcibly dropped, if it
       exists already.
    """
    if db_exists(c, name):
       if force:
           drop_db(c, name, checkfirst=False)
       else:
           raise RuntimeError("Database '{}' already exists!".format(name))

    create_db(c, name, owner=owner, checkfirst=False)

    # upload database dump to target server
    if workdir:
        curdir = os.getcwd()
        os.chdir(workdir)
    download(c, '{}.sql.gz'.format(name), user=user)
    c.put('{}.sql.gz'.format(name))
    c.local('rm {}.sql.gz'.format(name))
    if workdir:
        os.chdir(curdir)

    # restore database on target server
    c.run('gunzip --force {}.sql.gz'.format(name))
    c.sudo('psql --echo-errors --file={0}.sql {0}'.format(name), user='postgres')
    c.run('rm {}.sql'.format(name))
