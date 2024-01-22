from Measurement import MeasureWindTunnel, MeasureMock
import time

#Example usage
# windtunnel = MeasureWindTunnel()
windtunnel = MeasureMock()
windtunnel.zero_data()

timesteps = 50
for i in range(timesteps):
    print("Lift: %.3f kg, Drag: %.3f kg, Atmospheric pressure: %.2f kPa, Temperature: %.1f K, Diff pressure: %.1f Pa, velocity: %.1f m/s" % tuple(windtunnel.get_values()))
    time.sleep(0.5)
windtunnel.close()