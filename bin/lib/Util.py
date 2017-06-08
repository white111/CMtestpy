#!/usr/bin/python
################################################################################
#
# Module:      Util.py
#
# Author:      Joe White
#
# Descr:      ??
#
# Version:    (See below) $Id$
#
# Changes:
#	      Conversion to Python from PT.pm perl lib 0503017 JSW
#
# Still ToDo:
#
# License:   This software is subject to and may be distributed under the
#            terms of the GNU General Public License as described in the
#            file License.html found in this or a parent directory.
#            Forward any and all validated updates to Paul@Tindle.org
#
#            Copyright (c) 1993 - 2005 Paul Tindle. All rights reserved.
#            Copyright (c) 2005-2008 Stoke. All rights reserved.
#            Copyright (c) 2017 Joe White. All rights reserved.
#
################################################################################
VER = 'v0.1 5/03/2017'; # Conversion to Python
CVS_VER = ' [ CVS: $Id: PT.pm,v 1.9 2008/02/22 21:00:51 joe Exp $ ]';
#CMtestVersion['Util'] = VER + CVS_VER;
#______________________________________________________________________________

#import lib  # import private library functions for CMtestpy, see lib/__init__.py
#import lib.Logs
import sys
import time
import Globals
import re

#import psutil # will need a package  pip install psutil and ggc build of package, lots of pid utils

# Python use Term::ANSIColor;

#__________________________________________________________________________________
def exit(var):
    "Do a sys.exit()"
    sys.exit(var)
    return

#__________________________________________________________________________________
def Abort(Op):
    "Abort - sets or checks for an abort flag (file)."
    "##&Abort (check)        : Checks for the exsistance of the abort flag and Exits if found"
    "                    ##returns 0 or exits as appropriate"
    "    ##OR"
    "    ##&Abort (run_check) : Checks to make sure that a particular session is actually running"
    "                        ##return 1 if it is, 0 if not"
    "    ##OR"
    "    ##&Abort (set)        : Sets the abort flag for the next check, returns 0"

    ## Unconverted Python Code ??
    ##use PT;
    ##.
    ##.
    ##&Abort (check);
    ##OR
    ##&Abort (run_check);
    ##OR
    ##&Abort (set);
    

    File = Stats_Path + r'/system/' + Stats['Host_ID'] + r'-' + str(Stats['Session'])

    if  Op == 'run_check' :   # Checks to see if session is running
            # Acts on the system stat file, not the abort file
        if os.path.isfile(File) :
            return (1)
        else :
            return (0)

        if Op == 'rm' :
            try:
                Erc = os.delete(File)
            except:
                exit(0)    #This should only be called by Exit

        if Op == 'set' :
            if os.path.isfile(File) : # It's not running ...
                return (0) 
            Erc = os.delete(File)
            if Erc : Exit( 10, File ) 

        File += '-ABORT'

        if Op == 'check'  or  Op == 'clear' :
            if os.path.isfile(File) :
                Erc = os.delete(File)
                if Erc : Exit( 10,  'Unable to delete Abort flag file' ) 
                if Op == 'check'  :
                    Power('OFF')
                    Exit( 199, 'Operator Aborted' )
            return (0);

        if Op == 'set' :
            UMask = os.umask()
            os.umask(0)
            Erc = os.open(File, 'a').close()  # Touch a file
            os.umask(UMask)
            if Erc : Exit( 9, 'Unable to touch Abort file' ) 
            return (0);

        # Since every one of the above have an unconditional return ...
        Exit( 999, "Invalid call to \&Abort %s" %  Op )

    return
#__________________________________________________________________________
def Ask_User(Type, Var, Prompt) :
    "Ask user for input"

    if Prompt == '':  # &Ask_User ( Type Prompt ) [no Var] supported
        Prompt = Var;
        Var = ''

    Data;
    Start_Wait = int(time.time()); #Epoch time
    #Prompt =~ s/^\"(.*)\"$/$1/; # Strip off " and return
    Prompt = re.sub(r"^\"","",Prompt)
    Prompt = re.sub(r"\"$","",Prompt)
    Print_Log(11, "Asking User \'%s\' [ type = $Type, $Var = ] ..." % Prompt);

