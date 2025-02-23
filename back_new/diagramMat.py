
# Re-import required libraries after execution state reset
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

# Define data points
allocationplot = {
    "Dish Washer": {
        "schedule": (14, 22), 
        "period": (11, 12)
        },
    "Washing Machine": {
        "schedule": (10, 18), 
        "period": (11, 12)
        },
    "Cloth dryer": {
        "schedule": (18, 22), 
        "period": (11, 12)
        },
    "Oven 1": {
        "schedule": (18.5, 22), 
        "period": (11, 12)
        },
    "Oven 2": {
        "schedule": (12, 14.5), 
        "period": (11, 12)
        },
    "Cook Top": {
        "schedule": (18.5, 22), 
        "period": (11, 12)
        },
    "Microwave": {
        "schedule": (8, 14), 
        "period": (11, 12)
        },
    "Electric vehicle": {
        "schedule": (23, 6), 
        "period": (11, 12)
        },
    "Laptop": {
        "schedule": (17, 23), 
        "period": (11, 12)
        },
    "Vacuum cleaner": {
        "schedule": (10, 14), 
        "period": (11, 12)
        },
    "Air Condition 1": {
        "schedule": (8, 11), 
        "period": (11, 12)
        },
    "Air Condition 2": {
        "schedule": (19, 22), 
        "period": (11, 12)
        },
    "Water Heater": {
        "schedule": (17, 22), 
        "period": (11, 12)
        },
    "Refrigerator": {
        "schedule": (0, 23), 
        "period": (0, 23)
        },
    "Lighting 1": {
        "schedule": (7, 10), 
        "period": (7, 10)
        },
    "Lighting 2": {
        "schedule": (18, 1), 
        "period": (18, 1)
        },
}


def split_time_range(time_range):
    start, end = time_range
    if start > end:
        return [(start, 23), (0, end)]
    else:
        return [time_range]


def main():
    # Device positions for y-axis
    device_positions = list(range(len(allocationplot), 0, -1))  

    # Create figure
    fig, ax = plt.subplots(figsize=(16, 8))


    # Iterate through devices and plot their schedules
    for idex, (device, times) in enumerate(allocationplot.items()):
        y_pos = device_positions[idex]


        # schedule with orange
        for segment in split_time_range(times["schedule"]):
            ax.plot(segment, [y_pos, y_pos], color="#00A3E0", marker="o", markersize=6)

        # period with blue
        for segment in split_time_range(times["period"]):
            ax.plot(segment, [y_pos, y_pos], color="#fa4616", marker="o", markersize=6)


    # Formatting
    ax.set_yticks(device_positions)
    ax.set_yticklabels(allocationplot.keys())
    ax.set_xticks(range(0, 24))  # Hour range from 0 to 23
    ax.set_xlabel("Time (Hours)")
    ax.grid(True, linestyle="--", alpha=0.6)


    legend_elements = [
        Line2D([0], [0], color="#fa4616", lw=4, label="Optimized Scheduling to reduce cost and waiting time"),
        Line2D([0], [0], color="#00A3E0", lw=4, label="Available Operating Period during the day")
    ]
    ax.legend(
        handles=legend_elements,
        loc="upper center",       
        fontsize=12,
        frameon=True,
        bbox_to_anchor=(0.5, 1.15),  # Places it above the plot (adjust the second value for spacing)
        ncol=2  # Arranges legend items in one row (change if needed)
    )


    return plt, fig



plt, fig = main()
plt.show()




