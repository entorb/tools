@echo off

set myRepoBaseURL=https://github.com/entorb/
set myRepoName=COVID-19-Coronavirus-German-Regions.git
set myDirToDelete=data

REM 1. run create new mirror of remote repo
REM git clone --mirror %myRepoBaseURL%%myRepoName%
REM need to use bare instead of mirror, because of GitHub pull requests
git clone --bare %myRepoBaseURL%%myRepoName%

REM 2. cleanup
cd %myRepoName%
REM DL from https://rtyley.github.io/bfg-repo-cleaner/

java -jar ../bfg-1.14.0.jar --delete-folders cache 
java -jar ../bfg-1.14.0.jar --delete-folders data 
java -jar ../bfg-1.14.0.jar --delete-folders maps 
java -jar ../bfg-1.14.0.jar --delete-folders old 
java -jar ../bfg-1.14.0.jar --delete-folders plots-gnuplot 
java -jar ../bfg-1.14.0.jar --delete-folders plots-python 
java -jar ../bfg-1.14.0.jar --delete-folders plots-Excel 

pause

git reflog expire --expire=now --all
git gc --prune=now --aggressive

REM 3. push
REM git push
git push --set-upstream origin master -f
git push
pause

cd ..
