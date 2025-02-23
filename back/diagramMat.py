from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

solution = {
    "Dish Washer": (857,977),
    "Washing Machine": (611, 701),
    "Cloth Dryer": (1084, 1174),
    "Oven 1": (1114, 1204),
    "Oven 2": (722, 812),
    "Cook Top": (1140, 1170),
    "Microwave": (516, 528),
    "Electric Vehicle": (1390, 190), # 1390 + 240 = 1630 and to start from 0 i do 1630 - 1440 = 190
    "Laptop": (1028, 1148),
    "Vacuum Cleaner": (641, 701),
    "Air Condition 1": (480, 570),
    "Air Condition 2": (1156, 1246),
    "Water Heater": (1023, 1143),
    "Refrigerator": (0, 1440),
    "Lighting 1": (420, 600),
    "Lighting 2": (1080, 60)
}


def convert_minutes_to_time(minutes):
    """Convert minutes since midnight to HH:MM format."""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def transform_solution(solution):
    """Convert solution dictionary values to HH:MM format while keeping the structure."""
    period = {}
    
    for device, times in solution.items():
        if isinstance(times, tuple):  # If the value is a tuple
            period[device] = tuple(convert_minutes_to_time(t) for t in times)
        else:  # If it's a single integer
            period[device] = convert_minutes_to_time(times)
    
    return period

period = transform_solution(solution)

# Updated data with "HH:MM" format
allocationplot = {
    "Dish Washer": {"schedule": ("14:00", "22:00"), "period": period['Dish Washer']},
    "Washing Machine": {"schedule": ("10:00", "18:00"), "period": period['Washing Machine']},
    "Cloth Dryer": {"schedule": ("18:00", "22:00"), "period":period['Cloth Dryer']},
    "Oven 1": {"schedule": ("18:30", "22:00"), "period": period['Oven 1']},
    "Oven 2": {"schedule": ("12:00", "14:30"), "period": period['Oven 2']},
    "Cook Top": {"schedule": ("18:30", "22:00"), "period": period['Cook Top']},
    "Microwave": {"schedule": ("08:00", "14:00"), "period": period['Microwave']},
    "Electric Vehicle": {"schedule": ("23:00", "06:00"), "period": period['Electric Vehicle']},
    "Laptop": {"schedule": ("17:00", "23:00"), "period": period['Laptop']},
    "Vacuum Cleaner": {"schedule": ("10:00", "14:00"), "period": period['Vacuum Cleaner']},
    "Air Condition 1": {"schedule": ("08:00", "11:00"), "period": period['Air Condition 1']},
    "Air Condition 2": {"schedule": ("19:00", "22:00"), "period": period['Air Condition 2']},
    "Water Heater": {"schedule": ("17:00", "22:00"), "period": period['Water Heater']},
    "Refrigerator": {"schedule": ("00:00", "24:00"), "period": period['Refrigerator']},
    "Lighting 1": {"schedule": ("07:00", "10:00"), "period": period['Lighting 1']},
    "Lighting 2": {"schedule": ("18:00", "01:00"), "period": period['Lighting 2']},
}

def convert_to_time(time_str):
    """Convert 'HH:MM' string to a datetime object."""
    hours, minutes = map(int, time_str.split(":"))
    if hours >= 24:  # Handle edge case where time is 24:00
        hours = 23
        minutes = 59
    return datetime.datetime(2024, 1, 1, hours, minutes)

def split_time_range(time_range):
    """Handle overnight schedules that cross midnight."""
    start, end = time_range
    if convert_to_time(start) > convert_to_time(end):  # Overnight case
        return [(start, "24:00"), ("00:00", end)]
    return [time_range]

def main():
    device_positions = list(range(len(allocationplot), 0, -1))

    fig, ax = plt.subplots(figsize=(16, 8))

    # Iterate through devices and plot schedules
    for idx, (device, times) in enumerate(allocationplot.items()):
        y_pos = device_positions[idx]

        # Convert schedule and period times to datetime format
        for segment in split_time_range(times["schedule"]):
            ax.plot(
                [convert_to_time(segment[0]), convert_to_time(segment[1])],
                [y_pos, y_pos],
                color="#39b9e7fa",
                marker="o",
                markersize=10
            )

        for segment in split_time_range(times["period"]):
            ax.plot(
                [convert_to_time(segment[0]), convert_to_time(segment[1])],
                [y_pos, y_pos],
                color= "#01445D",
                marker="o",
                markersize=5,
    
            )

    # Formatting
    ax.set_yticks(device_positions)
    ax.set_yticklabels(allocationplot.keys())

    # Set x-axis format
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax.set_xlabel("Time (HH:MM)")
    ax.grid(True, linestyle="--", alpha=0.6)

    # Generate time ticks from 00:00 to 23:59
    time_ticks = [convert_to_time(f"{h:02d}:00") for h in range(0, 24)] + [convert_to_time("23:59")]
    ax.set_xticks(time_ticks)

    legend_elements = [
        Line2D([0], [0], color="#fa4616", lw=4, label="Optimized Scheduling to reduce cost and waiting time"),
        Line2D([0], [0], color="#00A3E0", lw=4, label="Available Operating Period during the day")
    ]
    ax.legend(
        handles=legend_elements,
        loc="upper center",
        fontsize=12,
        frameon=True,
        bbox_to_anchor=(0.5, 1.15),
        ncol=2
    )

    return plt, fig

plt, fig = main()
plt.show()