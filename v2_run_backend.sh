#!/bin/bash --login  

#SBATCH --job-name=backend_server  # Name the job
#SBATCH --account=interns202410-gpu  # Use your own project and the -gpu suffix
#SBATCH --partition=gpu  # Ensure partition is gpu
#SBATCH --nodes=1  # 1 node 
#SBATCH --gpus-per-node=4  # 1 GPU per node
#SBATCH --time=24:00:00  # Set time needed

# --------------------------
# Load the needed modules
module load pytorch/2.2.0-rocm5.7.3 
module list


# --------------------------
# Some paths
VENV_PATH=$MYSOFTWARE/appenv/bin/activate
PYTHON_SCRIPT=$MYSCRATCH/updated_gen_LLM/reverie/backend_server/reverie.py

export HF_HOME=$MYSCRATCH/hf_cache
echo "HF_HOME set to $HF_HOME"

# Setup instructions for SSH tunneling
host=$(hostname)
echo "*****************************************************"
echo "Setup - from your laptop, in a separate local terminal window run:"
echo "ssh -N -f -L ${port}:${host}:${port} $USER@setonix.pawsey.org.au"
echo "*****************************************************"
echo ""

# --------------------------
# Run the django application
cd $MYSCRATCH/updated_gen_LLM/reverie/backend_server


# Record the start time
start_time=$(date +%s)
echo "start time: $(date -d @$start_time)"

# run for a day
echo "Running the backend server: srun -N 1 -n 1 -c 8 --gres=gpu:4 bash -c 
  source $VENV_PATH && 
  pip list && 
  python $PYTHON_SCRIPT --forked_simulation base_the_ville_n25_30s  
                  --new_simulation simulation_base_the_ville_n25_24h_30s_run1
                  --option 'run 2880'    "

# change new_simulation to the name of the simulation you want to create to avoid File exists error

srun -N 1 -n 1 -c 8 --gres=gpu:4 bash -c "
  source $VENV_PATH && \
  pip list && \
  python $PYTHON_SCRIPT --forked_simulation base_the_ville_n25_30s  \
                  --new_simulation simulation_base_the_ville_n25_24h_30s_run1 \
                  --option 'run 2880' 
" 

# Record the end time
end_time=$(date +%s)
echo "End time: $(date -d @$end_time)"

# Calculate and display the duration
duration=$((end_time - start_time))
# Convert duration to hours, minutes, and seconds
hours=$((duration / 3600))
minutes=$(((duration % 3600) / 60))
seconds=$((duration % 60))
echo "*****************************************************"
echo "Job completed in $hours hours, $minutes minutes, and $seconds seconds."
echo "*****************************************************"
