#!/usr/bin/python
################################################################################
#
# Module:     File.py
#
# Author:      Paul Tindle ( mailto:Paul@Tindle.org )
#			 Joe White( mailto:joe@stoke.com )
#
# Descr:      Subs for file IO
#
# Version:    (See below) $Id$
#
# Changes:     Conversion to Python from Perl 050617 JSW
#              Syntax correct 5/9/17 JSW
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
#            Copyright (c) 2005-2008 Stoke. All rights reserved.
#            Copyright (c) 2017 Joe White. All rights reserved.
#
################################################################################
VER= 'v0.2 5/9/17'; # Syntax correct 5/9/17 JSW
CVS_VER = ' [ Git: $Id$ ]';
global CMtestVersion
if "CMtestVersion" not in globals() : CMtestVersion={}
CMtestVersion['File'] = VER + CVS_VER;
#__________________________________________________________________________________
import os.path
import os
from os import listdir, walk
from os.path import join, getsize
import zlib #CRC32 Checksum
import collections
import re
import sys
import Globals

#__________________________________________________________________________________
def fnstrip(Full_FN="", Specifier=9) :
    "Returns specified portions of a filename Invocation: fnstrip (c:/usr/tmp/foo.txt, X)"
    "else returns script start directory and script name"
       ############################################  Stop #################################
    if (not Full_FN == "") and ( Specifier < 9 ) :
        Ret_val1,Ret_val2 =os.path.split(Full_FN)
        #        X:        Returns:
        #        0        c:/usr/tmp/foo.txt     # Unchanged
        if Specifier == 0 : return(Full_FN)
        #*       1        c:/usr/tmp             # Parent path
        elif Specifier == 1 : 
            Ret_val=Ret_val1
        #        2        c:/usr/tmp/foo         # Parent dir + base filename
        elif Specifier == 2 : 
            Ret_val = Ret_val1 + PathSep + Ret_val2.split(".")[0] # ,_ = os.path.splitext(Full_FN)[0])
        #        3        foo.txt                # File name + extension
        elif Specifier == 3 : Ret_val = os.path.split(Full_FN)[1]
        #        4        tmp                    # Parent dir
        elif Specifier == 4 : Ret_val = os.path.pardir(Full_FN)[1]
        #*       6        c:/usr                 # Grand-parent path
        elif Specifier == 6 : Ret_val = os.path.split(Full_FN.split(".")[-2])[0]
        #        7        foo                    # Base filename
        elif Specifier == 7 : Ret_val = os.path.split(Full_FN.split(".")[-2])
        #        8        txt                    # File extension
        else: Ret_val = Ret_val.split(".")[-1]
        
        return(Ret_val)
    else :
        return ( os.getcwd() )

#__________________________________________________________________________________
def File_List (File_Path=".",No_Recurse=0):
    """Update Global Dir_List and File_list and returns a count of files in directory
    #    Updates:
    #       our @Dir_List  - List of (sub)dirs in a spec'd dir (&File_List)
    #       our @File_List - List of files in a spec'd dir (&File_List)
    """
    Globals.File_List = ''
    count = 0
    try:
        Globals.Dir_List = os.listdir(File_Path)
        for root, dirs, files in os.walk(File_Path):
            if Debug : print(root, "consumes ", end="")
            if Debug : print(sum([getsize(join(root, name)) for name in files]), end="")
            if Debug : print("bytes in ", len(files), "non-directory files")
            Globals.File_List.append(files)
            if 'CVS' in dirs: dirs.remove('CVS')  # don't visit CVS directories
            if '.git' in dirs: dirs.remove('.git')  # don't visit Git directories
            if No_Recurse : break
            Count += 1
            return (Count);
    except:
        exit("Unable to process File_Path: %s in FileList" % File_Path)
        return(0)
