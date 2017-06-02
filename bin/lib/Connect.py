#!/usr/bin/python
################################################################################
#
# Module:     Connect.py
#
# Author:      Paul Tindle ( mailto:Paul@Tindle.org )
#			 Joe White( mailto:joe@stoke.com )
#
# Descr:      Subs / procedures related to connecting to a DUT / UUT
#               via either a Serial port or a Telnet connection
#
# Version:    (See below) $Id$
#
# Changes:    Convert Perl V32.9 to Python
#
# Still ToDo:
#              - Move breaks from main loop to after the stats update
#              - Change <Include> to &   eg &Power
#              - Conver pipe (comm, telnet ssh ets from perl to Python(still learning)
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
VER= 'v0.1 5/24/2017'; # Conversion to Python from Perl 052317 JSW
CVS_VER = ' [ Git: $Id$ ]';
global CMtestVersion; 
if not "CMtestVersion" in globals() : CMtestVersion={}
CMtestVersion['Connect'] = VER + CVS_VER
#_______________________________________________________________________________
#use Device;

#import GUI - Not used yet
import lib.Logs
import time
import os.path
import pexpect #non standard library requires pip install pexpect before use, expect for python
import pexpect.fdpexpect
import serial # non standard lib from pip install pyserial
import string
if not os.name == "nt" : import pty # needed for pexpect, does not work on windows(no sudo termianl)
import telnetlib
#from clint.textui import colored, puts import colored #might need this for cross platfrom(win linux) text colors

#__________________________________________________________________________
def Alert(Msg):
        "Print a Message and wait for a return to continue, checks for A and aborts"


        Abort=0
        Start_Wait = time.time()
        global Stats

        if GUI :
                Abort = Dialog (Msg);
                if Answer.lower == 'abort' : Abort = 1 
        else :
                print(Logs.ASCIIcolor('blue'))
                #               print( "\n* * * $Msg * * *\n\n(Press any key to continue, or A to Abort) :")
                print("\n* * * $Msg * * *\n\n(Return key to continue) :")
                print(Logs.ASCIIcolor('reset'))
                X = input()[:-1] # get input and chop last char
                X = X.upper;
                if X == A : Abort = 1 

        if Abort :
                Stats['Result'] = 'ABORT'
                if not Quiet : print( "Aborting ...\n")

        Wait_Time += time.time() - Start_Wait
        return (Abort)
#__________________________________________________________________________
def Cmd_Expect(ConType, Port, File):                        
        "This sub takes an app, port and command file as args"
        "spawns the app, opens the cmd file, and"
        "processes the cmds individually. Quits the app on EOF"

        #!!! Port is now pre-determined so we can lose this arg.

        Sess = Stats['Session']
        if os.path.exists(File) : Exit (27, "Can\'t find Cmd file %s" %File) 

        KeyWord, Arg = ""
        ConExec, ExitCmd = ""
        Comm = ""

        if ConType == 'Serial' :
                if  not  SPort[Sess] in globals()  : Exit (34, "Serial port not defined for session %s" % Sess)
                if SPort[Sess].find(r"/dev/tty") :
                        Mk_Port   #Init.pm - just in case!
                        ConExec = "/usr/bin/minicom -C $Comm_Log $Sess";
                elif SPort[Sess].find(r":") : 
                        ConType = 'TermServer'
                        ConExec = "/usr/bin/telnet %s" % SPort[Sess]
                elif ConType == 'Telnet' :
                        if  not Port in globals() : Exit (33, "Connect::Cmd_Expect: Port not defined") 
                        ConExec = "/usr/bin/telnet %s" % Port
                elif ConType == 'ssh' :
                        ConExec = "/usr/bin/ssh %s -l mfg" % Port
                else  : Exit (107, "ConType %s ??" % ConType)

        Process_Cmd_File (Comm, File, 1);                        # Syntax check the cmd file

                                                                #!!! Add a test of whether we need a connection
                                                                #    so we can skip this next line if needed ...
                                                                #  OR make $Comm global and just put &Open_C
                                                                #    unless defined $Comm
        # HA Adds
        Comm = Open_Port(ConType, ConExec);
        Comm_Start = Comm    # HA Our starting Port pointer
        Comm_Current = Comm;  # HA Our Current Pointer

        Process_Cmd_File (Comm, File, 0);                        # Open the cmd file and start processing ...

        Tag (Cached,"Closing spawned connection ...")
        soft_close(Comm )
