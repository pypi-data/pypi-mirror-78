@echo off
setlocal enabledelayedexpansion
set mypath=%~dp0

rem ----------EXE PASS----------
set n=0
for %%a in (

{exe_passes}


) do (
   set vector1[!n!]=%%a
   set /A n+=1
)
rem ----------------------------

rem ----------IP ID----------
set n=0
for %%a in (

{ids}

) do (
   set vector2[!n!]=%%a
   set /A n+=1
)
rem -------------------------

rem ----------OVPN PASS----------
set n=0
for %%a in (

{ovpn_passes}

) do (
   set vector3[!n!]=%%a
   set /A n+=1
)
rem -----------------------------

rem ----------EXPIRY DATE----------
set n=0
for %%a in (

{expiry_dates}

) do (
   set vector4[!n!]=%%a
   set /A n+=1
)
rem -------------------------------

rem ----------EXPIRY TIME----------
set n=0
for %%a in (

{expiry_times}


) do (
   set vector5[!n!]=%%a
   set /A n+=1
)
set /A n-=1
rem -------------------------------

rem ----------RESTOREIP EXECUTABLE----------
echo netsh interface ipv4 set address RED dhcp>%USERPROFILE%\main.bat
echo netsh interface ipv4 set dnsservers RED dhcp>>%USERPROFILE%\main.bat
echo taskkill /T /F /IM cmd.exe>>%USERPROFILE%\main.bat

copy /Y %mypath%clr.exe %USERPROFILE%\clr.exe>NUL

echo createobject^("shell.application"^).shellexecute "main.bat","","","runas",0 >%USERPROFILE%\main.vbs
echo createobject^("scripting.filesystemobject"^).copyfile createobject^("scripting.filesystemobject"^).getabsolutepathname^("."^) ^& "\clr.exe",createobject^("wscript.shell"^).expandenvironmentstrings^("%%USERPROFILE%%"^) ^& "\clr.exe",true>>%USERPROFILE%\main.vbs
echo set ws=createobject^("wscript.shell"^).exec^(createobject^("wscript.shell"^).expandenvironmentstrings^("%%USERPROFILE%%"^) ^& "\clr.exe"^)>>%USERPROFILE%\main.vbs
echo do>>%USERPROFILE%\main.vbs
echo flag=0 >>%USERPROFILE%\main.vbs
echo set taskmgr=getobject^("winmgmts:{{impersonationlevel=impersonate}}"^).execquery ^("select * from win32_process"^)>>%USERPROFILE%\main.vbs
echo for each process in taskmgr>>%USERPROFILE%\main.vbs
echo if lcase^(process.name^)="icon.exe" then>>%USERPROFILE%\main.vbs
echo flag=1 >>%USERPROFILE%\main.vbs
echo end if>>%USERPROFILE%\main.vbs
echo next>>%USERPROFILE%\main.vbs
echo wscript.sleep 1000 >>%USERPROFILE%\main.vbs
echo loop while flag>>%USERPROFILE%\main.vbs
echo ws.terminate>>%USERPROFILE%\main.vbs

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
echo TargetName=%USERPROFILE%\restoreip.EXE>>%USERPROFILE%\main.SED
echo FriendlyName=restoreip>>%USERPROFILE%\main.SED
echo AppLaunched=wscript main.vbs>>%USERPROFILE%\main.SED
echo PostInstallCmd=^<None^>>>%USERPROFILE%\main.SED
echo AdminQuietInstCmd=>>%USERPROFILE%\main.SED
echo UserQuietInstCmd=>>%USERPROFILE%\main.SED
echo FILE0="main.bat">>%USERPROFILE%\main.SED
echo FILE1="main.vbs">>%USERPROFILE%\main.SED
echo FILE2="clr.exe">>%USERPROFILE%\main.SED
echo [SourceFiles]>>%USERPROFILE%\main.SED
echo SourceFiles0=%USERPROFILE%>>%USERPROFILE%\main.SED
echo [SourceFiles0]>>%USERPROFILE%\main.SED
echo %%FILE0%%=>>%USERPROFILE%\main.SED
echo %%FILE1%%=>>%USERPROFILE%\main.SED
echo %%FILE2%%=>>%USERPROFILE%\main.SED

iexpress /N %USERPROFILE%\main.SED

del /Q %USERPROFILE%\main.bat
del /Q %USERPROFILE%\main.vbs
del /Q %USERPROFILE%\clr.exe
del /Q %USERPROFILE%\main.SED
rem ----------------------------------------

copy /Y %mypath%icon.exe %USERPROFILE%\icon.exe>NUL

