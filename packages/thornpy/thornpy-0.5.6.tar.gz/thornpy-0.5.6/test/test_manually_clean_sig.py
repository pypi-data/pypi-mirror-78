import os
import unittest

from numpy import genfromtxt
import matplotlib.pyplot as plt
from thornpy.signal import manually_clean_sig

TEST_SPIKE_DATA = os.path.join('test', 'files', 'spike.csv')

class Test_ManuallyCleanSig(unittest.TestCase):

    def setUp(self):
        return

    def test_manually_clean_sig_with_y(self):
        data = genfromtxt(TEST_SPIKE_DATA, delimiter=',', names=True)
        
        x = data['time']
        y = data['stress']

        x, y = manually_clean_sig(x, y)

        _fig, ax = plt.subplots()
        
        ax.plot(x, y)
        ax.grid()
        ax.set_title('Cleaned Signal')
        plt.show()

        self.assertEqual(0,1)

    def tearDown(self):
        return