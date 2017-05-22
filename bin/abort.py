#!/usr/bin/python
################################################################################
#
# Module:      abort.py
#
# Author:      Paul Tindle ( mailto:Paul@Tindle.org )
#
# Descr:      Standalone utility to create the abort flag to stop a test cleanly
#
# Version:    0.1 $Id: abort.py,v 1.3 2008/02/20 23:05:33 joe Exp $
#
# Changes:   Convert from Perl 050317 JSW
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
#            Copyright (c) 2005-2008 Joe White. All rights reserved.
#
################################################################################
global CMtestVersion; CMtestVersion = {}
#module_name, package_name, ClassName, method_name, ExceptionName, function_name, GLOBAL_CONSTANT_NAME, global_var_name, instance_var_name, function_parameter_name, local_var_name
#__________________________________________________________________________
import platform
import sys
#sys.path.append("../lib;")
import os.path
from os.path import expanduser
import socket
from optparse import OptionParser
#import lib  # import private library functions for CMtestpy, see lib/__init__.py
from lib.Globals import *
import lib.Util
from lib.Util import Abort
#from lib.Globals import Myglobals

#_____________________________________________________________________________

def main():
    #Debug flag 
    #Debug = 1
    global Debug
    #Get input from command line
    usage = "usage: %prog session#"
    parser = OptionParser(usage)
    parser.add_option("-d", "--debug", action="count",  dest="Debug", default=0,
                      help="Turn on Debug Stetments")
    parser.add_option("-s", "--session", dest="Session", type="int",
                      help="Set Sesion number to abort")
    (options, args) = parser.parse_args()
    if not options.Session :
        parser.error("-s session# required")
    Debug += options.Debug
   
      
    OS = os.name
    if os.name == "nt":
        OS = "NT"
    else:
        OS = "Linux"
    
    #Get our base directory and find the Station Config File 
    if Debug > 0 : print ("OS path detected is:", os.path)
    PPATH = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
    if PPATH == '': PPATH = ".."
    
    if OS == "NT":
        Cfg_File = PPATH + "\cfgfiles\testctrl.defaults.cfg"
        TmpDir = expanduser("~")
    else:
        Cfg_File = '/usr/local/cmtest/testctrl.cfg'
        TmpDir = expanduser("~") + "/tmp"
        
    # Unsure if needed Perl Code
    #    pop @INC;
    #    unshift @INC, "$PPath/lib";
    #    unshift @INC, "$ENV{'LIB'}/lib";
    #        unshift @INC, '.';
    
    CmdFilePath = PPATH + "/cmdfiles"
    
    if Debug > 0 : print ("Session detected is: %d" % options.Session)
    if Debug > 0 : print ("OS detected is: %s " % OS )
    
    _Init()  # Init all startup needs
    
    Stats['Session'] = options.Session;
    
    if not Abort('run_check') :
        print (Bell + "Session doesn't appear to be running ... Aborting (this!)\n")
        sys.exit(0);
    
    Abort('set')
    
    print("Session "+ Stats['Session']+" on "+ Stats['Host_ID']+" will abort before next command\n")
    sys.exit(0);
    return

#_______________________________________________________________

def _Init():
    "Init Things needed for abort.py"
    #Globals:
    global stats
    global Stats_Path
    global Bell
    Bell       = r"";
    Stats_Path = r'/var/local/cmtest/stats';
    Stats      = {
      'Host_ID' : socket.gethostname(),                # HostID for logging purposes
      'Session' : '' 
      }

    Erc = 0    # Error code ( non-zero denotes an error occurred )

    #        &Init_All (1);
    #        &Init_Also (1);

    return
#_____________________________________________________________________________

if __name__ == "__main__":
    main()
