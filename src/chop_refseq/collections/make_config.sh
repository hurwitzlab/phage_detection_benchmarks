#!/bin/bash
cd ..

conf="collections/config.yaml"

echo "chopper:" > $conf
echo -e "\tpython3 ../genome_chopper/chopper.py" >> $conf
echo "lengths:" >> $conf
echo -e "\t500: \"500\"" >> $conf
echo -e "\t1000: \"1000\"" >> $conf
echo -e "\t3000: \"3000\"" >> $conf
echo -e "\t5000: \"5000\"" >> $conf

for kingdom in archaea bacteria fungi viral
do
	ls ../../data/refseq/$kingdom/*.fna > collections/all_${kingdom}.txt
	echo "$kingdom:" >> $conf
	cat collections/all_${kingdom}.txt | while read line || [[ -n "$line" ]];
	do
		path=${line%.fna}
		base=${path##*/}
		echo -e "\t${base}: \"${line}\"" >> $conf
	done
done
