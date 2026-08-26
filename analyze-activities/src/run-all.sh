#!/bin/bash

# ensure we are in the repo root dir
script_dir=$(dirname $0)
cd $script_dir/..
# store cwd as variable
cwd=$(pwd)

mkdir -p data
mkdir -p output

# only if older than 1h, start the pre-script
f=data/git/analyze-activities.log
if [ ! -f $f ] || [ $(find $f -mmin +60) ]; then
  echo "## git_1_export_history"
  src/git_1_export_history.sh
fi

f=data/influx-media.csv
if [ ! -f $f ] || [ $(find $f -mmin +60) ]; then
  echo "## influx download"
  python src/influx_1_download.py
fi

f=data/oura_sleep.csv
if [ ! -f $f ] || [ $(find $f -mmin +60) ]; then
  echo "## oura download"
  cd ../analyze-oura
  python src/fetch.py
  cp data/data_sleep.csv $cwd/$f
  cd $cwd
fi

f=data/rtm_tasks_completed.csv
if [ ! -f $f ] || [ $(find $f -mmin +60) ]; then
  echo "## rtm download"
  cd ../rememberthemilk
  python src/tasks_completed.py
  cp output/tasks_completed.csv $cwd/$f
  cd $cwd
fi

for job in cal git_2 oura strava rtm influx_2 lifelog join; do
  echo "## $job"
  python3 src/$job.py
done
