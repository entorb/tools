@echo off

FOR /D %%D in ("*") DO (

echo ===
echo === %%D ====
echo ===
cd %%D
git reflog expire --expire=now --all
git gc --prune=now --aggressive
cd ..
)

pause
