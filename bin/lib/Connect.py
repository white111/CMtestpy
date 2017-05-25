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
CVS_VER = ' [ CVS: $Id: Logs.pm,v 1.10 2011/01/21 18:38:56 joe Exp $ ]';
global CMtestVersion; 
if not "CMtestVersion" in globals() : CMtestVersion={}
CMtestVersion['Connect'] = VER + CVS_VER
#_______________________________________________________________________________
#use Device;

import lib.Expect
import lib.GUI
import lib.Logs
import time
import os.path
import pexpect #non standard library requires pip install pexpect before use, expect for python
import pexpect.fdpexpect
import serial

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
        if os.path.exists(File) : Exit (27, "Can\'t find Cmd file %s" %$File) 

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
}
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
        my Done = ""
        my Arg0 = ''

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
                try : Type,VarName,PromptOp = Arg.split()) :
                        Ask_User (Type,VarName,PromptOp); #Util.py
                except: pass
        "<Bypass>    - Skip a section"
        elif KeyWord == 'bypass':  #Start of Bypass
                if Check_Only: next
                if Bypass : Exit (999, "Nested bypass not allowed")
                elif  not Arg : Bypass = 1
                else : Bypass = 0                                             
                if $Bypass : Print_Log (11, "Start Bypass")  #print("Bypass set: $Bypass\n");
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
        elif KeyWord == 'comment' :
        elif KeyWord.find("^ctrl-") :
                if Check_Only: next
                if KeyWord == 'ctrl-send' :
                        Send_Ctrl(Arg);
                else : Send_Ctrl (KeyWord)
                
                "<End>    - Exit command file"
        elif KeyWord == 'end' :
                if Check_Only: next
                Done = 1;
                if not ExitCmd eq '' :
                        Tag (Cached,"Exiting comm session");
                        Comm.send (ExitCmd+"\n")
                          
                "<End>    - Exit command file"      
        elif KeyWord == 'ettc' :
                if Check_Only: next
                Stats['TTG'] = Arg;
                if not Loop_Time : Stats['ECT'] = time.time() + Arg ;
                Stats.Update_All
                Tag (Cached,"TTG = %s, ECT = %s \[%s . \]" % Arg, Stats['ECT'], PT_Date (Stats['ECT'],1));