#    return () unless lc $Type =~ /text/;

    if GUI :
        #($Erc, $Data) = system "java -jar Input.jar $Prompt";
        print ("No GUI support Yet")
        Exit (999, "Java failed to run") 
    else :   # Get user input from a prompt
        Data = input("%s: " % Prompt)[:-1]  # get Data and Chop
        if Data == "\["  : Exit( 198, "Get UI Abort" )
        Wait_Time += int(time.time()) - Start_Wait;

    if not Var == "":
        # Perl ${$Var} = Data;  Not sure yet how to conver or if Ask_User is needed, Python recomends Dictionaly instead
        Globals[Var] = Data
        return (0)
    else :
        return (Data)
#____________________________________________________________________________
def xChk_Sub(Sub):    
    "Init use it!  Create a subdirectory "

    if not Unix: Sub = re.sub(r"/\//\\/",Sub)
    try:
        os.mkdir(Sub)
        try :
            os.chmod(Sub, 777)
        except:
            Exit(999, r"Cant change mode on %s" % Sub)        
    except:
        Exit(999, r"Can't create directory %s" % Sub) 
    return
#__________________________________________________________________________________
def chomp(x) :
    "Remove return or line feed from end of line like perl"
    x = x.rstrip()
    x = x.strip()
    x = x.strip("\t")
    x = x.strip(' \t\n\r') 
    #if x.endswith("\r\n"): return x[:-2]
    #if x.endswith("\n"): return x[:-1]

    return x[:]
#__________________________________________________________________________________
def Cleanup(Var):
    "Cleanup - strip leading and trailing white space(s)."

    Var = re.sub(r"/^\s*//",Var)
    Var = re.sub(r"/\s*$//",Var)

    return (Var)
#____________________________________________________________________________________
def DataFile_Read(File):
    "# Sources list information from a file like:"
    "# [Hosts]"
    "# mfg1"
    "# mfg3"
    "# and loads the array @Hosts"
    "# or"
    "# [Part_Number_Key]"
    "# 001 = 00002"
    "# 002 = 00292"
    "# ="
    "# %Part_Number_Key {"
    "#    001 => '00002'"
    "#    002 => '00292'"
    "#  } "

    # The array/hash must be a pre-declared global

   
    Label = ''  # Could be a list name or a hash name
    PrintLog( "Reading data file %s ... \n" % File, 1);
    try:
        with open (File, r) as fh :
            for line in fh:
                line = line.strip()
                if line.startswith("#"): next  # Starts with a comment
                if line.rfind(): next  # Skip blank lines I think?
                if re.search(r"^\s*$") :  next  # Skip blank lines I think?
                line = line.rstrip() # remove trailing white space
                if re.search(r"\[.*\]\]", line) :    # It's a list/hash name with a path imbeded
                    Label=line[line.find("[")+1:line.find("]]")]
                    _,Label,Path=Line.split("[")
                    if Label == "Record" : Load_Web_Data (Label)        #  so load the last one
                    elif  Label == "Data"  : #its a new hash clear perls clear hash/array-perl %{$Label} = ();  @{$Label} = ();
                        Global[Label] = ''
                        del Global[label]   
                elif re.search(r"\[.*\]", line) :    # It's a list/hash name
                    mySubString=mystring[mystring.find("[")+1:mystring.find("]")]
                    _,Label=mystring.split("[")
                    if Label == "Record" : Load_Web_Data (Label)        #  so load the last one
                    elif  Label == "Data"  : #its a new hash clear perls clear hash/array-perl %{$Label} = ();  @{$Label} = ();
                        Global[Label] = ''
                        del Global[label]                       
                else : # It's data
                    if re.search(r"^\s*\S+\s*\=\s*.*\s*$", line) :
                        if Label == "" :
                            Var,Global[Var]=line.split("=")
                            chomp(Var)
                            if not Global[Var]:  return(2, r'$' + Var) 
                            #Global[Var] assigned above
                        else :
                            if not Label :  return (3, r'%' + Label)
                            _,Global[Label][Var] = line.split("=")
                            chomp(Global[Label][Var]) # Chomp remove any return linefeed
                            if Debug : print("We are in Datafileread %s %s->%s %s = %s" % Label, Label, Var, Global[Label][Var], line.split("="))
                    else :   # It's a list
                        if not Global[Label] : return (4, '@' + Label) 
                        # s/^\s*(.*)\s*/$1/;
                        Global[Label] = Var  # push a new value            
    except:
        print("Unbale to open file: % in Function: %" % File, func.__name__)
    #  Why, never called if First : Load_Web_Data(Label)  #Once again at the end of the file

    #fh.close()
    return (0)
