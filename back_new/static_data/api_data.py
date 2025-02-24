# Device data (durations and start ranges are now in minutes)
devices = {
    "Dish Washer": {"duration": 120, "consumption": 0.7, "start_range": (14 * 60, 22 * 60), "flexible": False},  
    "Washing Machine": {"duration": 90, "consumption": 1.1, "start_range": (10 * 60, 18 * 60), "flexible": False},  
    "Cloth Dryer": {"duration": 90, "consumption": 2.2, "start_range": (18 * 60, 22 * 60), "flexible": False},  
    "Oven 1": {"duration": 90, "consumption": 1.07, "start_range": (18 * 60 + 30, 22 * 60), "flexible": False},  
    "Oven 2": {"duration": 90, "consumption": 1.07, "start_range": (12 * 60, 14 * 60 + 30), "flexible": False},  
    "Cook Top": {"duration": 30, "consumption": 1.64, "start_range": (18 * 60 + 30, 22 * 60), "flexible": False},  
    "Microwave": {"duration": 12, "consumption": 1.0, "start_range": (8 * 60, 14 * 60), "flexible": False},  
    "Electric Vehicle": {"duration": 240, "consumption": 7.0, "start_range": (23 * 60, 6 * 60), "flexible": False},  
    "Laptop": {"duration": 120, "consumption": 0.05, "start_range": (17 * 60, 23 * 60), "flexible": False},  
    "Vacuum Cleaner": {"duration": 60, "consumption": 0.9, "start_range": (10 * 60, 14 * 60), "flexible": False},  
    "Air Condition 1": {"duration": 90, "consumption": 0.8, "start_range": (8 * 60, 11 * 60), "flexible": False},  
    "Air Condition 2": {"duration": 90, "consumption": 0.8, "start_range": (19 * 60, 22 * 60), "flexible": False},  
    "Water Heater": {"duration": 120, "consumption": 3.2, "start_range": (17 * 60, 22 * 60), "flexible": False},  
    "Refrigerator": {"duration": 1440, "consumption": 0.22, "start_range": (0, 23 * 60), "flexible": True},  
    "Lighting 1": {"duration": 180, "consumption": 2.1, "start_range": (7 * 60, 10 * 60), "flexible": True},  
    "Lighting 2": {"duration": 420, "consumption": 2.1, "start_range": (18 * 60, 1 * 60), "flexible": True},
}

# Electricity prices (example for 24 hours, in $/kWh)
given_prices = [
    0.10709, 0.104, 0.1, 0.08566, 0.085, 0.08553, 0.09507, 0.10307, 0.065, 0.04734, 0.001, 0.00054,
    0.00224, 0.00324, 0.0651, 0.09691, 0.09744, 0.094, 0.09858, 0.10103, 0.10572, 0.10105, 0.10319, 0.09905
]

num_minutes = 24 * 60  # 1440 minutes in a day

# allocationplot = {
#         "Dish Washer": {"schedule": ("14:00", "22:00"), "period": period['Dish Washer']},
#         "Washing Machine": {"schedule": ("10:00", "18:00"), "period": period['Washing Machine']},
#         "Cloth Dryer": {"schedule": ("18:00", "22:00"), "period":period['Cloth Dryer']},
#         "Oven 1": {"schedule": ("18:30", "22:00"), "period": period['Oven 1']},
#         "Oven 2": {"schedule": ("12:00", "14:30"), "period": period['Oven 2']},
#         "Cook Top": {"schedule": ("18:30", "22:00"), "period": period['Cook Top']},
#         "Microwave": {"schedule": ("08:00", "14:00"), "period": period['Microwave']},
#         "Electric Vehicle": {"schedule": ("23:00", "06:00"), "period": period['Electric Vehicle']},
#         "Laptop": {"schedule": ("17:00", "23:00"), "period": period['Laptop']},
#         "Vacuum Cleaner": {"schedule": ("10:00", "14:00"), "period": period['Vacuum Cleaner']},
#         "Air Condition 1": {"schedule": ("08:00", "11:00"), "period": period['Air Condition 1']},
#         "Air Condition 2": {"schedule": ("19:00", "22:00"), "period": period['Air Condition 2']},
#         "Water Heater": {"schedule": ("17:00", "22:00"), "period": period['Water Heater']},
#         "Refrigerator": {"schedule": ("00:00", "24:00"), "period": period['Refrigerator']},
#         "Lighting 1": {"schedule": ("07:00", "10:00"), "period": period['Lighting 1']},
#         "Lighting 2": {"schedule": ("18:00", "01:00"), "period": period['Lighting 2']},
#     }
    
# blue price = 0.145 #blue
# green price 0.13089
# yellow price = 0.0.12882