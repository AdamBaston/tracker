import unittest
from datetime import datetime, timedelta
from difflib import SequenceMatcher as SM
from peewee import *
from psutil import cpu_percent
import config
import tracker


class Testcase(unittest.TestCase):
    def setUp(self):
        config.DB = SqliteDatabase("test_track.db")
        config.QUERY_TIME = 30
        config.DB.create_tables(tracker.Entry, safe=True)
        config.DB.create_tables(tracker.Entry,safe=True)
    # def tearDown(self):
    #     for i in tracker.Entry.select():
    #         i.delete_instance()

    def testClean_db(self):
        now = datetime.utcnow()
        tracker.Entry(time=now - timedelta(hours=11), name="old_entry_1", value=1).save()
        tracker.Entry(time=now - timedelta(hours=3), name="allowed_entry", value=1).save()
        tracker.clean_db()
        # assert tracker.Entry.select().where(tracker.Entry.name == "allowed_entry") is True
        # assert tracker.Entry.select().where(tracker.Entry.name == "old_entry_1") is False
        self.assertFalse(tracker.Entry.select().where(tracker.Entry.name == "old_entry_1"), msg="Entry not there")
        self.assertTrue(tracker.Entry.select().where(tracker.Entry.name == "allowed_entry"), msg="Entry there")

    def testmain(self):
        tracker.main()
        tracker.main()
        assert tracker.Entry.select().where(tracker.Entry.value)
        q = tracker.Entry.select().order_by(tracker.Entry.id.desc()).where(tracker.Entry.name == "CPU").get()
        print(q.value,cpu_percent(interval=1))
        assert SM(None,str(q.value),str(cpu_percent(interval=1))).ratio() > 0.1
        # self.assertAlmostEqual(q.value,cpu_percent(interval=1))
        # self.assert(SM(None,q.value,cpu_percent(interval=1)).ratio() > 0.1)
        self.assertGreaterEqual(SM(None, str(12.5), str(cpu_percent(interval=1))).ratio(), 0.1)


if __name__ == '__main__':
    unittest.main()

