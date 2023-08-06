@echo off
setlocal enabledelayedexpansion

rem ----------IP ID----------
set n=0
for %%a in (

{ids}

) do (
   set vector1[!n!]=%%a
   set /A n+=1
)
rem -------------------------

rem ----------IP PASS----------
set n=0
for %%a in (

{ovpn_passes}

) do (
   set vector2[!n!]=%%a
   set /A n+=1
)
set /A n-=1
rem ---------------------------

rem ----------CHECK EXECUTABLE----------
echo taskkill /f /im openvpn.exe>%USERPROFILE%\kill.bat

echo @echo off>%USERPROFILE%\main.bat
echo setlocal enabledelayedexpansion>>%USERPROFILE%\main.bat
set /A total=!n!+1

for /L %%i in (0,1,!n!) do (
echo "C:\Program Files\OpenVPN\bin\openvpn.exe" --cd %%~dp0 --config rb%%i.vpn --askpass rb%%i --ping-exit 8 --script-security 2 --up kill.bat^|find /i "Inactivity timeout"^>NUL>>%USERPROFILE%\main.bat
echo if "%%time:~0,1%%" EQU " " ^(>>%USERPROFILE%\main.bat
echo if ^^!ERRORLEVEL^^! EQU 1 echo !vector1[%%i]!;ACTIVO^>^>%~dp0{file_name}.csv>>%USERPROFILE%\main.bat
echo if ^^!ERRORLEVEL^^! EQU 0 echo !vector1[%%i]!;INACTIVO^>^>%~dp0{file_name}.csv>>%USERPROFILE%\main.bat
echo ^) else ^(>>%USERPROFILE%\main.bat
echo if ^^!ERRORLEVEL^^! EQU 1 echo !vector1[%%i]!;ACTIVO^>^>%~dp0{file_name}.csv>>%USERPROFILE%\main.bat
echo if ^^!ERRORLEVEL^^! EQU 0 echo !vector1[%%i]!;INACTIVO^>^>%~dp0{file_name}.csv>>%USERPROFILE%\main.bat
echo ^)>>%USERPROFILE%\main.bat
set /A completed=%%i+1
echo echo !completed!/%total% COMPLETED>>%USERPROFILE%\main.bat
)

for /L %%i in (0,1,!n!) do (
copy %~dp0!vector1[%%i]:~0,6!\!vector1[%%i]!.ovpn %USERPROFILE%\rb%%i.vpn
)

for /L %%i in (0,1,!n!) do (
echo !vector2[%%i]!>%USERPROFILE%\rb%%i
)

echo [Version]>%USERPROFILE%\main.SED
echo Class=IEXPRESS>>%USERPROFILE%\main.SED
echo SEDVersion=3 >>%USERPROFILE%\main.SED
echo [Options]>>%USERPROFILE%\main.SED
echo PackagePurpose=InstallApp>>%USERPROFILE%\main.SED
echo ShowInstallProgramWindow=0 >>%USERPROFILE%\main.SED
echo HideExtractAnimation=1 >>%USERPROFILE%\main.SED
echo UseLongFileName=0 >>%USERPROFILE%\main.SED
echo InsideCompressed=0 >>%USERPROFILE%\main.SED
echo CAB_FixedSize=0 >>%USERPROFILE%\main.SED
echo CAB_ResvCodeSigning=0 >>%USERPROFILE%\main.SED
echo RebootMode=N>>%USERPROFILE%\main.SED
echo InstallPrompt=%%InstallPrompt%%>>%USERPROFILE%\main.SED
echo DisplayLicense=%%DisplayLicense%%>>%USERPROFILE%\main.SED
echo FinishMessage=%%FinishMessage%%>>%USERPROFILE%\main.SED
echo TargetName=%%TargetName%%>>%USERPROFILE%\main.SED
echo FriendlyName=%%FriendlyName%%>>%USERPROFILE%\main.SED
echo AppLaunched=%%AppLaunched%%>>%USERPROFILE%\main.SED
echo PostInstallCmd=%%PostInstallCmd%%>>%USERPROFILE%\main.SED
echo AdminQuietInstCmd=%%AdminQuietInstCmd%%>>%USERPROFILE%\main.SED
echo UserQuietInstCmd=%%UserQuietInstCmd%%>>%USERPROFILE%\main.SED
echo SourceFiles=SourceFiles>>%USERPROFILE%\main.SED
echo [Strings]>>%USERPROFILE%\main.SED
echo InstallPrompt=>>%USERPROFILE%\main.SED
echo DisplayLicense=>>%USERPROFILE%\main.SED
echo FinishMessage=>>%USERPROFILE%\main.SED
echo TargetName=%USERPROFILE%\check.EXE>>%USERPROFILE%\main.SED
echo FriendlyName=check>>%USERPROFILE%\main.SED
echo AppLaunched=cmd /C main.bat>>%USERPROFILE%\main.SED
echo PostInstallCmd=^<None^>>>%USERPROFILE%\main.SED
echo AdminQuietInstCmd=>>%USERPROFILE%\main.SED
echo UserQuietInstCmd=>>%USERPROFILE%\main.SED
echo FILE0="kill.bat">>%USERPROFILE%\main.SED
echo FILE1="main.bat">>%USERPROFILE%\main.SED
for /L %%i in (0,1,!n!) do (
set /A index=3+%%i
echo FILE!index!="rb%%i.vpn">>%USERPROFILE%\main.SED
)
for /L %%i in (0,1,!n!) do (
set /A index=3+!n!+1+%%i
echo FILE!index!="rb%%i">>%USERPROFILE%\main.SED
)
echo [SourceFiles]>>%USERPROFILE%\main.SED
echo SourceFiles0=%USERPROFILE%>>%USERPROFILE%\main.SED
echo [SourceFiles0]>>%USERPROFILE%\main.SED
echo %%FILE0%%=>>%USERPROFILE%\main.SED
echo %%FILE1%%=>>%USERPROFILE%\main.SED
for /L %%i in (0,1,!n!) do (
set /A index=3+%%i
echo %%FILE!index!%%=>>%USERPROFILE%\main.SED
)
for /L %%i in (0,1,!n!) do (
set /A index=3+!n!+1+%%i
echo %%FILE!index!%%=>>%USERPROFILE%\main.SED
)

iexpress /N %USERPROFILE%\main.SED

copy %USERPROFILE%\check.EXE %~dp0{file_name}.exe

del /Q %USERPROFILE%\kill.bat
del /Q %USERPROFILE%\main.bat
for /L %%i in (0,1,!n!) do (
del /Q %USERPROFILE%\rb%%i.vpn
)
for /L %%i in (0,1,!n!) do (
del /Q %USERPROFILE%\rb%%i
)
del /Q %USERPROFILE%\main.SED
del /Q %USERPROFILE%\check.EXE
rem ------------------------------------