#_______________________________________________________________________________
def File_Checksum (fileName) :
    " Return CRC32 checksum of file"
    prev = 0
    fileName=r"M:\python\cmtest30\cmtest\lib\Init_SSX.pm"
    for eachLine in open(fileName,"rb"):
        prev = zlib.crc32(eachLine, prev)
    Chksum = "%X"%(prev & 0xFFFFFFFF)
    if Debug : print ( "File: ",  fileName, "Checksum: ", Chksum    )
    return (Chksum);

#_______________________________________________________________________________
def File_Close (FileHandle) :
    "Closes the global file handle FH"

    FH = FileHandle
    FH.close 
    #   Perl Code unknow why $FH--
    FH_Count -= 1
    return

#_______________________________________________________________________________
def File_Open (File="", FH="", Mode="r") :
    "Opens the global file handle FH with File and Mode , defaults to read mode"

    if Mode == '': Mode = '<'               # Default
    if Mode == 'IN':  Mode = 'r'
    if Mode == 'OUT':  Mode = 'w'	    #Write apend
    if Mode == 'APEND':  Mode = 'a'	    #Write apend

    if File == '' : PT_Exit("Attempt to open <null> file") 
    try:
        FH = open (File, Mode)
        return(0)
    except:
        return(1)

#_______________________________________________________________________________
def File_Open_Recursive (File='') :
    "Opens the global file handle FH with File and Read Mode , defaults to read mode"

    if FH not in globals: FH = 'FH00' 
    FH_Count +=1
    File_Open( File, FH, 'r' );     #In only!
    return (FH);

#_______________________________________________________________________________
def Get_File_Stats (File='') :
    ' Originally &Show_Files_Attrs__Get_Stats for \
    ( $Date, $Size, $DateStr, $MIA ) = &Get_File_Stats ("$Dir1/$Name")'

    for root, dirs, files in os.walk(File):
        if Debug : print(root, "consumes ", end="")
        if Debug : print(sum([getsize(join(root, name)) for name in files]), end="")
        if Debug : print("bytes in ", len(files), "non-directory files")
        if 'CVS' in dirs: dirs.remove('CVS')  # don't visit CVS directories
        if No_Recurse : break

    Date     = 0;
    Size     = '  -?-'
    Date_Str = '   -'
    MIA      = 0

    try :
        os.stat(File).st_size 
        Size = os.stat(File).st_size                          # Size
        Date = os.stat(File).st_mtime  # Mod Date    conversion to date if needed = $^T - ( ( -M $File_Spec ) * 3600 * 24 );    
        Date_Str = PT_Date( Date, 1 );
    finally :
        MIA = 1;

    return ( Date, Size, Date_Str, MIA );

#_______________________________________________________________________________
def Show_File_Attrs(Dir1, Dir2, File2do):
    "Create a list of printable Atribuites"

    try:
        File2do
        global Files 
        Files = File2do
    except: pass

    Debug2 = 0

    global FileList;  FileList = {}       # Composite list of files (either path) Hash/Disconary
    global Files4Update; Files4Update = []     # List of files (no leading path)
    global cp_args; cp_args = []         # List of 'file1 file2' where master is newer
    global Files4Archive; Files4Archive = []    # List of files where copy is newer than master

    Offset = [35, 6, 11 ] ;    # Name   Size Date   Size Date
    Gap = [ 3, 1 ];            #      0     1     0     1
    Next_Col = Offset[1] + Gap[1] + Offset[2];
    #$Dir1 =~ s/\/$//;  #Don't completely understand, but appears to be an extra / in base path
                                    # if I remove in ptdisty::setvar, push path fails
    Files1 = [] 
    Files2 = []    # !!!WTF are these used for?
    try:
        for index in range( len(Files)) :
            Files1.append( Dir1 + Globals.PathSep + index)
            if ((opt_s and WWW_Path  != '') and Dir1.find(Globals.PathSep + "www" +Globals.PathSep)) :
                Files2.append(WWW_Path,index)  # Modified for Site server WWW files
                if Debug : print ("Show file attr push", Files2, WWW_Path,index)
            else :
                Files2.append(Dir2,Globals.PathSep,indesx)   # original JSW
            FileList[index] = 1
    finally: 
        Files1 = Show_Files_Attrs__Get_Files(Dir1)
        Files2 = Show_Files_Attrs__Get_Files(Dir2)


    if Quiet :

        print ( "_"*110, "\n\n") 
