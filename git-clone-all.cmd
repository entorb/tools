@echo off

REM first open and unlock the SSH Key for the computer via Putty Pageant

D:
cd D:\GitHub

FOR %%D in (arduino-sensorics, COVID-19-Coronavirus-German-Regions, HackerRank, private, raspi-sensorics, rememberthemilk, sql2csv, tools, tools-backup-scripts, tools-photos, twitter-gov-accounts) DO (

echo ===
echo === %%D ====
echo ===
git clone https://github.com/entorb/%%D
)

pause