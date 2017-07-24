@echo off
cd \VMI

set /A count=1
echo  # %count%    %date% %time% 

:FOREVER
vmitest.exe -ClientID hzhang -Server 10.37.133.101 -LoginID 202910 -Text "Happy Halloween" -WAVFiles "BwaaHaaHaa!" -Responses ""
sleep 45
echo  # %count%    %date% %time%

vmitest.exe -ClientID hzhang -Server 10.37.133.101 -LoginID 10067 -Text "" -WAVFiles "BwaaHaaHaa!" -Responses ""
sleep 45

vmitest.exe -ClientID hzhang -Server 10.37.133.101 -LoginID 10195 -Text "VMITest" -WAVFiles "BwaaHaaHaa!" -Responses ""
sleep 45

set /A count+=1
echo  # %count%    %date% %time%

goto FOREVER



:: vmitest.exe -ClientID hzhang -Server 10.37.133.101 -LoginID "test:T H F W" -Text "" -WAVFiles "BwaaHaaHaa!" -Responses ""