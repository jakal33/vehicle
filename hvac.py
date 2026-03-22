import matplotlib.pyplot as plt

class VehicleHVAC:
    def __init__(self, cabin_temp=25.0, outside_temp=30.0, hvac_power=5.0):
        """
        cabin_temp: initial cabin temperature in °C
        outside_temp: outside temperature in °C
        hvac_power: rate at which HVAC changes temperature (°C per minute)
        """
        self.cabin_temp = cabin_temp
        self.outside_temp = outside_temp
        self.hvac_power = hvac_power
        self.fan_speed = 1  # 1 (low) to 5 (high)
        self.target_temp = cabin_temp
    
    def set_target_temperature(self, temp):
        self.target_temp = temp
    
    def set_fan_speed(self, speed):
        self.fan_speed = max(1, min(speed, 5))  # clamp 1-5
    
    def step(self, dt=1.0):
        """
        Advance simulation by dt minutes.
        """
        # HVAC effect (proportional to difference from target and fan speed)
        temp_diff = self.target_temp - self.cabin_temp
        hvac_effect = self.hvac_power * self.fan_speed * (temp_diff / abs(temp_diff) if temp_diff != 0 else 0)
        
        # Cabin temperature changes
        # 70% HVAC effect, 30% passive heat transfer with outside
        passive_effect = 0.1 * (self.outside_temp - self.cabin_temp)
        self.cabin_temp += dt * (0.7 * hvac_effect + passive_effect)
        
        return self.cabin_temp

# Simulation parameters
sim_time = 60  # minutes
hvac = VehicleHVAC(cabin_temp=25, outside_temp=35, hvac_power=2)
hvac.set_target_temperature(22)
hvac.set_fan_speed(2)

# Run simulation
cabin_temps = []
time = []

for t in range(sim_time):
    cabin_temps.append(hvac.step())
    time.append(t)

# Plot results
plt.plot(time, cabin_temps, label='Cabin Temp')
plt.axhline(hvac.target_temp, color='r', linestyle='--', label='Target Temp')
plt.xlabel('Time (minutes)')
plt.ylabel('Cabin Temperature (°C)')
plt.title('Vehicle HVAC Simulation')
plt.legend()
plt.grid(True)
plt.show()
