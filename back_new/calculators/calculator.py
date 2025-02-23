from static_data.api_data import devices, num_minutes

# Helper function to calculate total cost and total waiting time
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

        # Log device details
        # print(f"\nDevice: {device}")
        # print(f"  Start: {start_minute // 60}:{start_minute % 60:02d}")
        # print(f"  Duration: {duration} minutes")
        # print(f"  Consumption: {consumption} kWh")
        # print(f"  Earliest Start: {earliest_start // 60}:{earliest_start % 60:02d}")
        # print(f"  Waiting Time: {waiting_time} minutes")

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

            # Log details for the current segment
            # print(f"  Segment: {current_minute // 60}:{current_minute % 60:02d} - {next_hour_start // 60}:{(next_hour_start % 60):02d}")
            # print(f"    Price: ${price:.5f}/kWh")
            # print(f"    Duration: {minutes_in_current_hour} minutes")
            # print(f"    Cost: ${segment_cost:.5f}")

            # Update the current minute and remaining duration
            current_minute += minutes_in_current_hour
            remaining_duration -= minutes_in_current_hour

        # Log the total cost for the device
        #print(f"  Total cost for {device}: ${device_cost:.5f}")
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