#__________________________________________________________________________
def Dump_Expect_Data(Data):
        "Dump our expect buffer"


        Labels = ['Exp_Pat_Pos', 'Exp_Error', 'Exp_Matched', 'Exp_Before', 'Exp_After']

        if not PT_Log == '' :
                try: PT_LOG =open(PT_Log,"r+") 
                except: Exit (3, "Can't open file: %s for cat" % PT_Log);

                PT_LOG.write( "\n" + '_' * 70 + "\n")
                PT_LOG.write("%s  -  %s\n" % PT_Date(time.time(), 2) , Log_Str)

                for Label in Labels :
                        for Dat in Data :
                                PT_LOG.write( "%s:\[%s\]\n" % Label, Dat)

                File_Close(PT_LOG)
                return
#__________________________________________________________________________
def Exec_Cmd(Comm, CFName, Line, KeyWord, Arg, Check_Only, Cache):
        """
        Exec_Cmd - The proceedure called having read one line of the current
        command file.
        &Exec_Cmd (<Comm>, <CFName>, <Line>, <KeyWord>, <Arg>, <Check_Only>, <Cached>);
        C<Alert> does what?.

        By default C<Exit> does not export any subroutines. The
        subroutines defined are
        Similar to C<nothing> in that it evaluates BLOCK setting C<$_> to each element
        of LIST in turn. C<first> returns the first element where the result from
        BLOCK is a true value. If BLOCK never returns true or LIST was empty then
        C<undef> is returned.

        $foo = first { defined($_) } @list    # first defined value in @list
            $foo = first { $_ > $value } @list    # first value in @list which
            # is greater than $value

        """

        #!!! <Set> and <UnSet> are still prototypes - DO NOT USE yet!

        global Stats
        global TimeOut
        Done = ""
        Arg0 = ''

        #   \/  - - - - - - - - - white space(s) (indentation) allowed
        #                    \/ - white space(s) required
        #
        #        <Alert>         Suspend processing and display a dialog box
        #        <Ask>           'Text16' Var Label
        #        <CheckData>     Check for the existance of <Arg> in $Buffer
        #        <CheckDataX>    Check for the exclusion of <Arg> in $Buffer
        #        <Comment>       Comment line. Deprecated in favor of a #
        #        <Ctrl-<x>>        chr - send a <ctrl>-<x> to the raw port, not via comm
        #        <Ctrl-Send>     <a char>
        #        <End>           Stop processing and close cmd file
        #        <ETTC>          Expected Time To Completion
        #        <Exec>          <&Subroutine>
        #        <GetData>       Returns all data prior to prompt -> $Buffer
        #        <Include>       file.inc. May include embedded global var: file${Type}.inc
        #        <IncludeX>      Same as <Include> but in $Tmp dir, no synatx check and ok if ! -f
        #        <Loop>          Start of loop, Arg contains ATT to end
        #                          Note: No parametric substitution performed inside loop!
        #        </Loop>         End of loop
        #        <Msg>           "Info for the operator and log"
        #        <Power>         [ ON | OFF | CYCLE <int sec delay>[default: 5 secs]]
        #        <Prompt>        "a string" | a_word
        #        <Send>          "a string" | a_word | <$global_var>        - sends literal + <cr>
        #        <Sendslow>          "a string" | a_word | <$global_var>        - sends literal + <cr> paced charaters
        #        <SendChar>      <char><Char><Char>...        - sends literal (without <cr>)     #        <Set>           <$global_var> [ = 1 ]
        #        <SendCharSlow>      <char><Char><Char>...        - sends literal (without <cr>)     #        <Set>           <$global_var> [ = 1 ] paced charaters
                #			*Note: sendslow can not send a single "0" scalar. Why?
                #        <Sleep>         <real> secs
        #        <Timeout>       <int> secs
        #        <UnSet>         <$global_var> [ = 0 ]
        #        <Wait>          <$TimeOut> for $Prompt
        #        <WaitFor>       "some string" | a_word | <$global_var>

        #Stoke...
        #        <Bypass>          Start of Bypass, Arg contains 0 bypass occurs
        #                          Note: No parametric substitution performed inside loop!
        #        </Bypass>         End of bypass
        #/Stoke...



        Type,VarName,PromptOp = ""
        "<Alert>    - Suspend processing and display a dialog box"
        if KeyWord == 'alert' :
                if Check_Only: next
                Done = Alert(Arg)
                "<Ask>    - Type, Var, Prompt Prompt the operator and wait for a <return>"
        elif KeyWord == 'ask' :
                if Check_Only: next
                try : 
                        Type,VarName,PromptOp = Arg.split() 
                        Ask_User (Type,VarName,PromptOp); #Util.py
                except: pass
                "<Bypass>    - Skip a section"
        elif KeyWord == 'bypass':  #Start of Bypass
                if Check_Only: next
                if Bypass : Exit (999, "Nested bypass not allowed")
                elif  not Arg : Bypass = 1
                else : Bypass = 0                                             
                if Bypass : Print_Log (11, "Start Bypass")  #print("Bypass set: $Bypass\n");
                elif KeyWord == '/bypass' :      
                        if Check_Only: next        
                        if  Bypass : Print_Log (11, "End Bypass") 
                        Bypass = 0      #End Bypass
                        
                        "<checkdata>    - Check the buffer for a string"
        elif KeyWord.find("^checkdata"):
                if Check_Only: next
                Tag (Cached,"Writing data to OutFile")
                if KeyWord == 'checkdatax' : Exclude = 1
                else: Exclude = 0
                Screen_Data(Arg, 1, Exclude)
        elif KeyWord.find("^icheckdata") :        #ignore case
                if Check_Only: next
                Tag (Cached,"Writing data to OutFile")
                if KeyWord == 'icheckdatax' : Exclude = 1
                else: Exclude = 0
                Screen_Datai (Arg, 1, Exclude)

                "<comment>    - Do Nothing"
        elif KeyWord == 'comment' : pass
        elif KeyWord.find("^ctrl-") :
                if Check_Only: next
                if KeyWord == 'ctrl-send' :
                        Send_Ctrl(Arg);
                else : Send_Ctrl (KeyWord)
                
                "<End>    - Exit command file"
        elif KeyWord == 'end' :
                if Check_Only: next
                Done = 1;
                if not ExitCmd == '' :
                        Tag (Cached,"Exiting comm session");
                        Comm.send (ExitCmd+"\n")
                          
                "<ettc>    - Estimated time to completion update"      
        elif KeyWord == 'ettc' :
                if Check_Only: next
                Stats['TTG'] = Arg;
                if not Loop_Time : Stats['ECT'] = time.time() + Arg ;
                Stats.Update_All
                Tag (Cached,"TTG = %s, ECT = %s \[%s . \]" % Arg, Stats['ECT'], PT_Date (Stats['ECT'],1));
                "<exec>    - exec a python subroutine" 
        elif KeyWord == 'exec': 
                if Check_Only: next
                Tag (Cached,"Exec'ing %s" % Arg);
                Arg = Arg[2:]                        # Remove the leading &
                try:
                        Func,val,_ = Arg.split("\(|\)")   # Split on "(" ")"
                        try: Func(val)
                        except: Print_Log (11, "Function call %s\(%s\) does not exsist" % Func,Val)
                except:
                        try: Func()
                        except: Print_Log (11, "Function call %s\(\) does not exsist" % Func)
                "<GetData>    - Grab expect buffer and log(XML)" 
        elif KeyWord == 'getdata' :
                if Check_Only: next
                Tag (Cached,"Writing data to OutFile")
                # Added to improve XML log parsing
                Last_Send = re.sub("[ ,\/,\\,__,>]","_", Last_Send)  #Change to single underscore
                if Arg == '' : Arg = Last_Send   # Affects the XML file
                Last_Send = ""
                Screen_Data(Arg, 0, 0)
                "<include>    - Include another command file"
        elif KeyWord == 'include' :
                Tag (Cached,"Sourcing include file %s" % Arg)
                p = re.compile(r"(.*?)\$\{(.*?)\}(.*?)")
                try: 
                        val = p.findall(Arg) 
                        if val[2]  == '' : Exit (999, "Embedded Cmd file variable %s not defined" % val[2])
                        Arg = val[1] + (val[2])  + val[3]
                        Process_Cmd_File (Comm, "%s/%s" % CmdFilePath, Arg , Check_Only)
                except: pass
                Print_Log (11, "Returning to cmd file %s" % CFName)
                "<includex>    - Include another command file from tmp dir no check"
        elif KeyWord == 'includex' :
                if Check_Only: next
                Tag (Cached,"Sourcing include file %s" % Arg);
                File ="%s/%s" % Tmp, Arg.tmp
                if  not os.path.exists(File) : next
                Process_Cmd_File (Comm, File, 0)
                Print_Log (11, "Returning to cmd file %s" % CFName);
                "<loop>    - Start a loop"
        elif KeyWord == 'loop' :                # Start of loop
                if Check_Only: next
                if Caching : Exit (999, "Nested loops not allowed")
                Caching = 1                  # Turns on looping
                Tag (Cached,"Starting loop at line %s" % Line)
                if not Loop_overide == 0  :  Arg = Loop_overide  # It's been overridden with -L
                Loop_Time = Arg
                Stats['TTG'] = Arg;        # This now overrides a previous ETTC
                Stats['ECT'] = time.time() + Arg
                "</loop>    - end  a loop"
        elif KeyWord == '/loop' :      # This is dealt with in the
                if Check_Only: next        #   calling sub &Process_Cmd_File
                "<Msg>  Print Msg to terminal"
        elif KeyWord == 'msg' :
                if Check_Only: next
                Stats['Result'] = a.lstrip = Arg.rstrip
                #    $Msg =   $Msg . $Term_Msg if (defined $Term_Msg && $Term_Msg ne '');  # Added For HA
                Print_Log (1, "\#%s%s:%s %s" % Stats['Session'], Stats['Result'], Term_Msg, Arg)
                "<Prompt>  Prompt the Operatior and wait"
        elif KeyWord == 'prompt' :
                Prompt = Arg
                "<Power>  Manage power Manual or Auto"
        elif KeyWord == 'power' :
                if Check_Only: next
                Erc = Power(Arg);
                "<Send>  Send a comand to our output stream"
        elif KeyWord.find(r"^send") :
                if Check_Only: next
                ArgStr  = 'null'
                if KeyWord.find(r"^sendslow") :
                        if KeyWord == 'sendslow' : ArgStr = Arg + "\n" 
                        else: ArgStr = Arg
                else :
                        if  KeyWord == 'send' : ArgStr = Arg + "\n"
                        else: ArgStr = Arg
                Tag (Cached,"Sending (%s) >%s<" % KeyWord,ArgStr )
                Log_Str += "[%s %s]\n" % KeyWord ,ArgStr
                if Debug : Comm.write(print_log_file ("\n#: $KeyWord >$ArgStr<\n"))
                # Added to improve XML log parsing
                if Last_KeyWord == 'send' or Last_KeyWord == 'sendslow' : Last_Send = ""
                Last_KeyWord = KeyWord;
                Last_Send = Last_Send + Arg
                if KeyWord == 'send' or KeyWord == 'sendslow': Arg = Arg + "\n" 
                if KeyWord.find("^sendslow") :
                        Comm.write(send_slow(0.01,Arg))
                else :
                        Comm.write(send ("$Arg"))
                "<Set>  Set a Varible 1:0"
        elif KeyWord.find(r"set$") :
                if Check_Only: next
                Arg = Arg[2:]         # Remove the leading $
                if KeyWord == 'set' :   Val =  1
                else:  Val =  0
                Tag (Cached,"Setting %s = %s" % Arg, Val)
                setattr(self)
                try: Arg
                except: Exit (999, "Attempted (un)set command on undeclared global \$" + Arg)
                self.Arg = Val  # Yes this will not work yet, working on it
                Print_Log (1, "Global var %s = %s" % Arg ,Val)
                "<Sleep>  Sleep x Seconds uSleep micor sec"
        elif KeyWord.find(r"sleep$") :
                if Check_Only: next
                if KeyWord == 'sleep' : time.sleep(Arg/1000000.0)
                else : time.sleep(Arg/1000.0)  #!!! Change when usleep is loaded
                Log_Str += "[%s %s]\n" % KeyWord,Arg
                "<Timout>  TIme in Seconds to wait for Text"
        elif KeyWord == 'timeout' :
                TimeOut = Arg 
                "<wait>  TIme in Seconds to wait for Text in supplied string"
        elif KeyWord.find(r"^wait") :                # <Wait> and <WaitFor>
                if Check_Only: next
                if Prompt.find(r"^\^") :   #IF A ^ IS FOUND AT THE BEGIINING OF THE PROMPT REGeXPRESSION MODE IS TRIGGERED
                        if KeyWord == 'wait' : Arg = Prompt  # Original
                        #$Arg =~ s/^\^(.*)/^\x1b.[0-9]+;[0-9]+H.\x1b.[0-9]+;[0-9]+H.?$1|^$1/ ; #"$Arg0\x1b.[0-9]+;[0-9]+H.\x1b.[0-9]+;[0-9]+H.?$Arg|$Arg0$Arg"
                        #[23;80H [24;1H> ]  http://vt100.net/docs/vt100-ug/chapter3.html#CUP, http://sourceforge.net/docman/display_doc.php?docid=9977&group_id=6894
                        Arg0 = '-re'
                        #print("New connect $Arg\n");
                else :
                        if KeyWord == 'wait' : Arg = Prompt   # Original
                        #print("Original connect [$Arg]\n");
                        Arg0 = Arg;
                        #$Arg0 = NULL;
                Tag (Cached,"Waiting %s for %s" % TimeOut, Arg);
                Log_Str += "[Waiting %s for \"%s\"]\n" % TimeOut,Arg
                Comm.write(clear_accum())
                if Debug:Comm.write(print_log_file ("\n#: Waiting %s for %s\n" % TimeOut,Arg))
                #my (@Ex) = $Comm -> expect($TimeOut, $Arg); # Original  Statement
                Ex = Comm.write(expect(TimeOut,Arg0, Arg ))
                Dump_Expect_Data(Ex);
                if Ex[1] :
                #if ($Exit_On_Timeout or $Startup) {
                        if Startup :
                                Exit (32, "Expect timed out (Waiting $TimeOut for $Arg) at $CFName line $Line!");
                        elif Exit_On_Timeout :
                                Log_Error ("Timeout!: %s" % Log_Str)
                                Final()
                        else :
                                Log_Error ("Timeout!: %s" % Log_Str)    # Unless $Mask_TMO
                                Print_Log ( 11, "Timed out after %s" % Log_Str)
                else :  Startup = 0 # We got though at lease 1 wait without a timeout!
                Buffer = Comm.write(before())
                Log_Str = ''
        else :
                Exit (999, "(Invalid keyword \"%s\" at line %s in Cmd file %s)" % KeyWord, Line, CFName);
        #print "\t\t\tDebug=$Debug, EOT=$Exit_On_Timeout, EOE=$Exit_On_Error\n";
        #&PETC ("Connect::Exec_Cmd: Debug is set") if ($Debug);
        return (Done)
        
