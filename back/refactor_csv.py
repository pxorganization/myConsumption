import numpy as np
import pandas as pd
import os

print("Current Directory:", os.getcwd())  # Τρέχων φάκελος
print("Files in directory:", os.listdir())  # Όλα τα αρχεία στον φάκελο
print("--------------------------------------------------------------------")

# Function to process historical price signals
def process_price_signals():
    """
    Process the price signals from the Excel file and return all historical prices.
    
    Returns:
        list: A list of lists, where each inner list contains 24 hourly prices for a day.
    """
    # Load data
    df = pd.read_excel('back/price_signals.xlsx')


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
print(process_price_signals())