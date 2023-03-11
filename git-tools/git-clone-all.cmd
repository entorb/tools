@echo off

REM first open and unlock the SSH Key for the computer via Putty Pageant

set baseurl=https://github.com/entorb

FOR %%D in (arduino-sensorics, COVID-19-Coronavirus-German-Regions, dissertation, HackerRank, private, raspi-sensorics, rememberthemilk, sql2csv, tools, tools-backup-scripts, tools-photos, twitter-gov-accounts) DO (

echo ===
echo === %%D ====
echo ===
git clone %baseurl%/%%D
)

pause

