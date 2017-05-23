#!/usr/bin/python
################################################################################
#
# Module:      Init.py
#
# Author:      Paul Tindle ( mailto:Paul@Tindle.org )
#			 Joe White( mailto:joe@stoke.com )
#
# Descr:      Main Library for Intitialization
#
# Version:    (See below) $Id$
#
# Changes:    Conversion Perl V1.17 to Python - JSW
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
#            Copyright (c) 2005-2013 Stoke. All rights reserved.
#            Copyright (c) 2017 Joe White. All rights reserved.
#
################################################################################
VER= 'v0.1 5/23/2017'; # Conversion to Python from Perl 052317 JSW
CVS_VER = ' [ Git: $Id$ ]'
CMtestVersionn['Init'] = VER + CVS_VER

#_____________________________________________________________________________
import Sys.Hostname    #Added for Ubuntu 9.10 support should work with Fedora
import File;
import Logs
import Util
import shutil
import Stats # qw( %Stats %TestData %Globals $Stats_Path);
# Not converted to Python use Cwd qw( abs_path ) What is it?
import time
usleep = lambda x: time.sleep(x/1000000.0)
# Not sure if this is going to be converted to Python JSW
##use SigmaProbe::SPUnitReport;
#use SigmaProbe::SPTestRun;
#use SigmaProbe::SPTimeStamp;
#use SigmaProbe::Local;
import Banner
from datetime import datetime, timedelta
from lib.Globals import *
import socket


#__________________________________________________________________________
def Final():
    "Last thing that's run before completion of cmtest"
    "Figures status and creates Event log"
    global Stats
    #&Print_Out_XML_Tag ();
    ID = Stats['UUT_ID']
    slot=0
    if (os.path.getsize(Out_File) and
         not ((Stats['UUT_ID'] == '') and  not Log_All )) : 
        Stamp = PT_Date(Stats['TimeStamp'], 9)
        if ID == '' : ID = 'unknown'
        Test_Log = TestLogPath+"/" + ID+"-"+Stamp.xml
        if TestLogPath == '':
            Exit (999, "Undefined test log path for %s" % Test_Log)
        try : 
            shutil.copy2(Test_Log, Out_File) #Copy like cp -p
        except:
            Exit (7, 'Failed log file copy')

    Stats.Update_Test_Times()

     
    if TestData['TEC'] == 0 and Stats['Result'] == 'INCOMPLETE' :
        Stats['Result'] = 'PASS'
    Stats['Status'] = 'Finished'
    Stats['TTG'] = 0
    Stats.Update_All
    XML_Tail()  #Added JSW - Stoke
    Print_Out_XML_Tag ()
    Print_Log (1, "Writing new Event & Cfg Log records ... ")
    Log_Event (Op_ID, PN[0], SN[0], TestData['TID'], Stats['Result'], fnstrip (Test_Log,3))
    Log_Event_Record (Op_ID, PN[0], SN[0], TestData['TID'], Stats['Result'], fnstrip (Test_Log,3))
    for i in range(1,25):        # Updated for 14 Slot Chassis 1/10/07
        if SN[i] == '': Log_Cfg (Op_ID, SN[0], (i - 1), PN[i], SN[i]) 
        if SN[i] == '': Log_Cfg_Record (Op_ID, SN[0], (i - 1), PN[i], SN[i]) 
        slot=i-1;
        if not SFPData_slot_ar[(slot)][0]['TYPE'] == '' :
        	for j in range(0,15) :
        		if not SFPData_slot_ar[(slot)][j]['PowerdBm'] == '' :
			    if not SFPData_slot_ar[(slot)][j]['SerialNo'] == '' :
				Log_Cfg (Op_ID, SN[0],slot+":"+j,SFPData_slot_ar[(slot)][j]['Vendor']+" "+SFPData_slot_ar[(slot)][j]['ModelNo']+" "+SFPData_slot_ar[slot][j]['PowerdBm']+"dBm",\
			             SFPData_slot_ar[(slot)][j]['SerialNo']) 
			    if not SFPData_slot_ar[(slot)][j]['SerialNo'] == '':
				Log_Cfg_Record (Op_ID, SN[0],slot+":"+j,SFPData_slot_ar[(slot)][j]['Vendor']+" "+SFPData_slot_ar[(slot)][j]['ModelNo']+" "+SFPData_slot_ar[(slot)][j]['PowerdBm']+"dBm", \
			             SFPData_slot_ar[(slot)][j]['SerialNo']) 
			else:
			    if not SFPData_slot_ar[(slot)][j]['SerialNo'] == '' : 
				Log_Cfg (Op_ID, SN[0],slot+":"+j,SFPData_slot_ar[(slot)][j]['Vendor']+" "+SFPData_slot_ar[(slot)][j]['ModelNo'], SFPData_slot_ar[(slot)][j]['SerialNo']) 
				if not SFPData_slot_ar[(slot)][j]['SerialNo'] == '' :
				    Log_Cfg_Record (Op_ID, SN[0],slot+":"+j,SFPData_slot_ar[(slot)][j]['Vendor']+" "+SFPData_slot_ar[(slot)][j]['ModelNo'], SFPData_slot_ar[(slot)][j]['SerialNo']) 
       	        
    Send_Email();  #Send our EMail Notifications

    #!!!    &Submit_SigmaQuest_Unit_Report;
    if GUI :Result (Stats['Result']) 
    #Convert seonds to Day Hour Min
    TTIME = datetime(1,1,1) + int(TestData['TTT'])
    TestTime = "DAYS:%i HOURS:%i MIN:%i SEC:%i" % TTIME.day, TTIME.hour, TTIME.minute, TTIME.second

    #Create Banner
    #Banner(new,fill,set)  final is tbd 
    banner_result = Banner(Stats['Result'], Stats['Result'])
    TID_result = Banner(TestData['TID'], TestData['TID'])
   
    Exit (0, "Finished! (%i) - %s %s %s!\n%s%s" % Test_Time, TestData['TID'],Session[Stats['Session']], Result[Stats['Result']],TID_result, banner_result)
    return
