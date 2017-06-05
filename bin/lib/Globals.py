#!/usr/bin/python
################################################################################
#
# Module:     Globals.py
#
# Author:      Joe White
#			
# Descr:      Define Cmtest globals
#
# Version:    (See below) $Id$
#
# Changes:    Conversion from Globals.pm perl to Python
#			
#
# Still ToDo:
#
# License:   This software is subject to and may be distributed under the
#            terms of the GNU General Public License as described in the
#            file License.html found in this or a parent directory.
#            Forward any and all validated updates to Paul@Tindle.org
#
#            Copyright (c) 1993 - 2005 Paul Tindle. All rights reserved.
#            Copyright (c) 2005-2012 Stoke. All rights reserved.
#            Copyright (c) 2017 Joe White. All rights reserved.
#
################################################################################
VER= 'v0.1 5/4/2017'; #Conversion to Python
CVS_VER = ' [ Git: $Id$ ]'
global CMtestVersion
if "CMtestVersion" not in globals() : CMtestVersion={}
CMtestVersion['Globals'] = VER + CVS_VER;
#______________________________________________________________________________

import sys    #Added for Ubuntu 9.10 support should work with Fedora
                # Global var defs
#import platform.uname  # Hostname
import platform
#import os.name
#import getpass.getuser
import getpass
#import os.getpid
import datetime
#import os.environ
import os
import time


#def Myglobals():
print ("Setting globals")

global Products ; Products = "SSX"
global CMPipe;  CMPipe = os.getenv('CmTest_Release_Pipe', "MIA")
#global AX4000_IP       = 'AX4000'      # Updated by TestCtrl.cfg
#global AX4000_USER     = 'AX4000'      # Updated by TestCtrl.cfg
global DefFanSpeed; DefFanSpeed = 'High'        # Updated by TestCtrl.cfg
global Debug_UUT; Debug_UUT     = 0        	  	  # Updated by TestCtrl.cfg, Default off
global Development; Development	= 0      		  # Updated by TestCtrl.cfg, Default off
global UUT_Ver_check; UUT_Ver_check	= 1 			  # Default is to check for versions
global UUT_Variable_ref; UUT_Variable_ref = []			  # Reference to hash values pulled from uutcfg dir
global Term_Msg; Term_Msg		  = ""			  # Modifies the output prompt when set(used by Init Termserver
global TelnetEscape; TelnetEscape	  = "["		      # ctrl[ modifies the telnet excape when using a daisy chanied terminal server (test equipment->dut)

global Baud; Baud            = '9600'               # Updated by TestCtrl.cfg
global Bell; Bell            = ""
global Comm_Log; Comm_Log        = ''                   # Log file for com app (minicom)
global Screen_Data; Screen_Data     = []                   # use this instead
global Debug; Debug = 0
global Erc; Erc             = 0
global Enable_EE_Write; Enable_EE_Write = 0                    # Update EEPROM data if required
global Errors; Errors          = [0,0,0]              # $Errors[0] = total error count since start of test
global Exit_On_Timeout; Exit_On_Timeout = 1                    # Normal state, may be changed in a cmd file
global Email_Notification; Email_Notification = 0          # 0 = No email notifications 1 = Send email to test step
global FH; FH              = 'F00'                # Global File Handle
global FH_count; FH_count              = 0                # Global File Handle counter (added in Python)
global FTest_Ptr; FTest_Ptr       = 0                    # Pointer to $TestData{FTEST}
global GUI; GUI             = 0                   # enable Tk interfaces, turned on by -g
global GUID; GUID            = 0                    # Global Unit ID (SigmaProbe)
global Home; Home            = os.name           # Will be '' if Win32, but that's OK!
#global Host_ID         = os.hostname
global Host_ID; Host_ID         = platform.uname()[1]      # uses import platform.uname
global Log_Str; Log_Str         = ''                   # For passing messages between subs
global MacAddr; MacAddr         = ''
global Main ; Main            = __file__      # Script file name without the path
global Last_Log_Time; Last_Log_Time = 0
# Perl Code conversion needed
#global Op_ID           = (defined $ENV{USERNAME}) ? $ENV{USERNAME}
#                     : (defined $ENV{USER}) ? $ENV{USER} : 'Unknown';
global Op_ID; Op_ID  = getpass.getuser()
global PN; PN              = []                   # @PN & @SN: [0] = system, [1] = MoBo, ...
global Quiet; Quiet           = 0                    # $opt_q parameter
global SN; SN              = []
global MAC; MAC              = []     			 # Added JW format "xx.xx.xx.xx.xx:x"(mac:qty)
global Cfg_File;  Cfg_File          = ""           #Not sure this is needed(pulled in from Perl)
global CmdFilePath; CmdFilePath = ""            #Not sure this is needed(pulled in from Perl)

