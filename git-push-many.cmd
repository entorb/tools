@echo off

cd ..

FOR /D %%D in ("*") DO (
REM FOR /D %%D in (private, tools, tools-backup-scripts, tools-photos) DO (
REM FOR /D %%D in (tools) DO (

echo ===
echo === %%D ====
echo ===
cd %%D
git add .
REM git commit -m "added more files"
git commit -m "improvements"
git push
cd ..
)

pause
