import time
import unittest
from waves import *

import matplotlib.pyplot as plt

notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#"]


def doScaleConcatenate(waves):
    dataToPlay = np.empty([])

    for note in notes:
        for i in waves:
            dataToplay = np.append(dataToplay, i.data)

        for i in reversed(waves):
            dataToplay = np.append(dataToplay, i.data)

    for note in reversed(notes):
        for i in waves:
            dataToplay = np.append(dataToplay, i.data)

        for i in reversed(waves):
            dataToplay = np.append(dataToplay, i.data)

    return dataToPlay


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

    def testSoundPlay(self):
        wave =  Wave(27.5,0.01,200)
        wave.play()
        time.sleep(20)


class OctaveTest(unittest.TestCase):
    def testOctavePianoCreation(self):
        baseFreq = 440
        octave = Octave(440)

        octave.populateStorageWaves()
        for i in octave.wavesStorage:
            octave.wavesStorage[i].play()
            time.sleep(1)

    def testMjScale(self):
        baseFreq = 220
        octave = Octave(baseFreq)

        octave.populateStorageWaves(duration=0.1)
        dataToplay = np.empty()

        for note in notes:
            dataToplay = np.append(dataToplay,doScaleConcatenate(octave.majorScale(note)))

        sd.play(dataToplay)
        time.sleep(40)

    def testMinNaturalScale(self):
        baseFreq = 220
        octave = Octave(baseFreq)

        octave.populateStorageWaves(duration=0.1)
        dataToplay = np.empty()

        for note in notes:
            dataToplay = np.append(dataToplay, doScaleConcatenate(octave.minorNaturalScale(note)))

        plt.plot(dataToplay)
        sd.play(dataToplay)
        time.sleep(40)
        plt.show()

if __name__ == '__main__':
    unittest.main()
