import math
import time
from Phidget22.Devices.VoltageRatioInput import VoltageRatioInput, BridgeGain, VoltageRatioSensorType

class MeasureWindTunnel:
    def __init__(self, callback_attached=lambda: None, callback_detached=lambda: None):
    # Initialize channels
        self.lift_channel = VoltageRatioInput()
        self.drag_channel = VoltageRatioInput()
        self.atmospheric_pressure_channel = VoltageRatioInput()
        self.temperature_channel = VoltageRatioInput()
        self.diff_pressure_channel = VoltageRatioInput()

        # List to keep track of which channels are attached
        self.attached = [False, False, False, False, False]
        self.callback_attached = callback_attached
        self.callback_detached = callback_detached

        #Connect channels to corresponding ports on correct phidget
        self.lift_channel.setDeviceSerialNumber(141133)
        self.lift_channel.setChannel(0)

        self.drag_channel.setDeviceSerialNumber(141133)
        self.drag_channel.setChannel(1)

        self.atmospheric_pressure_channel.setDeviceSerialNumber(149027)
        self.atmospheric_pressure_channel.setChannel(0)

        self.temperature_channel.setDeviceSerialNumber(149027)
        self.temperature_channel.setChannel(1)

        self.diff_pressure_channel.setDeviceSerialNumber(149027)
        self.diff_pressure_channel.setChannel(2)

        # Set function to execute when phidgets are attached
        self.lift_channel.setOnAttachHandler(self.__on_attach_handler)
        self.drag_channel.setOnAttachHandler(self.__on_attach_handler)
        self.atmospheric_pressure_channel.setOnAttachHandler(self.__on_attach_handler)
        self.temperature_channel.setOnAttachHandler(self.__on_attach_handler)
        self.diff_pressure_channel.setOnAttachHandler(self.__on_attach_handler)

        # Set function to execute when phidgets are detached
        self.lift_channel.setOnDetachHandler(self.__on_detach_handler)
        self.drag_channel.setOnDetachHandler(self.__on_detach_handler)
        self.atmospheric_pressure_channel.setOnDetachHandler(self.__on_detach_handler)
        self.temperature_channel.setOnDetachHandler(self.__on_detach_handler)
        self.diff_pressure_channel.setOnDetachHandler(self.__on_detach_handler)

        self.lift_channel.open()
        self.drag_channel.open()
        self.atmospheric_pressure_channel.open()
        self.temperature_channel.open()
        self.diff_pressure_channel.open()

        self.offset_lift = 0
        self.offset_drag = 0
        self.offset_diff_pressure = 0
        self.gain_lift = 9907.67275888859 # calculated by control panel
        self.gain_drag = 11148.3112741824 # calculated by control panel
        self.gain_diff_pressure = 1000

    # Zero data by taking the average of the first timesteps, and set the gain
    def zero_data(self, timesteps=5, interval=0.2, use_default=True, gain_lift=1000, gain_drag=1000):
        self.offset_lift = 0
        self.offset_drag = 0
        self.offset_diff_pressure = 0
        
        for _ in range(timesteps):
            self.offset_lift += self.lift_channel.getVoltageRatio()
            self.offset_drag += self.drag_channel.getVoltageRatio()
            self.offset_diff_pressure += self.diff_pressure_channel.getSensorValue()
            time.sleep(interval)
        
        self.offset_lift /= timesteps
        self.offset_drag /= timesteps
        self.offset_diff_pressure /= timesteps
        if not use_default:
            self.gain_lift = gain_lift
            self.gain_drag = gain_drag
    
    def set_callback_attached(self, callback):
        self.callback_attached = callback
    
    def set_callback_detached(self, callback):
        self.callback_detached = callback

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
            v = 0
        return [lift, drag, atmospheric_pressure, temperature, diff_pressure, v]
    
    # Close all channels, to allow other programs to use them
    def close(self):
        self.lift_channel.close()
        self.drag_channel.close()
        self.atmospheric_pressure_channel.close()
        self.temperature_channel.close()
        self.diff_pressure_channel.close()

    # Calls self.callback_attached when all phidgets are attached
    def __on_attach_handler(self, phidget):
        serial = phidget.getDeviceSerialNumber()
        port = phidget.getChannel()
        if serial == 141133:
            if port == 0:
                self.attached[0] = True
                phidget.setDataInterval(32)
                phidget.setBridgeGain(BridgeGain.BRIDGE_GAIN_128)
            elif port == 1:
                self.attached[1] = True
                phidget.setDataInterval(32)
                phidget.setBridgeGain(BridgeGain.BRIDGE_GAIN_128)
        elif serial == 149027:
            if port == 0:
                self.attached[2] = True
                phidget.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1115)
            elif port == 1:
                self.attached[3] = True
                phidget.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1124)
            elif port == 2:
                self.attached[4] = True
                phidget.setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1136)
        if all(self.attached):
            self.callback_attached()
    
    # Calls self.callback_detached when one phidgets is detached
    def __on_detach_handler(self, phidget):
        serial = phidget.getDeviceSerialNumber()
        port = phidget.getChannel()
        if serial == 141133:
            if port == 0:
                self.attached[0] = False
            elif port == 1:
                self.attached[1] = False
        elif serial == 149027:
            if port == 0:
                self.attached[2] = False
            elif port == 1:
                self.attached[3] = False
            elif port == 2:
                self.attached[4] = False
        # Only call when one is detached, to prevent multiple callbacks
        if sum(self.attached) == 4:
            self.callback_detached()