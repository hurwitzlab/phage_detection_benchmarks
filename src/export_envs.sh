#!/bin/bash -i

# Get activate_env alias
source ~/.bashrc

cd ../tool_envs

for tool_env in */
do
   cd $tool_env
   echo "Exporting $tool_env environment."
   activate_env
   if [$? == "0"]
      then
         conda env export > "${tool_env%?}_env.yml"
         conda deactivate
   fi
   cd ..
done
