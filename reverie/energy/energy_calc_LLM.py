import os
import json
import csv
from datetime import datetime, timedelta
import sys
sys.path.append('../backend_server')

import pandas as pd

from persona.prompt_template.gpt_structure import *

# Function to run the Language Model to predict appliance states
def run_LLM_prompt_appliance_states(descriptions, appliance, verbose=False):
    # Function to create input for the language model
    def create_prompt_input(descriptions, appliance):
        return [descriptions, appliance]

    # Function to extract the first JSON dictionary from a string
    def extract_first_json_dict(data_str):
        start_idx = data_str.find('{')
        end_idx = data_str.find('}', start_idx) + 1

        if start_idx == -1 or end_idx == 0:
            return None

        json_str = data_str[start_idx:end_idx]

        try:
            json_dict = json.loads(json_str)
            return json_dict
        except json.JSONDecodeError:
            return None

    # Function to clean up and extract relevant information from the GPT response
    def clean_up(gpt_response, prompt=""):
        gpt_response = extract_first_json_dict(gpt_response)

        keys = list(gpt_response.keys())
        # Extract the values of the first and second elements
        value_first_element = gpt_response.get(keys[0], "")
        value_second_element = gpt_response.get(keys[1], "")

        # Create cleaned_dict
        cleaned_dict = {"reason": value_first_element, "state": False} # value_first_element

        # Check if 'f' or 'F' is present in the reason
        if "t" in str(value_second_element) or "T" in str(value_second_element):
            cleaned_dict["state"] = True

        # Print the cleaned_dict
        print('cleaned dict')
        print(cleaned_dict)

        return cleaned_dict

    # Function to validate the GPT response
    def validate(gpt_response, prompt=""):
        try:
            print("ugh...")
            #print(extract_first_json_dict(gpt_response))
            return extract_first_json_dict(gpt_response)
        except:
            return False

    # Function to provide a fail-safe response in case of errors
    def get_fail_safe():
        return {"reason": "...", "state": False}

    # GPT parameters and prompt template
    gpt_param = {"engine": "", "max_tokens": 100, "temperature": 0, "top_p": 1, "stream": False,
                 "frequency_penalty": 0, "presence_penalty": 0, "stop": None}

    prompt_template = "applience_usage_reason.txt"

    # Create prompt input and generate the actual prompt
    prompt_input = create_prompt_input(descriptions, appliance)
    prompt = generate_prompt(prompt_input, prompt_template)
    fail_safe = get_fail_safe()

    # Run the language model and obtain the output
    output = safe_generate_response(prompt, gpt_param, 1, fail_safe, validate, clean_up)

    return output


# Function to calculate energy consumption based on appliance states
def calculate_energy(master_movement_file, objects_file=''):
    # Load master movement data from JSON file
    with open(master_movement_file, 'r') as file:
        master_movement_data = json.load(file)

    # Convert master movement data to a DataFrame
    #df_master_movement = pd.DataFrame.from_dict(master_movement_data, orient='index')
    output_data = []
    current_time = datetime.strptime('00:00:00', '%H:%M:%S')

    # Initialize variables to store previous state information
    prev_descriptions = None
    prev_appliance = None
    prev_state = None
    prev_reason = None

    # List of appliances to consider
    appliances = {"lightings in the Hobbs Cafe", "lightings in Isabella Rodriguez's house", "lightings in Maria Lopez's house", "lightings in Klaus Mueller's house", "air conditioner(heating and cooling)"} #, "game console", "microwave", "phone charger"}

    # Loop through each appliance
    for appliance in appliances:
        # Loop through each step in the master movement data
        for step, step_data in master_movement_data.items():
            if not step_data:
                continue

            print(step)

            # Calculate adjusted timestamp based on 12am start and 10-second steps
            adjusted_timestamp = (current_time + timedelta(seconds=int(step) * 10)).strftime('%Y-%m-%d %H:%M:%S')

            # Combine step_data and adjusted_timestamp into a dictionary
            combined_data = {
                "step": step,
                "timestamp": adjusted_timestamp,
                "step_data": step_data
            }


            # Extract descriptions for the current step
            #descriptions = df_master_movement.loc[step].apply(lambda x: x.get('description') if (isinstance(x, dict) and 'description' in x) else None)

            # TODO add person so that LLM knows who is doing what
            #descriptions = [user_data["description"] for user_data in step_data.values()]

            # Combine persona names with their descriptions
            combined_descriptions = {name: user_data["description"] for name, user_data in step_data.items()}

            print(prev_descriptions)
            print(combined_descriptions)
            print(prev_descriptions == combined_descriptions)

            # Skip if descriptions are the same as the previous step
            if prev_descriptions is not None and tuple(prev_descriptions) == tuple(combined_descriptions):
                print('debug, same description encountered')
                if prev_state:
                    # Append the output data with the previous state information
                    output_data.append({
                        "step": step,
                        "timestamp": adjusted_timestamp,
                        "appliance": prev_appliance,
                        "state": prev_state,
                        "reason": prev_reason
                    })
                continue

            # Run Language Model to predict appliance states
            gpt_output = run_LLM_prompt_appliance_states(combined_data, appliance)
            #gpt_output = {"reason": "...", "state": False} # for debugging and disable LLM

            # Extract relevant information from the GPT output
            appliance_state = gpt_output['state']
            reason = gpt_output['reason']

            # If appliance state is available, append to the output data
            if appliance_state:
                output_data.append({
                    "step": step,
                    "timestamp": adjusted_timestamp,
                    "appliance": appliance,
                    "state": appliance_state,
                    "reason": reason
                })

            # Reset previous state information
            prev_descriptions = combined_descriptions
            prev_appliance = appliance
            prev_state = appliance_state
            prev_reason = reason

            # Check once in a while and write the output to a CSV file
            if int(step) % 100 == 0:
                print('debug, saving to output file')
                output_file = "energy_output_LLM.csv"
                pd.DataFrame(output_data).to_csv(output_file, index=False)
                print(f"Energy calculation results written to {output_file}")


# Example usage
calculate_energy("../../environment/frontend_server/compressed_storage/July1_the_ville_isabella_maria_klaus-step-3-20/master_movement.json")


#TODO use this to text skip same descriptions
data = {"2281": {
    "Isabella Rodriguez": {
      "movement": [
        81,
        15
      ],
      "pronunciatio": "\ud83d\udc55\ud83d\udc56",
      "description": "waking up and completing her morning routine (getting dressed) @ the Ville:Isabella Rodriguez's apartment:main room:closet",
      "chat": None
    }
  },
  "2282": {
    "Isabella Rodriguez": {
      "movement": [
        81,
        16
      ],
      "pronunciatio": "\ud83d\udc55\ud83d\udc56",
      "description": "waking up and completing her morning routine (getting dressed) @ the Ville:Isabella Rodriguez's apartment:main room:closet",
      "chat": None
    }
  }
  }