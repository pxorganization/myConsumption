from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

def create_solution(schedule, devices):
    solution = {}
    for device, start_minute in schedule.items():
        duration = devices[device]["duration"]
        end_minute = start_minute + duration
        
        # Handle wrap-around cases (e.g., end_minute >= 1440)
        if end_minute > 1440:
            end_minute -= 1440
        
        # Add the device and its start/end times to the solution dictionary
        solution[device] = (start_minute, end_minute)
    
    return solution

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

# Function to create the allocationplot dictionary
def create_allocationplot(devices, period):
    allocationplot = {}
    for device, details in devices.items():
        start_range = details["start_range"]
        
        # Convert start_range to "HH:MM" format
        schedule_start = convert_minutes_to_time(start_range[0])
        schedule_end = convert_minutes_to_time(start_range[1])
        
        # Get the period from the period dictionary
        device_period = period[device]
        
        # Add the device and its details to the allocationplot dictionary
        allocationplot[device] = {
            "schedule": (schedule_start, schedule_end),
            "period": device_period
        }
    
    return allocationplot

def main(allocationplot):
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
        Line2D([0], [0], color="#01445D", lw=4, label="Optimized Scheduling to reduce cost and waiting time"),
        Line2D([0], [0], color="#39b9e7fa", lw=4, label="Available Operating Period during the day")
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

#plt, fig = main(allocationplot)
#plt.show()