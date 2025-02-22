import numpy as np
import random
import pandas as pd
import signal
import sys
from pprint import pprint

# Function to handle Ctrl+C
def signal_handler(sig, frame):
    print("\nTraining interrupted by user. Saving the model...")
    np.save("model_interrupted.npy", Q)
    print("Model saved to model_interrupted.npy")
    sys.exit(0)
    
# Register the signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Function to process historical price signals
def process_price_signals():
    
    # Load data
    df = pd.read_excel('price_signals.xlsx')

    # Create pivot table
    pivot_table = df.pivot(
        index="Hour",
        columns="Day",
        values="EURO conversion"
    )

    # Convert pivot table to numpy array and transpose it
    data_array = pivot_table.to_numpy().transpose()

    # Convert the numpy array to a list of lists
    data_list = data_array.tolist()

    return data_list

# Train the model using historical data
historical_prices = process_price_signals()

#print("Historical Prices:",historical_prices )

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
    "Refrigerator": {"duration": 1440, "consumption": 0.22, "start_range": (0, 24 * 60), "flexible": True},  
    "Lighting 1": {"duration": 180, "consumption": 2.1, "start_range": (7 * 60, 10 * 60), "flexible": True},  
    "Lighting 2": {"duration": 420, "consumption": 2.1, "start_range": (6 * 60, 23 * 60), "flexible": True},
}

# Electricity prices (example for 24 hours, in $/kWh)
electricity_prices = [
    0.10709, 0.104, 0.1, 0.08566, 0.085, 0.08553, 0.09507, 0.10307, 0.065, 0.04734, 0.001, 0.00054,
    0.00224, 0.00324, 0.0651, 0.09691, 0.09744, 0.094, 0.09858, 0.10103, 0.10572, 0.10105, 0.10319, 0.09905
]

# RL parameters
num_episodes = 50000  # Number of tries
learning_rate = 0.1
discount_factor = 0.95
epsilon = 1.0
epsilon_decay = 0.998
min_epsilon = 0.01

# Weights for the reward function
alpha = 0.7 # Weight for total cost
beta = 0.3   # Weight for total waiting time

# Initialize Q-table
num_devices = len(devices)
num_minutes = 24 * 60  # 1440 minutes in a day
Q = np.zeros((num_devices, num_minutes))

# Maximum power constraint in kW
max_power = 5.75  # Can be changed to 7.36 or 9.2

# Helper function to calculate total cost and total waiting time
def calculate_metrics(schedule, electricity_prices):
    total_cost = 0
    total_waiting_time = 0
    for device, start_minute in schedule.items():
        duration = devices[device]["duration"]
        consumption = devices[device]["consumption"]
        earliest_start = devices[device]["start_range"][0]

        # Calculate waiting time
        if start_minute >= earliest_start:
            waiting_time = start_minute - earliest_start
        else:
            waiting_time = (num_minutes - earliest_start) + start_minute
        waiting_time = max(0, waiting_time)  # Ensure waiting time is non-negative
        total_waiting_time += waiting_time

        # Log device details
        # print(f"\nDevice: {device}")
        # print(f"  Start: {start_minute // 60}:{start_minute % 60:02d}")
        # print(f"  Duration: {duration} minutes")
        # print(f"  Consumption: {consumption} kWh")
        # print(f"  Earliest Start: {earliest_start // 60}:{earliest_start % 60:02d}")
        # print(f"  Waiting Time: {waiting_time} minutes")

        # Calculate the cost for the device's operation
        device_cost = 0
        remaining_duration = duration
        current_minute = start_minute

        while remaining_duration > 0:
            # Wrap around if current_minute exceeds 1440 minutes
            current_minute = current_minute % num_minutes

            # Determine the end of the current hour
            current_hour = current_minute // 60
            next_hour_start = (current_hour + 1) * 60
            minutes_in_current_hour = min(next_hour_start - current_minute, remaining_duration)

            # Get the price for the current hour
            price = electricity_prices[current_hour]

            # Calculate the cost for the current segment
            segment_cost = consumption * price * (minutes_in_current_hour / 60)
            device_cost += segment_cost

            # Log details for the current segment
            # print(f"  Segment: {current_minute // 60}:{current_minute % 60:02d} - {next_hour_start // 60}:{(next_hour_start % 60):02d}")
            # print(f"    Price: ${price:.5f}/kWh")
            # print(f"    Duration: {minutes_in_current_hour} minutes")
            # print(f"    Cost: ${segment_cost:.5f}")

            # Update the current minute and remaining duration
            current_minute += minutes_in_current_hour
            remaining_duration -= minutes_in_current_hour

        # Log the total cost for the device
        #print(f"  Total cost for {device}: ${device_cost:.5f}")
        total_cost += device_cost

    return total_cost, total_waiting_time

