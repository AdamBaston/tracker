import unittest
from datetime import datetime, timedelta
from difflib import SequenceMatcher as SM
from peewee import *
from psutil import cpu_percent, virtual_memory
import config
import tracker
import web_ui
from playhouse.shortcuts import model_to_dict

class Testui(unittest.TestCase):
    def setUp(self):
        config.DB = SqliteDatabase("test_track.db")
        config.QUERY_TIME = 30
        config.DB.create_tables([tracker.Entry], safe=True)
        # config.DB.create_tables(tracker.Entry,safe=True)
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
        q = tracker.Entry.select().order_by(tracker.Entry.id.desc()).where(tracker.Entry.name == "RAM").get()
        # self.assertAlmostEqual(q.value,cpu_percent(interval=1))
        # self.assert(SM(None,q.value,cpu_percent(interval=1)).ratio() > 0.1)
        self.assertGreaterEqual(SM(None, str(q.value), str(virtual_memory()[2])).ratio(), 0.1)

    def testApi(self): # should pass on travis
        now = datetime.utcnow()
        data1 = tracker.Entry(time=now, name="CPU",value=2.5)
        data2 =tracker.Entry(time=now, name="CPU", value=3)
        test_data = []
        # test_data = model_to_dict(data1)+","+model_to_dict(data2)
        test_data.append(model_to_dict(data1))
        test_data.append(model_to_dict(data2))
        data1.save()
        data2.save()
        value = web_ui.cpu_api()
        print(value,"==")
        print(test_data)
        self.assertTrue(str(test_data.strip("[]")) is value)


if __name__ == '__main__':
    unittest.main()

