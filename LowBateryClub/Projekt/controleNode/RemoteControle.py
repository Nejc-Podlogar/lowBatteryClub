#!/usr/bin/env python
# coding: utf-8

# In[20]:


#import setup_path 
import airsim
import pyaudio
import wave
import struct


class PPM_Signal:

    def __init__(self, **kwargs):

        self.FORMAT = pyaudio.paInt16
        self.CHUNK = 1024
        self.RATE = 44100
        self.CHANNELS = 1
        self.maxRange = 70  #Največje število impulzov na joysticku
        self.minRange = 25  #Najmanjše število impulzov na joysticku

        self.client = airsim.CarClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)
        self.car_controls = airsim.CarControls()

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT, frames_per_buffer=self.CHUNK,rate=self.RATE, channels=self.CHANNELS, input=True)    #Pridobivanje podatkov iz mikrofona

        self.counterNeg = 0
        self.counterPos = 0
        self.longPos = 0
        self.longNeg = 0

        self.channelCounter = -1
        self.Enice = True

        self.c1 = 0.0
        self.c2 = 0.0
        self.c3 = 0.0
        self.c4 = 0.0
        self.c5 = 0.0
        self.c6 = 0.0
        self.c7 = 0.0
        self.c8 = 0.0


    def driving(self, hitrost, smer):
        self.car_controls.throttle = hitrost;
        self.car_controls.steering = smer;

        self.client.setCarControls(self.car_controls);
        # time.sleep(trajanje);

    def reverse(self, hitrost, smer, prestava):

        self.car_controls.is_manual_gear = True
        self.car_controls.manual_gear = prestava
        self.car_controls.throttle = hitrost
        self.car_controls.steering = smer
        print("Drive reverse!")
        self.client.setCarControls(self.car_controls)
        # time.sleep(trajanje)

        #nastavimo nazaj na Auto prestave
        self.car_controls.is_manual_gear = False
        self.car_controls.manual_gear = 0

    def brake(self, bremza):

        self.car_controls.brake = bremza

        self.client.setCarControls(self.car_controls)
        # time.sleep(trajanje)
        #Odstranimo brake, da lahko nato normalno kličemo ostale funkcije za vožnjo.
        self.car_controls.brake = 0

    def run(self):
        data = self.stream.read(self.CHUNK)
        format = "%dh"%(self.CHUNK)
        shorts = struct.unpack( format, data )

        for s in shorts:
            if s < 0:
                self.counterNeg = self.counterNeg + 1
                if self.counterNeg == 10:
                    if self.channelCounter >= 0:
                        if self.channelCounter == 0:
                            self.c1 = ((self.counterPos - self.minRange) / (self.maxRange - self.minRange)) * 2 - 1
                        elif self.channelCounter == 1:
                            self.c2 = ((self.counterPos - self.minRange) / (self.maxRange - self.minRange)) * 2 - 1
                        elif self.channelCounter == 2:
                            self.c3 = ((self.counterPos - self.minRange) / (self.maxRange - self.minRange)) * 2 - 1
                        elif self.channelCounter == 3:
                            self.c4 = ((self.counterPos - self.minRange) / (self.maxRange - self.minRange)) * 2 - 1

                        elif self.channelCounter == 3:
                            self.c5 = ((self.counterPos - self.minRange) / (self.maxRange - self.minRange)) * 2 - 1

                        elif self.channelCounter == 5:
                            self.c6 = ((self.counterPos - self.minRange) / (self.maxRange - self.minRange)) * 2 - 1

                        elif self.channelCounter == 6:
                            self.c7 = ((self.counterPos - self.minRange) / (self.maxRange - self.minRange)) * 2 - 1

                        elif self.channelCounter == 7:
                            self.c8 = ((self.counterPos - self.minRange) / (self.maxRange - self.minRange)) * 2 - 1


                    self.counterPos = 0
                    self.longNeg = self.longNeg + 1

                    if self.Enice == True:
                        self.channelCounter += 1
                        self.Enice = False

            else:
                self.counterPos = self.counterPos + 1
                self.counterNeg = 0
                if self.counterPos == 22:
                    self.Enice = True

                if self.counterPos == 150:
                    print(self.c1,  self.c3,  self.c4,  self.c5, self.c6, self.c7, self.c8)

                    if self.c1 > 0:
                        self.driving(self.c3, self.c1)
                    elif self.c1 < 0:
                        self.reverse(self.c3, self.c1, -1)

                    self.channelCounter = -1
                if self.counterPos == 40:
                    self.longPos = self.longPos + 1
