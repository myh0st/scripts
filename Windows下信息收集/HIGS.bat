@echo off
REM ---------------------------------------------
REM Host Information Gathering Script (Windows Edition)
REM Written by Jason Ross <algorythm@gmail.com>
REM ---------------------------------------------
REM Version: 0.3
REM Last Modified: 2014.06.03
REM ---------------------------------------------
REM Simple Windows batch file to gather system
REM information for use during a host config
REM review, or as an aid to Incident Response.
REM All output goes into a folder which named
REM whatever the %COMPUTERNAME% variable is set to.
REM ---------------------------------------------
REM Depends on the psloglist tool from SysInternals
REM (now Microsoft). It's part of the PSTools suite
REM http://technet.microsoft.com/en-us/sysinternals/bb896649.aspx
REM ---------------------------------------------
REM Tested on the following platforms:
REM Server:
REM    Windows 2003 SP2
REM    Windows Server 2012
REM Desktop:
REM    Windows 7 Professional (32 bit)
REM    Windows 7 Professional (64 bit)
REM    Windows XP SP3
REM    Windows XP SP2
REM ---------------------------------------------
REM TODO: update this to check for powershell
REM       and use that to perform more robust
REM       checks. Also needs to be updated badly
REM       to utilize the newer features of IIS
REM ---------------------------------------------
REM This program is free software: you can redistribute it and/or modify
REM it under the terms of the GNU General Public License as published by
REM the Free Software Foundation, either version 3 of the License, or
REM (at your option) any later version.
REM
REM This program is distributed in the hope that it will be useful,
REM but WITHOUT ANY WARRANTY; without even the implied warranty of
REM MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
REM GNU General Public License for more details.
REM
REM You should have received a copy of the GNU General Public License
REM along with this program.  If not, see <http://www.gnu.org/licenses/>.
REM ---------------------------------------------
REM Copyright 2010-2014 Jason Ross <algorythm /at/ gmail /dot/ com>
REM ---------------------------------------------
md %COMPUTERNAME%
cd %COMPUTERNAME%


echo =================
echo Gathering basic information
echo =================
echo Host Configuration Tool >> basic-info.txt
echo Output Created on %DATE% at %TIME% >> basic-info.txt
echo ================= >> basic-info.txt
echo Domain: %USERDOMAIN% >> basic-info.txt
echo This host: %COMPUTERNAME% >> basic-info.txt
echo This script running as: %USERNAME% >> basic-info.txt
echo ================= >> basic-info.txt
echo Environment Variables: >> basic-info.txt
set >> basic-info.txt
echo ================= >> basic-info.txt
echo System Info: >> basic-info.txt
systeminfo >> basic-info.txt
echo Done!
echo.


echo =================
echo Detecting installed software
echo =================
reg export HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall reg.txt
find "DisplayName" reg.txt |find /V "ParentDisplayName" > tmplist.txt
for /f "tokens=2,3 delims==" %%a in (tmplist.txt) do (echo %%a >> software.txt)
echo Done!
echo.


echo =================
echo Detecting installed hotfixes
echo =================
wmic qfe list >hotfixes.txt
echo Done!
echo.

echo =================
echo Creating list of registered services
echo =================
sc query state= all >> services.txt
echo Done!
echo.


echo Enumerating network servers visible to this host
echo ================= > net-view.txt
net view >> net-view.txt
echo Done!
echo.


echo =================
echo Gathering local user and group information
echo =================
net localgroup >> localgroups.txt
net user >> localusers.txt
net localgroup administrators >> localadminusers.txt
echo Done!
echo.


echo =================
echo Gathering shared folder information
echo =================
net view /a \\%COMPUTERNAME% >> shares.txt
echo Done!
echo.


echo =================
echo Gathering IP configuration
echo =================
ipconfig /all >> ipconfig.txt
echo Done!
echo.


echo =================
echo Detecting open ports
echo =================
netstat -ban >> netstat.txt
echo Done!
echo.


echo =================
echo Checking scheduled jobs
echo =================
at >> at.txt
echo Done!
echo.


echo =================
echo Checking IIS sites
echo =================
%windir%\system32\inetsrv\AppCmd.exe list site > IIS_sites.txt
echo Done!
echo.


echo =================
echo Dumping the registry
echo =================
reg export HKLM hklm.reg
reg export HKCU hkcu.reg
reg export HKCU hkcr.reg
reg export HKCU hku.reg
reg export HKCU hkcc.reg
echo Done!
echo.


echo =================
echo Collecting logs, this may take a bit...
echo =================
..\psloglist -x system > system.log
..\psloglist -x security > security.log
..\psloglist -x application > application.log
echo Done!
echo.


echo =================
echo Cleaning up temporary files
echo =================
del reg.txt tmplist.txt
echo Done!
echo.


echo =================
echo Host Information Gathering Script finished.
echo =================
echo.
