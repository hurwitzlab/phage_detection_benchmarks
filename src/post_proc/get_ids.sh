#!/usr/bin/bash

in_dir=$1
out_dir=$2

if [ ! -d "$out_dir" ]; then
   mkdir $out_dir
fi

echo "match" > $out_dir/ids.csv

grep -r ">" $in_dir/*/*.fna >> $out_dir/ids.csv
