# -*- coding: utf-8 -*-

"""Unit tests of library lib_mda"""

# Run these tests with command:
# python -m unittest lib_mda_test.py -v

import os
import unittest
import sys
sys.path += ["../"]

import pandas as pd

import importlib
import importlib.util
import lib_mda
importlib.reload(lib_mda)

DATA_TEST_DIR = os.path.join("data")

class TestExtractTransitions_OQB_PF2_7_TestCase(unittest.TestCase):
    def setUp(self):

        data_test_filename = os.path.join(DATA_TEST_DIR,
                                          "events_doha_OQB_PF2_7.csv")
        
        self.events_df = \
            pd.read_csv(data_test_filename,
                        sep=";",
                        parse_dates=["DATETIME"]).set_index("DATETIME")

    def test_opening_m(self):
        event_start_specs = {
            "CONTENT": "MSD closed & locked",
            "LEVEL": "Reset"
        }
        event_end_specs = {
            "CONTENT": "MSD Fully Opened",
            "LEVEL": "Set"
        }

        data_res_filename = os.path.join(DATA_TEST_DIR,
                                         "events_doha_OQB_PF2_7_opening_m_res.csv")

        trans_res_df = pd.read_csv(data_res_filename,
                                   sep=";",
                                   parse_dates=["datetime_start", "datetime_end"])

        trans_test_df = \
            lib_mda.extract_transitions(self.events_df,
                                        event_start_specs,
                                        event_end_specs)
        
        pd.testing.assert_frame_equal(trans_test_df.reset_index(drop=True),
                                      trans_res_df)

    def test_opening_r(self):
        event_start_specs = {
            "CONTENT": "MSD open command",
            "LEVEL": "Set"
        }
        event_end_specs = {
            "CONTENT": "MSD closed & locked",
            "LEVEL": "Reset"
        }

        data_res_filename = os.path.join(DATA_TEST_DIR,
                                         "events_doha_OQB_PF2_7_opening_r_res.csv")

        trans_res_df = pd.read_csv(data_res_filename,
                                   sep=";",
                                   parse_dates=["datetime_start", "datetime_end"])

        trans_test_df = \
            lib_mda.extract_transitions(self.events_df,
                                        event_start_specs,
                                        event_end_specs)
        
        pd.testing.assert_frame_equal(trans_test_df.reset_index(drop=True),
                                      trans_res_df)


    def test_closing_m(self):
        event_start_specs = {
            "CONTENT": "MSD Fully Opened",
            "LEVEL": "Reset"
        }
        event_end_specs = {
            "CONTENT": "MSD closed & locked",
            "LEVEL": "Set"
        }

        data_res_filename = os.path.join(DATA_TEST_DIR,
                                         "events_doha_OQB_PF2_7_closing_m_res.csv")
        trans_res_df = pd.read_csv(data_res_filename,
                                   sep=";",
                                   parse_dates=["datetime_start", "datetime_end"])

        trans_test_df = \
            lib_mda.extract_transitions(self.events_df,
                                        event_start_specs,
                                        event_end_specs)
        
        pd.testing.assert_frame_equal(trans_test_df.reset_index(drop=True),
                                      trans_res_df)

    def test_closing_r(self):
        event_start_specs = {
            "CONTENT": "MSD open command",
            "LEVEL": "Reset"
        }
        event_end_specs = {
            "CONTENT": "MSD Fully Opened",
            "LEVEL": "Reset"
        }

        data_res_filename = os.path.join(DATA_TEST_DIR,
                                         "events_doha_OQB_PF2_7_closing_r_res.csv")
        trans_res_df = pd.read_csv(data_res_filename,
                                   sep=";",
                                   parse_dates=["datetime_start", "datetime_end"])

        trans_test_df = \
            lib_mda.extract_transitions(self.events_df,
                                        event_start_specs,
                                        event_end_specs)
        
        pd.testing.assert_frame_equal(trans_test_df.reset_index(drop=True),
                                      trans_res_df)

        

        
if __name__ == '__main__':

    # test = TestExtractTransitions_OQB_PF2_7_TestCase()
    # test.setUp()

    # event_start_specs = {
    #         "CONTENT": "MSD open command",
    #         "LEVEL": "Set"
    #     }
    # event_end_specs = {
    #         "CONTENT": "MSD closed & locked",
    #         "LEVEL": "Reset"
    #     }

    # trans_test_df = \
    #     lib_mda.extract_transitions(test.events_df,
    #                                 event_start_specs,
    #                                 event_end_specs)
    # durations_df = trans_test_df["datetime_end"] - trans_test_df["datetime_start"]
    
    # test = ExtractTransitionsOpeningMTestCase()
    # test.setUp()

    # events_start_query = " and ".join(['`{}`.str.contains("{}")'.format(k,v) for
    #                                    k, v in test.event_start_specs.items()])
    # events_start_df = test.events_df.query(events_start_query)

    # events_end_query = " and ".join(['`{}`.str.contains("{}")'.format(k,v) for
    #                                  k, v in test.event_end_specs.items()])
    # events_end_df = test.events_df.query(events_end_query)

    # events_seq_df = pd.concat([events_start_df, events_end_df],
    #                           axis=0)\
    #                   .sort_index()\
    #                   .reset_index()\
    #                   .rename(columns={test.events_df.index.name: "datetime"})

    # events_var = list(events_seq_df.columns)
    
    # events_seq_shift_df = events_seq_df.shift(-1)

    # # Rename columns appropriately
    # events_seq_df.rename(columns={v:v + '_start' for v in events_var},
    #                      inplace=True)
    # events_seq_shift_df.rename(columns={v:v + '_end' for v in events_var},
    #                            inplace=True)

    # trans_tmp_df = pd.concat([events_seq_df, events_seq_shift_df],
    #                          axis=1)
    
    # trans_start_query = " and ".join(['`{}_start`.str.contains("{}")'.format(k,v) for
    #                                   k, v in test.event_start_specs.items()])

    # trans_end_query = " and ".join(['`{}_end`.str.contains("{}")'.format(k,v) for
    #                                   k, v in test.event_end_specs.items()])

    # trans_query = " and ".join([trans_start_query, trans_end_query])

    # trans_df = trans_tmp_df.query(trans_query)[["datetime_start", "datetime_end"]]
        
    unittest.main()
