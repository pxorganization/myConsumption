import pandas as pd
import numpy as np
from pprint import pprint


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


def main():
    data_list = process_price_signals()
    pprint(data_list)


if __name__ == "__main__":
    main()