#!/bin/bash -i

# Author:  Kenneth Schackart
# Date:    9 June 2021
# Purpose: Create conda environments for each directory in ../tool_envs using exported yamls


# Get activate_env alias from ~/.bashrc
source ~/.bashrc

# Relative path to where all the tool environment directories are
cd ../tool_envs

# Initialize a counter variables
n_envs = 0
n_partials = 0

# Iterate through each tool environment directory
# Create environment from yaml
# Check that environment was created and can be activated
# Deactivate the conda environment
# Go back up to the tool_envs directory
for tool_env in */
do
   cd $tool_env
   echo "Creating $tool_env environment."
   FILE="${tool_env%?}_env.yml"
   if [ -f $FILE ]; then
      conda env create --file $FILE
      if [$? == "0"]; then
         echo "Created env from $FILE."
         activate_env
         if [$? == "0"]; then
            n_envs=$((n_envs + 1))
            conda deactivate
         else
            echo "Env created from $FILE but could not be activated."
            n_partials=$((n_partials + 1))
         fi
      fi
   else
      echo "File: $FILE not found. Skipping."
   fi
   cd ..
done

echo "Done."
echo "Successfully created $n_envs conda environments."
echo "Created $n_partials environments that could not be activated."