#__________________________________________________________________________
def Add_2_Flat_Cmd_File(Str) :

        chomp(Str)
        try: FH = open (Tmp+ r"/FlatCmdFile.dat", 'r+')  
        except: Exit (3, "Can't open %s for cat" % FH)
        FH.write(Str+"\n")
        close(FH)
        return()        
#__________________________________________________________________________
def Open_Port(ConType, ConExec, baud="9600", Trap='fail',user='',pw=''):
        "Open a Serial, TFP,SSH,Telnet for read write add passing of baud,trap,user,pw"

        if ConType == 'Serial':  # Using Minicom
                Header = 'Welcome'
                ExitCmd = "\cA" + "Q\n"
                Trap = 'lock failed'
        elif ConType == 'pySerial':  # pyserial import serial
                Header = ''  #Nothing avaiable on connect
                ExitCmd = ""  #no exit command this direct to device to close()
                Trap = '[Could not exclusively lock port|could not open port]' #these are returne from open()
                if "Linux" : OpenPort = serial.Serial("/dev/ttyS1", baud ,parity="N", bytesize=8,stopbits=1,timeout=1,xonxoff=0,dsrdtr=0,rtscts=0, exclusive=True)
                if "NT" :  OpenPort = serial.Serial("COM1", baud ,parity="N", bytesize=8,stopbits=1,timeout=1,xonxoff=0,dsrdtr=0,rtscts=0, exclusive=True)
                if "Linux" : OpenExpect = pexpect.fdpexpect.fdspawn(OpenPort) # now can do OpenExpect.[sendline,expect,before,after etc)
                if "NT" :  exit ("Don't know how to make pexpect work yet on NT")
