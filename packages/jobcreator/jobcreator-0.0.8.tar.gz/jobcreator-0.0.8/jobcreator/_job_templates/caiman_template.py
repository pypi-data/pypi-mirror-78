import os


def caiman_job_file(
    data_path: str,
    jobcreator_output_dir: str,
    job_name: str,
    email: str,
    n_cpu: int = 8,
    mem_per_cpu: int = 25,
    tmp_size: int = 150,
    job_time: str = "04:00:00",
    qos: str = "6hours",
    log_file: str = "myrun.o",
    error_file: str = "myrun.e",
    mc_settings_file: str = "default",
    cnmf_settings_file: str = "default",
    qc_settings_file: str = "default",
):
    mem_per_cpu = str(mem_per_cpu) + "G"
    tmp_size = str(tmp_size) + "G"

    # get the name of the file and make the path to the temp dir
    data_pattern = os.path.join(data_path, "*.tif*")

    # save the error and log files to the results dir
    log_file = os.path.join(jobcreator_output_dir, log_file)
    error_file = os.path.join(jobcreator_output_dir, error_file)

    # stub for naming the environment file
    env_file_stub = os.path.join(jobcreator_output_dir, "job_")

    job_file = f"""#!/bin/bash

#SBATCH --job-name={job_name}                   #This is the name of your job
#SBATCH --cpus-per-task={n_cpu}                  #This is the number of cores reserved
#SBATCH --mem-per-cpu={mem_per_cpu}              #This is the memory reserved per core.
#SBATCH --tmp={tmp_size}

#SBATCH --time={job_time}        #This is the time that your task will run
#SBATCH --qos={qos}           #You will run in this queue

# Paths to STDOUT or STDERR files should be absolute or relative to current working directory
#SBATCH --output={log_file}%j     #These are the STDOUT and STDERR files
#SBATCH --error={error_file}%j
#SBATCH --mail-type=END,FAIL,TIME_LIMIT
#SBATCH --mail-user={email}        #You will be notified via email when your task ends or fails


#Remember:
#The variable $TMPDIR points to the local hard disks in the computing nodes.
#The variable $HOME points to your home directory.
#The variable $SLURM_JOBID stores the ID number of your job.

# set environment variables
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1

#load your required modules below
#################################
module purge
module load Anaconda3

#add your command lines below
#############################
echo "moving files"
for file in {data_pattern}; do cp "$file" $TMP;done

echo "analysis"
source activate caiman
conda env export > {env_file_stub}$SLURM_JOBID_env.yml

caiman_runner --file $TMP --ncpus {n_cpu} --mc_settings {mc_settings_file} --cnmf_settings {cnmf_settings_file} --qc_settings {qc_settings_file}

for file in $TMP/*.mmap; do cp "$file" {jobcreator_output_dir};done
for file in $TMP/*.hdf5; do cp "$file" {jobcreator_output_dir};done
for file in $TMP/*.pkl; do cp "$file" {jobcreator_output_dir};done
"""

    return job_file
