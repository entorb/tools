@echo off

FOR /D %%D in ("*") DO (
echo ===
echo === %%D ====
echo ===
cd %%D
git pull
cd ..
)

pause
