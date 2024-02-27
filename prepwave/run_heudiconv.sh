#!/bin/bash
# ------------------------------------------------------------------
# [Author] Anuja Negi
#          Bash script to run heudiconv for converting dicoms to 
#          BIDS for the bling data
# ------------------------------------------------------------------

VERSION=0.1.0
SUBJECT=bling-heudiconv-convert
USAGE="Usage: bash run_heudiconv.sh"

#TODO: take these as input arguments
subjects=("COL")
data_dir="prepwave/data/dicoms"
heuristics_file="prepwave/heuristics/heuristic_bling.py"
exception_file="prepwave/exceptions/exception_bling.sh"
output_dir="prepwave/data/sub-$subject/"

for subject in ${subjects[@]}
do  
    
    sessions=$(find $data_dir/$subject/ -mindepth 1 -maxdepth 1 -type d | sort)

    for session in ${sessions[@]}
    do
        # dry pass to figure out naming for heuristic file
        session=${session##*/}
        echo -e "\nRunning heudiconv dry pass for subject $subject - session "$session...
        heudiconv -d $data_dir/{subject}/{session}/*/* -s $subject -ss $session -c none -f convertall -o $output_dir/ --overwrite
    
        # session management
        session_id=$(( $session_id + 1 ))
        . "$exception_file"

        # run heudiconv for coversions using the custom heuristics file
        echo -e "\nConverting for subject" $subject "- session #"$session_id $session" using heudiconv..."
        heudiconv -d $data_dir/{subject}/$session/*/* -s $subject -ss $session_id -f $heuristics_file -o $output_dir/ -c dcm2niix -b --overwrite
        
    done
done