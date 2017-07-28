#!/usr/bin/python
################################################################################
#
# Module:      UserID.py
#
# Author:      Paul Tindle ( mailto:Paul@Tindle.org )
#
# Descr:       Utility for appending encrypted user_ids to a current
#                 data file, typically maintained in ../cfgfiles/users.cfg and
#                 distributed to /usr/local/cmtest/users.cfg
#
# Version:    See Below
#
# Changes:       06/22/17 Conver uid.pl to Python
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
VER= 'v0.1 5/9/2017'; # Conversion to Python from Perl 050917 JSW
CVS_VER = ' [ CVS: $Id: Logs.pm,v 1.10 2011/01/21 18:38:56 joe Exp $ ]';
global CMtestVersion; 
if not "CMtestVersion" in globals() : CMtestVersion={}
CMtestVersion['cmtest'] = VER + CVS_VER
import sys
sys.path.append("./lib;")
import Globals
#from Globals import *
import Util
import Init
import FileOp
import Logs
import Connect

import os
import os.path
from os.path import expanduser
import socket
from optparse import OptionParser
#import lib  # import private library functions for CMtestpy, see lib/__init__.py
#import Globals
#print(globals())
#from lib.Util import Abort
#from lib.Globals import Myglobals

#import Mav
#import Power
#import lib.GUI
import sys, traceback  # catch keyboard interupt
import platform
from os.path import isfile, join
#__________________________________________________________________________

def main(): # 2005-09-12 v2
    """
    #           1) [Securely] Save a master user_id | user Name | current euid
    #              to allow for regeneration of all keys should the master key
    #              need to change
    #
    #           2) Add getopts to include CLSs:
    #               -b batch create from master (above)
    #               -c create new users.cfg file
    #               -m multiple adds (current mode) default: 1 add only
    #                See below BEGIN block
    #
    """    

    usage = "usage: %prog session#"
    parser = OptionParser(usage)
    parser.add_option("-d", "--debug", action="count",  dest="Debug", default=0,
                      help="Turn on Debug Stetments")
    parser.add_option("-v", "--verbose", action="count",  dest="Verbose", default=0,
                      help="Turn on more output") 
    parser.add_option("-U", "--User", dest="User", default="None",
                      help="Set User ID")
    parser.add_option("-P", "--Pass", dest="Password", default="None",
                      help="Set User Password")    
    (options, args) = parser.parse_args()
    #if not options.Session :
        #parser.error("-s session# required")
    Globals.Debug += options.Debug
    Globals.Verbose += options.Verbose
    Globals.CurrentUserPass = options.Password
    Globals.CurrentUserID = options.User

    OS = os.name
    if os.name == "nt":
        Globals.OS = "NT"
    else:
        Globals.OS = "Linux"
    if Globals.Debug  : print ("Detected OS: %s " % Globals.OS)    

    #Get our base directory and find the Station Config File 
    File = os.path.abspath(__file__)
    Globals.GP_Path = FileOp.fnstrip(File,1)
    PPATH = FileOp.fnstrip(File,1)
    if Globals.Debug : print ("OS path detected is: %s " % Globals.GP_Path)
    if Globals.GP_Path == '': Globals.GP_Path = ".."

    if Globals.OS == "NT":
        Globals.Cfg_File = join(Globals.GP_Path,"cfgfiles","testctrl.defaults.cfg")
        #Globals[LogPath] = "\Logs"
        TmpDir = expanduser("~")
    else:
        Globals.Cfg_File = '/usr/local/cmtest/testctrl.cfg'
        #Globals[LogPath] = r"/var/local/cmtest/logs"
        TmpDir = expanduser("~") + "/tmp"  

    if Globals.Debug  : print ("Config path detected is: %s " % Globals.Cfg_File)
    #if OS == 'nt':
        #Cfg_File = PPath + "/" + "cfgfiles/testctrl.defaults.cfg"
        #Tmp = os.getenv('TMP', "NO_TMP")
    #else :
        #Cfg_File = r'/usr/local/cmtest/testctrl.cfg'
        #Tmp = os.getenv(expanduser("~") + "/tmp", "NO_TMP")
    
    _Init()
    Exists = 0
    Create = 0
    if os.path.isfile(Globals.GlobalVar["UsersCfgPath"]):
        print("User ID file found: %s" % Globals.GlobalVar["UsersCfgPath"])
        Exists = 1
    else:
        print("No user ID file found")
        Create = Util.YN ("Can\'t find existing userid file %s! Create?" % Globals.GlobalVar["UsersCfgPath"])
        Globals.Erc = Util.DataFile_Write (Globals.GlobalVar["UsersCfgPath"], 'x', 'User_ID')
        if Globals.Erc : print( "Create Write_Data_File failed with Erc= ") #%s " % Globals.Erc) 

  # if not Create and not Exists : Util.exit("Can't do anything")

    if not Create:
        Globals.Erc = Util.Read_Data_File (Globals.GlobalVar["UsersCfgPath"])
        _PrintLog ("Read_Data returned a Erc %s" % Globals.Erc)
    
    Count = _Print_Debug()
    _PrintLog ("Read eUIDs for $Count existing users")
    
    Done  = 0
    Added = 0
    while not Done :
        Name, UID, Level = _Add_User()
        if Name == '' :
            #$Done = &YN ('Finished');
            Done = 1
        else  :
            try: 
                Globals.User_ID[UID] and Global.User_ID[UID] and not Name 
                print( "\n")
                _PrintLog ("Key already defined for user %s !" % Globals.User_ID[UID])
                time.sleep(1)
            except:
                Globals.User_ID[UID]    = Name;
                if not Level == '' : Globals.User_Level[UID] = Level 
                Added +=1
    
    if not Added :
        _PrintLog ('No new users added...!')
        Util.exit("Done")
    
    _Print_Debug()
    
    print("\n\nUpdating %s with %s new users" %(Globals.GlobalVar["UsersCfgPath"], Added))
    Util.PETC("Press Return to Continue")
    
    #my $Erc = &Write_Data_File ($File, 'new', 'hash', 'User_ID');
    #print "Write_Data_File failed with Erc=$Erc" if $Erc;
    
    #$Erc = &Write_Data_File ($File, 'cat', 'hash', 'User_Level');
    #print "Write_Data_File failed with Erc=$Erc" if $Erc;
    #Globals.Erc = Util.Write_Data_File(Globals.GlobalVar["UsersCfgPath"])
    Globals.Erc = Util.DataFile_Write (Globals.GlobalVar["UsersCfgPath"], 'r+',"dictionary","User_ID");
    if Globals.Erc : print( "DataFile_Write(r+) failed with Erc" ) #=%s" % Globals.Erc)

    #Globals.Erc = Util.Write_Data_File(Globals.GlobalVar["UsersCfgPath"])
    Globals.Erc = Util.DataFile_Write (Globals.GlobalVar["UsersCfgPath"], 'r+',"dictionary","User_Level");
    if Globals.Erc: print("DataFile_Write(r+) failed with Erc") #=%s" % Globals.Erc)
    
    exit()
    return

