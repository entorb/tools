@echo off

Update of 30.07.2022:
see https://github.com/entorb/COVID-19-Coronavirus-German-Regions/blob/master/truncate-data-commit-history.sh




set myRepoBaseURL=https://github.com/entorb/
set myRepoName=COVID-19-Coronavirus-German-Regions

echo 1. create new mirror of remote repo
REM git clone --mirror %myRepoBaseURL%%myRepoName%
REM need to use bare instead of mirror, because of GitHub pull requests
git clone --bare %myRepoBaseURL%%myRepoName%
pause

echo 2. cleanup
mkdir bfg-backup-dirs

cd %myRepoName%
REM DL from https://rtyley.github.io/bfg-repo-cleaner/

move cache ..\bfg-backup-dirs\
java -jar ../bfg-1.14.0.jar --delete-folders cache 
move data ..\bfg-backup-dirs\
java -jar ../bfg-1.14.0.jar --delete-folders data 
pause

git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo 3. restore some dirs
move ..\bfg-backup-dirs\cache .\
move ..\bfg-backup-dirs\data .\

pause

echo 4. push
git push --set-upstream origin master -f
git push
pause

cd ..
