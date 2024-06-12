#!/bin/bash

# export MTK_PASS=
# export MTK_USER=admin
# export MTK_HOST=192.168.1.11

set -e
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

INFILE=${SCRIPT_DIR}/routeros_path_list.txt
OUTFILE=${SCRIPT_DIR}/ros_paths.py
BACKUPFILE=${SCRIPT_DIR}/ros_paths.py.bak$(date +%Y%m%d_%H%M%S)

echo "Backing up '$OUTFILE' to '$BACKUPFILE'"
mv -f $OUTFILE $BACKUPFILE || true


cat $INFILE | while read ros_path; do
    RESULT=$(sshpass -p $MTK_PASS ssh -n $MTK_USER@$MTK_HOST ":put [$ros_path remove 10000]" || true)
    if [[ $RESULT == "no such item" ]]; then
        echo "list   /$ros_path"
        echo "\t'/$ros_path'," >> /tmp/routeros_list_paths.txt
    else
        echo "item   /$ros_path"
        echo "\t'/$ros_path'," >> /tmp/routeros_item_paths.txt
    fi 
done

echo "import array\n" >> $OUTFILE

echo "ROUTEROS_LIST_PATHS = [" >> $OUTFILE
cat /tmp/routeros_list_paths.txt >> $OUTFILE
echo "]\n" >> $OUTFILE

echo "ROUTEROS_ITEM_PATHS = [" >> $OUTFILE
cat /tmp/routeros_item_paths.txt >> $OUTFILE
echo "]\n" >> $OUTFILE
