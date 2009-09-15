#!/bin/bash

if [ $# -lt 2 ]; then
  echo "usage: $0 repository test_id index application"
  exit
fi

ROOT_DIR=~/AppBenchmark
remote=$1
test_id=$2
index=$3
application=$4

dest_dir="~/AppRepository/$test_id/$index"
echo $dest_dir

#scp ${ROOT_DIR}/logs/${application}/*.log ${remote}:${dest_dir}/
#mkdir -p ${ROOT_DIR}/logs/${application}/backup
#mv ${ROOT_DIR}/logs/${application}/*.log ${ROOT_DIR}/logs/${application}/backup

#scp ${ROOT_DIR}/logs/*.log ${remote}:${dest_dir}/
#mkdir -p ${ROOT_DIR}/logs/backup
#mv ${ROOT_DIR}/logs/*.log ${ROOT_DIR}/logs/backup

scp /tmp/data*.log ${remote}:${dest_dir}/
mkdir -p ${ROOT_DIR}/logs/backup
mv /tmp/data*.log ${ROOT_DIR}/logs/backup
