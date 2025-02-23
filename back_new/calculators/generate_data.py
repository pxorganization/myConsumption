import random
import pandas as pd

# Function to generate the array of arrays
def generate_normal_random():
    # Create a list of 30 arrays, each containing 24 random values
    arrays = []
    for _ in range(30):
        # Generate a single array with 24 random values between 0.085 and 0.135
        array = [round(random.uniform(0.085, 0.135), 3) for _ in range(24)]
        arrays.append(array)
    return arrays

# Function to process historical price signals
def process_price_signals():
    
    # Load data
    df = pd.read_excel('./extraction/price_signals.xlsx')
    # Create pivot table
    pivot_table = df.pivot(
        index="Hour",
        columns="Day",
        values="EURO conversion"
    )

    # Convert pivot table to numpy array and transpose it
    data_array = pivot_table.to_numpy().transpose()
    # Convert the numpy array to a list of lists
    #data_list = data_array.tolist()
    return data_array.tolist()