#________________________________________________________________
def DataFile_Write(File, Action="r+", Type="variblestr", Label=''):
    r"Write_Data_File (FullFS-File, [r+,w(overwrite)], [dictionary|list|varible], VarName)"
    "#           Note: The array/hash must be a pre-declared global"
    #Does not appear to be used, changing definitions to match Python List Tuple Dictionary Varible

    Pr_             = '  '   # Line Preamble

    if Type == '' : 
        Type = "variblestr"
    else :
        return (7, "Don\'t understand call \&DataFile_Write " + \
                "File=%s, Action=%s, Type=%s, Label=%s" % File, Action, Type, Label)

    fh = ''
    PrintLog("Writing data file %s (%s, %s, %s)... \n" % File, Action, Type, Label )

    try  :
        fh = open(File,Action )    
    finally:
        return (2)

    if Action == "w" : fh.write( "# Created by &Data_File::Write (%s, %s, %s) on: %s # %s \$\n\n" % Action, Type, Label, int(time.time()) + "! Do not edit!\n\n", Id )

    print ( "\n\n")

    Str = Type + " " + Label +" not defined!"
    if Type == 'dictionary' :
        if  Global[Label]:  return (3, Str) 
        fh.write("\n\[%s\]\n\n" % Label)
        for key in Global[Label] :
            if not Global[Label][key] == '' : fh.write( Pr_ + key + FPad(key) + Global[Label][key] + "\n")
    elif Type == 'list' :
        if not Label :  return (4, Str) 
        fh.write("\n\%s\]\n\n" % Label )
        for item  in Label :
            fh.write(Pr_ + item + "\n")
    elif Type == 'varible' :
        if Label : return (5, Str) 
        fh.write( "\n\n" +Pr_ + "Label" + "\t\=" + Label + "\n\n")
    else :
        return (6, "Don\'t understand call \&DataFile::Write_ ('File', %s, %s, %s)" % Action, Type, Label);
    fh.write("\n")

    fh.close()
    return (0)

#_______________________________________________________________________________
def FPad(Label):
    "Field Pad - allignment 12 char base size"

    Field_Pad = 12
    Field_Pad = Field_Pad - len(Label)
    return (' ' * Field_Pad + '= ')

#_______________________________________________________________________________
def Debug_Cat(File):
    "Takes a fully qualified filename as an argument and, if $Debug \
    cats the file to STDOUT"

    if Debug :
        print("\n\n%s\n\n" % File)
        if os.path.exists(File ) :
            with open (File, r) as fh :
                for line in fh: 
                    print (line)
        else :
            print( File + "... doesn't exist!\n")
    return

#_____________________________________________________________________________
def Exit(erc, Msg) :
    "Calls Exit_TestExec()"
    Exit_TestExec(erc,Msg) 
    return
#_____________________________________________________________________________
def Exit_TestExec( erc, Msg) :
    r"A cleaner variant of bye or exit! "
    r"Renamed (from &Exit) 03-09-22 to avoid redef. "
    r"Exit() must be the responsibility of 'main' (even"
    r"if it's just sub Exit Exit_TestExec ()  "

    # - Assigns global $Erc
    # - Tag msg with ERROR... if nz $Erc
    # - prints msg to screen
    # - Logs Msg to $0 xlog

    # ?? cat Msg to the $0 history log
    Erc = erc;    # Assign the global $Erc
    chomp(Msg)
    if Erc :
        Type = 2
    else :
        Type = 1

    if Stats['Status'] == 'Active'  :    # Remove any active tests
        Stats['Status'] = 'Error' ;

    Stats.Update_All 

    if Erc == 198 :         # (PETC Abort)
        print( "Bailing on Exit without logging...\n")
        Abort('rm')
        exit(0)

    if not Stats['Result'] == "PASS" : ASCIIColor('red')
    if Stats['Result'] == "PASS" : ASCIIColor('green')
    if Erc :
        Log_Error(Msg)
    else :
        if not Msg == '' :   Print_Log( Type, Msg ) 

    ASCIIColor('reset')
    Log_History(2)
    if not ERC == 107 : Stats.Session('delete')    # Release this session
    if HA_Session and not HA_Session == 0 :
        if not Erc == 107 and not opt_f : Stats.Session('delete',HA_Session)     # Release this HA session
    exit(Erc)
    return
