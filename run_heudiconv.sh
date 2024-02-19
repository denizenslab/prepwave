#!/bin/bash
# ------------------------------------------------------------------
# [Author] Anuja Negi
#          Bash script to run heudiconv for converting dicoms to 
#          BIDS for the bling data
# ------------------------------------------------------------------

VERSION=0.1.0
SUBJECT=bling-heudiconv-convert
USAGE="Usage: bash run_heudiconv.sh"

subjects=("COL")
data_dir="data/tunnel/dicoms"
heuristics_file="bling_heuristic.py"

for subject in ${subjects[@]}
do  
    output_dir="data/sub-$subject/"
    sessions=$(find $data_dir/$subject/ -mindepth 1 -maxdepth 1 -type d | sort)

    for session in ${sessions[@]}
    do
        # dry pass to figure out naming for heuristic file
        session=${session##*/}
        echo -e "\nRunning heudiconv dry pass for subject $subject - session "$session...
        heudiconv -d $data_dir/{subject}/{session}/*/* -s $subject -ss $session -c none -f convertall -o $output_dir/ --overwrite
    
    
        # run heudiconv for coversions using the custom heuristics file
        session_id=$(( $session_id + 1 ))
        #exceptions for COL subject
        if [[ $subject == "COL" ]]
        then
            if [[ $session == "20190607LG" ]]
            then
                session_id=2
            fi
            if [[ $session == "20190709LG" ]]
            then
                session_id=2
            fi
            if [[ $session == "20210810COL" ]]
            then
                session_id=3
            fi
            if [[ $session == "20210920COL" ]]
            then
                session_id=4
            fi
            if [[ $session == "20201013COL" ]]
            then
                session_id=5
            fi
            if [[ $session == "20201017COL" ]]
            then
                session_id=6
            fi

        fi

        echo -e "\nConverting for subject" $subject "- session #"$session_id $session" using heudiconv..."
        heudiconv -d $data_dir/{subject}/$session/*/* -s $subject -ss $session_id -f $heuristics_file -o $output_dir/ -c dcm2niix -b --overwrite
        
    done
    # run BIDS validator
    # echo -e "\nRunning BIDS validator on $output_dir ..."
    # bids-validator $output_dir
done