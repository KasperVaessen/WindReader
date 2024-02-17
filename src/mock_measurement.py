import time
import numpy as np
import math

# Mock class for testing
class MeasureWindTunnel:
    def __init__(self, callback_attached=lambda: None, callback_detached=lambda: None):
        self.offset_lift = 0
        self.offset_drag = 0
        self.offset_diff_pressure = 0
        self.callback_attached = callback_attached
        self.callback_detached = callback_detached
        self.callback_attached()
        
    
    def zero_data(self, timesteps=5, interval=0.2, use_default=True, gain_lift=1000, gain_drag=1000):
        for _ in range(timesteps):
            self.offset_lift += -0.2
            self.offset_drag += 0.05
            self.offset_diff_pressure += 200
            time.sleep(interval)
        
        self.offset_lift /= timesteps
        self.offset_drag /= timesteps
        self.offset_diff_pressure /= timesteps

    def set_callback_attached(self, callback):
        self.callback_attached = callback
    
    def set_callback_detached(self, callback):
        self.callback_detached = callback
    
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
            v = 0
        return [lift, drag, atmospheric_pressure, temperature, diff_pressure, v]
    def close(self):
        pass



    




