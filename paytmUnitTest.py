__author__ = 'Kelly Moylan'
import unittest
import paytm
from pandas.util.testing import assert_frame_equal
import pandas as pd
import datetime


class myTestDD(unittest.TestCase):

    # Finds bad input file name
    def test_bad_tdata_input(self):
        self.assertRaises(Exception, paytm.read_transactions,"badfile.txt")

    # Finds bad input file name
    def test_bad_rcdata_input(self):
        self.assertRaises(Exception, paytm.read_cancels,"badfile.txt")

    # Check for proper date conversion
    def test_good_time_convert(self):
        temp = pd.DataFrame(paytm.convert_ship_time(pd.DataFrame(data=["2015-07-04 00:12:44.0"], columns=['item_ship_by_date'])), columns=['item_ship_by_date'])
        temp2 = datetime.datetime.strptime("2015-07-04 00:12:44.0", "%Y-%m-%d %H:%M:%S.%f")
        temp3 = pd.DataFrame(data=[temp2],columns=['item_ship_by_date'])
        assert_frame_equal(temp, temp3)

    # Incorrect date entry
    def test_bad_ship_time_convert(self):
        self.assertRaises(Exception, paytm.convert_ship_time, pd.DataFrame(data=["not a date"], columns=['item_ship_by_date']))

    # Incorrect date entry
    def test_bad_fulfill_time_convert(self):
        self.assertRaises(Exception, paytm.convert_fulfil_time, pd.DataFrame(data=["not a date"], columns=['fulfillment_shiped_at']))

    # Wrong column name
    def test_bad_tdata_grouping(self):
        self.assertRaises(Exception, paytm.group_transactions, pd.DataFrame(data=[["ijf43ijfaj",4,5]], columns=['merchant_id','qty_shipped','lates']))

    # Wrong column name
    def test_bad_rcdata_grouping(self):
        self.assertRaises(Exception, paytm.group_cancels, pd.DataFrame(data=[["ijf43ijfaj",4,5]], columns=['merch_id','cancel_number','return_num']))

if __name__ == '__main__':
    unittest.main()
