from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
import time
import matplotlib.pyplot as plt

def plotDynamically(chan, am_seconds):
    timesteps = am_seconds*10
    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 8))
    line1, = ax.plot([0 for _ in range(timesteps)])

    X = [0 for _ in range(timesteps)]
    for i in range(timesteps):
        try:
            X[i:len(X)] = [chan.getSensorValue() for _ in range(len(X)-i)]
        except PhidgetException as e:
            X[i:len(X)] = [chan.getVoltageRatio()*1000000 for _ in range(len(X)-i)]
        line1.set_ydata(X)
        figure.canvas.draw()
        ax.set_ylim(min(X), max(X))
        figure.canvas.flush_events()
        time.sleep(0.1)


# Setup Bridge: 0=lift(kg), 1=drag(kg), moet geconvert en gezeroed worden (convert *1000 - nul waarde. Niet echt calibratie proces)
# If properly calibrated, the following values should be used: 0.8 mV/V rated output, with 0.78kg max capacity
# https://www.phidgets.com/?prodid=223#Tab_Specifications
bridge = [VoltageRatioInput(), VoltageRatioInput()]
for i, ch in enumerate(bridge):
    ch.setDeviceSerialNumber(141133)
    ch.setChannel(i)
    ch.openWaitForAttachment(5000)

# Setup Interface 0=atmospheric pressure(kPa), 1=temperature(C), 2=diff Pressure(kPa, maar moet Pa, ook nog zeroën)
interface = [VoltageRatioInput(), VoltageRatioInput(), VoltageRatioInput()]
for i, ch in enumerate(interface):
    ch.setDeviceSerialNumber(149027)
    ch.setChannel(i)
    ch.openWaitForAttachment(5000)

# Settings for Bridge 
for ch in bridge:
    ch.setDataInterval(32)
    ch.setBridgeGain(BridgeGain.BRIDGE_GAIN_128)

interface[0].setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1115)
interface[1].setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1124)
interface[2].setSensorType(VoltageRatioSensorType.SENSOR_TYPE_1136)


# TODO: how to calibrate the bridge sensors?
plotDynamically(bridge[0], 10)




# try:
#     input("Press Enter to Stop\n")
#     for ch in bridge:
#         ch.close()
# except (Exception, KeyboardInterrupt):
#     pass