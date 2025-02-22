import numpy as np
import random
import pandas as pd

def process_price_signals():
    
    df = pd.read_excel('price_signals.xlsx')

    pivot_table = df.pivot(
        index="Hour",
        columns="Day",
        values="EURO conversion"
    )

    data_array = pivot_table.to_numpy().transpose()
    data_list = data_array.tolist()

    return data_list

historical_prices = process_price_signals()

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

electricity_prices = [
    0.10709, 0.104, 0.1, 0.08566, 0.085, 0.08553, 0.09507, 0.10307, 0.065, 0.04734, 0.001, 0.00054,
    0.00224, 0.00324, 0.0651, 0.09691, 0.09744, 0.094, 0.09858, 0.10103, 0.10572, 0.10105, 0.10319, 0.09905
]

num_episodes = 50000
learning_rate = 0.1
discount_factor = 0.95
epsilon = 1.0
epsilon_decay = 0.998
min_epsilon = 0.01

alpha = 0.7
beta = 0.3

num_devices = len(devices)
num_minutes = 24 * 60
Q = np.zeros((num_devices, num_minutes))

def calculate_metrics(schedule):
    total_cost = 0
    total_waiting_time = 0
    for device, start_minute in schedule.items():
        duration = devices[device]["duration"]
        consumption = devices[device]["consumption"]
        earliest_start = devices[device]["start_range"][0]

        if start_minute >= earliest_start:
            waiting_time = start_minute - earliest_start
        else:
            waiting_time = (num_minutes - earliest_start) + start_minute
        waiting_time = max(0, waiting_time)
        total_waiting_time += waiting_time
        device_cost = 0
        remaining_duration = duration
        current_minute = start_minute

        while remaining_duration > 0:
            current_minute = current_minute % num_minutes
            current_hour = current_minute // 60
            next_hour_start = (current_hour + 1) * 60
            minutes_in_current_hour = min(next_hour_start - current_minute, remaining_duration)
            price = electricity_prices[current_hour]
            segment_cost = consumption * price * (minutes_in_current_hour / 60)
            device_cost += segment_cost
            current_minute += minutes_in_current_hour
            remaining_duration -= minutes_in_current_hour
        total_cost += device_cost

    return total_cost, total_waiting_time

for episode in range(num_episodes):
    schedule = {}
    for device in devices:
        start_range = devices[device]["start_range"]
        if start_range[1] > start_range[0]:
            if random.random() < epsilon:
                if not devices[device]["flexible"]:
                    start_minute = random.randint(start_range[0], start_range[1] - devices[device]["duration"])
                else:
                    start_minute = start_range[0]
            else:
                device_index = list(devices.keys()).index(device)
                if not devices[device]["flexible"]:
                    start_minute = np.argmax(Q[device_index, start_range[0]:start_range[1]]) + start_range[0]
                else:
                    start_minute = start_range[0]
        else:
            if random.random() < epsilon:
                if not devices[device]["flexible"]:
                    total_minutes = (num_minutes - start_range[0]) + start_range[1]
                    start_minute = (start_range[0] + random.randint(0, total_minutes - devices[device]["duration"])) % num_minutes
                else:
                    start_minute = start_range[0]
            else:
                device_index = list(devices.keys()).index(device)
                if not devices[device]["flexible"]:
                    q_values = np.concatenate((Q[device_index, start_range[0]:], Q[device_index, :start_range[1]]))
                    start_minute = (np.argmax(q_values) + start_range[0]) % num_minutes
                else:
                    start_minute = start_range[0]
        schedule[device] = start_minute

    total_cost, total_waiting_time = calculate_metrics(schedule)
    reward = - (alpha * total_cost + beta * total_waiting_time)

    for device, start_minute in schedule.items():
        device_index = list(devices.keys()).index(device)
        Q[device_index, start_minute] += learning_rate * (reward + discount_factor * np.max(Q[device_index, :]) - Q[device_index, start_minute])

    epsilon = max(min_epsilon, epsilon * epsilon_decay)

np.save("model_1M.npy", Q)

learned_schedule = {}
for device in devices:
    device_index = list(devices.keys()).index(device)
    start_range = devices[device]["start_range"]
    
    if devices[device]["flexible"]:
        best_start_minute = start_range[0]
    else:
        if start_range[1] > start_range[0]:
            best_start_minute = np.argmax(Q[device_index, start_range[0]:start_range[1]]) + start_range[0]
        else:
            q_values = np.concatenate((Q[device_index, start_range[0]:], Q[device_index, :start_range[1]]))
            best_start_minute = (np.argmax(q_values) + start_range[0]) % num_minutes
    learned_schedule[device] = best_start_minute

print("\nOptimal Schedule:")
for device, start_minute in learned_schedule.items():
    print(f"{device} - {start_minute // 60}:{start_minute % 60:02d}")

total_cost, total_waiting_time = calculate_metrics(learned_schedule)

print(f"\nTotal loops: {num_episodes}")
print(f"\nTotal Cost: ${total_cost:.5f}")
print(f"Total Waiting Time: {total_waiting_time} minutes")