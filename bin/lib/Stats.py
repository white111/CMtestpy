#!/usr/bin/python
################################################################################
#
# Module:      Stats.py
#
# Author:      Paul Tindle ( mailto:Paul@Tindle.org )
#			   Joe White ( mailto:joe@stoke.com )
#
# Descr:      The customization modules for each OEM. May be referred to
#               as <OEM>.pm in comments
#
# Version:    (See below) $Id$
#
# Changes:    05/31/17 Convert Perl to Python
#
#
# Still ToDo:
#
# License:   This software is subject to and may be distributed under the
#            terms of the GNU General Public License as described in the
#            file License.html found in this or a parent directory.
#            Forward any and all validated updates to Paul@Tindle.org
#
#            Copyright (c) 1995 - 2005 Paul Tindle. All rights reserved.
#            Copyright (c) 2005-2008 Stoke. All rights reserved.
#            Copyright (c) 2017 Joe White. All rights reserved.
#
################################################################################
VER= 'v0.1 5/31/2017'; # Conversion to Python from Perl 053117 JSW
CVS_VER = ' [ Git: $Id$ ]';
global CMtestVersion; 
if not "CMtestVersion" in globals() : CMtestVersion={}
CMtestVersion['Stats'] = VER + CVS_VER

from lib.Globals import *

#__________________________________________________________________________________
def Read(Stats_File):
        """ Read stats from files """
        global Stats
        try:
                with open (Stats_File, r) as fh :
                        for line in fh:
                                chomp(line)
                                if line.startswith("#"): next  # Starts with a comment
                                if line.rfind(): next  # Skip blank lines I think?
                                Param, Data=line.split("=")
                                Data  = Cleanup (Data)
                                Param = Cleanup (Param) 
                                if re.search(r"\[.*\]", line) :
                                        _,Section = line.split("[")
                                if Section == "Stats" : Stats[Param] = Data
                                if Section == "TestData" : TestData[Param] = Data
                                if Section == "Globals" : Globals[Param] = Data
                                #else ignore
        except:
                Exit (8, "Can\'t open $Stats_File for read")
        fh.close
        return
#__________________________________________________________________________________
def Session(Op, Sess=Stats['Session']):
        global Stats
        if not Stats_Path : exit( "Stats_Path not defined! Did testctrl.cfg get sourced??")
           
        File = Stats_Path + '/system/' + Stats['Host_ID'] + '-'
        FileName = File + Sess
        UMask = os.umask()
        os.umask(0)
        Done = 0
        if Op == 'delete' :
                try:
                        os.remove(FileName)
                except OSError:
                        pass
        if Op == 'next' :
                Stats['Session'] = 1
                while (os.path.exsists(File + Stats['Session']) or Done) :
                        Stats['Session'] += 1
                        FileName = File + Stats['Session']
                        try:
                                Erc = open(FileName, 'a').close() # touch
                                Erc = os.chmod(FileName, stat.S_IRWXO) # chmod 777 $FileName"
                        except: 
                                print ( "Unable  to modify file %s" % FileName)
                                Print_Log (2, "Problem touching %s " % FileName) 
                Tag = '>'
                Done = 1
        if Op == 'read' :
                if not os.path.exsists(FileName) : return (0) 
                Tag = '<'
                Done = 1
        if Op == 'write' :
                Tag = '>';
                Done = 1


        o

        if Op == 'read': 
                try:
                        STATS = open(Tag +FileName)
                        PID = STATS
                        return (PID)
                except:
                        Exit (8, "Can\'t open Stats File: %s for %s" % File,Op)
        else :
                print("STATS %s" % Stats['PID'])

        STATS.close
        os.umask(UMask)

        return (0)
#__________________________________________________________________________________
def Update(Stat, Value):
        """ Update a Stat with a Value """
        global Stats

        Stats[Stat] = Value;
        Stats.Write()
        return
#__________________________________________________________________________________
def Update_All():
        """ Update all Stats """

        Update_Test_Times()
        Stats.Write()
        return
#__________________________________________________________________________________
def Update_Test_Times():
        """ Update all Stats times """
        global Stats
        if Stats['ECT']: Stats['TTG'] = Stats['ECT'] - time.time() 
        if Stats['Status'] == 'Finished' : Stats['TTG'] = 0 
        TestData['TTT'] = time.time() - Stats['TimeStamp']
        TestData['ATT'] = TestData['TTT'] - Wait_Time
        if TestData['TEC'] : TestData['TSLF'] = time.time() - TestData['TOLF'] 
        TestData['ERC']  = Erc

        if Debug : Globals['Loop_Time'] = Loop_Time
        return
#__________________________________________________________________________________
def  Write ():
        """ Write stats - used by update functions """ 
        
        Stats['Updated'] = time.time()
        # Because of the Package declaration(Perl) Likly not needed for Python ...
        Stats_Path    = Stats_Path
        Host_ID       = Host_ID
        LogSN     = LogSN

        File1 = Stats_Path+ "/" + Host_ID + '-' + getppid + '.txt'
        File2 = Stats_Path + "/" + Stats['UUT_ID'] + '.txt'

        if Stats['UUT_ID'] == '' :
                Stats_File = File1
        else :
                if os.path.exsists(File):
                        Print_Log (11, "Renaming stats file from %s to %s" % File1,File2)
                        os.rename(File1,File2)
                        
                Stats_File = File2;

        if not os.path.isdir(Stats_Path) : Stats_File = Tmp+ "/" + TmpStats.txt   #For early debug!: 
        try :
                STATS = open(Stats_File, 'w')
                STATS.write( "\n[Stats]\n")

                L1 = 15        # Pad (right of key) amount

                for Key in Stats :
                        STATS.write( Pad(Key, L1) + "= " + Stats[Key] + "\n")

                STATS.write( "\n[TestData]\n" )

                for Key in TestData :
                        STATS.write(Pad(Key, L1) + "= " + TestData[Key] + "\n")

                STATS.write("\n[Globals]\n")

                for Key in Globals :
                        #Var = 'main::' + Key  # Pointer operation
                        STATS.write(Pad(Key, L1) + "= " + Key + "\n")
        
        except: 
                Exit (8, "Can\'t open Stats File: %s for write" % Stats_File)        
        STATS.close
        return
#_____________________________________________________________________________
1;