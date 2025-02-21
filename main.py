import numpy as np
import random

# Device data (durations and start ranges are now in minutes)
devices = {
    "Dish Washer": {"duration": 120, "consumption": 0.7, "start_range": (14 * 60, 22 * 60), "flexible": False},  
    "Washing Machine": {"duration": 90, "consumption": 1.1, "start_range": (10 * 60, 18 * 60), "flexible": False},  
    "Cloth Dryer": {"duration": 90, "consumption": 2.2, "start_range": (18 * 60, 22 * 60), "flexible": False},  
    "Oven 1": {"duration": 90, "consumption": 1.07, "start_range": (18 * 60 + 30, 22 * 60), "flexible": False},  
    "Oven 2": {"duration": 90, "consumption": 1.07, "start_range": (12 * 60, 14 * 60 + 30), "flexible": False},  
    "Cook Top": {"duration": 30, "consumption": 1.64, "start_range": (18 * 60 + 30, 22 * 60), "flexible": False},  
    "Microwave": {"duration": 12, "consumption": 1.0, "start_range": (8 * 60, 14 * 60), "flexible": False},  
    "Electric Vehicle": {"duration": 240, "consumption": 7.0, "start_range": (8 * 60, 6 * 60), "flexible": False},  
    "Laptop": {"duration": 120, "consumption": 0.05, "start_range": (17 * 60, 23 * 60), "flexible": False},  
    "Vacuum Cleaner": {"duration": 60, "consumption": 0.9, "start_range": (10 * 60, 14 * 60), "flexible": False},  
    "Air Conditioner 1": {"duration": 90, "consumption": 0.8, "start_range": (8 * 60, 11 * 60), "flexible": False},  
    "Air Conditioner 2": {"duration": 90, "consumption": 0.8, "start_range": (19 * 60, 22 * 60), "flexible": False},  
    "Water Heater": {"duration": 120, "consumption": 3.2, "start_range": (17 * 60, 22 * 60), "flexible": False},  
    "Refrigerator": {"duration": 1440, "consumption": 0.22, "start_range": (0, 23 * 60), "flexible": True},  
    "Lighting 1": {"duration": 180, "consumption": 2.1, "start_range": (7 * 60, 10 * 60), "flexible": True},  
    "Lighting 2": {"duration": 420, "consumption": 2.1, "start_range": (6 * 60, 23 * 60), "flexible": True},
}

# Electricity prices (example for 24 hours, in $/kWh)
electricity_prices = [
    0.10709, 0.104, 0.1, 0.08566, 0.085, 0.08553, 0.09507, 0.10307, 0.065, 0.04734, 0.001, 0.00054,
    0.00224, 0.00324, 0.0651, 0.09691, 0.09744, 0.094, 0.09858, 0.10103, 0.10572, 0.10105, 0.10319, 0.09905
]

# RL parameters
num_episodes = 10000  # Number of tries
learning_rate = 0.1
discount_factor = 0.95
epsilon = 1.0
epsilon_decay = 0.995
min_epsilon = 0.01

# Weights for the reward function
alpha = 0.5  # Weight for total cost
beta = 0.5   # Weight for total waiting time

# Initialize Q-table
num_devices = len(devices)
num_minutes = 24 * 60  # 1440 minutes in a day
Q = np.zeros((num_devices, num_minutes))