#_______________________________________________________________
def First_Time():
    " Check if test evironment is setup before running cmtest"

    Print_Log ( 1, "Running First_Time")

    print("\n\tThe main Test Controller configuration file (%s) is MIA!\n", % Cfg_File)
    print("\tPlease copy the defaults file '/var/local/cmtest/dist/cfgfiles/testctrl.defaults.cfg'\n")
    print("\tto /usr/local/cmtest and then edit the definitions as appropriate\n")
    print("\tAborting...\n\n")

    exit()

    # OR eventually if GUI...
    #system "java -jar First_Time.jar $Test_Cfg_XMLFile"
        #or die "Can't run java form";
    #&XML2Hash ($Test_Cfg_XMLFile); #This is now the one modified by Jez's jar
    # Then return to continue reading reading the cfg file
    return
#_______________________________________________________________
def Get_Release_Info():
    "Get our release pipe from env and compare to config

    File = GP_Path+"/bin/Release.id"
    Str  = ''
    if os.path.exists(File) :
        Erc = Read_Cfg_File (File);
	if Erc: exit( "Init died with Erc=$Erc trying to read Cfg_File")                # NB: No Erc translation yet!
        TestData['Ver'] = Version
        TestData['Pipe'] = Pipe
        Str = "Release_Info: File = %s: Version=%s Pipe=%s" % File, Version, Pipe
        if not Pipe == os.getenv('CmTest_Release_Pipe',"Not Found") :
        	exit("Init died with Pipe mismatch CMtest pipe:%s diff from ENV pipe:%s" % Pipe, os.getenv('CmTest_Release_Pipe',"Not Found") 
    else :
        Str = "File not found!" % File;

    if not Version == '' : return (Str)
    else return("No version")

#__________________________________________________________________________
def Init_All(Util_only):
    " This is the 1st Init stage, done before getopts,"
    "usually called at the beginning of &main::Init"
    global GP_Path
    global Cg_File
    global Tmp
    if os.geteuid()==0 and  not Util_only: exit(  "\n\tLet\'s not let \'root\' run a test - parochial ownership of files awaits!\n\n")
    # Acquired from cmtest.pl BEGIN block in v30 2006/02/15
    OS = os.name
    if os.name == "nt":
	OS = "NT"
    else:
	OS = "Linux"

    GP_Path = File.fnstrip()
    if GP_Path == '' : GP_Path = '..'       # for a $0 of ./

 #Get our base directory and find the Station Config File 
    File.fnstrip()
    if Debug > 0 : print ("OS path detected is:", File.fnstrip())
    PPATH = File.fnstrip()
    if PPATH == '': PPATH = ".."

    if OS == "NT":
	Cfg_File = PPATH + "\cfgfiles\testctrl.defaults.cfg"
	TmpDir = expanduser("~")
    else:
	Cfg_File = '/usr/local/cmtest/testctrl.cfg'
	TmpDir = expanduser("~") + "/tmp"  

    if OS == 'nt':
	Cfg_File = PPath + "/" + "cfgfiles/testctrl.defaults.cfg"
	Tmp = os.getenv('TMP', "NO_TMP")
    else :
	Cfg_File = r'/usr/local/cmtest/testctrl.cfg'
	Tmp = os.getenv(expanduser("~") + "/tmp", "NO_TMP")


    CmdFilePath = r"../" + GP_Path +r"/cmdfiles"
# end [acquired]

    try: 
	os.path.isdir(Tmp) # $Tmp is declared in $Globals
        try:
	    os.path.isfile(Tmp)
	except:
	    exit("Attempting to create \%s: file %s exists!" % Tmp, Tmp)
    except:
            try:
		os.mkdir(Tmp)
	    except:
		exit("Can\'t create tmp directory %s" % Tmp)
	
    if not Util_only:         # Required for test oriented scripts only ...

        try: 
	    os.path.isfile(Cfg_File)
	    First_Time 
	    Erc = Read_Cfg_File(Cfg_File)  # $Cfg_File is defined in main:: BEGIN block
	    if Erc: 
		exit("Init died with Erc=%s trying to read Cfg_File \'%s\'" % Erc, Cfg_File)                # NB: No Erc translation yet!
	try:
	    os.path.isfile(Cfg_File):
		exit("Cfg_File:%s doesn\'t exist" % Cfg_file)    # Temporary, until ...

        Erc = Log_History(1)
        if Erc : exit("Init died with Erc=%s trying to open History log" % Erc)

	#!! Check to make sure that GUID is set
        TestLogPath = LogPath+"/logfiles"
        if not os.path.isdir(TestLogPath) :
	    Exit(999, "No permenant log file path >%s<" % TestLogPath)
	return
#__________________________________________________________________________
def Init_Also(Util_only) :
    "This is the 3rd Init stage, done after getopts, etc"
    "usually called at the end of &main::Init"
    global GUI
    global Pid
    global XLog
    if Debug : 
	print( "\n\tDebug=%i\n\tQuiet=%i\n\tVerbose=%i\n\n" % Debug, Quiet,Verbose)

    Show_INC
    #our $GUI = ($ENV{DISPLAY} eq '') ? 0 : 1;        # !!! but what about Win32?
    GUI = 0

    #!!! we can probably lose this test, since disty.pm is the only declarer
    #     of $Util_Only, since no one else uses Init.pm!
    if not Util_only :        # Session = '' ...
	if not SessionForce :
	    Stats.Session ('next')               # Sets the next Session No.
        else :
            Stats['Session'] = Session;
            Pid = Stats.Session ('read');        # Returns 0 if available
                 # check the process table ...
            if Pid and not Pid == Stats['PID'] or Is_Running(Pid, 1) :
                 # The requested session is already running!
                if not SessionForce : Exit(107, "Session %i start declined" % Session) 
                Print_Log (11, "Forcing session %i" % Session)
            Stats.Session ('write')                # Tags the Session.

        Tmp += '/s' + Stats['Session']
        if not os.path.isdir : 
	    try : os.mkdir(Tmp)
	    except: exit("Unable to Create tmp dir %s" % Tmp)
        Arc_Logs (Tmp, '_logs')
        os.umask(0)
        Arc_File = "2arc2\_logs\_" + time.time()
        try:
	    fh = open(Arc_File,"w")
	    close(fh)
	except:
	    exit("Unable to create Arc_File %s" % Arc_File)

    # Set up log files...
    XLog = Tmp+"/"+Main+r".log";
    #!!!    &Read_Version;
    Msg = Get_Release_Info      # Sets $Version, etc or Aborts on error!
    if not Quiet : print( "\n\n" )
    if Stats['Session'] : Log_Str += "Session "+ Stats['Session']+": "
    Log_Str += "Starting %s version %s at %s" % Main, TestData['Ver'], PT_Date(time.time(), 2)
    Erc = Print_Log (1, Log_Str)
    Log_Str = ''
    if Erc : Exit (3, "(%s)" % Xlog)
    Print_Log (11,"This PID = %s, ShellPID = %s" % Stats['PID'], Stats['PPID'])
    Print_Log (11, 'path = ' + abs_path (GP_Path))
    for Module in( INC ) :
        Vers = Version[fnstrip(Module, 7)]
        Module  = INC[Module]  #Value (Full path / filename)
        if Module[0:1] == '.' :
            Module = osos.getcwd() +  "/" + Module
        Log_Str = "Lib: " + Module
	if Vers == '' : Log_Str += "\t[Ver: %s]" % Vers
        if not str.find(Module, "python") : Print_Log (11, Log_Str)
        IncAge = time.time() - stat.st_mtime(Module)
        if IncAge < 1000 : Print_Log (1, "Using new Module") 
    
    Log_Str = ''

    if not Util_only:                 # Required for test oriented scripts only ...
        Abort ('clear');             # Remove any lurking abort flags
        Stats['Status'] = 'UserID'
        Stats ['Power'] = 0  #Power supply on count
     	Stats.Update_All()
        print ("\n")
        if UserID == 'none' :
            X = Ask_User( 'text16', 'UserID', 'Please enter your UserID#' )
        
        UserID_tmp = UserID
	############################  Stop ##############################
        UserID = crypt $UserID, $Key;
        &UID_Check ($UserID_tmp);  #Exit on fail!  Use adduser.pl ...

        $Stats{'UserID'} = $UserID;
        $Stats{'Status'} = 'Menu';
        &Stats::Update_All();

        $Comm_Log = "$Tmp/Comm.log";
        # system "rm -f $Comm_Log";        # OR
#        &Rotate_Log ($Comm_Log, 10);
                                                        # Aborts on error!
        &Abort ('check');             # Make sure there isn't an ABORT flag lurking

                                      # Figure the UUT_IP address ...

        my (@IPA) = split (/\./, $UUT_IP_Base);
        my $UUT_IP_Top = $IPA[3] + $UUT_IP_Range - 1;        # Highest sub allowed
        $IPA[3] += ($Stats{'Session'} - 1);            # 1 per session or
        &Exit (28, "No IP addr available for this session") if $IPA[3] > $UUT_IP_Top;
        $UUT_IP  = "$IPA[0]\.$IPA[1]\.$IPA[2]\.$IPA[3]";
        $IPA[3]++; ##$IPA[3]++;  There is a possibility of conflict, but we shuld end up using 2 session if the second IP is used.
        &Exit (28, "No Secondary IP addr available for this session") if $IPA[3] > $UUT_IP_Top;
        $UUT_IP_SEC  = "$IPA[0]\.$IPA[1]\.$IPA[2]\.$IPA[3]";

        &Print_Log (11, "UUT_IP  = $UUT_IP");
        &Print_Log (11, "CmdFilePath = $CmdFilePath");

                        # Assign the output file ...

        $Out_File = ($opt_O eq '') ? "$Tmp/cmtest.xml" : $opt_O;
        system "rm -f $Out_File";
        &Print_Out_XML_Tag ('Test');

        $Erc = 0;
        &Stats::Update_All;

        $PT_Log = "$Tmp/Expect.log";
        system "rm -f $PT_Log";

        $shucks = 0;
        $SIG{INT} = \&catch_zap;
#        $SIG{QUIT} = \&catch_zap;
    }
        # "Get set, ..... GO!....."
}
#----------------------------------------------------------------
sub catch_zap { # Striaght out of PPv3:413
    my $signame = shift;
    our $shucks++;
    &Power ('OFF');
    $Stats{'Status'} = 'Aborted';

    &Exit(998,"<Ctrl>-C Aborted");

}
#_______________________________________________________________
sub Invalid {

        my ($Usage) = @_;
        print "$Bell$Usage";
        exit ($Erc);

}
#_______________________________________________________________
sub Mk_Port {

    my $Port = $Stats{'Session'};
    my $File = "/etc/minirc.$Port";
    $File = "/etc/minicom/minirc.$Port" if $Linux_gbl eq 'Ubuntu';

    my $UMask = umask; umask 0;

    open OUT, ">$File" or &Exit (35, "Can\'t cpen minicom cfg file $File for port $Port");

    print OUT "# Machine-generated file created " . localtime() . "\n";
    print OUT "pr port             $SPort[$Port]\n";
    print "Setting buad rate to $Baud \n";  # Baud is from testctlr.cfg and menu execution
    print OUT "pu baudrate         $Baud\n";
    print OUT "pu minit\n";
    print OUT "pr rtscts           No\n";
    print OUT "pu histlines        4000\n";

    close OUT;
    umask $UMask;
}
#_______________________________________________________________
sub UID_Check {  # $UserID strarts out as an encypted pw, then ->user_name

    my ($Tmp) = @_;

    # $UserID is our global, to be retrieved from %User_ID{PW}

    $Erc = &Read_Data_File ("/usr/local/cmtest/users.cfg");   # was $GP_Path/cfgfiles/users.cfg
    &Exit ( 999, "Can't read User cfg file") if $Erc;

#    &Print_Debug;  $uid.pl

    my $Msg = "UID_Check: Key=\'$UserID\', ";
    $User_Level = $User_Level{$UserID};
    $UserID = $User_ID{$UserID};
    $Msg .= "UID=" . $Tmp . ', ' if $UserID eq '';
    $Msg .= "User=$UserID Level=$User_Level";
    &Print_Log (11, $Msg);
    if ($Development eq 0) {
    	&Exit ( 999, "Failed user authentication")  if ($UserID eq '') ;
    } else {
    	&Print2XLog ("Warning: Failed user authentication\n") if ($UserID eq '');
    	}

    return ();
}

#__________________________________________________________________________
1;