####################################  Stop #########################################
                } elsif ($KeyWord eq 'exec') {
                        next if $Check_Only;
                        &Tag ($Cached,"Exec'ing $Arg");
                        $Arg =~ s/^\&//;                        # Remove the leading &
                if ( $Arg =~ /(.*)\((.*)\)/ ) {
                        &{$1}($2);
                        } else {
                                &{$Arg};
                        }
                } elsif ($KeyWord eq 'getdata') {
                        next if $Check_Only;
                        &Tag ($Cached,"Writing data to OutFile");
                        # Added to improve XML log parsing
                $Last_Send =~ s/[ ,\/,\\,__,>]/_/g;  #Change to single underscore
                $Arg = $Last_Send if $Arg eq '';  # Affects the XML file
                $Last_Send = "" ;
                &Screen_Data ($Arg, 0, 0);
                } elsif ($KeyWord eq 'include') {
                        &Tag ($Cached,"Sourcing include file $Arg");

                        if ($Arg =~ /(.*)\$\{(.*)\}(.*)/) {
                                &Exit (999, "Embedded Cmd file variable $2 not defined")
                            if ${$2} eq '';
                        $Arg = $1 . ${$2} . $3;
                        }
                        &Process_Cmd_File ($Comm, "$CmdFilePath/$Arg", $Check_Only);
                &Print_Log (11, "Returning to cmd file $CFName");
                #!!!                    unless $Check_Only;

        } elsif ($KeyWord eq 'includex') {
                next if $Check_Only;
                &Tag ($Cached,"Sourcing include file $Arg");
                        my $File ="$Tmp/$Arg.tmp";
                next if ! -f $File;
                &Process_Cmd_File ($Comm, $File, 0);
                &Print_Log (11, "Returning to cmd file $CFName");
                #!!!            unless $Check_Only;

        } elsif ($KeyWord eq 'loop') {                # Start of loop
                next if $Check_Only;
                &Exit (999, "Nested loops not allowed")
                        if $Caching;
                $Caching = 1;                   # Turns on looping
                &Tag ($Cached,"Starting loop at line $Line");
                        $Arg = $opt_L unless $opt_L eq ''; # It's been overridden with -L
                $Loop_Time = $Arg;
                $Stats{'TTG'} = $Arg;        # This now overrides a previous ETTC
                $Stats{'ECT'} = time + $Arg;

                } elsif ($KeyWord eq '/loop') {      # This is dealt with in the
                        next if $Check_Only;        #   calling sub &Process_Cmd_File

                        } elsif ($KeyWord eq 'msg') {
                                next if $Check_Only;
                        $Stats{'Result'} =~ /^(.)/;
                        #    $Msg =   $Msg . $Term_Msg if (defined $Term_Msg && $Term_Msg ne '');  # Added For HA
                &Print_Log (1, "\#$Stats{'Session'}$1:$Term_Msg $Arg");

                } elsif ($KeyWord eq 'prompt') {
                        $Prompt = $Arg;

                        } elsif ($KeyWord eq 'power') {
                                next if $Check_Only;
                        $Erc = &Power ($Arg);

                        } elsif ($KeyWord =~ /^send/) {
                                next if $Check_Only;
                                my $ArgStr = 'null';
                        if ($KeyWord =~ /^sendslow/) {
                            $ArgStr = ($KeyWord eq 'sendslow') ? "$Arg<cr>" : $Arg;
                        } else {
                                        $ArgStr = ($KeyWord eq 'send') ? "$Arg<cr>" : $Arg;
                                }
                &Tag ($Cached,"Sending ($KeyWord) >$ArgStr<");
                        $Log_Str .= "[$KeyWord $ArgStr]\n";
                $Comm -> print_log_file ("\n#: $KeyWord >$ArgStr<\n") if $Debug;
                # Added to improve XML log parsing
                $Last_Send = "" if ($Last_KeyWord eq 'send' || $Last_KeyWord eq 'sendslow');
                $Last_KeyWord = $KeyWord;
                $Last_Send = $Last_Send . $Arg;
                $Arg = $Arg . "\n" if ($KeyWord eq 'send' || $KeyWord eq 'sendslow');
                if ($KeyWord =~ /^sendslow/) {
                        $Comm -> send_slow (0.01,"$Arg");
                        } else {
                                #$Comm -> send_slow (0.01,"$Arg");
                                $Comm -> send ("$Arg") ;
                        }

                #    } elsif ($KeyWord eq 'set') {
        } elsif ($KeyWord =~ /set$/) {
                next if $Check_Only;
                $Arg =~ s/^\$//;                        # Remove the leading $
                        my $Val = ($KeyWord eq 'set') ? 1 : 0;
                &Tag ($Cached,"Setting \$$Arg = $Val");
                &Exit (999, "Attempted (un)set command on undeclared global \$" . $Arg)
                if !defined ${$Arg};
                ${$Arg} = $Val;
                &Print_Log (1, "Global var $Arg = $Val");

                        } elsif ($KeyWord =~ /sleep$/) {
                                next if $Check_Only;
                                if ($KeyWord eq 'sleep') {
                                sleep $Arg;
                            } else {
                                sleep $Arg/1000;  #!!! Change when usleep is loaded
                                # usleep $Arg;
                        }
                        $Log_Str .= "[$KeyWord $Arg]\n";

                } elsif ($KeyWord eq 'timeout') {
                        $TimeOut = $Arg ;

                        #    } elsif ($KeyWord eq 'unset') {
        #        next if $Check_Only;
        #        $Arg =~ s/^\$//;                        # Remove the leading $
        #        &Tag ($Cached,"Setting \$$Arg false");
        #        ${$Arg} = 0;

        } elsif ($KeyWord =~ /^wait/) {                # <Wait> and <WaitFor>
                next if $Check_Only;
                if ($Prompt =~ /^\^/ ) { ;   #IF A ^ IS FOUND AT THE BEGIINING OF THE PROMPT REGeXPRESSION MODE IS TRIGGERED
                                                                                $Arg = $Prompt if $KeyWord eq 'wait';  # Original
                                                                                    $Arg =~ s/^\^(.*)/^\x1b.[0-9]+;[0-9]+H.\x1b.[0-9]+;[0-9]+H.?$1|^$1/ ; #"$Arg0\x1b.[0-9]+;[0-9]+H.\x1b.[0-9]+;[0-9]+H.?$Arg|$Arg0$Arg"
                                         #[23;80H [24;1H> ]  http://vt100.net/docs/vt100-ug/chapter3.html#CUP, http://sourceforge.net/docman/display_doc.php?docid=9977&group_id=6894
                                         $Arg0 = '-re';
                   #print("New connect $Arg\n");
                        } else {
                                                        $Arg = $Prompt if $KeyWord eq 'wait';  # Original
                            #print("Original connect [$Arg]\n");
                            $Arg0 = $Arg;
                        #$Arg0 = NULL;
                                                }
                        &Tag ($Cached,"Waiting $TimeOut for $Arg");
                $Log_Str .= "[Waiting $TimeOut for \"$Arg\"]\n";
                $Comm -> clear_accum();
                        $Comm -> print_log_file ("\n#: Waiting $TimeOut for $Arg\n") if $Debug;
                #my (@Ex) = $Comm -> expect($TimeOut, $Arg); # Original  Statement
                #my (@Ex) = $Comm -> expect($TimeOut,'-re', "$Arg0\x1b.[0-9]+;[0-9]+H.\x1b.[0-9]+;[0-9]+H.?$Arg|$Arg0$Arg");
                my (@Ex) = $Comm -> expect($TimeOut,$Arg0, $Arg );
                        &Dump_Expect_Data(@Ex);
                        if ($Ex[1]) {
                            #if ($Exit_On_Timeout or $Startup) {
                            if ($Startup) {
                                 &Exit (32, "Expect timed out (Waiting $TimeOut for $Arg) at $CFName line $Line!");
                                } elsif ( $Exit_On_Timeout) {
                                     &Log_Error ("Timeout!: $Log_Str");
                                     &Final;

                                } else {
                                     &Log_Error ("Timeout!: $Log_Str");    # Unless $Mask_TMO
                                 &Print_Log ( 11, "Timed out after $Log_Str");
                             }
                         } else {
                                $Startup = 0; # We got though at lease 1 wait without a timeout!
                        }
                        $Buffer = $Comm -> before();
                        $Log_Str = '';

                } else {

                        &Exit (999, "(Invalid keyword \"$KeyWord\" at line $Line in Cmd file $CFName)");
                }
                #print "\t\t\tDebug=$Debug, EOT=$Exit_On_Timeout, EOE=$Exit_On_Error\n";
                #&PETC ("Connect::Exec_Cmd: Debug is set") if ($Debug);
                return ($Done);

        }
        #__________________________________________________________________________
        sub Add_2_Flat_Cmd_File {

                my ($Str) = @_;

                my $FH;

                chomp $Str;
                open ($FH, ">>$Tmp/FlatCmdFile.dat") || &Exit (3, "Can't open $FH for cat");
                print $FH "$Str\n";
                close $FH;
        }

