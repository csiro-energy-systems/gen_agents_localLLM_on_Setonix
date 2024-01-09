import sys
sys.path.append('backend_server')

from persona.prompt_template.gpt_structure import *

def run_LLM_prompt_appliance_states(descriptions, current_appliance_state, appliance, verbose=False): 
  def create_prompt_input(descriptions, current_appliance_state, appliance): 
    prompt_input = [descriptions, 
                    current_appliance_state,
                    appliance]
    return prompt_input
  
  def __func_clean_up(gpt_response, prompt=""):
    cr = gpt_response.strip()
    if cr[-1] == ".": cr = cr[:-1]
    return cr

  def __func_validate(gpt_response, prompt=""): 
    try: 
      gpt_response = __func_clean_up(gpt_response, prompt="")
    except: 
      return False
    return True 

  #def get_fail_safe(act_game_object): 
  #  fs = f"{act_game_object} is idle"
  #  return fs

  #print ("asdhfapsh8p9hfaiafdsi;ldfj as DEBUG 6") ########
  gpt_param = {"engine": "", "max_tokens": 1, # True or False 
               "temperature": 0, "top_p": 1, "stream": False,
               "frequency_penalty": 0, "presence_penalty": 0, "stop": None}
  prompt_template = "backend_server/persona/prompt_template/energy_uage_calc/applience_usage_TrueFalse.txt" ########
  prompt_input = create_prompt_input(descriptions, current_appliance_state, appliance)  ########
  prompt = generate_prompt(prompt_input, prompt_template)
  #example_output = "True" ########
  #special_instruction = "The output should ONLY be either True or False" ########
  
  #prompt = '"""\n' + prompt + '\n"""\n'
  #prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
  #prompt += "Example output json:\n"
  #prompt += '{"output": "' + str(example_output) + '"}'
  
  fail_safe = "energy usage not generated correctly" ########
  #output = ChatGPT_safe_generate_response(prompt, example_output, special_instruction, 3, fail_safe,
  #                                        __chat_func_validate, __chat_func_clean_up, True)
  #print(prompt)
  output = safe_generate_response(prompt, gpt_param, 3, fail_safe,
                                   __func_validate, __func_clean_up)
  
  return output
  #if output != False: 
  #  return output, [output, prompt, gpt_param, prompt_input, fail_safe]
  

import os
import json
import csv
from datetime import datetime, timedelta
import pandas as pd

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
        adjusted_timestamp = (current_time + timedelta(seconds=int(step) * 10)).strftime('%Y-%m-%d %H:%M:%S')

        # Use initial state for step 0
        current_state = initial_state.copy() if step == "0" else previous_state

        # Perform LLM calculations which outputs Ture or False for each appliance 
        # LLM, based on descriptions and current state, calculate the appliance usage
        
        descriptions = df_master_movement.loc[step].apply(lambda x: x.get('description') if (isinstance(x, dict) and 'description' in x) else None)


        
        for appliance in initial_state.keys():
            
            object_state = run_LLM_prompt_appliance_states(descriptions, current_state, appliance)
            print(object_state)
            
            current_state[appliance] = object_state

            if object_state:
                output_data.append({
                    "step": step,
                    "timestamp": adjusted_timestamp,
                    #"descriptions": descriptions,
                    "appliance": appliance,
                    "state": object_state
                })          

        # Update previous state for the next iteration
        previous_state = current_state

        # check once in a while
        if int(step)%100==0:
          # Write the output to a CSV file using pandas
          output_file = "energy_output.csv"
          pd.DataFrame(output_data).to_csv(output_file, index=False)
          print(f"Energy calculation results written to {output_file}")

# Example usage
calculate_energy("../environment/frontend_server/compressed_storage/July1_the_ville_isabella_maria_klaus-step-3-20/master_movement.json", "../environment/frontend_server/static_dirs/assets/the_ville/matrix/special_blocks/game_object_blocks_copy.csv")

