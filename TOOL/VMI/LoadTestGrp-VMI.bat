@echo off
cd \VMI

set /A count=1
echo  # %count%    %date% %time% 

:FOREVER
vmitest.exe -ClientID gresurreccion -Server 10.37.144.4 -LoginID 113 -Text "This is a load test message from Gary!" -WAVFiles "" -Responses "" -Priority "2"
REM vmitest.exe -ClientID gresurreccion -Server 10.37.144.4 -LoginID 321 -Text "This is a load test message from Gary!" -WAVFiles "" -Responses "" -Priority "2"
vmitest.exe -ClientID gwbush -Server 10.37.144.4 -LoginID 100 -Text "This is a load test message from George!" -WAVFiles "" -Responses "" -Priority "2"
REM vmitest.exe -ClientID tmsoby -Server 10.37.144.4 -LoginID 200 -Text "This is a load test message from Ted" -WAVFiles "" -Responses "" -Priority "2"
REM vmitest.exe -ClientID dwilliams -Server 10.37.144.4 -LoginID Everyone -Text "This is a load test message to Everyone!" -WAVFiles "" -Responses "" -Priority "2"
sleep 3
echo  # %count%    %date% %time%


set /A count+=1
echo  # %count%    %date% %time%

if %count% LSS 3 goto FOREVER



:: vmitest.exe -ClientID gresurreccion -Server 10.37.144.4 -LoginID "Room 4101 Assistant" -Text "Happy Holidays" -WAVFiles "BwaaHaaHaa!" -Responses ""