random.seed(42)

# Training the RL agent using historical data
try:
    for day_prices in historical_prices:
        electricity_prices = day_prices  # Use prices for the current day
        print(f"\nTraining on Day")

        for episode in range(num_episodes):
            schedule = {}
            for device in devices:
                start_range = devices[device]["start_range"]
                if start_range[1] > start_range[0]:  # Normal range (e.g., 14:00-22:00)
                    if random.random() < epsilon:  # Explore
                        if not devices[device]["flexible"]:
                            start_minute = random.randint(start_range[0], start_range[1] - devices[device]["duration"])
                        else:
                            start_minute = start_range[0]
                    else:  # Exploit
                        device_index = list(devices.keys()).index(device)
                        if not devices[device]["flexible"]:
                            start_minute = np.argmax(Q[device_index, start_range[0]:start_range[1]]) + start_range[0]
                        else:
                            start_minute = start_range[0]
                else:  # Cyclic range (e.g., 23:00-07:00)
                    if random.random() < epsilon:  # Explore
                        if not devices[device]["flexible"]:
                            total_minutes = (num_minutes - start_range[0]) + start_range[1]
                            start_minute = (start_range[0] + random.randint(0, total_minutes - devices[device]["duration"])) % num_minutes
                        else:
                            start_minute = start_range[0]
                    else:  # Exploit
                        device_index = list(devices.keys()).index(device)
                        if not devices[device]["flexible"]:
                            q_values = np.concatenate((Q[device_index, start_range[0]:], Q[device_index, :start_range[1]]))
                            start_minute = (np.argmax(q_values) + start_range[0]) % num_minutes
                        else:
                            start_minute = start_range[0]

                schedule[device] = start_minute

            # Calculate metrics
            total_cost, total_waiting_time = calculate_metrics(schedule, electricity_prices)
            reward = - (alpha * total_cost + beta * total_waiting_time)

            # Update Q-table
            for device, start_minute in schedule.items():
                device_index = list(devices.keys()).index(device)
                Q[device_index, start_minute] += learning_rate * (reward + discount_factor * np.max(Q[device_index, :]) - Q[device_index, start_minute])

            # Decay epsilon
            epsilon = max(min_epsilon, epsilon * epsilon_decay)

except KeyboardInterrupt:
    # Handle Ctrl+C
    print("\nTraining interrupted by user. Saving the model...")
    np.save("model_interrupted.npy", Q)
    print("Model saved to model_interrupted.npy")
    sys.exit(0)

# Save the Q-table to a file after training on all historical data
np.save("model_trained_historical.npy", Q)
print("\nQ-table saved to model_trained_historical.npy")

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

# Calculate and print the total cost and waiting time
total_cost, total_waiting_time = calculate_metrics(learned_schedule, electricity_prices)

print(f"\nTotal loops: {num_episodes}")
print(f"\nTotal Cost: ${total_cost:.5f}")
print(f"Total Waiting Time: {total_waiting_time} minutes")