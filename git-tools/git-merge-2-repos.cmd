@echo off
REM from https://medium.com/@checko/merging-two-git-repositories-into-one-preserving-the-git-history-4e20d3fafa4e
mkdir merged_repo
REM 1. init new repo
cd merged_repo
git init
touch test.txt
git add .
git commit -m "Initialize new repo"

set repo1="d:\GitHub-Backups\COVID-19-Coronavirus-German-Regions - 210523-no-data"
set repo2="d:\GitHub-Backups\COVID-19-Coronavirus-German-Regions - 210813-no-data"

REM 2. Add the first remote repository
git remote add -f repo1 %repo1%
git merge --allow-unrelated-histories repo1/master

REM 3. Create a sub directory and move all repo1 files to it.
mkdir repo1_backup
echo "manually move * -> repo1_backup/
pause
REM Linux: mv * repo1_backup/
REM Win: manually
git add .
git commit -m "Move repo1 files to repo1 directory, excluding .git dir"

REM 4. Add the second remote repository
git remote add -f repo2 %repo2%
git merge --allow-unrelated-histories repo2/master

REM 5. Fix any merge conflicts and complete the merge as follows
REM git merge --continue

pause
git status
pause

echo manually delete dir repo1_backup
pause
git add .
git commit -m "remove repo1_backup"
pause

copy %repo2%\.git\config .git\config
git status

echo now use git-bfg-cleanup-delete-history-of-dir.cmd to drop dir repo1_backup from history
pause




git push