#__________________________________________________________________________
sub Open_Port {

        my ($ConType, $ConExec) = @_;
        my $Comm;
        my $Trap = '';
        my $user = '';
    my $pw	= '';

    if ($ConType eq 'Serial') {
            $Header = 'Welcome';
            $ExitCmd = "\cA" . "Q\n";
            $Trap = 'lock failed';
            } elsif ($ConType eq 'Telnet') {
                $ExitCmd = 'exit';
                $Header = 'Connected to';
                } elsif ($ConType eq 'TermServer') {
                    $ExitCmd = "\c]quit";
                $Header = 'Connected to';
                $Trap = 'is being used by';
            } elsif ($ConType eq 'TermServerPW') {
                #Welcome to the MRV Communications' LX Series Server
                #Port 11 Speed 9600
                #login: root
           #Password: *******
                #Password:
                if ( $Default_Termserver_Config{ExitCmd} )  {
                        $ExitCmd = $Default_Termserver_Config{ExitCmd};
                        } else {
                                $ExitCmd = "\c]quit";
                        }
                $Header = 'Welcome to the MRV Communications';
                $pw = $Default_Termserver_Config{PORTPW};
                $user = $Default_Termserver_Config{USER};
                $Trap = 'Login incorrect';
        } else {
                die 'What am I doing here??';
        }
    &Print2XLog("Logging in to port: with User:$user PW:$pw ",0,1);

    my $Count = 5;
    my $Done = 0;

    &Exit (110, "Call to Exec_Cmd_File on $OS system") if $OS eq 'Win32';
                    my $Msg = "Spawning $ConType connection: $ConExec ..";
    &Print_Log (1, $Msg) if $Debug;
    #&Print_Log (0, $Msg) if ! $Debug;

        while (! $Done and $Count) {

                $Comm = Expect->spawn($ConExec)
                or &Exit (31, "Couldn't start $ConExec: $!\n");

                $Comm->log_file("$Tmp/ExComm.log", "w");

            if ($Debug) {
                 $Expect::Exp_Internal = $Verbose;        # Turn on verbose mode if -v
#                        $Expect::Debug = 1;
#                        $Comm->log_file("$Tmp/expect.log", "w");        # Log all!
         }

         $Comm->log_stdout(0);                # prevents the program's output from being shown on our STDOUT
             $Expect::Log_Stdout = 0;        # but this one does it globally!

         # The acid test to see if we are connected...

                print "." unless $Quiet;
                my (@Ex) = $Comm -> expect(5, $Header, $Trap);
                $Comm -> expect(3,"ogin:");
                &Dump_Expect_Data(@Ex);
                if ($Ex[0] == 1) {      # if ($Comm -> expect(5, $Header)) { 1 if matched, undef if timeout
                                        # Got the expected response
                                        if ( $user ne '') {    # login needed
                                                               &Exec_Cmd ($Comm, 'login', 'login', "send", $user);
                                                        $Comm -> expect(3,"ssword");
                                                        &Exec_Cmd ($Comm, 'password', 'password', "send", $pw);
                                     if ($Comm -> expect(3,"incorrect") =~ 'incorrect') {
                            $Count--;
                    }
                    }
                                        $Done = 1;
                                 } elsif ($Ex[0] == 2) { # Caught the trap
                                                         &Exit (999, "Trapped Error condition: $Trap");
                                      } else {
                                              $Count--;
                                      }

                if ($Done and $Count) {                                        # There were some retries left!
                        print " done!\n" unless $Quiet;
                } elsif (! $Done and $Count) {                        # Go round again
                        sleep 4;
                } else {        # We're out of retries!
                        print " Failed!\n" unless $Quiet;
                        my $Msg = "$ConExec FAILED to start!!\n";
                        &Exit (31, $Msg);
                }
        }
        unless ($Trap eq '') {
                (@Ex) = $Comm -> expect(2, $Trap);
                &Dump_Expect_Data(@Ex);
                if ($Ex[0]) {      # undef if timeout
                               # Got the trap response
                           &Exit (999, "Trapped Error condition: $Trap");
                           }

        }

        return ($Comm);
}
#__________________________________________________________________________
sub Process_Cmd_File {

        my ($Comm, $File, $Check_Only, $No_Worries) = @_;
        my ($CFName) = fnstrip ($File, 3);
        my $Endtime = '';


        return (0) if not -f $File and $No_Worries;  #Only execute it it
                                                        # the file exists

        my ($Msg) = ($Check_Only) ? 'Syntax checking' : 'Processing';
        $Msg .= " Cmd file \'$CFName\'";
        &Print_Log (1, "$Msg ...") unless
                $Check_Only or $Debug or !$opt_v ;

        $FH++;

        &Exit (999, "Cmd files nested too deep!")
                if ($FH > $CmdFileNestLmt);

        &Exit (2, "Cmd file $File not found") unless -s $File;
        open ($FH, "<$File") || &Exit (2, "Can\'t open Cmd file $File");

        my $Line = 0;
        my $Done = 0;
        while (<$FH>) {
                $Comm = $Comm_Current;   #HA Update our Port pointer, incase it changed
                $Stats{'Status'} = 'Active' unless ($Check_Only  && $Line eq 0);
                $Stats{'Status'} = 'Check' if ($Check_Only && $Line eq 0);
            &Stats::Update_All if $Line eq 0;
        &Abort (check);

        $Line++ unless $Done;   # Tags the last line used
        &Print_Log (11, "Command Done") if $Done;
        next if $Done;

        $Log_Str = "$Msg - Line $Line\n";    # This should now get written to the Expect log

        chomp;
        s/^\s*(.*)\s*$/$1/;     # Remove any leading/trailing whitespace
        s/^\s*(.*)\s*[\n|\r]$/$1/;     # Remove returns/linfeeds  JSW 020106 - Fix for returns/linefeed added to INC files

        next if /^\s*$/;        # (now) null lines
        next if /^\#/;          # Commented out

        &Add_2_Flat_Cmd_File ("\t\t\t\t# $Log_Str$_\n") unless $Check_Only;
        /^\<(\w+)\>\s*(.*)$/;
        $KeyWord = lc $1;
        $Arg = $2;
        my $Raw_Arg_1 = $2;
        $Arg =~ s/\s*[\"|\'](.*)[\"|\']\s*$/$1/;  #Modified by JW 031406, still some spaces getting through why?
                     my $Raw_Arg_2 = $Arg;
                     &Print2XLog  ("Found Variable: $Arg = <${$Arg}>\n",1) if $Arg =~ /^\$(.*)/ ;
                     $KeyWord =~ s/\<(\/.*)\>/$1/;  #</Loop> will not have matched above
                               # (because '/' is not matched by \w)!
                  # v29 Why do this at all? The only place we want interpolation is alread done in the <INCLUDE> cmd
        #      $Arg = $$1 if $Arg =~ /^\$(.*)/ # Change it to a pointer to the global
        #                 and !$Check_Only
                                       #                 and !($KeyWord =~ /set$/);
                # Array of Hash ex: $UUT_Variable_ref[0]->{Sahasera}
                  if  (! $Bypass) {
                          if (($Arg =~ /^\$(.*)\[(.*)\]\[(.*)\]->\{(.*)\}/) and !$Check_Only and !($KeyWord =~ /set$/)) {  # Array of Hash ex: $UUT_Variable_ref[0]->{Sahasera}
                                                                                                                           my $Arg_save = $Arg;
                                                                                                                                   $Arg = ${$1}[$2][$3]->{$4};
                                                                                                                           &Print2XLog  ("Found 2way Variable List->HASH: $Arg_save = <$Arg>",1)
                                                                                                          } elsif (($Arg =~ /^\$(.*)\[(.*)\]->\{(.*)\}/) and !$Check_Only and !($KeyWord =~ /set$/)) {  # Array of Hash ex: $UUT_Variable_ref[0]->{Sahasera}
                                                                                                         my $Arg_save = $Arg;
                                                                                                         $Arg = ${$1}[$2]->{$3};
                                                                                                         &Print2XLog  ("Found Variable List->HASH: $Arg_save = <$Arg>",1);
                                                                                                       } elsif ( $Arg =~ /^\$(.*)\[(.*)\]\[(.*)\]/ and !$Check_Only and !($KeyWord =~ /set$/)) {
                   my $Arg_save = $Arg;
                   $Arg = ${$1}[$2][$3];
                   } elsif ( $Arg =~ /^\$(.*)\[(.*)\]/ and !$Check_Only and !($KeyWord =~ /set$/)) {
                       my $Arg_save = $Arg;
                  $Arg = ${$1}[$2];
                  &Print2XLog  ("Found Variable List-: $Arg_save = <$Arg>",1)

                 &Print2XLog  ("Found 2 WAY Variable List-: $Arg_save = <$Arg>",1)
          } elsif ( $Arg =~ /^\$(.*)/ and !$Check_Only and !($KeyWord =~ /set$/) and !($Arg =~ /^\$\{(.*)\}/)) {
                  $Arg = $$1 ;
                  &Print2XLog  ("Found Variable: <$$Arg> = $Arg, Raw: $Raw_Arg_1 : $Raw_Arg_2 : $_ ",1)
                  } elsif ($Arg =~ /\$w+/) {
                         &Print2XLog  ("Warning: Found Possible Variable in : $Arg") ;
                  } elsif ($Arg =~ /\[(.*)\]{3,}/) {
                          &Print2XLog  ("Warning: Found Possible Variable dimension too deep : $Arg") ;
                  }
                  }
                  &Tag ($Cached,"Reading $CFName line $Line\: $KeyWord=$Arg") unless $Check_Only;

#Stoke!        unless ($KeyWord =~ /ctrl-\w?|end|wait|send|\/loop|getdata/) {
unless ($KeyWord =~ /ctrl-\w?|end|wait|send|\/loop|\/bypass|getdata/) {

        # check to make sure $Arg is valid
        $Erc = 25;
        &Exit (2, "Null $Raw_Arg_1,$Raw_Arg_2,$Arg_save Arg at $CFName line $Line: Cmd=\'$KeyWord\': Arg=\'$Arg\'") if $Arg eq '';
                $Erc = 0;
}



if ($Check_Only or ! $Caching or  ($KeyWord =~ /include/)  ) {
        if (  ! $Bypass  or ($KeyWord eq '/bypass')) {    # see if we are bypassing any code or ending bypass
                                                          $Done = &Exec_Cmd ($Comm, $CFName, $Line, $KeyWord, $Arg, $Check_Only, 0);
                                                                  } else {
                                                                          &Print_Log (11, "Bypass: $KeyWord $Arg");
                                                                  }
        } elsif ($KeyWord eq '/loop') {    # Now exec everything in @LBuffer

                while ($TestData{'ATT'} < $Loop_Time) {
                        $Endtime = &PT_Date(time+$Stats{'TTG'},2);
                        &Abort (check);
                        $Stats{'Loop'}++;
                    #&Print_Log (1, "Session $Stats{'Session'}: Starting loop $Stats{'Loop'} (TTG=$Stats{'TTG'})");
                &Print_Log (1, "Session $Stats{'Session'}: Starting loop $Stats{'Loop'} (TTG=$Stats{'TTG'}) End Time: $Endtime)");
                foreach $Cmd (@LBuffer) {
                        if (  ! $Bypass  or ($Cmd =~ /\/bypass/)) {    # see if we are bypassing any code or ending bypass
                                                                       &Print_Log (11, "LBuffer Exec: $Cmd");
                                                                       $Done = &Exec_Cmd ($Comm, split (/,,/, $Cmd));     # was /,/ 3/15/12
                                                                       } else {
                                                                               &Print_Log (11, "Bypass: $Cmd");
                                                                       }
                }
                &Stats::Update_All;
                &Print_Log (11, "Ending loop: ATT = $TestData{'ATT'}, LoopTime = $Loop_Time");
                }
                &Tag ($Cached,"Ending loop after $Stats{'Loop'} cycles");
                $Caching = 0;                   # Turns off caching, ready to execute
                $Loop_Time = 0;
                @LBuffer = ();         # In case a crazy want's to start another loop!

                } else {
                        &Print_Log (11, "Caching: $CFName,$Line,$KeyWord,$Arg,$Check_Only,1");
                                push @LBuffer, "$CFName,,$Line,,$KeyWord,,$Arg,,$Check_Only,,1" ;
                                #push @LBuffer, "$CFName,$Line,$KeyWord,$Arg,$Check_Only,1" ;
                }
        }

        &Tag ($Cached,"Closing cmd file $File at line $Line");
        close $FH;
        $FH--;
        return();
}

#__________________________________________________________________________
sub Send_Ctrl {        # Send a literal ctrl character to the terminal session

                       my ($Chr) = @_;
                       my $Foo;
                       ($Foo, $Chr) = split /-/, $Chr;

                       my $Dev = $SPort[$Stats{'Session'}];

        &Tag ($Cached,"Sending <Ctrl>-$Chr to $Dev");
        my $Tmp_File = "$Tmp/ctrl";
        open (TMP, ">$Tmp_File");
        print TMP "\c$Char";
        close TMP;
        system "cat $Tmp_File > $Dev";
}
#__________________________________________________________________________
sub Tag {

#!!!    return if $Verbose < 2;

my ($Cached, $Msg) = @_;
my $Str = ''; # "!\tTag: ";
$Str .= ($Cached) ? 'Cached' : ''; # 'Live';
&Print_Log (11, "$Str: $Msg");

}
#__________________________________________________________________________
1;
