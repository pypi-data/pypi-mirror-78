# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

import sqlalchemy as sa
import sqlalchemy.exc as saexc

from twisted.internet import defer
from twisted.trial import unittest

from buildbot.test.util import migration
from buildbot.util import sautils


class Migration(migration.MigrateTestMixin, unittest.TestCase):

    def setUp(self):
        return self.setUpMigrateTest()

    def tearDown(self):
        return self.tearDownMigrateTest()

    def create_tables_and_insert_data(self, conn):
        metadata = sa.MetaData()
        metadata.bind = conn

        # create tables (prior to schema migration)
        masters = sautils.Table(
            "masters", metadata,
            sa.Column('id', sa.Integer, primary_key=True),
        )
        masters.create()

        users = sautils.Table(
            "users", metadata,
            sa.Column("uid", sa.Integer, primary_key=True),
        )
        users.create()

        workers = sautils.Table(
            "workers", metadata,
            sa.Column("id", sa.Integer, primary_key=True),
        )
        workers.create()

        sourcestamps = sautils.Table(
            'sourcestamps', metadata,
            sa.Column('id', sa.Integer, primary_key=True),
        )
        sourcestamps.create()

        schedulers = sautils.Table(
            'schedulers', metadata,
            sa.Column("id", sa.Integer, primary_key=True),
        )
        schedulers.create()

        buildsets = sautils.Table(
            'buildsets', metadata,
            sa.Column('id', sa.Integer, primary_key=True),
        )
        buildsets.create()

        builders = sautils.Table(
            'builders', metadata,
            sa.Column('id', sa.Integer, primary_key=True),
        )
        builders.create()

        tags = sautils.Table(
            'tags', metadata,
            sa.Column('id', sa.Integer, primary_key=True),
        )
        tags.create()

        changesources = sautils.Table(
            'changesources', metadata,
            sa.Column("id", sa.Integer, primary_key=True),
        )
        changesources.create()

        buildrequests = sautils.Table(
            'buildrequests', metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('buildsetid', sa.Integer,
                      sa.ForeignKey("buildsets.id", ondelete='CASCADE'),
                      nullable=False),
            sa.Column('builderid', sa.Integer,
                      sa.ForeignKey('builders.id', ondelete='CASCADE'),
                      nullable=False),
        )
        buildrequests.create()

        builds = sautils.Table(
            'builds', metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('builderid', sa.Integer,
                      sa.ForeignKey('builders.id', ondelete='CASCADE')),
            sa.Column('buildrequestid', sa.Integer,
                      sa.ForeignKey(
                          'buildrequests.id', use_alter=True,
                          name='buildrequestid', ondelete='CASCADE'),
                      nullable=False),
            sa.Column('workerid', sa.Integer,
                      sa.ForeignKey('workers.id', ondelete='CASCADE')),
            sa.Column('masterid', sa.Integer,
                      sa.ForeignKey('masters.id', ondelete='CASCADE'),
                      nullable=False),
        )
        builds.create()

        buildrequest_claims = sautils.Table(
            'buildrequest_claims', metadata,
            sa.Column('brid', sa.Integer,
                      sa.ForeignKey('buildrequests.id', ondelete='CASCADE'),
                      nullable=False),
            sa.Column('masterid', sa.Integer,
                      sa.ForeignKey('masters.id', ondelete='CASCADE'),
                      index=True, nullable=True),
        )
        buildrequest_claims.create()

        build_properties = sautils.Table(
            'build_properties', metadata,
            sa.Column('buildid', sa.Integer,
                      sa.ForeignKey('builds.id', ondelete='CASCADE'),
                      nullable=False),
            sa.Column('name', sa.String(256), nullable=False),
        )
        build_properties.create()

        steps = sautils.Table(
            'steps', metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('buildid', sa.Integer,
                      sa.ForeignKey('builds.id', ondelete='CASCADE')),
        )
        steps.create()

        logs = sautils.Table(
            'logs', metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('stepid', sa.Integer,
                      sa.ForeignKey('steps.id', ondelete='CASCADE')),
        )
        logs.create()

        logchunks = sautils.Table(
            'logchunks', metadata,
            sa.Column('logid', sa.Integer,
                      sa.ForeignKey('logs.id', ondelete='CASCADE')),
            sa.Column('first_line', sa.Integer, nullable=False),
            sa.Column('last_line', sa.Integer, nullable=False),
        )
        logchunks.create()

        buildset_properties = sautils.Table(
            'buildset_properties', metadata,
            sa.Column('buildsetid', sa.Integer,
                      sa.ForeignKey('buildsets.id', ondelete='CASCADE'),
                      nullable=False),
            sa.Column('property_name', sa.String(256), nullable=False),
        )
        buildset_properties.create()

        changesource_masters = sautils.Table(
            'changesource_masters', metadata,
            sa.Column('changesourceid', sa.Integer,
                      sa.ForeignKey('changesources.id', ondelete='CASCADE'),
                      nullable=False, primary_key=True),
            sa.Column('masterid', sa.Integer,
                      sa.ForeignKey('masters.id', ondelete='CASCADE'),
                      nullable=False),
        )
        changesource_masters.create()

        buildset_sourcestamps = sautils.Table(
            'buildset_sourcestamps', metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('buildsetid', sa.Integer,
                      sa.ForeignKey('buildsets.id', ondelete='CASCADE'),
                      nullable=False),
            sa.Column('sourcestampid', sa.Integer,
                      sa.ForeignKey('sourcestamps.id', ondelete='CASCADE'),
                      nullable=False),
        )
        buildset_sourcestamps.create()

        connected_workers = sautils.Table(
            'connected_workers', metadata,
            sa.Column('id', sa.Integer, primary_key=True, nullable=False),
            sa.Column('masterid', sa.Integer,
                      sa.ForeignKey('masters.id', ondelete='CASCADE'),
                      nullable=False),
            sa.Column('workerid', sa.Integer,
                      sa.ForeignKey('workers.id', ondelete='CASCADE'),
                      nullable=False),
        )
        connected_workers.create()

        changes = sautils.Table(
            'changes', metadata,
            sa.Column('changeid', sa.Integer, primary_key=True),
            sa.Column('sourcestampid', sa.Integer,
                      sa.ForeignKey('sourcestamps.id', ondelete='CASCADE')),
            sa.Column('parent_changeids', sa.Integer,
                      sa.ForeignKey('changes.changeid', ondelete='CASCADE'),
                      nullable=True),
        )
        changes.create()

        change_files = sautils.Table(
            'change_files', metadata,
            sa.Column('changeid', sa.Integer,
                      sa.ForeignKey('changes.changeid', ondelete='CASCADE'),
                      nullable=False),
            sa.Column('filename', sa.String(1024), nullable=False),
        )
        change_files.create()

        change_properties = sautils.Table(
            'change_properties', metadata,
            sa.Column('changeid', sa.Integer,
                      sa.ForeignKey('changes.changeid', ondelete='CASCADE'),
                      nullable=False),
            sa.Column('property_name', sa.String(256), nullable=False),
        )
        change_properties.create()

        change_users = sautils.Table(
            "change_users", metadata,
            sa.Column("changeid", sa.Integer,
                      sa.ForeignKey('changes.changeid', ondelete='CASCADE'),
                      nullable=False),
            sa.Column("uid", sa.Integer,
                      sa.ForeignKey('users.uid', ondelete='CASCADE'),
                      nullable=False),
        )
        change_users.create()

        scheduler_masters = sautils.Table(
            'scheduler_masters', metadata,
            sa.Column('schedulerid', sa.Integer,
                      sa.ForeignKey('schedulers.id', ondelete='CASCADE'),
                      nullable=False, primary_key=True),
            sa.Column('masterid', sa.Integer,
                      sa.ForeignKey('masters.id', ondelete='CASCADE'),
                      nullable=False),
        )
        scheduler_masters.create()

        scheduler_changes = sautils.Table(
            'scheduler_changes', metadata,
            sa.Column('schedulerid', sa.Integer,
                      sa.ForeignKey('schedulers.id', ondelete='CASCADE')),
            sa.Column('changeid', sa.Integer,
                      sa.ForeignKey('changes.changeid', ondelete='CASCADE')),
        )
        scheduler_changes.create()

        builders_tags = sautils.Table(
            'builders_tags', metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('builderid', sa.Integer,
                      sa.ForeignKey('builders.id', ondelete='CASCADE'),
                      nullable=False),
            sa.Column('tagid', sa.Integer,
                      sa.ForeignKey('tags.id', ondelete='CASCADE'),
                      nullable=False),
        )
        builders_tags.create()

        objects = sautils.Table(
            "objects", metadata,
            sa.Column("id", sa.Integer, primary_key=True),
        )
        objects.create()

        object_state = sautils.Table(
            "object_state", metadata,
            sa.Column("objectid", sa.Integer,
                      sa.ForeignKey('objects.id', ondelete='CASCADE'),
                      nullable=False),
            sa.Column("name", sa.String(length=255), nullable=False),
        )
        object_state.create()

        users_info = sautils.Table(
            "users_info", metadata,
            sa.Column("uid", sa.Integer,
                      sa.ForeignKey('users.uid', ondelete='CASCADE'),
                      nullable=False),
            sa.Column("attr_type", sa.String(128), nullable=False),
        )
        users_info.create()

        # insert data
        conn.execute(masters.insert(), [
            dict(id=1),
        ])
        conn.execute(objects.insert(), [
            dict(id=1),
        ])
        conn.execute(object_state.insert(), [
            dict(objectid=1, name='size'),
        ])
        conn.execute(users.insert(), [
            dict(uid=1),
            dict(uid=2),
        ])
        conn.execute(users_info.insert(), [
            dict(uid=1, attr_type='first_name'),
            dict(uid=1, attr_type='last_name'),
            dict(uid=2, attr_type='first_name'),
            dict(uid=2, attr_type='last_name'),
        ])
        conn.execute(builders.insert(), [
            dict(id=1),
            dict(id=2),
        ])
        conn.execute(tags.insert(), [
            dict(id=1),
            dict(id=2),
        ])
        conn.execute(builders_tags.insert(), [
            dict(id=1, builderid=1, tagid=1),
            dict(id=2, builderid=2, tagid=1),
            dict(id=3, builderid=2, tagid=2),
        ])
        conn.execute(workers.insert(), [
            dict(id=1),
            dict(id=2),
        ])
        conn.execute(connected_workers.insert(), [
            dict(id=1, masterid=1, workerid=1),
            dict(id=2, masterid=1, workerid=2),
        ])
        conn.execute(changesources.insert(), [
            dict(id=1),
        ])
        conn.execute(changesource_masters.insert(), [
            dict(changesourceid=1, masterid=1),
        ])
        conn.execute(sourcestamps.insert(), [
            dict(id=1),
            dict(id=2),
        ])
        conn.execute(changes.insert(), [
            dict(changeid=1, sourcestampid=1),
            dict(changeid=2, sourcestampid=2, parent_changeids=1),
        ])
        conn.execute(change_users.insert(), [
            dict(changeid=1, uid=1),
            dict(changeid=2, uid=2),
        ])
        conn.execute(change_properties.insert(), [
            dict(changeid=1, property_name='release_lvl'),
            dict(changeid=2, property_name='release_lvl'),
        ])
        conn.execute(change_files.insert(), [
            dict(changeid=1, filename='README'),
            dict(changeid=2, filename='setup.py'),
        ])
        conn.execute(schedulers.insert(), [
            dict(changeid=1),
        ])
        conn.execute(scheduler_masters.insert(), [
            dict(schedulerid=1, masterid=1),
        ])
        conn.execute(scheduler_changes.insert(), [
            dict(schedulerid=1, changeid=1),
            dict(schedulerid=1, changeid=2),
            dict(schedulerid=None, changeid=None),
        ])
        conn.execute(buildsets.insert(), [
            dict(id=1),
            dict(id=2),
        ])
        conn.execute(buildset_properties.insert(), [
            dict(buildsetid=1, property_name='color'),
            dict(buildsetid=2, property_name='smell'),
        ])
        conn.execute(buildset_sourcestamps.insert(), [
            dict(id=1, buildsetid=1, sourcestampid=1),
            dict(id=2, buildsetid=2, sourcestampid=2),
        ])
        conn.execute(buildrequests.insert(), [
            dict(id=1, buildsetid=1, builderid=1),
            dict(id=2, buildsetid=1, builderid=2),
            dict(id=3, buildsetid=2, builderid=1),
            dict(id=4, buildsetid=2, builderid=2),
        ])
        conn.execute(buildrequest_claims.insert(), [
            dict(brid=1, masterid=1),
            dict(brid=2, masterid=1),
            dict(brid=3, masterid=1),
            dict(brid=4, masterid=1),
        ])
        conn.execute(builds.insert(), [
            dict(id=1, builderid=1, buildrequestid=1, workerid=2, masterid=1),
            dict(id=2, builderid=2, buildrequestid=2, workerid=1, masterid=1),
            dict(id=3, builderid=1, buildrequestid=3, workerid=1, masterid=1),
            dict(id=4, builderid=2, buildrequestid=4, workerid=2, masterid=1),
        ])
        conn.execute(build_properties.insert(), [
            dict(buildid=1, name='buildername'),
            dict(buildid=2, name='buildername'),
            dict(buildid=3, name='buildername'),
            dict(buildid=4, name='buildername'),
        ])
        conn.execute(steps.insert(), [
            dict(id=1, buildid=1),
            dict(id=2, buildid=1),
            dict(id=3, buildid=2),
            dict(id=4, buildid=2),
            dict(id=5, buildid=1),
            dict(id=6, buildid=1),
            dict(id=7, buildid=2),
            dict(id=8, buildid=2),
        ])
        conn.execute(logs.insert(), [
            dict(id=1, stepid=1),
            dict(id=2, stepid=2),
            dict(id=3, stepid=3),
            dict(id=4, stepid=4),
            dict(id=5, stepid=5),
            dict(id=6, stepid=6),
            dict(id=7, stepid=7),
            dict(id=8, stepid=8),
            dict(id=9, stepid=None),
        ])
        conn.execute(logchunks.insert(), [
            dict(logid=1, first_line=0, last_line=100),
            dict(logid=2, first_line=0, last_line=100),
            dict(logid=3, first_line=0, last_line=100),
            dict(logid=4, first_line=0, last_line=100),
            dict(logid=5, first_line=0, last_line=100),
            dict(logid=6, first_line=0, last_line=100),
            dict(logid=7, first_line=0, last_line=100),
            dict(logid=8, first_line=0, last_line=100),
            dict(logid=None, first_line=0, last_line=100),
        ])

    @defer.inlineCallbacks
    def test_update(self):
        def setup_thd(conn):
            self.create_tables_and_insert_data(conn)

        def verify_thd(conn):
            """Can't verify much under SQLite

            Even with PRAGMA foreign_keys=ON, the cascading deletes are
            actually ignored with SQLite, so we can't really test the behaviour
            in that environment.
            """
            metadata = sa.MetaData()
            metadata.bind = conn

            changes = sautils.Table('changes', metadata, autoload=True)
            builds = sautils.Table('builds', metadata, autoload=True)
            workers = sautils.Table('workers', metadata, autoload=True)
            sourcestamps = sautils.Table('sourcestamps', metadata, autoload=True)

            conn.execute(sourcestamps.delete().where(sourcestamps.c.id == 1))

            if conn.dialect.name not in ('mysql', 'sqlite'):
                q = sa.select([changes.c.changeid])
                self.assertEqual(conn.execute(q).fetchall(), [(2,)])

            q = sa.select([changes.c.parent_changeids]).where(
                    changes.c.changeid == 2)
            self.assertEqual(conn.execute(q).fetchall(), [(None,)])

            conn.execute(workers.delete().where(workers.c.id == 1))

            if conn.dialect.name not in ('mysql', 'sqlite'):
                q = sa.select([builds.c.id, builds.c.workerid]).order_by(
                        builds.c.id)
                self.assertEqual(conn.execute(q).fetchall(),
                                 [(1, 2), (2, None), (3, None), (4, 2)])

            with self.assertRaises(saexc.DatabaseError):
                conn.execute(builds.insert(), [
                    dict(id=5, builderid=None, buildrequestid=4,
                         workerid=2, masterid=1),
                ])

        with self.assertWarnsRegex(
                UserWarning,
                'Inconsistent data found in DB: table .+?, deleting invalid rows'):
            yield self.do_test_migration(51, 52, setup_thd, verify_thd)
