from gcpds.utils import loaddb
import unittest

import logging
logging.basicConfig(level=logging.DEBUG)


########################################################################
class TestLoadDB(unittest.TestCase):
    """"""

    # ----------------------------------------------------------------------
    def _test_database(self, database):
        """"""
        db = getattr(loaddb, database)(database)
        db.load_subject(1)

        run, classes = db.get_run(0)
        self.assertEqual(run.shape[0], classes.shape[0])

        run, classes = db.get_run(0, classes=[0, 1])
        self.assertEqual(len(set(classes)), 2)

        run, classes = db.get_run(0, channels=[1, 2, 3, 4])
        self.assertEqual(run.shape[1], 4)

        run, classes = db.get_run(0, classes=[0, 1], channels=[1, 2, 3])
        self.assertEqual(run.shape[1], 3)
        self.assertEqual(len(set(classes)), 2)

        self.assertRaises(Exception, lambda: db.get_run(
            0, classes=[0, 1], channels=[0, 2, 3]))

        self.assertRaises(Exception, lambda: db.load_subject(999))

        db.get_epochs(0)

    # ----------------------------------------------------------------------
    def test_bci2a(self):
        """"""
        self._test_database('BCI2a')

    # ----------------------------------------------------------------------
    def test_giga(self):
        """"""
        self._test_database('GIGA')

    # ----------------------------------------------------------------------
    def test_high_gamma(self):
        """"""
        # Could kill a low memory computer
        self._test_database('HighGamma')









