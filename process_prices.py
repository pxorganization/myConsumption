import pandas as pd


def process_price_signals():
    # Load data
    df = pd.read_excel('price_signals.xlsx')

    # Create pivot table
    pivot_table = df.pivot(
        index="Hour",
        columns="Day",
        values="EURO conversion"
    )

    return pivot_table.to_numpy()


def main():
    data_array = process_price_signals()
    print(data_array)


if __name__ == "__main__":
    main()
