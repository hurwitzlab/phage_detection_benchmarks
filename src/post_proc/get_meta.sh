in_dir=$1
out_dir=$2

# -n      Suppress (double) printing
# ^.*     Anything at the beginning
# of\s    Word "of" followed by whitespace
# \(      Begin first capture group
# \S*     Any number of non-whitespace characters
# \)      End first capture group
# \s      Whitespace
# \(      Begin second capture group
# .[^,]*  Any number of anything but comma
# \)      End of second capture group
# ,*      Any number of commas
# .*      Any number of anything else
# $/      End of match string
# \1,\2   Capture group 1 comma capture group 2
# /p      Print result
echo "refseqID,description" > $out_dir/organisms.csv
grep -r ">" $in_dir | sed -n 's/^.*of\s\(\S*\)\s\(.[^,]*\),*.*$/\1,\2/p' >> $out_dir/organisms.csv