global Stats; Stats           = {                     # Used by the Stats mechanism
            'ECT'        :'',                  # Expected Completion Time
            'ELT'        : '',                  # Expected Loop Time
            #'Host_ID'    : $ENV{HOSTNAME},      # HostID for logging purposes
            'Host_ID'    : Host_ID,      # # uses use Sys::Hostname; for ubuntu and fedora
            'Loop'       : 0,                   # Loop counter (and flag!)
            'PID'        : os.getpid(),                  # PID for this process
            'PPID'       : os.getppid(),             # PID for shell that launched this
            'Power'      : '',                  # Which power module to switch
            'Result'     : 'INCOMPLETE',        # Final Result
            'Session'    : 0,                   # Session no [1..#Ports on the system]
            'Started'    : int(time.time()),  #epoch time   # Ascii version of TimeStamp  python using PT_Date (time,1)
            'Status'     : '',                  # OK|Running|Finished fluff
            'TimeStamp'  : int(time.time()),                # Start-time - used for all logging finctions
            'TTG'        : '',                  # (Test) Time To Go ($Stats{ECT} - time)
            'Updated'    : int(time.time()),                # Time stamp of last update
            'UUT_ID'     : ''                   # Primary Serial no to be used for logging purposes
        }

global Stats_Path; 
Stats_Path      = ''
global Tmp; Tmp             =  "$Home/tmp"

global TestData; TestData = {
            'ATT'        : 0,                   # Actual Test Time (excl. wait time) (secs)
            'Diag_Ver'   : '',                  # Diag version extracted from header
            'ERC'        : '',                  # The last $Erc reported
            'Power'      : '',                  # Which power module (A|B) was in use (last or on 1st error
            'TID'        : '',                  # Test ID
            'TOLF'       : '',                  # Time Of Last Failure (time code) [set in &Logs::Log_Error]
            'TSLF'       : '',                  # Time Since Last Failure (secs)
            'TEC'        : 0,                   # Total Error Count
            'TTF'        : '',                  # Time To Failure (secs)
            'TTT'        : 0,                   # Total Test Time (secs)
            'SW_Ver'     : '',                  # (UUT Installed) SW Version
            'Ver'        : '',                   # Code version
            'Pipe'       : os.getenv('CmTest_Release_Pipe', "MIA"),   # $ENV{CmTest_Release_Pipe}                   # Code Pipe Selected
        }

global Test_Log ; Test_Log        = ''                   # File name of the (possibly permenant) test results log
global TestLogPath; TestLogPath     = ''                   # subdirectory of $LogPath
global UUT_IP ; UUT_IP         = ''                   # The IP Address to be assigned for this session
global UUT_IP2 ; UUT_IP2         = ''                   # The IP Address to be assigned to the next session
                                                 #  (we need to know this for systest run)
global UUT_Type;UUT_Type        = ''                  # Specific product discovered in boot banner
global Verbose;Verbose         = 0;                    # $opt_v parameter
global Wait_Time;Wait_Time       = 0                    # This one will be incremented during waits to offset TTT
global XLog;XLog            = ''                   # Rotated eXecution Log
global XML_Tags ; XML_Tags        = []                   # Somewhere to save the tags so to create the end tag
global WebData; WebData = []                        #Moved from PT.py 5/15/17
        #
        # The %Globals hash is used to:
        #
        # Define ligitimate global variables:
        #                - if ! defined $$Globals{$Which_Key} then
        #                -                abort with $Erc = $DErc
        #                - elsif $$Globals{$Which_Key} [is non-zero]
        #                -                abort with $Erc = $$Globals{$Which_Key}
        #
        #                - Declare ligitimate but unessential vars by
        #                                'Var' => 0

global GlobalVar; GlobalVar = {   # Globals Dictionary will use to replace perl string pointer to string ${$Var} = Data
            "CmdFilePath"     : 21,
            "HashDefPath"     : 21,
            "Location"        : 21,
            "LogPath"         : 21,  # usually /var/local/cmtest/logs from testctrl.cfg
            "LogPathLocal"          : 21,
            "Out_File"        : 0,
            "PC_IP1"          : 0,
            "PC_IP2"          : 0,
            "Power_Switch_IP" : 0,
            "Power_Switch2_IP" : 0,
            "Stats_Path"      : 21,
            "UUT_IP_Base"     : 21,
            "UUT_IP_Range"    : 21,
            "User"            :21,
            "PW"            :21,
            }
global Menu_List;Menu_List = {};
global Menu_Desc;Menu_Desc = {};
global Menu_Cmd;Menu_Cmd  = {};
global GP_Path; GP_Path ="none"

global Util_only;  Util_only = 0
global UserID; UserID = "none"
global Out_File; Out_File = "" # optional -O ouput xml file

# from Connect
global Loop_Time;Loop_Time       = 0;        # ATT inside of the loop cycle
global LBuffer;LBuffer         = ();       # Loop buff
global Caching; Caching         = 0;        # Set by a <Loop> cmd, unset by </Loop>
#    our $Retry_Count     = 0;        # Set by a <Retry> cmd, unset by </Retry>
global PathSep; 
if os.name == "nt" : PathSep = "\\" 
else: PathSep = "/"
#print(globals())
print ("Globals init .. Done:%i" % Debug)
                #return
#__________________________________________________________________________
1;