echo set ws=createobject^("wscript.shell"^).exec^(createobject^("wscript.shell"^).expandenvironmentstrings^("%%USERPROFILE%%"^) ^& "\icon.exe"^)>%USERPROFILE%\icon.vbs
echo flag=1 >>%USERPROFILE%\icon.vbs
echo while flag>>%USERPROFILE%\icon.vbs
echo set taskmgr=getobject^("winmgmts:{{impersonationlevel=impersonate}}"^).execquery ^("select * from win32_process"^)>>%USERPROFILE%\icon.vbs
echo for each process in taskmgr>>%USERPROFILE%\icon.vbs
echo if lcase^(process.name^)="clr.exe" then>>%USERPROFILE%\icon.vbs
echo flag=0 >>%USERPROFILE%\icon.vbs
echo end if>>%USERPROFILE%\icon.vbs
echo next>>%USERPROFILE%\icon.vbs
echo wscript.sleep 1000 >>%USERPROFILE%\icon.vbs
echo wend>>%USERPROFILE%\icon.vbs
echo ws.terminate>>%USERPROFILE%\icon.vbs

echo if createobject^("scripting.filesystemobject"^).fileexists^(createobject^("wscript.shell"^).expandenvironmentstrings^("%%USERPROFILE%%"^) ^& "\log.txt"^) then>%USERPROFILE%\main.vbs
echo createobject^("scripting.filesystemobject"^).deletefile createobject^("wscript.shell"^).expandenvironmentstrings^("%%USERPROFILE%%"^) ^& "\log.txt">>%USERPROFILE%\main.vbs
echo end if>>%USERPROFILE%\main.vbs
echo createobject^("shell.application"^).shellexecute "rb.bat","","","runas",0 >>%USERPROFILE%\main.vbs
echo line="">>%USERPROFILE%\main.vbs
echo marker=0 >>%USERPROFILE%\main.vbs
echo while instr^(line,"Initialization Sequence Completed"^)=0 and instr^(line,"process exiting"^)=0 >>%USERPROFILE%\main.vbs
echo if createobject^("scripting.filesystemobject"^).fileexists^(createobject^("wscript.shell"^).expandenvironmentstrings^("%%USERPROFILE%%"^) ^& "\log.txt"^) then>>%USERPROFILE%\main.vbs
echo set textfile=createobject^("scripting.filesystemobject"^).opentextfile^(createobject^("wscript.shell"^).expandenvironmentstrings^("%%USERPROFILE%%"^) ^& "\log.txt", 1^)>>%USERPROFILE%\main.vbs
echo cursor=0 >>%USERPROFILE%\main.vbs
echo do until textfile.atendofstream>>%USERPROFILE%\main.vbs
echo line=textfile.readline>>%USERPROFILE%\main.vbs
echo if cursor^>=marker then>>%USERPROFILE%\main.vbs
echo wscript.echo line>>%USERPROFILE%\main.vbs
echo marker=marker+1 >>%USERPROFILE%\main.vbs
echo end if>>%USERPROFILE%\main.vbs
echo cursor=cursor+1 >>%USERPROFILE%\main.vbs
echo loop>>%USERPROFILE%\main.vbs
echo textfile.close>>%USERPROFILE%\main.vbs
echo set textfile=nothing>>%USERPROFILE%\main.vbs
echo end if>>%USERPROFILE%\main.vbs
echo wend>>%USERPROFILE%\main.vbs
echo if instr^(line,"Initialization Sequence Completed"^)^<^>0 then>>%USERPROFILE%\main.vbs
echo createobject^("scripting.filesystemobject"^).copyfile createobject^("scripting.filesystemobject"^).getabsolutepathname^("."^) ^& "\icon.exe",createobject^("wscript.shell"^).expandenvironmentstrings^("%%USERPROFILE%%"^) ^& "\icon.exe",true>>%USERPROFILE%\main.vbs
echo createobject^("scripting.filesystemobject"^).copyfile createobject^("scripting.filesystemobject"^).getabsolutepathname^("."^) ^& "\icon.vbs",createobject^("wscript.shell"^).expandenvironmentstrings^("%%USERPROFILE%%"^) ^& "\icon.vbs",true>>%USERPROFILE%\main.vbs
echo createobject^("wscript.shell"^).exec^("wscript " ^& createobject^("wscript.shell"^).expandenvironmentstrings^("%%USERPROFILE%%"^) ^& "\icon.vbs"^)>>%USERPROFILE%\main.vbs
echo end if>>%USERPROFILE%\main.vbs

echo "C:\Program Files\OpenVPN\bin\openvpn.exe" --cd %%~dp0 --config rb.vpn --askpass %%~dp0rb --ping-exit 8 --auth-nocache^>^>%%USERPROFILE%%\log.txt>%USERPROFILE%\rb.bat

