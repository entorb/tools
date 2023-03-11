@echo off

FOR /D %%D in ("*") DO (
echo ===
echo === %%D ====
echo ===
cd %%D
git fetch origin
git reset --hard origin/main
git pull 
cd ..
)

pause