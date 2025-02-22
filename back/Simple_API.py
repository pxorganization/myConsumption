from fastapi import FastAPI
import numpy as np

# Initialize FastAPI app
app = FastAPI()

num_minutes = 24 * 60  # 1440 minutes in a day

# Load the Q-table from a file
Q = np.load("43_100_lightwave.npy")
print("Q-table loaded from 43_100_lightwave.npy")

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

# Electricity prices (example for 24 hours, in $/kWh)
given_prices = [
    0.10709, 0.104, 0.1, 0.08566, 0.085, 0.08553, 0.09507, 0.10307, 0.065, 0.04734, 0.001, 0.00054,
    0.00224, 0.00324, 0.0651, 0.09691, 0.09744, 0.094, 0.09858, 0.10103, 0.10572, 0.10105, 0.10319, 0.09905
]

num_minutes = 24 * 60  # 1440 minutes in a day

# Function to generate a new schedule
def generate_schedule():
    schedule = {}
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
        
        # Convert numpy.int64 to native Python int
        schedule[device] = int(best_start_minute)
    return schedule

# Function to calculate total cost and total waiting time
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

            # Update the current minute and remaining duration
            current_minute += minutes_in_current_hour
            remaining_duration -= minutes_in_current_hour

        total_cost += device_cost
    return total_cost, total_waiting_time

def calculate_total_cost_per_hour(schedule, electricity_prices):
    total_cost_per_hour = [0] * 24
    for device, start_minute in schedule.items():
        duration = devices[device]["duration"]
        consumption = devices[device]["consumption"]
        earliest_start = devices[device]["start_range"][0]

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

            # Update the current minute and remaining duration
            current_minute += minutes_in_current_hour
            remaining_duration -= minutes_in_current_hour

            # Add the cost to the corresponding hour
            total_cost_per_hour[current_hour] += segment_cost

    return total_cost_per_hour

def calculate_total_consumption_per_hour(schedule, electricity_prices):
    total_consumption_per_hour = [0] * 24
    for device, start_minute in schedule.items():
        duration = devices[device]["duration"]
        consumption = devices[device]["consumption"]
        earliest_start = devices[device]["start_range"][0]

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

            # Update the current minute and remaining duration
            current_minute += minutes_in_current_hour
            remaining_duration -= minutes_in_current_hour

            # Add the cost to the corresponding hour
            total_consumption_per_hour[current_hour] += consumption * (minutes_in_current_hour / 60)

    return total_consumption_per_hour

schedule = generate_schedule()
print("Schedule:", schedule)
total_cost, total_waiting_time = calculate_metrics(schedule, given_prices)

# Endpoint to get a new schedule
@app.get("/getSchedule")
def get_schedule():
    return schedule

# Endpoint to calculate total cost
@app.get("/getTotalCost")
def get_total_cost():
    return total_cost

# Endpoint to calculate total waiting time
@app.get("/getTotalWaitingTime")
def get_total_waiting_time():
    return total_waiting_time

@app.get("/getEnergyCost")
def get_energy_cost():
    return calculate_total_cost_per_hour(schedule, given_prices)

@app.get("/getConsumption")
def get_consumption():
    return calculate_total_consumption_per_hour(schedule, given_prices)

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)