<<<<<<< HEAD
        elif ConType == 'Telnet' : 
                OpenExpect = telnetlib.Telnet(ConExec)
                #TelnetExpectpy(FH,Send="",Prompt,Timeout=10)
                if TelnetExpectpy(OpenExpect, user, "login: ", 3) :
                        if pw:
                                if TelnetExpectpy(OpenExpect, pw, Trap, 3) :
                                        print ("Telnet %s Connected via password", ConExec)
                        print ("Telnet %s Connected", ConExec)
                else:
                        print ("Telnet connect failed")
=======
        elif ConType == 'Telnet' : # Direct telnet to a system but still using Expect to look at output
>>>>>>> 6dc68281cf4ba985451c72c1a1397d2c7844cf1a
                ExitCmd = 'exit'
                Header = 'Connected to'
        elif ConType == 'TermServer' :  #still telnet but talking to a serial port through Telnet
                ExitCmd = "\c]quit"
                Header = 'Connected to'
                Trap = 'is being used by'
        elif ConType  == 'TermServerPW' : #Termserver needs a PW
                #Welcome to the MRV Communications' LX Series Server
                #Port 11 Speed 9600
                #login: root
                #Password: *******
                #Password:
                if Default_Termserver_Config[ExitCmd] :
                        ExitCmd = Default_Termserver_Config[ExitCmd]
                else :
                        ExitCmd = "\c]quit"
                Header = 'Welcome to the MRV Communications';
                pw = Default_Termserver_Config[PORTPW]
                user = Default_Termserver_Config[USER]
                Trap = 'Login incorrect'
        else :
                exit( 'What am I doing here?? no connection method found' + ConType)
                
        Print2XLog("Logging in to port: with User:%s PW:%s " % user,pw ,0,1);

        Count = 5
        Done = 0

        if OS == 'NT' : Exit (110, "Call to Exec_Cmd_File on NT system") ;
        Msg = "Spawning %s connection: %s .." % ConType, ConExec
        if Debug :Print_Log (1, Msg) 
        #&Print_Log (0, $Msg) if ! $Debug;

        while (not Done and Count) :
                try : Comm = Expect.spawn(ConExec)
                except: Exit (31, "Couldn't start : $!\n" % ConExec);
                Comm.log_file(Tmp+"/ExComm.log", "w")
                if Debug : Expect.Exp_Internal(Verbose)        # Turn on verbose mode if -v
                #                        $Expect::Debug = 1;
                #                        $Comm->log_file("$Tmp/expect.log", "w");        # Log all!

                Comm.log_stdout(0)                # prevents the program's output from being shown on our STDOUT
                Expect.Log_Stdout(0)        # but this one does it globally!

                # The acid test to see if we are connected...
                if not Quiet: print (".") 
                Ex = Comm.expect(5, Header, Trap)
                Comm.expect(3,"ogin:")
                Dump_Expect_Data(Ex)
                if Ex[0] == 1 :     # if ($Comm -> expect(5, $Header)) { 1 if matched, undef if timeout
                        # Got the expected response
                        if  not user == '' :   # login needed
                                Exec_Cmd(Comm, 'login', 'login', "send", user)
                                Comm.expect(3,"ssword")
                                Exec_Cmd (Comm, 'password', 'password', "send", pw)
                                if Comm.expect(3,"incorrect").find('incorrect') : Count -=1
                        Done = 1
                elif Ex[0] == 2 : # Caught the trap
                        Exit (999, "Trapped Error condition: $Trap")
                else : Count -= 1

                if Done and Count :                                        # There were some retries left!
                        if not Quiet : print( " done!\n" )
                elif not Done and Count :                       # Go round again
                        time.sleep(4/1000000.0)
                else :        # We're out of retries!
                        if not Quiet: print(" Failed!\n" )
                        Msg = "%s FAILED to start!!\n" % ConExec
                        Exit (31, Msg)

        if not Trap == '' :
                Ex = Comm.expect(2, Trap)
                Dump_Expect_Data(Ex)
                if Ex[0] :      # undef if timeout
                               # Got the trap response
                        Exit (999, "Trapped Error condition: $Trap");

        return (Comm)
