import unittest
from tracker import web_ui, config, tracker
from peewee import *
from datetime import datetime, timedelta


class Testcase(unittest.TestCase):
    def setUp(self):
        config.DB = SqliteDatabase("test_track.db")
        config.QUERY_TIME = 30
        config.DB.create_table(tracker.Entry,safe=True)

    def tearDown(self):
        for i in tracker.Entry.select():
            i.delete_instance()

    def testClean_db(self):
        now = datetime.utcnow()
        tracker.Entry(time=now-timedelta(hours=11),name="old_entry_1",value=1).save()
        tracker.Entry(time=now-timedelta(hours=3), name="allowed_entry", value=1).save()
        tracker.clean_db()
        assert tracker.Entry.select().where(tracker.Entry.name == "allowed_entry") is True
        assert tracker.Entry.select().where(tracker.Entry.name == "old_entry_1") is False

if __name__ == '__main__':
    unittest.main()