#____________________________________________________________________________
def Get_INCs(List):
    "Usage by ?  get includes from whom?"

    Module = ''
    for Module in INC : #Value (Full path / filename)
        if not re.search.lower("perl", Module): INC[Module] = List
    return (List)

#________________________________________________________________
def HexDump(Str, Format=1):    
    "Return a string in a printable format similar to the Unix 'od' (Octal Dump) cmd"

    Count = 0    # Char on a line
    A, B = ''
    Set = 0
    Out = ''
    Val = ''
    Count = 0
    for i in Str :
        Count +=1
        Sub = i
        Hex    =  "{0:02x}".format(ord(Sub)) # Unsigned hex
        Val    =  "{0:02o}".format(ord(Sub)) # Unsigned ochar

        Val = Pad( Val, 2, '0', 2 )
        # Substitute the non-printable chars ...
        if SubVal < 30 :
            Char = r"*"
        else :
            Char = Sub

        A += Pad( Val,  3, ' ', 2 ) + ' '    # 1st line
        B += Pad( Char, 3, ' ', 2 ) + ' '    # 2nd line

        if Count == 16 or i == len(Str) - 1 : 
            Addr = Pad( Set, 6, '0', 2 )
            #                        $Out[1] .= "$Addr  $A\n        $B\n\n";
            Out += Addr + "  " + A + "\n        " + B + "\n\n"
            Count = 0
            A = ''
            B = ''
            Set = Set + 10

        if 0 :
            for Var in tuple("SubVal Hex Val Hash HexHash Char").split() :
                print( "\%s=>%s<, " % Var , Value)
                print("\nA=%s\nB=%s\nOut=%s\n" % A, B, Out)
            PETC()
    return (Out)

#____________________________________________________________________________
def Is_Running(Grep_Str, Check_PID='', Owner='root'):
    "Test to see if a cron or cmtest running"

                        # Test to see if something is
                        #  in the process table
#
# State: [ Untested | Debug | Test | Pilot | Released ]
#   WinXP:     Test
#   Linux:     Test
#
# Caller(s):   cron.pl cmtest.pl (Init.pm)
# Final:       lib/PT2.pm
    Its_Running = 0
    if Check_PID == '' : Check_PID = 1 
    #!!!     return 1 if $Grep_Str eq '';  # Added 8/2/04 !
    Cmd,pField = ''
    if OS == 'Linux' :
        Cmd = 'ps -a';
        if Check_PID : 
            pField = 0 
        else:
            pFiled = 3
    else :
        Cmd = 'qprocess';
        if Check_PID : 
            pField = 3 
        else:
            pFiled = 4
    try:
        ps = subprocess.Popen(['ps -a', 'aux'], stdout=subprocess.PIPE).communicate()[0]
        processes = ps.split('\n')
    except:
        Exit (999, "Error opening pipe to ps")
    sep = re.compile('[\s]+')
    for row in processes:
        pid,_,_,pidname = sep.split(row)    
        if re.search("^%s" % Grep_Str) : Its_Running = 1

    ps.close()
    Print_Log (11, "Grep_Str running = %s" % Its_Running);
    return (Its_Running);
#________________________________________________________________
def Load_Web_Data(Label) :
    "Load Records for Web Data?"

    if not re.search( "Data|Record", Label) : return
#    return unless $Label eq 'Data' or
#                  $Label eq 'Record';

    Key = Set_RecKey(Rec_Keys)

    PrintLog ("[Load_Web_Data \%%s] Key = \'%s\'" % Label, Key, 1 );
    if Key == '' : return

    for Attr in  Global[Label] :
        if Label[Attr] :   WebData[Key][Attr] = Label[Attr] 
    return
#________________________________________________________________
def xLoad_Dictionary(File): # was xLoad_Hash in perl
    " Load a Dictionary from a file"
    Print_Log( 11, "Loading hash(es) from file %s ... " % File);
    try:
        with open (File, r) as fh :
            for line in fh:
                if re.search("^\#", line) : next     # Commented out
                chomp(line)
                if re.search("^$", line) : next      # Blank line
                if Debug : PETC("\nIn: >%s<" % line) 
                Data = split("\t", line)    # Key, Data1, Data2, ...
                Key = Data[0];
                i   = 0
                for HashName in Hash :
                    i+=1
                    HashName[Key] = Data[i]
                    if Debug :PETC("Hash %s) %s\{%s\} =  %s" % i,HashName,Key, Data[i] )
    except:
        return (1)

    if not Quiet: print( "\n")

    IN.close()
    return (0)

