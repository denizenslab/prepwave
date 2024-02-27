#exceptions for COL subject
#!/bin/bash
# ------------------------------------------------------------------
# [Author] Anuja Negi
#          Bash script listing all the exceptions for the bling dataset
# ------------------------------------------------------------------

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
