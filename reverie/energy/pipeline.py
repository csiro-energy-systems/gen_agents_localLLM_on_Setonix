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
    "July1_the_ville_isabella_maria_klaus-step-3-21",
    "July1_the_ville_isabella_maria_klaus-step-3-20"
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
    if os.path.exists(os.path.join(compressed_dir, dir_name)):
        # If the directory exists, construct the path to master_movement.json
        master_json_path = os.path.join(compressed_dir, dir_name, "master_movement.json")
        print(master_json_path)

        # Check if master_movement.json exists
        if os.path.exists(master_json_path):                
            # Now you can use master_json for further processing
            data = calculate_energy(master_json_path, object_file)
            
            
            
        else:
            print(f"master_movement.json not found in directory: {dir_name}")
    else:
        ## compress simulations
        compress4energy(file)


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
      
# Calculate mean for each timestamp
mean_values = combined_data.groupby('step')['state'].mean().reset_index()
std_values = combined_data.groupby('step')['state'].std().reset_index()
print(mean_values)

# Plotting mean values
plt.figure(figsize=(10, 6))
plt.plot(mean_values['step'], mean_values['state'], label='Mean', color='blue')

# Convert 'step' column to numeric
mean_values['step'] = pd.to_numeric(mean_values['step'])
# Calculate adjusted timestamp
current_time = datetime.strptime('00:00:00', '%H:%M:%S')

# TODO, this is super redundant. Do vector operation
'''
adjusted_timestamps = []

for step in mean_values['step']:
    adjusted_timestamp = (current_time + timedelta(seconds=step * 10)).strftime('%H:%M:%S')
    adjusted_timestamps.append(adjusted_timestamp)

# Add the adjusted_timestamps list to the mean_values DataFrame
mean_values['adjusted_timestamp'] = adjusted_timestamps
'''

#mean_values['adjusted_timestamp'] = (current_time + timedelta(seconds=mean_values['step'] * 10)).dt.strftime('%H:%M:%S')

plt.fill_between(mean_values['step'],
                 mean_values['state'] - std_values['state'],
                 mean_values['state'] + std_values['state'],
                 color='lightgray', label='± 1 Std Dev', alpha=0.5)

plt.title('Time Series Plot with Mean and Standard Deviation')
plt.xlabel('Timestamp')
plt.ylabel('State')
plt.legend()
plt.grid(True)

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