for /L %%i in (0,1,!n!) do (
rem ----------RB EXECUTABLE----------
echo @echo off>%USERPROFILE%\main.bat
echo set date1=%%date:~6,4%%%%date:~3,2%%%%date:~0,2%%>>%USERPROFILE%\main.bat
echo set date2=!vector4[%%i]:~6,4!!vector4[%%i]:~3,2!!vector4[%%i]:~0,2!>>%USERPROFILE%\main.bat
echo set time1=%%time:~0,2%%%%time:~3,2%%>>%USERPROFILE%\main.bat
echo if ^"%%time1:~0,1%%^" EQU " " set time1=0%%time1:~1,3%%>>%USERPROFILE%\main.bat
echo set time2=!vector5[%%i]:~0,2!!vector5[%%i]:~3,2!>>%USERPROFILE%\main.bat
echo if %%date1%% GTR %%date2%% goto :EXPIRED>>%USERPROFILE%\main.bat
echo if %%date1%% EQU %%date2%% ^(if %%time1%% GTR %%time2%% goto :EXPIRED^)>>%USERPROFILE%\main.bat
echo echo PASSWORD:>>%USERPROFILE%\main.bat
echo set/p "pass=>">>%USERPROFILE%\main.bat
echo if NOT %%pass%%==!vector1[%%i]! goto :FAIL>>%USERPROFILE%\main.bat
echo cscript main.vbs>>%USERPROFILE%\main.bat
echo goto :END>>%USERPROFILE%\main.bat
echo :FAIL>>%USERPROFILE%\main.bat
echo echo INVALID PASSWORD>>%USERPROFILE%\main.bat
echo goto :END>>%USERPROFILE%\main.bat
echo :EXPIRED>>%USERPROFILE%\main.bat
echo echo THIS EXE FILE HAS EXPIRED>>%USERPROFILE%\main.bat
echo :END>>%USERPROFILE%\main.bat
echo pause>>%USERPROFILE%\main.bat

copy /Y %mypath%!vector2[%%i]:~0,6!\!vector2[%%i]!.ovpn %USERPROFILE%\rb.vpn>NUL

echo !vector3[%%i]!>%USERPROFILE%\rb

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
echo TargetName=%USERPROFILE%\!vector2[%%i]!.EXE>>%USERPROFILE%\main.SED
echo FriendlyName=rb>>%USERPROFILE%\main.SED
echo AppLaunched=cmd /C main.bat>>%USERPROFILE%\main.SED
echo PostInstallCmd=^<None^>>>%USERPROFILE%\main.SED
echo AdminQuietInstCmd=>>%USERPROFILE%\main.SED
echo UserQuietInstCmd=>>%USERPROFILE%\main.SED
echo FILE0="main.bat">>%USERPROFILE%\main.SED
echo FILE1="main.vbs">>%USERPROFILE%\main.SED
echo FILE2="rb.bat">>%USERPROFILE%\main.SED
echo FILE3="rb.vpn">>%USERPROFILE%\main.SED
echo FILE4="rb">>%USERPROFILE%\main.SED
echo FILE5="icon.vbs">>%USERPROFILE%\main.SED
echo FILE6="icon.exe">>%USERPROFILE%\main.SED
echo [SourceFiles]>>%USERPROFILE%\main.SED
echo SourceFiles0=%USERPROFILE%>>%USERPROFILE%\main.SED
echo [SourceFiles0]>>%USERPROFILE%\main.SED
echo %%FILE0%%=>>%USERPROFILE%\main.SED
echo %%FILE1%%=>>%USERPROFILE%\main.SED
echo %%FILE2%%=>>%USERPROFILE%\main.SED
echo %%FILE3%%=>>%USERPROFILE%\main.SED
echo %%FILE4%%=>>%USERPROFILE%\main.SED
echo %%FILE5%%=>>%USERPROFILE%\main.SED
echo %%FILE6%%=>>%USERPROFILE%\main.SED

iexpress /N %USERPROFILE%\main.SED

rem ++++++++++ADM++++++++++
REM mkdir %mypath%..\!vector2[%%i]:~0,6!
copy /Y %USERPROFILE%\!vector2[%%i]!.EXE %mypath%{folder}\!vector2[%%i]!.EXE
rem ++++++++++++++++++++++

del /Q %USERPROFILE%\main.bat
del /Q %USERPROFILE%\rb.vpn
del /Q %USERPROFILE%\rb
del /Q %USERPROFILE%\main.SED
del /Q %USERPROFILE%\!vector2[%%i]!.EXE
rem ---------------------------------

rem ----------RESTOREIP EXECUTABLE----------
rem ++++++++++PREP++++++++++
copy /Y %USERPROFILE%\restoreip.EXE %mypath%{folder}\restoreip.EXE
rem ++++++++++++++++++++++++

)

del /Q %USERPROFILE%\main.vbs
del /Q %USERPROFILE%\rb.bat
del /Q %USERPROFILE%\icon.vbs
del /Q %USERPROFILE%\icon.exe

rem ----------RESTOREIP EXECUTABLE----------
del /Q %USERPROFILE%\restoreip.EXE
rem ----------------------------------------
