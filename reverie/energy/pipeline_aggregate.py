import sys 
import os 
from datetime import datetime, timedelta

import pandas as pd
import matplotlib.pyplot as plt

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory (generative_agents_localLLM) to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)

# Now you can import modules from the 'reverie' package
from compress_sim_storage import compress4energy
from energy.energy_calc_string_match import calculate_energy

# simcodes
files = [
    "mistral-7b-1",
    "mistral-7b-2",
    "mistral-7b-3",
    "mistral_debug",
    "mistral-7b-4",
    "mistral-7b-5",
    "mistral-7b-6",
    "mistral-7b-n5-1",
    "mistral-7b-n5-2",
    "mistral-7b-n5-3",
    "mistral-7b-n5-4",
    "mistral-7b-n5-5",
    "mistral-7b-n5-6",
]

# 10s per step, 6 is 1 min, 60 is 10 mins, 360 is 1hr 
window_size = 360

# fontsize of the plot
font_size = 20

object_file ="../../environment/frontend_server/static_dirs/assets/the_ville/matrix/special_blocks/game_object_blocks_copy.csv"

# data_array = []  # If you need to store individual dataframes
total_usage_array = []
person_usage_array = []
isabella_usage_array = []
maria_klaus_usage_array = []

for file in files:

    ## extract energy usage from simulations
    # Check inside generative_agents_localLLM/environment/frontend_server/compressed_storage
    compressed_dir = "../../environment/frontend_server/compressed_storage"
    
    # Assuming file name without extension is used as directory name
    dir_name = os.path.splitext(os.path.basename(file))[0]
    
    # Check if the directory exists
    if not os.path.exists(os.path.join(compressed_dir, dir_name)):
        ## compress simulations
        compress4energy(file)

    # If the directory exists, construct the path to master_movement.json
    master_json_path = os.path.join(compressed_dir, dir_name, "master_movement.json")

    # Check if master_movement.json exists
    if os.path.exists(master_json_path):                
        # Now you can use master_json for further processing
        data = calculate_energy(master_json_path, object_file)
        
    else:
        print(f"master_movement.json not found in directory: {dir_name}")

    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    # Convert 'state' column to numeric (assuming it's boolean)
    df['step'] = pd.to_numeric(df['step'])
    df['state'] = df['state'].astype(int)
    #print(df)
    
    # calculate per person 
    person_usage_per_step = df.groupby(['step', 'person'])['state'].sum().reset_index()
    isabella_usage = person_usage_per_step[person_usage_per_step['person'].isin(['Isabella Rodriguez'])]
    # Filter person_usage_per_step for Maria Lopez and Klaus Mueller
    maria_klaus_usage = person_usage_per_step[person_usage_per_step['person'].isin(['Maria Lopez', 'Klaus Mueller'])]


    # Append the data to the total_usage_array or perform other operations
    total_usage_per_step = df.groupby(['step'])['state'].sum().reset_index()

    #person_usage_array.append(person_usage_per_step)
    isabella_usage_array.append(isabella_usage)
    maria_klaus_usage_array.append(maria_klaus_usage)
    total_usage_array.append(total_usage_per_step)
    
# Concatenate the total_usage arrays into a single dataframe
isabella_total = pd.concat(isabella_usage_array, axis=0)
maria_klaus_total = pd.concat(maria_klaus_usage_array, axis=0)
combined_data_total = pd.concat(total_usage_array, axis=0)

# Calculate rolling mean and standard deviation for each timestamp

mean_values = combined_data_total.groupby('step')['state'].mean().reset_index()
mean_values['rolling_mean'] = mean_values['state'].rolling(window=window_size).mean().fillna(0)
std_values = combined_data_total.groupby('step')['state'].std().reset_index()
std_values['rolling_std'] = std_values['state'].rolling(window=window_size).std().fillna(0)

# Convert 'step' values to hours
mean_values['hours'] = mean_values['step'] * 10 / 3600

# Plotting mean values
plt.figure(figsize=(12, 8))

# Subplot for Combined Data
plt.plot(mean_values['hours'], mean_values['rolling_mean'], label='Mean', color='blue')
plt.fill_between(mean_values['hours'],
                 mean_values['rolling_mean'] - std_values['rolling_std'],
                 mean_values['rolling_mean'] + std_values['rolling_std'],
                 color='lightgray', label='± 1 Std Dev', alpha=0.5)
plt.title('Aggregated Mean of All Household Daily Usage', fontsize=font_size)
plt.xlabel('Hours', fontsize=font_size)
plt.xticks(fontsize=font_size)
plt.ylabel('State of Appliances', fontsize=font_size)
plt.yticks(fontsize=font_size)
plt.ylim(top=0.85)   # Set y-axis limits
plt.legend(fontsize=font_size, loc='upper left')

# Adjust layout
plt.tight_layout()

# Save the figure to a file (adjust the filename and format as needed)
plt.savefig('time_series_plot.pdf')
