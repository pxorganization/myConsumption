from static_data.api_data import devices, given_prices, num_minutes
from calculators.calculator import calculate_metrics, calculate_total_cost_per_hour, calculate_total_consumption_per_hour
from diagramMat import create_allocationplot, transform_solution, create_solution, main

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Allow requests from Angular (localhost:4200)
    allow_credentials=True,  # Allow cookies or authorization headers if needed
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

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

def get_total_cost_by_price(schedule, price):
    total_cost_per_hour =0
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

            # Calculate the cost for the current segment
            segment_cost = consumption * price * (minutes_in_current_hour / 60)
            device_cost += segment_cost

            # Update the current minute and remaining duration
            current_minute += minutes_in_current_hour
            remaining_duration -= minutes_in_current_hour

            # Add the cost to the corresponding hour
            total_cost_per_hour += segment_cost

    return total_cost_per_hour

def get_comparison_plans():
    current_percent = total_cost

    blue_percent = get_total_cost_by_price(schedule, 0.145)
    green_percent = get_total_cost_by_price(schedule, 0.13089)
    yellow_percent = get_total_cost_by_price(schedule, 0.12882)

    blue_diff = ((current_percent  - blue_percent) / current_percent) * 100
    green_diff = ((current_percent - green_percent) / current_percent) * 100
    yellow_diff = ((current_percent - yellow_percent) / current_percent) * 100

    return [blue_diff, green_diff, yellow_diff]

# Load the Q-table from a file
Q = np.load("ai_models/43_100_lightwave.npy")
print("Q-table loaded from 43_100_lightwave.npy")

schedule = generate_schedule()
total_cost, total_waiting_time = calculate_metrics(schedule, given_prices)

@app.get("/getImage")
def get_schedule():
    solution = create_solution(schedule, devices)
    period = transform_solution(solution)
    allocationplot = create_allocationplot(devices, period)

    main(allocationplot)
    return "Image created"
    
@app.get("/getComparisonPlans")
def get_comparison():
    return get_comparison_plans()

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