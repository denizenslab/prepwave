#!/bin/bash

subjects=("COL" )
data_dir="data/test/dicoms"
output_dir="data/bling_data"


# dry pass to figure out naming for heuristic file
for subject in ${subjects[@]}
do  
    sessions=$(find $data_dir/$subject/ -mindepth 1 -maxdepth 1 -type d)
    for session in ${sessions[@]}
    do
        echo \n "Running heudiconv dry pass for subject $subject - session "${session##*/}...
        heudiconv -d $data_dir/{subject}/{session}/*/* -s $subject -ss ${session##*/} -c none -f convertall -o $output_dir/
    done
done

# subject="COL"
# # get folder names in dicom folder
# folders=$(find data/test/dicoms/$subject/ -maxdepth 1 -type d -name "*")
# # print folder names
# # echo $folders
# # print only folder names and not full path
# # iterate through folders
# for folder in $folders:
# do
#     echo ${folder##*/}
# done