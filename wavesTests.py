import unittest
from waves import *

import matplotlib.pyplot as plt


class WavesTests(unittest.TestCase):
    def testSingleFreq(self):
        wave = Wave(4,8,10)
        plt.plot(wave.time,wave.data)
        plt.show()

    def testAdd(self):
        wave3 = Wave(4,8,10)
        wave1 = Wave(3,1,10)
        wave2= Wave(4,3,10)
        wave = wave1+wave2+wave3
        plt.plot(wave.time, wave.data)
        plt.show()

    def testMultiFreq(self):
        wave = Wave([4,3,4], [8,1,3], 10)
        plt.plot(wave.time, wave.data)
        plt.show()

    def testInvers(self):
        wave = -Wave([4, 3, 4], [8, 1, 3], 10)
        plt.plot(wave.time, wave.data)
        plt.show()


if __name__ == '__main__':
    unittest.main()