#__________________________________________________________________________________
def NDT():
    "return current epoch time formated as 20020630.085901 "

    return ( PT_Date( int(time.time()), 9 ) );

#__________________________________________________________________________________
def Pad(Orig_Str="", Len_Int=0, Pad_Str=' ', Where=0):
    " Return a string with things added (<sp> default)"
    "# $Where = 1 pads on the right (Default)"
    "#          2 on the left"
    "#          3 pads on both sides, centering"
    "# original string in a new string $Len_Int long"

    if Pad_Str == '': Pad_Str = ' ' 
    
    while ( len(Orig_Str) < Len_Int ) :
        if Where == 2  :
            Orig_Str = Pad_Str + Orig_Str
        elif Where == 3  :
            Orig_Str = Pad_Str + Orig_Str + Pad_Str
            if len(Orig_Str) > Len_Int  : chop(Orig_Str) 
        else :
            Orig_Str = Orig_Str + Pad_Str

    while ( len(Orig_Str) > Len_Int ) :
        chop(Orig_Str)

    return (Orig_Str)

#__________________________________________________________________________________
def Parse (Length, Data=''):
    "#Return the front Nth of $_ -(Data)"
    "# stripping any leading / trailing ' 's"
    "# and update $_"
    Chunk  = ''
    if Data == '' :
        Exit(999, "No Data value passed to parse")
        return
    if Length : 
        Chunk = Data[0,Length]
        if Length < len(Data) : Data = Data[Data, Length + 1 ] 
    else :
        Chunk = Data;

    Chunk = re.sub("^ *", "", Chunk)      # Remove leading spaces
    Chunk = re.sub(" *$", "", Chunk)     # Remove trailing spaces

    return (Chunk)
#__________________________________________________________________________________
def PETC(MSG):
    "Generate a XML record"
    r"<XML>"
    "  <Callers>"
    "   cron.pl"
    "  </Callers>"
    "  <State options=\" Untested | Debug | Test | Pilot | Released>"
    "   <WinXP val=\"Released\" \/>"
    "   <Linux val=\"Released\" \/>"
    " </State>"
    "  <Final>"
    "   lib/PT2.pm"
    "  </Final>"
    "</XML>"


    #   Press
    #   _ Enter
    #     _ To
    #       _ Continue
    #         _

    X = ""
    Start_Wait = int(time.time()) #Epoh
    if GUI :
        Button = Message( MSG + "\n\n\nPress [OK] to continue, [Cancel] to Abort", 3,1 )
        if Button.lower == 'ok': return () 
        if Button.lower == 'cancel' : exit 
    else :
        if not MSG : MSG = 'Press <CR> to Continue, Q to End, R to Run'
        if not PETC_Dont_Stop :
            if not Silent : MSG += ""
            print(MSG+":")
            X = input()[:-1]  # get input and chop last char
            X.upper
            if X == 'Q' : exit 
            if X == 'R' : PETC_Dont_Stop = 1

    Wait_Time += int(time.time()) - Start_Wait;

    return (X)

#__________________________________________________________________________________

def PrintLog(Data) :
    " # This cannot be, be cause of the problem of variable dereferencing"
    "# NO package DataFile"
    Print2XLog (Data)
    return
