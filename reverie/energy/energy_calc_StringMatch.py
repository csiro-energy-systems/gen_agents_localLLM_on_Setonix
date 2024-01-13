# this code is similar to energy_calc.py as it finds out the state of the appliance. However, it uses traditional pattern matching and semantic matching of the text 
# From description of the SIMs, find out which appliance is being used 

import sys
#sys.path.append('backend_server')

#from persona.prompt_template.gpt_structure import *


import os
import json
import csv
from datetime import datetime, timedelta
import pandas as pd
import re

def load_appliances(objects_file):
    # Load the CSV file with object information
    appliances = []
    with open(objects_file, 'r') as file:
        objects_data = csv.reader(file)
        #next(objects_data)  # Skip header

        for row in objects_data:
            appliance = row[3].strip()  # Assuming appliance is in the fourth column
            appliances.append(appliance)
        
    # Initialize the initial state dictionary
    initial_state = {appliance: False for appliance in appliances}

    return initial_state

def calculate_energy(master_movement_file, objects_file):
    # Get the initial state from the objects file
    initial_state = load_appliances(objects_file)

    # Load the JSON file
    with open(master_movement_file, 'r') as file:
        master_movement_data = json.load(file)

    # Convert the master_movement_data to a DataFrame
    df_master_movement = pd.DataFrame.from_dict(master_movement_data, orient='index')

    # Initialize variables
    output_data = []
    current_time = datetime.strptime('00:00:00', '%H:%M:%S')


    # Iterate over steps
    for step, step_data in master_movement_data.items():
        # Skip if step_data is an empty dictionary
        if not step_data:
            continue

        # Sometimes step_data is {} and does not contain anything. Should I keep it as current_state?
        print(step)

        # Calculate the adjusted timestamp based on 12am start and 10-second steps
        adjusted_timestamp = (current_time + timedelta(seconds=int(step) * 10)).strftime('%H:%M:%S')

        for person, actions in step_data.items():
            description = actions['description']

            # fix this part 
            for appliance in initial_state.keys():
                
                # Check if the appliance string is present in the description using case-insensitive matching
                #print(description)
                object_state = bool(re.search(appliance, description, flags=re.IGNORECASE))            
                #print('------')
                #print(object_state)
                
                #if object_state: # plot becomes different
                output_data.append({
                    "step": step,
                    "timestamp": adjusted_timestamp,
                    "person": person,
                    "appliance": appliance,
                    "state": object_state
                })          

    # Write the output to a CSV file using pandas
    output_file = "energy_output.csv"
    pd.DataFrame(output_data).to_csv(output_file, index=False)
    print(f"Energy calculation results written to {output_file}")

    # TODO return output_data


# TODO main
    
# Example usage
calculate_energy("../../environment/frontend_server/compressed_storage/July1_the_ville_isabella_maria_klaus-step-3-20/master_movement.json", "../../environment/frontend_server/static_dirs/assets/the_ville/matrix/special_blocks/game_object_blocks_copy.csv")

