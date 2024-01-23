import math
import time
import numpy as np
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *

class MeasureWindTunnel:
    def __init__(self):
    # Initialize channels
        self.lift_channel = VoltageRatioInput()
        self.drag_channel = VoltageRatioInput()
        self.atmospheric_pressure_channel = VoltageRatioInput()
        self.temperature_channel = VoltageRatioInput()
        self.diff_pressure_channel = VoltageRatioInput()

        #Connect channels to corresponding ports on correct phidget
        self.lift_channel.setDeviceSerialNumber(141133)
        self.lift_channel.setChannel(0)
        self.lift_channel.openWaitForAttachment(5000)

        self.drag_channel.setDeviceSerialNumber(141133)
        self.drag_channel.setChannel(1)
        self.drag_channel.openWaitForAttachment(5000)

        self.atmospheric_pressure_channel.setDeviceSerialNumber(149027)
        self.atmospheric_pressure_channel.setChannel(0)
        self.atmospheric_pressure_channel.openWaitForAttachment(5000)

        self.temperature_channel.setDeviceSerialNumber(149027)
        self.temperature_channel.setChannel(1)
        self.temperature_channel.openWaitForAttachment(5000)

        self.diff_pressure_channel.setDeviceSerialNumber(149027)
        self.diff_pressure_channel.setChannel(2)
        self.diff_pressure_channel.openWaitForAttachment(5000)

        # Set data meassure rate
        self.lift_channel.setDataInterval(32)
        self.drag_channel.setDataInterval(32)

        # Set bridge gain (128 means very accurate, but low range, but the range is big enough for our application)
        self.lift_channel.setBridgeGain(BridgeGain.BRIDGE_GAIN_128)
        self.drag_channel.setBridgeGain(BridgeGain.BRIDGE_GAIN_128)

        # Set sensor type
        self.atmospheric_pressure_channel.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1115)
        self.temperature_channel.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1124)
        self.diff_pressure_channel.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1136)

        self.offset_lift = 0
        self.offset_drag = 0
        self.offset_diff_pressure = 0
        self.gain_lift = 1000
        self.gain_drag = 1000
        self.gain_diff_pressure = 1000

    def zero_data(self, proper=True, timesteps=5, interval=0.2):
        for _ in range(timesteps):
            self.offset_lift += self.lift_channel.getVoltageRatio()
            self.offset_drag += self.drag_channel.getVoltageRatio()
            self.offset_diff_pressure += self.diff_pressure_channel.getSensorValue()
            time.sleep(interval)
        
        self.offset_lift /= 5
        self.offset_drag /= 5
        self.offset_diff_pressure /= 5
        if proper:
            self.gain_lift = 9907.67275888859 # calculated by control panel
            self.gain_drag = 11148.3112741824 # calculated by control panel

    def get_values(self):
        lift = (self.lift_channel.getVoltageRatio()-self.offset_lift)*self.gain_lift*9.81
        drag = (self.drag_channel.getVoltageRatio()-self.offset_drag)*self.gain_drag*9.81
        atmospheric_pressure = self.atmospheric_pressure_channel.getSensorValue()
        temperature = self.temperature_channel.getSensorValue()+273.15
        diff_pressure = (self.diff_pressure_channel.getSensorValue() - self.offset_diff_pressure)*self.gain_diff_pressure

        c_algGasConst = 8.31
        c_molMassa = 0.0288
        # Ideal gas law: pV = nRT
        airDensity = c_molMassa * atmospheric_pressure * 1000 / (c_algGasConst * temperature)
        if diff_pressure > 0:
            # dynamic pressure: q = 1/2 * rho * v^2
            v = math.sqrt(2 * diff_pressure / airDensity)
        else:
            v = -9999
        return [lift, drag, atmospheric_pressure, temperature, diff_pressure, v]
    
    def close(self):
        self.lift_channel.close()
        self.drag_channel.close()
        self.atmospheric_pressure_channel.close()
        self.temperature_channel.close()
        self.diff_pressure_channel.close()

    # def set_on_attach_handler(self, handler):
    #     self.lift_channel.setOnAttachHandler(handler)
    #     self.drag_channel.setOnAttachHandler(handler)
    #     self.atmospheric_pressure_channel.setOnAttachHandler(handler)
    #     self.temperature_channel.setOnAttachHandler(handler)
    #     self.diff_pressure_channel.setOnAttachHandler(handler)


class MeasureMock:
    def __init__(self):
        self.offset_lift = 0
        self.offset_drag = 0
        self.offset_diff_pressure = 0
    def zero_data(self, proper=True, timesteps=5, interval=0.2):
        for _ in range(timesteps):
            self.offset_lift += -0.2
            self.offset_drag += 0.05
            self.offset_diff_pressure += 200
            time.sleep(interval)
        
        self.offset_lift /= 5
        self.offset_drag /= 5
        self.offset_diff_pressure /= 5
    def get_values(self):
        lift = (np.random.normal(-0.2, 0.1)-self.offset_lift)*9.81
        drag = (np.random.normal(0.05, 0.01)-self.offset_drag)*9.81
        atmospheric_pressure = 100.85
        temperature = 294.9
        diff_pressure = np.random.normal(200, 20)-self.offset_diff_pressure

        c_algGasConst = 8.31
        c_molMassa = 0.0288
        # Ideal gas law: pV = nRT
        airDensity = c_molMassa * atmospheric_pressure * 1000 / (c_algGasConst * temperature)
        if diff_pressure > 0:
            # dynamic pressure: q = 1/2 * rho * v^2
            v = math.sqrt(2 * diff_pressure / airDensity)
        else:
            v = -9999
        return [lift, drag, atmospheric_pressure, temperature, diff_pressure, v]
    def close(self):
        pass



    




