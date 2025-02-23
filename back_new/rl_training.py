from calculators.generate_data import generate_normal_random, process_price_signals
from static_data.api_data import devices, given_prices, num_minutes
from calculators.calculator import calculate_metrics

import numpy as np
import random
import sys

# RL parameters
num_episodes = 10
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
Q = np.zeros((num_devices, num_minutes))

#TODO
# Maximum power constraint in kW in a household
max_power = 5.75  # Can be changed to 7.36 or 9.2

#In case nothing works this is the way out
#complete_data = generate_normal_random()

# Create a mixed array from all data sources
complete_data = generate_normal_random()
complete_data.append(given_prices)
for day in process_price_signals():
    complete_data.append(day)

# Training the RL agent using historical data (42 days for now)
try:
    for day_prices in complete_data:
        electricity_prices = day_prices
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

            # Calculate metrics & awards
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
    np.save("back_new/ai_models/model_interrupted.npy", Q)
    print("Model saved to model_interrupted.npy")
    sys.exit(0)

# Save the Q-table to a file after training on all historical data
np.save("./ai_models/model_trained_historical.npy", Q)
print("\nQ-table saved to model_trained_historical.npy")