#        my $Msg = ($ChkSumIt) ? 'ON!' : 'disabled (force copy!)';
#        print "\nCopy on \'same-size \/ checksum-fail only\' is $Msg\n\n";

        GapStr = ();
        for index in range(Gap) :
            GapStr.append( ' '* index)

        #                &PETC(">$GapStr[0]<, >$GapStr[1]<" );
        #                &PETC(($Gap[0] + $Next_Col)*2);

        print ( Pad( "System hostname:", Offset[0], ' ', 2,GapStr[0], ENV['HOSTNAME'], "\n"))
        print (Pad ('Search Path:', 35, ' ', 2), '   ', Dir2)


        print ("\n")

        print ("\n", '_' * Offset[0], "\n")

        print (Pad( 'Master Path:', Offset[0], ' ', 2 ), GapStr[0],
               'V' * Next_Col,
               '-'  (Gap[0] * 2 + Next_Col), Dir1, "\n")

        print (Pad( 'Copy Path:', Offset[0], ' ', 2 ), GapStr[0],
               ' ' * (Gap[0]  + Next_Col),
               'V' * Next_Col,
               '-' * Gap[0], Dir2, "\n");

        Show_Files_Attrs__Bars (Offset[0], GapStr[0], Next_Col);

        #  &Pad( $Dir1, $Next_Col ), $GapStr[0], &Pad( $Dir2, $Next_Col ), "\n";

        print (Pad( 'FileName', Offset[0]), GapStr[0],
               Pad( 'Size', Offset[1] + Gap[1] ),
               Pad( 'Date', Offset[2] + Gap[0] ),
               Pad( 'Size', Offset[1] + Gap[1] ),
               Pad( 'Date', Offset[2] + Gap[0] ), "\n")

        Show_Files_Attrs__Bars (Offset[0], GapStr[0], Next_Col);
#        print '_' x $Offset[0], $GapStr[0], '_' x $Offset[1], $GapStr[1],
#          '_' x $Offset[2], $GapStr[0], '_' x $Offset[1], $GapStr[1],
#          '_' x $Offset[2], "\n";


    # Compare each file ...
    Name = collections.OrderedDict(FileList.items())
    for index in Name : 
        Msg   = ''
        Date1, Size1, DS1, MIA1  = Get_File_Stats(Dir1,Globals.PathSep,Name);
        Name2 = Name;
        Dir_2 = Dir2;
        F1 = split( GLobals.PathSep, Name)[-1];     # Dest only
        D1 = split( Globals.PathSep, Name)[1];     # Dest only
        if D1 == 'tftpboot' : next	#and ! $Verbose;  # Added JW - Skip showing tftp
        if D1 == 'cfgfiles' :
            Name2 = F1
            Dir_2 = re.sub( Globals.PathSep+ "\w{1}$", "", Dir_2)            # Remove the release pipe  Dir_2 = r"joe/test/g"

        if D1 == 'www' and WWW_Path != '' :
            Dir_2 = WWW_Path;            # We have alread remove release pipe, change DIR2 to /
            Dir_2 = re.sub.i(Globals.PathSep+" www" + Globals.PathSep + "$", "", Dir_2)            # Remove WWW

        Date2, Size2, DS2, MIA2  = Get_File_Stats(Dir_2,Globals.PathSep,Name2)

        SizeDiff = Size1 - Size2;
        if SizeDiff <= 0 :  Size2 = ''      # No need to reprint it!

        Age = Date1 - Date2            # +ve if master (1st) is newer
        if (2 > Age and Age > -2) : Age = 0  # A 1 sec diff	 on identical files!

        if SizeDiff or Age == 1 : NotTheSame = 1 
        else : NotTheSame = 0
        if MIA1 or MIA2 == 1  :  MIA = 1 
        else : MIA = 0

        if ( MIA ) : 
            Msg += 'MIA'
        elif (NotTheSame and not SizeDiff):   # different Dates only
            if (ChkSumIt and File_Checksum(Dir1,Globals.PathSep,Name) == File_Checksum(Dir2,Globals.PathSep,Name2)) : 
                if ChkSumIt: Msg += '(CS passed!)' 
                NotTheSame = 0
            else :
                if ChkSumIt: Msg += 'CS failed!' 
                if not Age : DS2 = ''       # No need to reprint it!

        if NotTheSame :
            if not MIA1 :
                Files4Update.append(Name)
                cp_args.append(Dir1,Globals.PathSep,Name," ",Dir2,Globals.PathSep,Name2)
            if Age > 0 :   # The Master has been updated
                Msg += '*'
            else :
                Msg += '*' * 10
                Files4Archive.append(Dir2,Globals.PathSep,Name2)

        Str = Pad(Name2, Offset[0]) + GapStr[0]     # Name
        Str += Pad( Size1, Offset[1], ' ', 2 ) + GapStr[1]
        Str += Pad( DS1, Offset[2] ) + GapStr[0]
        if (NotTheSame or MIA2) :
            Str += Pad( Size2, Offset[1], ' ', 2 ) + GapStr[1] + Pad( DS2, Offset[2] ) + r"  <-! " + Msg
        elif (Age and  not SizeDiff) :      # Must have passed the chksum!
            Str += 'ok' + ' ' * (Offset[1] - 1) + Pad( DS2, Offset[2] )
        else :
