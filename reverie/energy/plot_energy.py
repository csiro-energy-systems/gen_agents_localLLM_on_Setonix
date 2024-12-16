import matplotlib.pyplot as plt
import pandas as pd

def plot_appliance_and_combined_data_from_csv(file_path, save_path=None):
    # Load data from CSV
    data = pd.read_csv(file_path)

    # Convert the timestamp column to datetime format
    data['timestamp'] = pd.to_datetime(data['timestamp'])

    # Get unique appliances
    appliances = data['appliance'].unique()

    # Create subplots for each appliance and an additional subplot for combined states
    fig, axs = plt.subplots(len(appliances) + 1, 1, figsize=(10, 4 * (len(appliances) + 1)), sharex=True)

    for i, appliance in enumerate(appliances):
        # Filter data for the current appliance
        appliance_data = data[data['appliance'] == appliance]

        # Plot for each person
        for person in appliance_data['person'].unique():
            person_data = appliance_data[appliance_data['person'] == person]
            axs[i].plot(person_data['timestamp'], person_data['state'], label=f'{person} - {appliance}')

        axs[i].set_title(f"Appliance: {appliance}")
        axs[i].set_ylabel("State")
        axs[i].legend()

        # TODO fix this later
        # Combine states for the current appliance
        combined_usage = appliance_data.groupby('timestamp')['state'].sum()
        #axs[-1].plot(appliance_data['timestamp'], combined_usage, label=f'Total Usage - {appliance}', linestyle='dashed')

    axs[-1].set_title("Combined States for All Appliances")
    axs[-1].set_ylabel("State")
    axs[-1].legend()

    # Set common x-axis label
    axs[-1].set_xlabel("Time")

    # Save the plot if save_path is provided
    if save_path:
        plt.savefig(save_path)
    else:
        # Show the plot if save_path is not provided
        plt.tight_layout()
        plt.show()


def plot_total_usage_per_person_with_legend(file_path, save_path=None):
    # Load data from CSV
    try:
        data = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        print("Error: Empty CSV file.")
        return

    # Check if the DataFrame has any columns
    if data.empty or len(data.columns) == 0:
        print("Error: No columns to parse from file.")
        return

    # Convert the timestamp column to datetime format #TODO, only plot time not date
    data['timestamp'] = pd.to_datetime(data['timestamp'])

    # Group by person, timestamp, and appliance, summing the states
    total_usage_per_person_appliance = data.groupby(['person', 'timestamp', 'appliance'])['state'].sum().reset_index()

    # Create subplots for each person and an additional subplot for combined states
    fig, axs = plt.subplots(len(total_usage_per_person_appliance['person'].unique()) + 1, 1, figsize=(10, 4 * (len(total_usage_per_person_appliance['person'].unique()) + 1)), sharex=True)

    # Plot individual appliance usage for each person
    for i, person in enumerate(total_usage_per_person_appliance['person'].unique()):
        person_data = total_usage_per_person_appliance[total_usage_per_person_appliance['person'] == person]

        # Plot for each appliance
        for appliance in person_data['appliance'].unique():
            appliance_data = person_data[person_data['appliance'] == appliance]
            axs[i].plot(appliance_data['timestamp'], appliance_data['state'], label=f'{person} - {appliance}')

        axs[i].set_title(f"Individual Appliance Usage - {person}")
        axs[i].set_ylabel("State")
        axs[i].legend(fontsize='small') # TODO Place legend outside the chart

    # Group by timestamp, summing the states
    total_usage = data.groupby(['timestamp'])['state'].sum().reset_index()
    axs[-1].plot(total_usage['timestamp'], total_usage['state'], label='Overall Total Usage', linestyle='dashed')

    axs[-1].set_title("Overall Total Usage for All Appliances")
    axs[-1].set_ylabel("State")
    axs[-1].legend()

    # Set common x-axis label
    axs[-1].set_xlabel("Time")

    # Save the plot if save_path is provided
    if save_path:
        plt.savefig(save_path)
    else:
        # Show the plot if save_path is not provided
        plt.tight_layout()
        plt.show()


# TODO main
        

# Specify the path to your CSV file
csv_file_path = 'energy_output.csv'

# Specify the path to save the total usage plot (optional)
save_path_total_usage = 'plot_per_person.png'

# Plot the total usage data and save the plot
plot_total_usage_per_person_with_legend(csv_file_path, save_path_total_usage)




# Specify the path to your CSV file
csv_file_path = 'energy_output.csv'

# Specify the path to save the combined plot (optional)
save_path_combined = 'plot_appliance.png'

# Plot the data and save the combined plot
plot_appliance_and_combined_data_from_csv(csv_file_path, save_path_combined)


