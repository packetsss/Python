# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from simple_pid import PID
pid = PID(1, 0.1, 0.05, setpoint=1)
# steering: (0.1, 0.0005, 0.35)
# throttle: (0.25, 0.0, 0.005)

# Assume we have a system we want to control in controlled_system
# v = controlled_system.update(0)


# Compute new output from the PID according to the systems current value
control = pid(0)
print(control)

print(control)
control = pid(32)
print(control)

# Feed the PID output to the system and get its current value
# v = controlled_system.update(control)

