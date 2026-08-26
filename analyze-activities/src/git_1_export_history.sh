#!/bin/bash

# ensure we are in the repos root dir
script_dir=$(dirname $0)
cd $script_dir/..

# cleanup
rm -fr data/git
mkdir -p data/git

cd ..

# loop over all repos
for D in $(ls -d */); do
  # remove trailing /
  D="${D%/}"

  # skip non-git dirs
  if [ ! -d "$D/.git" ]; then
    echo "$D is no git repo"
    continue
  fi

  echo $D
  cd $D

  git log --author=Torben --date=iso-strict --pretty="format:%ad: %s" --shortstat >../analyze-activities/data/git/$D.log

  cd ..
done

# %cd: committer date
# %h: abbreviated commit hash
# %s: commit subject
# %cn: committer name
# %an: author name
