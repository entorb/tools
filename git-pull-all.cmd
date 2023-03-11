@echo off

D:
cd D:\GitHub\entorb

FOR /D %%D in ("*") DO (
echo ===
echo === %%D ====
echo ===
cd %%D
git pull
cd ..
)

pause