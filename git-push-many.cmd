@echo off

D:
cd D:\GitHub\entorb

FOR /D %%D in (private, tools, tools-backup-scripts, tools-photos) DO (
echo ===
echo === %%D ====
echo ===
cd %%D
git add .
git commit -m "added more files"
git push
cd ..
)

pause