#__________________________________________________________________________________
def PT_Date(Time=int(time.time()), Type=0):
    "PT_Date - return a date in various formats."
    "PT_Date (time, format);        [default format = 0]"
    "PT_Date ()"
    "PT_Date (time);                -> returns current time as a string"
    "PT_Date (1234567);                -> returns a date string for specified time int"
    "Format:    Returns:"
    "0          2002/06/30 08:59        [default]"
    "1          06/30 08:59"
    "2          06/30 08:59:01"
    "6          06/30/02"
    "8          06-30-02"
    "9          20020630.085901        [same as NTD function]"

    Date_Str = {};
    #time.local() =time.struct_time(tm_year=2017, tm_mon=5, tm_mday=17, tm_hour=15, tm_min=42, tm_sec=39, tm_wday=2, tm_yday=137, tm_isdst=1)

    #perl ( $Nsec, $Nmin, $Nhour, $Nmday, $Nmon, $Nyear, $Nwday, $Nyday, $Nisdst ) = localtime($Time);
    tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.localtime()
    tm_mon = Pad( str(tm_mon), 2, '0', 2 )
    tm_mon = Pad( str(tm_mday), 2, '0', 2 )
    tm_mon = Pad( str(tm_hour), 2, '0', 2 )
    tm_mon = Pad( str(tm_min), 2, '0', 2 )
    tm_mon = Pad( str(tm_sec), 2, '0', 2 )


    Date_Str[0] = str(tm_year)+"/"+str(tm_mon)+"/"+str(tm_mday)+" "+str(tm_hour)+"\:"+str(tm_min)
    Date_Str[1] = str(tm_mon)+"/"+str(tm_mday)+" "+str(tm_hour)+"\:"+str(tm_min)
    Date_Str[2] = Date_Str[1] + ":" + str(tm_sec)
    Date_Str[6] = str(tm_mon)+"/"+str(tm_mday)+"/"+ str(tm_year )[2:4]   # last two dig of 4 dig year
    Date_Str[8] = str(tm_year)+"-"+str(tm_mon)+"-"+str(tm_mday)                      #New!
    Date_Str[9] = str(tm_year)+str(tm_mon)+str(tm_mday)+"\."+str(tm_hour)+str(tm_min)+str(tm_sec)

    if Type == "[0-2689]" :
        return ( Date_Str[Type] )
    else:
        return (str(time.time()))
#__________________________________________________________________________________
def PT_Sleep(Time):
    "Sleep for x seconds"

    for i in rnage(0,Time) :
        if not Quiet : print(".")
        time.sleep( 1 )
    return

#________________________________________________________________
def Read_Cfg_File(File):
    "Sources parametric data from a file like:"
    "logFile = /tmp/log.txt"
    "Returns the # found"
    result = None
    try:
        if Globals.Debug : print("Read_Cfg_File trying to open: %s" % File)
        with open (File, 'r') as fh :
            if Globals.Debug : print("Read_Cfg_File opened: %s" % File)
            for line in fh:
                line = chomp(line) 
                #if Globals.Debug : print("Read_Cfg_File line: %s" % line)
                if not (line.strip().startswith("#") or  line == '') :  #Comment  or not re.search("^$", line) or re.search("^$", line)   re.search("^\s*\#"
                    if Globals.Debug : print("Read_Cfg_File line clean: %s" % line)
                    #Param = re.sub("\s+", '', Param)    #Remove any white spaces
                    #Data  = re.sub("^\s+", '', Data)    #Remove any leading/trailing white spaces
                    #Data  = re.sub("\s+$", '', Data)    #Remove any leading/trailing white spaces
                    #if not Param == '' or not Param == 'CmdFilePath': 
                    #if re.search("[(.*)]",line) :   #its a GlobalVar["name']
                    if line.startswith("[") : result= re.search("\[(.*)\]",line)
                    if re.search("=",line): 
                        Param,Data = line.split("=")  #its a parm and a value for GlobalVar
                        Param = chomp(Param)
                        Data = chomp(Data)
                        print (Param,Data)
                        if result: 
                            Globals.result.group(1)[Param]=Data
                            print("Found Result",result.group(1),Param,Data)
                        else: 
                            Globals.GlobalVar[Param]=Data
                        
                    #if result : 
                        #GlobalVarName = result.group(1)
                        #if Globals.Debug : print( "Read_Cfg_File found GlobalVar Name: %s" % GlobalVarName ) 
                            #Param1,Param2 = Data.split()
                            #Globals.GlobalVar[Param1][Param2] = Data
                        #else :
                            #Globals.GlobalVar[Param] = Data
    except:
        print("Read_Cfg_File failed to read %s" % File)
        return (1)
    print (Globals.joe['DefFanSpeed'])
    fh.close()
    return (0)
#________________________________________________________________
def Read_Data_File(File):
    " Might have been written by &Write_Data_File"

    Global.Erc, Data  = DataFile_Read(File)
    if not Erc : return (0) 
    if Global.Erc == 1 :
        PrintLog ("Unable to read Data File: %s" % File);
        return (2)
    elif Global.Erc :
        Exit (Global.Erc, "Attempt to load undefined var: %s" % Data);

    return (0)

