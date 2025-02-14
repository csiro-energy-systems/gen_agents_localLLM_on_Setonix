import sys
import os
from datetime import datetime, timedelta

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory (generative_agents_localLLM) to the Python path
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.append(parent_dir)

# Now you can import modules from the 'reverie' package
from compress_sim_storage import compress4energy
from energy.energy_calc_string_match import calculate_energy




if __name__ == "__main__":
    # Simulation files
    simulation_names = [
        # "test-simulation-24hour",
        # "simulation_base_the_ville_n25_24h_30s_run1_15h",
        "simulation_base_the_ville_n25_30s_run2_1day"   
    ]
    
    
    object_file = "../../environment/frontend_server/static_dirs/assets/the_ville/matrix/special_blocks/game_object_blocks_copy.csv"
    
    for simulation_name in simulation_names:
        # Extract energy usage from simulations
        # Check inside generative_agents_localLLM/environment/frontend_server/compressed_storage
        compressed_dir = "../../environment/frontend_server/compressed_storage"
        
        # Use the file name (without extension) as the directory name
        dir_name = os.path.splitext(os.path.basename(simulation_name))[0]
        
        # Check if the directory exists, and compress the simulation if it does not
        if not os.path.exists(os.path.join(compressed_dir, dir_name)):
            compress4energy(simulation_name)
            print(f"Energy compressed successfully for {simulation_name}")
        
        
        # Construct the path to master_movement.json
        master_json_path = os.path.join(compressed_dir, dir_name, "master_movement.json")
        
        # Check if master_movement.json exists
        if os.path.exists(master_json_path):
            # Calculate energy usage from the master JSON file
            calculate_energy(master_json_path, object_file, simulation_name)
        else:
            print(f"master_movement.json not found in directory: {dir_name}")
            continue  # Skip to the next file if JSON is not found
