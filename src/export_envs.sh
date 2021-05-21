#!/bin/bash -i

# Author:  Kenneth Schackart
# Date:    21 May 2021
# Purpose: Export conda environments for each directory in ../tool_envs


# Get activate_env alias from ~/.bashrc
source ~/.bashrc

# Relative path to where all the tool environment directories are
cd ../tool_envs

# Initialize a counter variable
n_exports = 0

# Iterate through each tool environment directory
# Activate the proper conda environment using bash alias
# If the conda environment exists and was activated then export it
# Deactivate the conda environment
# Go back up to the tool_envs directory
for tool_env in */
do
   cd $tool_env
   echo "Exporting $tool_env environment."
   activate_env
   if [$? == "0"]
      then
         conda env export > "${tool_env%?}_env.yml"
         n_exports=$((n_exports + 1))
         conda deactivate
   fi
   cd ..
done

echo "Done. Exported $n_exports conda environments"
