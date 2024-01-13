import sys 
import pandas as pd
import matplotlib.pyplot as plt
from generative_agents_localLLM.reverie.compress_sim_storage import compress_sim_storage
from generative_agents_localLLM.reverie.energy.energy_calc import energy_calc
# from generative_agents_localLLM.reverie.energy.plot_energy import plot_energy

# Assuming 'files' is a list of file paths
files = [
    '',
    ''
]

# data_array = []  # If you need to store individual dataframes
total_usage_array = []

for file in files:
    # compress simulations
    compress_sim_storage(file)

    # extract energy usage from simulations
    data = energy_calc("../environment/frontend_server/compressed_storage/July1_the_ville_isabella_maria_klaus-step-3-20/master_movement.json", "../environment/frontend_server/static_dirs/assets/the_ville/matrix/special_blocks/game_object_blocks_copy.csv")

    # Convert the timestamp column to datetime format
    # data['timestamp'] = pd.to_datetime(data['timestamp'])
    total_usage = data.groupby(['timestamp'])['state'].sum().reset_index()
    
    total_usage_array.append(total_usage)

# Concatenate the total_usage arrays into a single dataframe
combined_data = pd.concat(total_usage_array, axis=1)

# Calculate mean and standard deviation for each timestamp
mean_values = combined_data.mean(axis=1)
std_dev_values = combined_data.std(axis=1)

# Plotting (you can use your preferred plotting method)
plt.plot(mean_values, label='Mean Usage')
plt.fill_between(mean_values.index, mean_values - std_dev_values, mean_values + std_dev_values, alpha=0.2, label='Standard Deviation')
plt.xlabel('Timestamp')
plt.ylabel('Usage')
plt.legend()

# Save the plot
plt.savefig('path/to/save/your/plot.png')






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