# Helper function to calculate total cost and total waiting time
def calculate_metrics(schedule):
    total_cost = 0
    total_waiting_time = 0
    for device, start_minute in schedule.items():
        duration = devices[device]["duration"]
        consumption = devices[device]["consumption"]
        earliest_start = devices[device]["start_range"][0]
        
        #duration 2 hours
        #23:00 - 06:00
        # Εστω οτι ξεκινάει 02:00
        # Αρα 120
        # 120 - 1380
        # max(0, 120 - 1380)

        # changed code
        if start_minute >= earliest_start:
            waiting_time = start_minute - earliest_start
        else:
            waiting_time = (1440 - earliest_start) + start_minute
        waiting_time = max(0, start_minute - earliest_start)
        total_waiting_time += waiting_time

        # Calculate the cost for each minute the device is running
        #print(f"\nDevice: {device} (Start: {start_minute // 60}:{start_minute % 60:02d}, Duration: {duration} minutes)")
        device_cost = 0
        for minute_offset in range(duration):
            minute = (start_minute + minute_offset) % num_minutes  # Handle wrap-around for overnight devices
            hour = minute // 60  # Convert minute to hour for electricity price lookup
            price = electricity_prices[hour]
            device_cost += consumption * (price / 60)  # Cost per minute
            #if minute_offset % 60 == 0:  # Print every hour
                #print(f"  Minute {minute // 60}:{minute % 60:02d}, Price: ${price:.5f}/kWh, Consumption: {consumption / 60:.5f} kWh/min, Cost: ${consumption * (price / 60):.5f}")
        total_cost += device_cost
        #print(f"Total cost for {device}: ${device_cost:.5f}")

    return total_cost, total_waiting_time

# Training the RL agent
for episode in range(num_episodes):
    schedule = {}
    for device in devices:
        start_range = devices[device]["start_range"]
        if start_range[1] > start_range[0]:  # Normal range (e.g., 14:00-22:00)
            if random.random() < epsilon:  # Explore
                #print(random.randint(start_range[0], start_range[1] - devices[device]["duration"]))
                if not devices[device]["flexible"]:
                    start_minute = random.randint(start_range[0], start_range[1] - devices[device]["duration"])
                else:
                    start_minute = start_range[0]
            else:  # Exploit
                device_index = list(devices.keys()).index(device)
                start_minute = np.argmax(Q[device_index, start_range[0]:start_range[1]]) + start_range[0]
        else:  # Cyclic range (e.g., 23:00-07:00)
            if random.random() < epsilon:  # Explore
                if not devices[device]["flexible"]:
                    start_minute = random.choice(
                    list(range(start_range[0], num_minutes)) + list(range(0, start_range[1]))
                )
                else:
                    start_minute = start_range[0]
            else:  # Exploit
                device_index = list(devices.keys()).index(device)
                q_values = np.concatenate((Q[device_index, start_range[0]:], Q[device_index, :start_range[1]]))
                start_minute = (np.argmax(q_values) + start_range[0]) % num_minutes
        schedule[device] = start_minute

    # Calculate metrics
    total_cost, total_waiting_time = calculate_metrics(schedule)
    #print(total_cost, total_waiting_time)
    reward = - (alpha * total_cost + beta * total_waiting_time)

    # Update Q-table
    for device, start_minute in schedule.items():
        device_index = list(devices.keys()).index(device)
        Q[device_index, start_minute] += learning_rate * (reward + discount_factor * np.max(Q[device_index, :]) - Q[device_index, start_minute])

    # Decay epsilon
    epsilon = max(min_epsilon, epsilon * epsilon_decay)

# Save the Q-table to a file
np.save("q_table.npy", Q)
print("Q-table saved to q_table.npy")

# Print the learned schedule
learned_schedule = {}
for device in devices:
    device_index = list(devices.keys()).index(device)
    start_range = devices[device]["start_range"]
    if start_range[1] > start_range[0]:  # Normal range
        best_start_minute = np.argmax(Q[device_index, start_range[0]:start_range[1]]) + start_range[0]
    else:  # Cyclic range
        q_values = np.concatenate((Q[device_index, start_range[0]:], Q[device_index, :start_range[1]]))
        best_start_minute = (np.argmax(q_values) + start_range[0]) % num_minutes
    learned_schedule[device] = best_start_minute

#save

print("\nOptimal Schedule:")
for device, start_minute in learned_schedule.items():
    print(f"{device} - {start_minute // 60}:{start_minute % 60:02d}")

# Calculate and print the total cost and waiting time
total_cost, total_waiting_time = calculate_metrics(learned_schedule)

print(f"\nTotal loops: {num_episodes}")
print(f"\nTotal Cost: ${total_cost:.5f}")
print(f"Total Waiting Time: {total_waiting_time%60} minutes")