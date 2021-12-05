import math

import numpy as np
import sounddevice as sd
from enum import Enum

class Filter:
    def __init__(self,duration,rate=44100):
        self.rate = rate
        self.duration = duration
        self.time = np.linspace(0,duration,int(rate*duration))

        self.calculateData()
    def calculateData(self):
        pass

class LinearFilter(Filter):
    def __init__(self):
        super(self)

    def calculateData(self):
        self.data = np.array(
            [1 for i in range(0,self.rate*self.duration)]
        )

class GaussianFilter(Filter):
    def calculateData(self):
        self.data =  np.exp(-np.square(self.time-self.duration/2)
                  /np.square(self.duration/4))

class RCChargeFilter(Filter):
    def calculateData(self):
        #TODO how can i use parameters to fit good the filter(?)
        self.data = (1-np.exp(-self.time))

class RCDischargeFilter(Filter):
    def calculateData(self):
        # TODO how can i use parameters to fit good the filter(?)
        self.data = np.exp(-self.time)



class Wave:
    def __init__(self,freq,ampl,duration,rate=44100):
        self.frequency = freq if type(freq)==list else [freq]
        self.amplitude = ampl if type(ampl)==list else [ampl]
        self.duration = duration

        self.time = np.linspace(0,self.duration,int(rate*duration))


        self.data = np.sum([
           np.exp(-np.square(self.time-duration/2)
                  /np.square(duration/4))
            *a*np.sin(
                2*math.pi*f*self.time)
            for a,f in zip(self.amplitude,self.frequency)],0)

        self.rate = rate
    def __add__(self, other):
        rate = max([self.rate,other.rate])
        freq = self.frequency + other.frequency
        amp = self.amplitude + other.amplitude
        duration = max([self.duration,other.duration])
        return Wave(freq,amp,duration,rate)

    def __neg__(self):
        self.data = -self.data
        return self
    def __sub__(self, other):
        self.__add__(self,-other)

    def __eq__(self, other):
        return self.frequency == other.frequency and self.amplitude == other.amplitude


    def play(self):
        sd.play(self.data,self.rate)





class TONES(Enum):
    TONE = 2
    SEMITONE = 1
    THREESEMITONE = 6


class Octave():
    def __init__(self,baseFrequency):
        self.notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B",
                     "C1","C1#","D1","D1#","E1","F1","F1#","G1","G1#","A1","A1#","B1"]
        self.equivalence = {
            "C#": "Db",
            "D#": "Eb",
            "F#": "Gb",
            "G#": "Ab",
            "A#": "Bb",
            "C1#":"D1b"
        }
        self.baseFreq = baseFrequency
        self.freqMap = {}
        self.wavesStorage = {}


        self.mjScale = [
            TONES.TONE,TONES.TONE,TONES.SEMITONE,
            TONES.TONE,TONES.TONE,TONES.TONE,TONES.SEMITONE]

        self.arabScale = [
            TONES.SEMITONE, TONES.THREESEMITONE, TONES.SEMITONE,
            TONES.TONE, TONES.SEMITONE, TONES.THREESEMITONE, TONES.SEMITONE
        ]

        self.mjArmonicScale = [
            TONES.TONE,TONES.TONE,TONES.TONE,
            TONES.TONE,TONES.SEMITONE,TONES.SEMITONE
        ]

        self.minNaturalScale = [
            TONES.TONE, TONES.SEMITONE, TONES.TONE,
            TONES.TONE, TONES.SEMITONE, TONES.TONE, TONES.TONE
        ]


        self.mjNeapolitan = [
            TONES.SEMITONE, TONES.TONE, TONES.TONE,
            TONES.TONE, TONES.SEMITONE, TONES.THREESEMITONE, TONES.SEMITONE
        ]

        self.minNeapolitan = [
            TONES.TONE, TONES.TONE, TONES.SEMITONE,
            TONES.TONE, TONES.TONE, TONES.TONE, TONES.SEMITONE
        ]


        self.populateWaves()

    def populateWaves(self):
        for i,n in enumerate(self.notes):
            self.freqMap[n] = self.baseFreq*(2**(i/12))

    def populateStorageWaves(self,duration):
        for i in self.notes:
            self.createWave(i,duration=duration)

    def createWave(self,note,amp=0.1,duration=1):
        if note not in self.wavesStorage.keys():
            self.wavesStorage[note] = Wave(
            self.freqMap[note],amp,duration
        )
        return self.wavesStorage[note]


    def majorScale(self,fromWhere):
        baseOff = self.notes.index(fromWhere)
        toRet = [self.wavesStorage[self.notes[baseOff]]]
        for i in self.mjScale:
            baseOff = baseOff+i.value
            toRet.append(self.wavesStorage[self.notes[baseOff]])
        return toRet

    def minorNaturalScale(self):
        return [self.wavesStorage[i] for i in self.minNaturalScale]






