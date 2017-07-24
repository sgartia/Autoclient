@echo off
cd \VMI

set /A count=1
echo  # %count%    %date% %time% 

:FOREVER
REM vmitest.exe -ClientID gresurreccion -Server 10.37.144.4 -LoginID 321 -Text "BwaaHaaHaa" -WAVFiles "" -Responses "" -Priority "2"
REM vmitest.exe -ClientID gresurreccion -Server 10.37.144.4 -LoginID 100 -Text "BwaaHaaHaa" -WAVFiles "" -Responses "" -Priority "2"
REM vmitest.exe -ClientID gresurreccion -Server 10.37.144.4 -LoginID 200 -Text "BwaaHaaHaa" -WAVFiles "" -Responses "" -Priority "2"
REM vmitest.exe -ClientID Rauland-Urgent-THRAllianceVSTG -Server 10.37.133.102 -LoginID 9920032816 -Text "THR Rauland Urgent Test Text Message" -WAVFiles "" -Responses "" -Priority "2"
vmitest.exe -ClientID Rauland-Urgent-THRAllianceVSTG -Server 10.37.133.101 -LoginID Everyone -Text "THR Rauland Urgent Test Text Message" -WAVFiles "" -Responses "" -Priority "2"
sleep 3
echo  # %count%    %date% %time%


set /A count+=1
echo  # %count%    %date% %time%

if %count% LSS 3 goto FOREVER



:: vmitest.exe -ClientID gresurreccion -Server 10.37.144.4 -LoginID "Room 4101 Assistant" -Text "Happy Holidays" -WAVFiles "BwaaHaaHaa!" -Responses ""