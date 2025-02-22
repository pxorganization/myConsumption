import numpy as np

# Load the Q-table from a file
Q = np.load("../43_100_lightwave.npy")

num_minutes = 24 * 60  # 1440 minutes in a day

# Device data (durations and start ranges are now in minutes)
devices = {
    "Dish Washer": {"duration": 120, "consumption": 0.7, "start_range": (14 * 60, 22 * 60), "flexible": False},  
    "Washing Machine": {"duration": 90, "consumption": 1.1, "start_range": (10 * 60, 18 * 60), "flexible": False},  
    "Cloth Dryer": {"duration": 90, "consumption": 2.2, "start_range": (18 * 60, 22 * 60), "flexible": False},  
    "Oven 1": {"duration": 90, "consumption": 1.07, "start_range": (18 * 60 + 30, 22 * 60), "flexible": False},  
    "Oven 2": {"duration": 90, "consumption": 1.07, "start_range": (12 * 60, 14 * 60 + 30), "flexible": False},  
    "Cook Top": {"duration": 30, "consumption": 1.64, "start_range": (18 * 60 + 30, 22 * 60), "flexible": False},  
    "Microwave": {"duration": 12, "consumption": 1.0, "start_range": (8 * 60, 14 * 60), "flexible": False},  
    "Electric Vehicle": {"duration": 240, "consumption": 7.0, "start_range": (23 * 60, 6 * 60), "flexible": False},  
    "Laptop": {"duration": 120, "consumption": 0.05, "start_range": (17 * 60, 23 * 60), "flexible": False},  
    "Vacuum Cleaner": {"duration": 60, "consumption": 0.9, "start_range": (10 * 60, 14 * 60), "flexible": False},  
    "Air Conditioner 1": {"duration": 90, "consumption": 0.8, "start_range": (8 * 60, 11 * 60), "flexible": False},  
    "Air Conditioner 2": {"duration": 90, "consumption": 0.8, "start_range": (19 * 60, 22 * 60), "flexible": False},  
    "Water Heater": {"duration": 120, "consumption": 3.2, "start_range": (17 * 60, 22 * 60), "flexible": False},  
    "Refrigerator": {"duration": 1440, "consumption": 0.22, "start_range": (0, 23 * 60), "flexible": True},  
    "Lighting 1": {"duration": 180, "consumption": 2.1, "start_range": (7 * 60, 10 * 60), "flexible": True},  
    "Lighting 2": {"duration": 420, "consumption": 2.1, "start_range": (18 * 60, 1 * 60), "flexible": True},
}

# Print the learned schedule
learned_schedule = {}
for device in devices:
    device_index = list(devices.keys()).index(device)
    start_range = devices[device]["start_range"]
    
    if devices[device]["flexible"]:
        # For flexible devices, always start at the earliest possible time
        best_start_minute = start_range[0]
    else:
        if start_range[1] > start_range[0]:  # Normal range
            best_start_minute = np.argmax(Q[device_index, start_range[0]:start_range[1]]) + start_range[0]
        else:  # Cyclic range
            q_values = np.concatenate((Q[device_index, start_range[0]:], Q[device_index, :start_range[1]]))
            best_start_minute = (np.argmax(q_values) + start_range[0]) % num_minutes
    
    learned_schedule[device] = best_start_minute

print("\nOptimal Schedule:")
for device, start_minute in learned_schedule.items():
    print(f"{device} - {start_minute // 60}:{start_minute % 60:02d}")