#________________________________________________________________
def Read_Init_File(File):
    "# Sources list information from a file like:"
    "# [Hosts]"
    "# mfg1"
    "# mfg3"
    "# and loads the array @Hosts"
    "# The array must be a pre-declared global list"
    Path= "";    

    Print_Log( 11, "Reading cfg file %s ... \n" % File );
    List = []

    try:
        with open (File, r) as fh :
            for line in fh:
                chomp(line)
                if re.search("^\s*\#", line): next #Comment
                if re.search("^$", line): next # Blank line
                if re.search("\[.*\[.*\]\]/", line) :   # It's a section marker and Path   added 2/12/15 JSW
                    Path=line[line.find("[")+1:line.find("]]")]
                    _,List,Path=Line.split("[")		    
                elif re.search("\[.*\]", line) :    # It's a section marker
                    List = line[line.find("[")+1:line.find("]")]
                    Path= ""
                else :    # It's just data
                    List.append( Path+ line)
                        #print "push push $List  @{$List}, $Path.$_\n";		
    except :
        return(2)

    fh.close
    return (0)

#____________________________________________________________________________
def Set_RecKey(Fields):
    "Returns an extrapolated string (to be used for global $RecKey"
    # &PrintLog ("");

    Key   = ''
    for Var in (Fields) :
        Val = Record[Var]
        Key2Add = Record[Var]
        if not Key == '' : Key += '|' 
        Key += Key2Add
        if Key2Add == '' : Key = ''  # Null it if any element is null

    PrintLog ("[Set_RecKey]\tKey=\'%s\'" % Key, 1 )

    return (Key)

#________________________________________________________________
def Set_Time_Now():
    "This is here to enabling a tickle function to update $Nyear, $N...etc..."

    PT_Date (int(time.time())+1);

#__________________________________________________________________________________
def Show(Var):
    "# This is of limited usage. Careful about using it with a 'local' or 'my' var"
    "# since it won't be determined here, since it's outside it's primary block"

    PETC("%s = %s" % Var,Global[Var])

    return

#__________________________________________________________________________________
def Show_INCs(): 
    "# Pulled from Init"

    if Debug :
        print ("OS = %s\n" % OS)
        for i in INC :
            if not  "perl" :  print( "%s\n" % i ) 
            print("\nNew Files ( warmer than 30 mins ):\n\n")
    for Key  in INC : 
        File = INC[Key]
        Old = int ( (os.path.getmtime(File) * 24 * 60) + 0.5) # Mins old
        if not Old > 30 : print ("%s [%s mins]\n" % File,Old )

#________________________________________________________________
def Write_Data_File(File):
    " # &Write_Data_File (FullFS-File, [new|(cat)], [hash|list|scalar], VarName)"
    "#   Note: The array/hash must be a pre-declared global"
    Erc, Data  = DataFile_Write (File)
    if Erc == 2 :
        PrintLog ("Unable to read Data File %s" % File);
        return (2)
    elif Erc :
        Exit (Erc, "Attempt to write undefined var: %s" % Data);

    return (0)

#_____________________________________________________________________________
def YN(Msg, Default):
    " Originally from PT2"
    "Prompt user for a Y(es), N(o) or Q(uit)"
    "Return a 1, 0 or exit resp\'ly"

    Var = ""
    Msg = Msg +"(y/n/q)"
    if not Default == '' : Msg += "["+ Default +"]"
    while (1) :
        PETC_Dont_Stop = 0    # To avoid a hang!
        Var = PETC(Msg+"?")
        if Var == '' and not Default == '' : Var = Default.upper 
        if Var == 'Y' :
            return(1)
        else :
            return(0)

#_______________________________________________________________________________
def strip_ansi_codes(s):
    """
    >>> import blessings
    >>> term = blessings.Terminal()
    >>> foo = 'hidden'+term.clear_bol+'foo'+term.color(5)+'bar'+term.color(255)+'baz'
    >>> repr(strip_ansi_codes(foo))
    u'hiddenfoobarbaz'
    """
    return re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', s)
    #return re.sub(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]', '', s)
    #return re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?\\r\\n', '', s)
#_______________________________________________________________________________

1;
