import math

import numpy as np


class Wave:
    def __init__(self,freq,ampl,duration,rate=44100):
        self.frequency = freq if type(freq)==list else [freq]
        self.amplitude = ampl if type(ampl)==list else [ampl]
        self.duration = duration

        self.time = np.linspace(0,self.duration,int(rate*duration))
        self.data = np.sum([
            a*np.sin(
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





class Octave():
    def __init__(self,baseFrequency):
        notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        equivalence = {
            "C#": "Db",
            "D#": "Eb",
            "F#": "Gb",
            "G#": "Ab",
            "A#": "Bb",
        }
        self.baseFreq = baseFrequency
        self.freqMap = {}

    def populateWaves(self):
        for i,n in enumerate(self.notes):
            self.freqMap[n] = self.baseFreq*(2**(i/12))

    def createWave(self,note,):
        return Wave(
            self.freqMap[note]
        )






