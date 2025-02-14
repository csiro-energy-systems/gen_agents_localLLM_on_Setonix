#!/bin/bash --login  

#SBATCH --job-name=energy_calc_LLM  # Name the job
#SBATCH --account=interns202410 # Use your own project and the -gpu suffix
#SBATCH --nodes=1  # 1 node 
#SBATCH --time=01:00:00  # Set time needed

# --------------------------
# Load the needed modules
module load pytorch/2.2.0-rocm5.7.3 
module list


# --------------------------
# Some paths
VENV_PATH=$MYSOFTWARE/appenv/bin/activate
# PYTHON_SCRIPT=$MYSCRATCH/updated_gen_LLM/reverie/energy/energy_calc_LLM.py
PYTHON_SCRIPT=$MYSCRATCH/updated_gen_LLM/reverie/energy/pipeline_compress_and_convert.py

# export HF_HOME=$MYSCRATCH/hf_cache
# echo "HF_HOME set to $HF_HOME"


# --------------------------
# Run the django application
cd $MYSCRATCH/updated_gen_LLM/reverie/energy/


# Record the start time
start_time=$(date +%s)
echo "start time: $(date -d @$start_time)"

echo "Running the backend server: srun -N 1 -n 1 -c 8  bash -c 
  source $VENV_PATH && 
  python $PYTHON_SCRIPT     "

## change new_simulation to the name of the simulation you want to create to avoid File exists error
srun -N 1 -n 1 -c 8 bash -c "
  source $VENV_PATH && \
  python $PYTHON_SCRIPT  
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
