from static_data.api_data import devices, given_prices, num_minutes
from calculators.calculator import calculate_metrics, calculate_total_cost_per_hour, calculate_total_consumption_per_hour

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

# Load the Q-table from a file
Q = np.load("ai_models/43_100_lightwave.npy")
print("Q-table loaded from 43_100_lightwave.npy")

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

schedule = generate_schedule()
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