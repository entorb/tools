@echo off

FOR /D %%D in ("*") DO (
REM FOR /D %%D in (private, tools, tools-backup-scripts, tools-photos) DO (
REM FOR /D %%D in (tools) DO (

echo ===
echo === %%D ====
echo ===
cd %%D
git add .
git commit -m "improvements"
git push
cd ..
)

pause
