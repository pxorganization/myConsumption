import random


# Function to generate the array of arrays
def generate_random_arrays():
    # Create a list of 30 arrays, each containing 24 random values
    arrays = []
    for _ in range(30):
        # Generate a single array with 24 random values between 0.085 and 0.135
        array = [round(random.uniform(0.085, 0.135), 3) for _ in range(24)]
        arrays.append(array)
    return arrays


# Generate the random arrays
random_arrays = generate_random_arrays()

# Print the result
for array in random_arrays:
    print(array)