#__________________________________________________________________________
def Process_Cmd_File(Comm, File, Check_Only, No_Worries) :
        "Loop through command files"
        CFName = fnstrip(File, 3)
        Endtime = ''
        if not os.path.exists(File) and No_Worries: return (0) ;  #Only execute it it
                                                        # the file exists
        if Check_Only : Msg = "Syntax checking" 
        else : Msg = 'Processing'
        Msg += " Cmd file \'%s\'"% CFName
        if Check_Only or Debug or Verbose : Print_Log (1, "%s ..." % Msg)

        FH += 1  
        if FH > CmdFileNestLmt :  Exit (999, "Cmd files nested too deep!")
        if not os.path.exists(File) :
                try: FH = open(File , 'r') 
                except : Exit (2, "Can\'t open Cmd file %s" % File);

        Line = 0
        Done = 0
        with open (File, r) as fh :
                for line in fh:
                        Comm = Comm_Current;   #HA Update our Port pointer, incase it changed
                        if not (Check_Only and Line == 0) : Stats['Status'] = 'Active' 
                        if Check_Only and Line == 0 : Stats['Status'] = 'Check' 
                        if Line == 0 : Stats.Update_All
                        Abort(check)
                        if not Done : Line += 1    # Tags the last line used
                        if Done : Print_Log (11, "Command Done") 
                        if Done : next 
                        Log_Str = "%s - Line %s\n" % Msg, Line    # This should now get written to the Expect log
                        chomp(line)
                        line.rstring      # Remove any leading/trailing whitespace
                        # s/^\s*(.*)\s*[\n|\r]$/$1/;     # Remove returns/linfeeds  JSW 020106 - Fix for returns/linefeed added to INC files
                        if line.find(r"^\s*$") : next        # (now) null lines
                        if line.find(r"^\#") : next          # Commented out
                        if not Check_Only : Add_2_Flat_Cmd_File ("\t\t\t\t# %s%s\n" % Log_Str, line)
                        p = re.compile(r"^\<(\w+)\>\s*(.*)$")  # Get the keyword
                        val = p.findall(Arg)                         
                        KeyWord = p[1].lower
                        Raw_Arg_1 = Arg = p[2]
                        Arg = Arg.translate(None,string.whitespace)  # Remove any white space
                        Raw_Arg_2 = Arg;
                        if Arg.find(r"^\$(.*)")  : Print2XLog ("Found Variable: %s = <%s>\n" % Arg, Arg ,1) 
                        p = re.compile(r"<(\/.*)\>")  #</Loop> will not have matched above
                        Keyword = p.findall(line)
                        if  not Bypass :
                                p = re.compile(r"/^\$(.*)\[(.*)\]\[(.*)\]->\{(.*)\}")
                                val = p.findall(Arg)
                                if Arg.find(r"^\$(.*)\[(.*)\]\[(.*)\]->\{(.*)\})") and  not Check_Only and not KeyWord.find("set$") :
                                        # Array of Hash ex: $UUT_Variable_ref[0][x]->{Sahasera}
                                        Arg_save = Arg
                                        pp = re.compile(r"^\$(.*)\[(.*)\]\[(.*)\]->\{(.*)\})")
                                        val2 = pp.findall(Arg)
                                        #now build or command UUT_Variable_ref[0][x][Sahasera]
                                        Arg = pp[1][pp[2]][pp[3]][pp[4]]
                                        Print2XLog  ("Found 2way Variable List->HASH: %s = %s" % Arg_save ,Arg , 1)
                                elif Arg.find(r"^\$(.*)\[(.*)\]->\{(.*)\}") and not Check_Only and \
                                         not KeyWord.find("set$") :
                                        # Array of Hash ex: $UUT_Variable_ref[0]->{Sahasera}
                                        Arg_save = Arg;
                                        pp = re.compile(r"^\$(.*)\[(.*)\]->\{(.*)\}")
                                        val2 = pp.findall(Arg)
                                        #now build or command UUT_Variable_ref[0][Sahasera]
                                        Arg = pp[1][pp[2]][pp[3]]                                       
                                        Print2XLog  ("Found Variable List->HASH: %s = %s" % Arg_save , Arg , 1)
                                elif  Arg.find(r"^\$(.*)\[(.*)\]\[(.*)\]") and  not Check_Only \
                                       and  not KeyWord.find(r"set$") :
                                        Arg_save = Arg
                                        pp = re.compile(r"^\$(.*)\[(.*)\]\[(.*)\]")
                                        val2 = pp.findall(Arg)
                                        #now build or command UUT_Variable_ref[0][Sahasera]
                                        Arg = pp[1][pp[2]][pp[3]]                                       
                                elif  Arg.find(r"^\$(.*)\[(.*)\]") and not Check_Only and not KeyWord.find(r"set$") :
                                        Arg_save = Arg
                                        pp = re.compile(r"^\$(.*)\[(.*)\]")
                                        val2 = pp.findall(Arg)
                                        #now build or command UUT_Variable_ref[0][Sahasera]
                                        Arg = pp[1][pp[2]]                                          
                                        Print2XLog  ("Found Variable List-: %s = <%s>" % Arg_save,Arg ,1)
                                        Print2XLog  ("Found 2 WAY Variable List-: %Arg_save = <%s>" % Arg_save,Arg , 1)
                                elif Arg.find(r"^\$(.*)") and not Check_Only and not KeyWord.find(r"set$") \
                                     and  not Arg.find(r"^\$\{(.*)\}/") :
                                        pp = re.compile(r"^\$(.*)")
                                        val2 = pp.findall(Arg)
                                        #now build or command UUT_Variable_ref[0][Sahasera]
                                        Arg = pp[1]                                        
                                        Print2XLog  ("Found Variable: <%s> = %s, Raw: %s : %s : %s " % Arg,Arg,Raw_Arg_1, Raw_Arg_2, val ,1)
                                elif Arg.find(r"\$w+") :
                                        Print2XLog  ("Warning: Found Possible Variable in : %s" % Arg) 
                                elif Arg.find(r"\[(.*)\]{3,}") :
                                        Print2XLog  ("Warning: Found Possible Variable dimension too deep : %s" % Arg) 
                                
                        
                                if not Check_Only : Tag (Cached,"Reading %s line %s\: %s=%s" % CFName, Line, KeyWord,Arg) 
                                #        unless ($KeyWord =~ /ctrl-\w?|end|wait|send|\/loop|getdata/) {
                                if not KeyWord.find(r"ctrl-\w?|end|wait|send|\/loop|\/bypass|getdata") :
                                        # check to make sure $Arg is valid
                                        Erc = 25
                                        if Arg == '' : Exit (2, "Null %s,%s,%s Arg at %s line %s: Cmd=\'%s\': Arg=\'%s\'" % Raw_Arg_1,Raw_Arg_2,Arg_save,CFName,Line,KeyWord,Arg) 
                                        Erc = 0
         
                                if Check_Only or not Caching or  KeyWord.find("include") :
                                        if not Bypass  or KeyWord == r'/bypass' :     # see if we are bypassing any code or ending bypass
                                                Done = Exec_Cmd (Comm, CFName, Line, KeyWord, Arg, Check_Only, 0)
                                        else :
                                                Print_Log (11, "Bypass: %s %s" % KeyWord, Arg)
                                elif KeyWord == r'/loop' :    # Now exec everything in @LBuffer
                                        while TestData['ATT'] < Loop_Time : 
                                                Endtime = PT_Date(time.time() + Stats['TTG'],2)
                                                Abort (check)
                                                Stats['Loop'] +=1
                                                Print_Log (1, "%s: Starting loop %s (%s) End Time: %s)" % Session,Stats['Session'],Stats['Loop'],Stats['TTG'],Endtime);
                                                for Cmd in LBuffer:
                                                        if not Bypass or Cmd.find("\/bypass") :    # see if we are bypassing any code or ending bypass
                                                                Print_Log (11, "LBuffer Exec: "+ Cmd)
                                                                Done = Exec_Cmd (Comm, Cmd.split(",,"))     # was /,/ 3/15/12
                                                        else :
                                                                Print_Log (11, "Bypass: " + Cmd)
                                                Stats.Update_All()
                                                Print_Log (11, "Ending loop: ATT = %s, LoopTime = %s" % TestData['ATT'], Loop_Time);
                                        Tag (Cached,"Ending loop after %s cycles" % Stats['Loop'])
                                        Caching = 0                   # Turns off caching, ready to execute
                                        Loop_Time = 0
                                        LBuffer = []         # In case a crazy want's to start another loop!
                                else :
                                        Print_Log (11, "Caching: %s,%s,%s,%s,%s,1" % CFName,Line,KeyWord,Arg,Check_Only)
                                        LBuffer.append("%s,,%s,,%s,,%s,,%s,,1" % CFName,Line,KeyWord,Arg,Check_Only)
        # end of while
        Tag (Cached,"Closing cmd file %s at line %s" % File,Line)
        close(FH)
        FH -= 1
        return()

