@echo off
rem This batch file simulating smartphone for testing the http messaging framework.
rem Needs an AB to be running and pinging the server.
rem Use AB's IP as deviceip
rem Supply comma seperated list of serverip


:if NOT "%JAVA_HOME%" == "" goto start
:echo Unable to determine the value of JAVA_HOME.
:goto eof

:start

SET LIB=C:\Autoclient\httpclient\lib

C:\jre\bin\java.exe -classpath %LIB%\server.jar;%LIB%\logi.crypto1.1.2.jar;%LIB%\httpclient-4.2.2.jar;%LIB%\httpcore-4.2.2.jar;%LIB%\httpmime-4.2.2.jar;%LIB%\kxml2-2.3.0.jar;%LIB%\commons-logging-1.1.1.jar;%LIB%\vocerahttpclient.jar message.client.VoceraHttpClient %1 %2 %3 %4 %5 %6 %7 %8 %9


:eof