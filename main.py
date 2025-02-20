import numpy as np
import random

# Device data (durations and start ranges are now in minutes)
devices = {
    "Dish Washer": {"duration": 120, "consumption": 0.7, "start_range": (14 * 60, 22 * 60)},  # 14:00-22:00
    "Washing Machine": {"duration": 90, "consumption": 0.5, "start_range": (10 * 60, 20 * 60)},  # 10:00-20:00
    "Cloth Dryer": {"duration": 120, "consumption": 1.0, "start_range": (12 * 60, 22 * 60)},  # 12:00-22:00
    "Oven": {"duration": 90, "consumption": 2.0, "start_range": (18 * 60, 22 * 60)},  # 18:00-22:00
    "Vacuum Cleaner": {"duration": 60, "consumption": 0.3, "start_range": (9 * 60, 18 * 60)},  # 9:00-18:00
    "Water Heater": {"duration": 180, "consumption": 1.5, "start_range": (6 * 60, 23 * 60)},  # 6:00-23:00
    "Air Conditioner": {"duration": 480, "consumption": 1.2, "start_range": (8 * 60, 22 * 60)},  # 8:00-22:00
    "Microwave": {"duration": 30, "consumption": 1.0, "start_range": (7 * 60, 22 * 60)},  # 7:00-22:00
    "Night Device": {"duration": 240, "consumption": 0.8, "start_range": (23 * 60, 7 * 60)},  # 23:00-7:00
    "Night Device": {"duration": 330, "consumption": 1.2, "start_range": (1 * 60, 23 * 60)},  # 01:00-23:00
}

# Electricity prices (example for 24 hours, in $/kWh)
electricity_prices = [
    0.10709, 0.104, 0.1, 0.08566, 0.085, 0.08553, 0.09507, 0.10307, 0.065, 0.04734, 0.001, 0.00054,
    0.00224, 0.00324, 0.0651, 0.09691, 0.09744, 0.094, 0.09858, 0.10103, 0.10572, 0.10105, 0.10319, 0.09905
]

# RL parameters
num_episodes = 1  # Number of tries
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
        waiting_time = max(0, start_minute - earliest_start)
        total_waiting_time += waiting_time

        # Calculate the cost for each minute the device is running
        print(f"\nDevice: {device} (Start: {start_minute // 60}:{start_minute % 60:02d}, Duration: {duration} minutes)")
        device_cost = 0
        for minute_offset in range(duration):
            minute = (start_minute + minute_offset) % num_minutes  # Handle wrap-around for overnight devices
            hour = minute // 60  # Convert minute to hour for electricity price lookup
            price = electricity_prices[hour]
            device_cost += consumption * (price / 60)  # Cost per minute
            if minute_offset % 60 == 0:  # Print every hour
                print(f"  Minute {minute // 60}:{minute % 60:02d}, Price: ${price:.5f}/kWh, Consumption: {consumption / 60:.5f} kWh/min, Cost: ${consumption * (price / 60):.5f}")
        total_cost += device_cost
        print(f"Total cost for {device}: ${device_cost:.5f}")

    return total_cost, total_waiting_time

# Training the RL agent
for episode in range(num_episodes):
    schedule = {}
    for device in devices:
        start_range = devices[device]["start_range"]
        if start_range[1] > start_range[0]:  # Normal range (e.g., 14:00-22:00)
            if random.random() < epsilon:  # Explore
                start_minute = random.randint(start_range[0], start_range[1] - devices[device]["duration"])
            else:  # Exploit
                device_index = list(devices.keys()).index(device)
                start_minute = np.argmax(Q[device_index, start_range[0]:start_range[1]]) + start_range[0]
        else:  # Cyclic range (e.g., 23:00-07:00)
            if random.random() < epsilon:  # Explore
                start_minute = random.choice(
                    list(range(start_range[0], num_minutes)) + list(range(0, start_range[1]))
                )
            else:  # Exploit
                device_index = list(devices.keys()).index(device)
                q_values = np.concatenate((Q[device_index, start_range[0]:], Q[device_index, :start_range[1]]))
                start_minute = (np.argmax(q_values) + start_range[0]) % num_minutes
        schedule[device] = start_minute

    # Calculate metrics
    total_cost, total_waiting_time = calculate_metrics(schedule)
    print(total_cost, total_waiting_time)
    reward = - (alpha * total_cost + beta * total_waiting_time)

    # Update Q-table
    for device, start_minute in schedule.items():
        device_index = list(devices.keys()).index(device)
        Q[device_index, start_minute] += learning_rate * (reward + discount_factor * np.max(Q[device_index, :]) - Q[device_index, start_minute])

    # Decay epsilon
    epsilon = max(min_epsilon, epsilon * epsilon_decay)

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