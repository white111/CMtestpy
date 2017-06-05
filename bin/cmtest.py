#!/usr/bin/python
################################################################################
#
# Module:      cmtest.py
#
# Author:      Paul Tindle ( mailto:Paul@Tindle.org )
#
# Descr:      Main Test executive
#
# Version:    0.1 $Id$
#
# Changes:   05/18/17 Conversion from perl - JSW
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
import Globals
#from Globals import *
import Util
import Init
import FileOp
import Logs
import Connect
import sys
sys.path.append("../lib;")
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



#__________________________________________________________________________
def main():
    
    #Globals.Myglobals()
    #import Globals
    print (Globals.Debug)
    #print("My Debug = %i" % Debug)
    print(globals())
    #Debug flag 
    
    #global Debug
    #Debug = 1
    #global Verbose
    #global Menu1
    #global session
    #global Cfg_File
    #global Tmp
    #global CmdFilePath
    #global Version
    #global Session
    #global SessionForce
    #global CMPipe; CMPipe=os.getenv('CmTest_Release_Pipe', "No_Pipe") 
    #global UserID
    #global Out_File
    #global Loop_overide
    #global shucks; shucks = 0
    #global GlobalVar
    #print (global())
    #Get input from command line
    usage = "usage: %prog session#"
    parser = OptionParser(usage)
    parser.add_option("-d", "--debug", action="count",  dest="Debug", default=0,
                      help="Turn on Debug Stetments")
    parser.add_option("-v", "--verbose", action="count",  dest="Verbose", default=0,
                      help="Turn on more output") 
    parser.add_option("-B", "--Batch", type="int",  dest="Menu1", default=0,
                      help="Batch Mode - no Menu prompt, does not support multi level menu" )  
    parser.add_option("-s", "--session", dest="Session", type="int", default=0,
                      help="Set Sesion #, Default is first avaiable")
    parser.add_option("-L", "--Loop", dest="Loop", type="int", default=0,
                     help="Overide all Loop counts(seconds)")    
    parser.add_option("-F", "--Force", dest="Force", type="int", default=0,
                      help="Force Session #")
    parser.add_option("-U", "--User", dest="User", default="None",
                      help="Set User ID")
    parser.add_option("-O", "--Output", dest="Output", default=r"cmtest.xml",
                      help="Set Output XML file, will default to tmp/cmtest.xml")       
    (options, args) = parser.parse_args()
    #if not options.Session :
        #parser.error("-s session# required")
    Globals.Debug += options.Debug
    Globals.Verbose += options.Verbose
    Globals.Menu1 = options.Menu1
    Globals.Session = options.Session
    Globals.SessionForce = options.Force
    Globals.UserID = options.User
    Globals.Out_File = options.Output
    Globals.Loop_overide = options.Loop

    OS = os.name
    if os.name == "nt":
        OS = "NT"
    else:
        OS = "Linux"
        

    
    #Get our base directory and find the Station Config File 
    File = os.path.abspath(__file__)
    PPATH = FileOp.fnstrip(File,1)
    if Globals.Debug > 0 : print ("OS path detected is: %s " % PPATH)
    if PPATH == '': PPATH = ".."

    if OS == "NT":
        Cfg_File = PPATH + r"\cfgfiles\testctrl.defaults.cfg"
        #Globals[LogPath] = "\Logs"
        TmpDir = expanduser("~")
        if Globals.Debug > 0 : print ("Config path detected is: %s " % Cfg_File)
    else:
        Cfg_File = '/usr/local/cmtest/testctrl.cfg'
        #Globals[LogPath] = r"/var/local/cmtest/logs"
        TmpDir = expanduser("~") + "/tmp"  

    #if OS == 'nt':
        #Cfg_File = PPath + "/" + "cfgfiles/testctrl.defaults.cfg"
        #Tmp = os.getenv('TMP', "NO_TMP")
    #else :
        #Cfg_File = r'/usr/local/cmtest/testctrl.cfg'
        #Tmp = os.getenv(expanduser("~") + "/tmp", "NO_TMP")


    CmdFilePath = r"../" + PPATH +r"/cmdfiles"

    Logs.ASCIIColor('reset')

    _Init()
    GUI = 0
    # uneeded Perl &GUI_Init if $GUI;
    Quiet = 0;  # Don't allow since we only have a char menu right now
    shucks = 0
    try:
        Menu_main()  # Bring up menu and start excution
    except KeyboardInterrupt:
        print( "Shutdown requested...exiting")
        _catch_zap()
    except Exception:
        traceback.print_exc(file=sys.stdout)
        sys.exit(0)

    if not Quiet : print("done\n") 
    Exit (0)

#_____________________________________________________________________________
def _Init():
    "Initialize Cmtest"
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
    Erc = 101
    Force = options.Force
    Erc = 0
    Init_Also (0)
    return
#____________________________________________________________________________________
def _catch_zap(): 
    global shucks; shucks +=1
    Power ('OFF');
    Stats['Status'] = 'Aborted';
    Exit(998,"<Ctrl>-C Aborted");

#____________________________________________________________________________________





if __name__ == "__main__":
    main()