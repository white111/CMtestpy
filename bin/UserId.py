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
from os.path import isfile, join

def main() : # 2005-09-12 v2
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
    Globals.CurrentUserPass = options.PASSWORD
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
    Exists = 1
else:
        Create = Util.YN ("Can\'t find existing encrypted userid file $File! Create?"))
    

if not Create or Exists : Util.exit("Can't do anything")

if not Create:
    Globals.Erc = Util.Read_Data_File (Globals.GlobalVar["UsersCfgPath"])
    Logs.PrintLog ("Read_Data returned a Erc %s" % Globals.Erc)

Count = Print_Debug()
Logs.PrintLog ("Read eUIDs for $Count existing users")

Done  = 0
Added = 0
while not Done :
    Name, UID, Level = Add_User()
    if Name == '' :
        #$Done = &YN ('Finished');
        Done = 1
    elif  Globals.User_ID[UID] and
             Global.User_ID[UID] not Name 
        print( "\n")
        Logs.PrintLog ("Key already defined for user %s !" % Globals.User_ID[UID]")
        sleep 1
    else :
        Globals.User_ID[UID]    = Name;
        if not Level == '' : Globals.User_Level[UID] = Level 
        Added +=1

if not Added :
    Logs.PrintLog ('No new users added...!')
    Utile.exit()

Print_Debug()

print("\n\nUpdating %s with %s new users" %(File, Added))
Util.PETC()

#my $Erc = &Write_Data_File ($File, 'new', 'hash', 'User_ID');
#print "Write_Data_File failed with Erc=$Erc" if $Erc;

#$Erc = &Write_Data_File ($File, 'cat', 'hash', 'User_Level');
#print "Write_Data_File failed with Erc=$Erc" if $Erc;

my $Erc = &Write_Data_File ($File, '>', '%User_ID');
print "Write_Data_File failed with Erc=$Erc" if $Erc;

$Erc = &Write_Data_File ($File, '%User_Level');
print "Write_Data_File failed with Erc=$Erc" if $Erc;

exit;

#_______________________________________________________________________________

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
    Globals.Erc = 101
   
    Globals.Erc = 0
    Init.Init_Also(0)
    return
#_________________________________________________________________________________

sub Exit     {
    my ( $erc, $Msg ) = @_;
    &PrintLog ($Msg,0,0,1) if $erc;
    exit;
}

sub PrintLog { &main::Print2XLog (@_)}

sub Print_Debug {

    my $Count = '?';
    if ($Debug) {
        $Count = 0;
        my @Level = qw( - admin supervisor user);
        print "\nUsers:\n";
        foreach  ( keys %User_ID ) {
            $Count++;
            print "\t$User_ID{$_} \t: $_ \($Level[$User_Level{$_}]\)\n";
        }
        print "\n";
    }
    return ($Count);
}

sub Add_User {

    print "\n\n\tLeave \'Name\' field blank to Finish\n\n";

    my $Name = &Get_User_Data(' Name', 0);
    return () if $Name eq '';

    my $ID = &Get_User_Data('   ID', 1);

    my $Level = &Get_User_Data('Level', 1);

    return ($Name, crypt ($ID, $Key), $Level);
}

sub Get_User_Data {  #Kiss version of PT:Ask_User

    my ($Prompt, $Required) = @_;
    my $Data;
    while (1) {
        printf  "$Prompt: ";
        chop( $Data = <STDIN> );
        if ( $Data eq "\[" ) { return (); }
        if ( lc $Data eq 'q' ) { return (); }
        return ($Data) if length ($Data)
                       or !$Required;
    }


}

#____________________________________________________________________________________





if __name__ == "__main__":
    main()