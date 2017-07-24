@echo off
cd \VMI

set /A count=1
echo  # %count%    %date% %time% 

:FOREVER
vmitest.exe -ClientID gresurreccion -Server 10.37.144.4 -LoginID tmosby -Text "Happy Holidays" -WAVFiles "BwaaHaaHaa!" -Responses ""
sleep 45
echo  # %count%    %date% %time%

vmitest.exe -ClientID gresurreccion -Server 10.37.144.4 -LoginID dwilliams -Text "" -WAVFiles "BwaaHaaHaa!" -Responses ""
sleep 45

vmitest.exe -ClientID gresurreccion -Server 10.37.144.4 -LoginID tiger -Text "VMITest" -WAVFiles "BwaaHaaHaa!" -Responses ""
sleep 45

set /A count+=1
echo  # %count%    %date% %time%

goto FOREVER



:: vmitest.exe -ClientID hzhang -Server 10.37.133.101 -LoginID "test:T H F W" -Text "" -WAVFiles "BwaaHaaHaa!" -Responses ""