#            Str += "\t/-/";
#            Str += "\t\< \"";
            Str += "ok";

        if not Quiet : print(Str)

        if Debug2 : 
            print ("\n", "\tName1 \t= $Name\n", "\tName2 \t= $Name2\n",
                   "\tMIA1 \t= $MIA1\n", "\tMIA2 \t= $MIA2\n",
                   "\tDate1\t= $Date1\n", "\tDate2\t= $Date2\n", "\tAge  \t= $Age\n",
                   "\tSize1\t= $Size1\n", "\tSize2\t= $Size2\n",
                   "\tSDiff\t= $SizeDiff\n", "\t\!Same\t= $NotTheSame\n");
            PETC()
    Show_Files_Attrs__Bars (Offset[0], GapStr[0], Next_Col)

    return

#_______________________________________________________________________________________________

def Show_Files_Attrs__Bars(Offset, GapStr, Next_Col):
    " Print _ line for Atribuite list  "

    print( '_' * Offset, GapStr, '_' * Next_Col, GapStr,
           '_' * Next_Col, "\n")
    return
#_______________________________________________________________________________________________

def Show_Files_Attrs__Get_Files (Path):
    "Get file list ?"

    #  No sure this is needed File_List = [];
    New_List = [];
    #File_List(Path);
    for index in range(File_List(Path)) :    # $Path/the/file.txt -> the/file.txt
        index.strip( Path + Globals.PathSep ) 
        New_List.append( index)
        # not sure this is needed $FileList{$FNwoPath} = 1;  # !!!WTF

    return (New_List);
#_______________________________________________________________________________________________


def xShow_Files_Attrs__Sub_File_Name(Dir, MyName):
    "Get file list ??"
    Old_Name = MyName;
    if not( os.path.isfile(Dir + Globals.PathSep + MyName)) :            # Try any known substitutions
        D1 = MyName.split(Globals.PathSep)[0]     # Because .xxxrc files are buried
        F1 = MyName.split(Globals.PathSep)[1]     # Because .xxxrc files are buried
        if D1 == "cfgfiles": MyName = F1 
#         $MyName = &fnstrip ($MyName, 2) if &fnstrip ($MyName, 8) eq 'pl';
    if Old_Name != MyName : 
        Print2XLog ("Dir=" + Dir + r", Old=" + Old_Name + r", New=" + MyName, 1) 
    return(MyName);

#_______________________________________________________________________________
1;
