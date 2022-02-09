#!/usr/bin/env bash

GLOBS=$1
PARENT_DIR=$2
OUT_FILE=$3

# If the output file already exists, remove it
if [ -f $OUT_FILE ]; then
	rm $OUT_FILE
fi

# Find files matching the globs, write to file
for GLOB in $(cat $GLOBS)
do
	echo $(ls $PARENT_DIR$GLOB) >> $OUT_FILE
	
done

echo "Done."
