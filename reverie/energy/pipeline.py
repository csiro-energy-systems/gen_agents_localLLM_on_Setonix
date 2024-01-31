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
    #"July1_the_ville_isabella_maria_klaus-step-3-20",
    #"llama2-13b",
    #"mistral-7b-1",
    #"mistral-7b-2",
    #"mistral-7b-3",
    #"mistral_debug",
    #"mistral-7b-eco-1",
    #"mistral-7b-eco-2",
    "mistral-7b-n5-1",
    "mistral-7b-n5-2",
    "mistral-7b-n5-3",
]

object_file ="../../environment/frontend_server/static_dirs/assets/the_ville/matrix/special_blocks/game_object_blocks_copy.csv"

# data_array = []  # If you need to store individual dataframes
total_usage_array = []

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
    print(master_json_path)

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
    
    # Append the data to the total_usage_array or perform other operations
    total_usage_per_step = df.groupby(['step'])['state'].sum().reset_index()
    print(total_usage_per_step)

    total_usage_array.append(total_usage_per_step)
    

# Concatenate the total_usage arrays into a single dataframe
combined_data = pd.concat(total_usage_array, axis=0)
# Print rows where 'state' is equal to 3
print(combined_data)
      
# Calculate rolling mean and standard deviation for each timestamp
window_size = 360
mean_values = combined_data.groupby('step')['state'].mean().reset_index()
mean_values['rolling_mean'] = mean_values['state'].rolling(window=window_size).mean().fillna(0)
std_values = combined_data.groupby('step')['state'].std().reset_index()
std_values['rolling_std'] = std_values['state'].rolling(window=window_size).std().fillna(0)

# Plotting mean values
plt.figure(figsize=(10, 6))
plt.plot(mean_values['step'], mean_values['rolling_mean'], label='Mean', color='blue')

# Convert 'step' column to numeric
mean_values['step'] = pd.to_numeric(mean_values['step'])

# Calculate adjusted timestamp
current_time = datetime.strptime('00:00:00', '%H:%M:%S')

plt.fill_between(mean_values['step'],
                 mean_values['rolling_mean'] - std_values['rolling_std'],
                 mean_values['rolling_mean'] + std_values['rolling_std'],
                 color='lightgray', label='± 1 Std Dev', alpha=0.5)

# Additional plot settings
plt.xlabel('Step')
plt.ylabel('Mean +/- 1 Std Dev')
plt.title('Moving Average with Standard Deviation')
plt.legend()

# Save the figure to a file (adjust the filename and format as needed)
plt.savefig('time_series_plot.png')






# plot energy usage from simulations
#plot_total_usage_per_person_with_legend(csv_file_path, save_path_total_usage)
#plot_appliance_and_combined_data_from_csv(csv_file_path, save_path_combined)

# how do we do analysis?




'''
the plots we are interested are 


1. which appliance has been used on what time during a day
2. per person plot to see what appliances the person has used during the day
3. accumulate 1 and 2 and find means with respect to x axis, like Dai'd GAN, use SD as well
4. Can we find randomness from step3, or does it change based on the event in SIMs?

# some simulations do not have large steps to reach the end of th day
'''