#__________________________________________________________________________
def Send_Ctrl(Chr):
        "Send a literal ctrl character to the terminal session"
        Foo, Chr = Chr.split("-")
        Dev = SPort[Stats['Session']]
        Tag (Cached,"Sending <Ctrl>-%s to %s" % Chr, Dev)
        Tmp_File = Tmp + "/ctrl"
        Tmp = open (Tmp_File, "w");
        TMP.write("\c%s" %Char)
        close(TMP)
        Dev.write("\c%s" %Char)  # Trying this first if not will need to cat file
        return
#__________________________________________________________________________
def Tag(Cached, Msg):
        "Write a Tag"

        #!!!    return if $Verbose < 2;
        Str = '' # "!\tTag: ";
        if Cached : Str += 'Cached' # 'Live';
        Print_Log (11, "%s: %s" % Str,Msg)
#__________________________________________________________________________
def TelnetExpectpy(FH,Send="",Prompt='',Timeout=10):
        """
        Simple Python based Expect routing using just telnetlib, return the buffer
        """
        After = (client.read_very_eager().decode('ascii'))  # clear buffer
        client.write(Send.encode('ascii') + "\r\n".encode('ascii'))
        try:
                Before = (strip_ansi_codes(client.read_until(Prompt.encode('ascii') , Timeout).decode('ascii')))
        except :
                Before = 0
        After = (client.read_very_eager().decode('ascii'))
        return(Before, After)
#__________________________________________________________________________
1;