#_______________________________________________________________________________

def _Init():
    "Initialize UserID"
    if Globals.Debug : print("In this Function %s" % __name__)
    global Linux_gbl
    global Erc
    global Force
    
    if not os.name == "nt" :
        Linux_gbl = 'Ubuntu';  # Added 3/4/10 to support Ubuntu install
        try:
            with open ("/etc/*release", r) as fh :
                for line in fh:    
                    if re.search(r"Ubuntu", line) : Linux_gbl = 'Ubuntu'
                    elif re.search(r"Fedora", line) : Linux_gbl = 'Fedora'
                    elif re.search(r"CentOS", line) : Linux_gbl = 'CentOS'
                    else : 
                        Linux_gbl = 'unknown';
                        print ("Un-suported linux type found, I am going to die now")
                        exit()
        except:
            print ("Un-suported linux type found, are we Windows? I am going to die now")
            if not Debug : exit()
    #else we are NT
    print ("Debug in _Init %i" % Globals.Debug)
    Init.Init_All (0)
    Globals.Erc = 101
   
    Globals.Erc = 0
    #Init.Init_Also(0)
    return
#_________________________________________________________________________________

def _Exit( erc, Msg)   :
    """ Local Exit routine for Abort """
    if erc: PrintLog (Msg,0,0,1) 
    exit()
#_________________________________________________________________________________

def _PrintLog( Var ):
    Logs.Print2XLog(Var)
    return
#_________________________________________________________________________________

def _Print_Debug() :

    Count = '?'
    if Globals.Debug :
        Count = 0
        Level = ( "-","admin supervisor","user")
        print("\nUsers:")
        for key in Globals.User_ID:
            Count +=1
            #print( "\t%s \t: %s \(%s]\)" % (Globals.User_ID[key],key, Level[Globals.User_Level[key]] ))
            print( "\t%s \t: %s \(%s]\)" % (Globals.User_ID[key],key, Level ))
        print ("")
    return (Count);
#_________________________________________________________________________________

def _Add_User():

    print( "\n\n\tLeave \'Name\' field blank to Finish\n\n")
    
    Name = _Get_User_Data(' Name', 0)
    if Name == '' :
        ID = ''
        Level = ''
        Name = ''        
        return ('','','') 

    ID = _Get_User_Data('   ID', 1)

    Level = _Get_User_Data('Level', 1)

    #return (Name, crypt (ID, Key), Level)
    return (Name, ID, Level)

#_________________________________________________________________________________
def _Get_User_Data (Prompt, Required) :
    """Kiss version of Util.Ask_User"""
    Data = ""
    while 1 :
        Data = input("%s: " % Prompt)  # get Data and no Chop
        if Data == "\["  : Exit( 198, "Get UI Abort" )
        if Data.lower == 'q' : return ()
        if Data or not Required: return (Data) 

#____________________________________________________________________________________


if __name__ == "__main__":
    main()