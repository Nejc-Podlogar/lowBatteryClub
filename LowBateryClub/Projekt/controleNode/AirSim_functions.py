import airsim
import cv2
import os
import time
import pprint
import numpy as np

class Car:
    def __init__(self): #Konstruktor
        self.client = airsim.CarClient()
        self.client.enableApiControl(True)
        self.car_controls = airsim.CarControls()

    def returnClient(self):
        return self.client


    def changeApiConstrol(self):
        self.client.enableApiControl(False if self.client.isApiControlEnabled() else True)


    def connectToUnity(self):
        return airsim.CarClient()   #returna object s katerim kot argument kličemo ostale funkcije


    def checkConnectInfo(self): #preveris ce je povezava uspešna
        try:
            self.client.confirmConnection()
            return True
        except:
            return False


    def getCarState(self):  #gear, handbrake, rpm, speed
        try:
            return self.client.getCarState()
        except:
            return False;


    def getDistanceSensorData(self):    #distance, max_distance, min_distance
        try:
            return self.client.getDistanceSensorData()
        except:
            return False;


    def getImuData(self):
        try:
            self.client.simPrintLogMessage("TEST")
            return self.client.getImuData()
        except:
            return False;


    def getMagnetometerData(self):  #magnetic_field_body pa znotraj tega so x_val, y_val ter z_val
        try:
            return self.client.getMagnetometerData()
        except:
            return False

    def getSceneImage(self):
        responses = self.client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.Scene)])

        if responses[0].pixels_as_float:
            #print("Type %d, size %d, pos %s" % (responses[0].image_type, len(responses[0].image_data_float), pprint.pformat(responses[0].camera_position)))
            airsim.write_pfm(os.path.normpath('/temp/cv_mode_' + str(x) + "_" + '.pfm'), airsim.get_pfm_array(responses[0]))
        else:
            #print("Type %d, size %d, pos %s" % (responses[0].image_type, len(responses[0].image_data_uint8), pprint.pformat(responses[0].camera_position)))
            airsim.write_file('img.png', responses[0].image_data_uint8)


    def goForward(self, throttle, steering):
        self.car_controls.throttle = throttle
        self.car_controls.steering = steering
        self.client.setCarControls(self.car_controls)

        #time.sleep(0.01)

    def goReverse(self, gear, throttle, steering, time1):
        self.car_controls.throttle = throttle
        self.car_controls.is_manual_gear = True
        self.car_controls.manual_gear = gear
        self.car_controls.steering = steering
        self.client.setCarControls(self.car_controls)

        #time.sleep(time1)

        self.car_controls.is_manual_gear = False
        self.car_controls.manual_gear = 0

    def goBreak(self, breake, steering):
        self.car_controls.breake = breake
        #self.car_controls.steering = steering
        self.client.setCarControls(self.car_controls)

        #time.sleep(time1)
        self.car_controls.breake = 0


#if __name__ == "__main__":
    #x = Car()   #klic konstruktorja

    #client = airsim.CarClient()

    #print(client.simGetImage())

    #print(x.checkConnectInfo());

    #y = x.getCarState()
    #print(y.speed) #kako dobit posamezno komponento iz returna

    #y = x.getMagnetometerData()
    #print(y.magnetic_field_body.x_val)

    #print(x.getMagnetometerData())
