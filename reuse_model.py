import numpy as np

# Load the Q-table from a file
Q = np.load("model_1M.npy")
print("Q-table loaded from q_table_1M.npy")

# Device data (same as before)
devices = {
    "Dish Washer": {"duration": 120, "consumption": 0.7, "start_range": (14 * 60, 22 * 60), "flexible": False},  
    "Washing Machine": {"duration": 90, "consumption": 1.1, "start_range": (10 * 60, 18 * 60), "flexible": False},  
    # Add the rest of the devices...
}

# Generate a schedule using the loaded Q-table
learned_schedule = {}
for device in devices:
    device_index = list(devices.keys()).index(device)
    start_range = devices[device]["start_range"]
    if start_range[1] > start_range[0]:  # Normal range
        best_start_minute = np.argmax(Q[device_index, start_range[0]:start_range[1]]) + start_range[0]
    else:  # Cyclic range
        q_values = np.concatenate((Q[device_index, start_range[0]:], Q[device_index, :start_range[1]]))
        best_start_minute = (np.argmax(q_values) + start_range[0]) % (24 * 60)
    learned_schedule[device] = best_start_minute

# Print the schedule
print("\nOptimal Schedule:")
for device, start_minute in learned_schedule.items():
    print(f"{device} - {start_minute // 60}:{start_minute % 60:02d}")