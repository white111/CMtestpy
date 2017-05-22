#!/usr/bin/python
################################################################################
#
# Module:      cmtest.py
#
# Author:      Paul Tindle ( mailto:Paul@Tindle.org )
#
# Descr:      Main Test executive
#
# Version:    0.1 $Id: cmtest.pl,v 1.6 2011/12/12 22:53:09 joe Exp $
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
#            Copyright (c) 2005-2008 Joe White. All rights reserved.
#
################################################################################
VER= 'v0.1 5/9/2017'; # Conversion to Python from Perl 050917 JSW
CVS_VER = ' [ CVS: $Id: Logs.pm,v 1.10 2011/01/21 18:38:56 joe Exp $ ]';
CMtestVersionn['cmtest'] = VER + CVS_VER

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

#__________________________________________________________________________
def main():

    our $OS = ($ENV {'OS'} eq 'Windows_NT') ? 'Win32' : 'Linux';

    my (@Check_Path) = split (/\/|\\/, $0);
    pop @Check_Path;  pop @Check_Path;      # $FN, then 'bin'
    our $PPath = join '/', @Check_Path;   # Now contains our root directory
        $PPath = '..' if $PPath eq '';      # for a $0 of ./
    our $Cfg_File;
    our $Tmp;

    if ($OS eq 'Win32') {
         $Cfg_File = "$PPath/cfgfiles/testctrl.defaults.cfg";
         $Tmp = $ENV{'TMP'};
    } else {
         $Cfg_File = '/usr/local/cmtest/testctrl.cfg';
         $Tmp = "$ENV{'HOME'}/tmp";
    }

    pop @INC;
    unshift @INC, "$PPath/lib";
#    unshift @INC, "$ENV{'LIB'}/lib";
    unshift @INC, '.';

    our $CmdFilePath = "$PPath/cmdfiles";
}

our %Version;
our $CMPipe=$ENV{'CmTest_Release_Pipe'};

#use warnings;
use Connect;
use File;
use Getopt::Std qw(:DEFAULT);
use Init;
use Logs;
use Mav;
use Power;
use PT;
use GUI;
use Term::ANSIColor;


    print color 'reset';
    _Init;
    $GUI = 0;
    &GUI_Init if $GUI;
    $Quiet = 0;  # Don't allow since we only have a char menu right now
    &Menu_main();

    print "done\n" unless $Quiet;
    &Exit (0);

#_____________________________________________________________________________
sub _Init:()

                #Globals:
    our $Linux_gbl = 'Ubuntu';  # Added 3/4/10 to support Ubuntu install
    if (! system "cat /etc/*release | grep -q 'Ubuntu'" ) {
    	$Linux_gbl = 'Ubuntu';
       } elsif (! system "cat /etc/*release | grep -q 'Fedora'" ) {
        $Linux_gbl = 'Fedora';
       } elsif (! system "cat /etc/*release | grep -q 'CentOS'" ) {
        $Linux_gbl = 'CentOS';
       } else {
         $Linux_gbl = 'unknown';
         print "Un-suported linux type found, I am going to die now";
         die
       }
    our @Menu_List = ();
    our @Menu_Desc = ();
    our @Menu_Cmd  = ();

    &Init_All (0);

    our $Usage = "
    Usage: $0 [-dfghqv] [-L <NewLoopCount>] [ -M Menu_Item ] [-Z <Session>]\n
      Where:
         -d:     Debug mode
         -f:#    Force [-Z session]
         -g:*    GUI mode
         -h:     Print this message
         -L:*    Loopcount over-ride
         -M:     Menu Item [batch mode]
         -q:     Quiet mode
         -v:     Verbose mode (ignored with -q)
         -Z:     Session no [Default: first available from 1 ]

       [* = WIP feature - not yet implemented / released]
       [# = Deprecated]
";
     $Erc = 101;

             # Process the command line arguments...

     &getopts ('C:L:M:U:Z:dfghqv1') || &Invalid ($Usage);

     #!!! really??? -f option (hidden):  Force (Serial no update, ...)

     $CmdFilePath = $opt_C unless $opt_C eq ''; #Hidden $CmdFilePath override!
     our $Force = ($opt_f) ? 1 : 0;
     $Erc = 0;
     &Init_Also (0);
}

#____________________________________________________________________________________

if __name__ == "__main__":
    main()