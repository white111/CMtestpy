#!/usr/bin/python
################################################################################
#
# Module:      powerswitch.py
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
VER= 'v0.1 11/6/2017'; # Conversion to Python from Perl 050917 JSW
CVS_VER = ' [ CVS: $Id: Logs.pm,v 1.10 2011/01/21 18:38:56 joe Exp $ ]';
global CMtestVersion; 
if not "CMtestVersion" in globals() : CMtestVersion={}
CMtestVersion['powerswitch'] = VER + CVS_VER;



import Globals
#from Globals import *
import Util
import Init
import FileOp
import Logs
import pysnmp

#use Net::SNMP;

#______________________________________________________________________________

def main():
        hostname = shift
        community = "private";
        Globals.States   = ( 0 );
        
        internallist = ("Outlet 1","Outlet 2","Outlet 3","Outlet 4","Outlet 5","Outlet 6","Outlet 7","Outlet 9")
      
        
        # enterprises.apc.products.hardware.masterswitch.sPDUOutletControl
        # apc = {enterprises 318}
        # products = {apc 1}
        # hardware = {products 1}
        # masterswitch = {hardware 4}
        # sPDUOutletControl = {masterswitch 4}
        # sPDUOutletControlTable = {sPDUOutletControl 2}
        # sPDUOutletControlEntry = {sPDUOutletControlTable 1}
        # sPDUOutletCtl = {sPDUOutletCtl 3}
        # sPDU
        sPDUOutletControlTable_oid = "1.3.6.1.4.1.318.1.1.4.4.2"
        sPDUOutletCtl = "sPDUOutletControlTable_oid +".1.3"
        sPDUOutletCtlName = sPDUOutletControlTable_oid+ ".1.4"
        
        portNames = []
        portStatus =[]
        opts =""
        port =0
        action = ""
        l = ""
        a = ""
        result = ""
        
        
        portIPs = {
                "Outlet 1"        : "1",
                "Outlet 2"        : "2",
                "Outlet 3"        : "3",
                "Outlet 4"        : "4",
                "Outlet 5"        : "5",
                "Outlet 6"        : "6",
                "Outlet 7"        : "7",
                "Outlet 8"        : "8"
        }
        
        my @statusArray = ("outletOn",
                "outletOff", "outletReboot", "outletUnknown", "outletOnWithDelay",
                "outletOffWithDelay", "outletRebootWithDelay");
        
        
        my ($session, $error) = Net::SNMP->session(
                -hostname => "$hostname",
                -community => "$community"
        );
        
        if (!defined($session)) {
                printf("ERROR opening SNMP session: %s.\n", $error);
                exit 1;
        }
        
        # find out what the power switch things the host names are.
        # we'll use these to see if anything is obviously wrong.
        getPortNames();
        getOutletStatus();
        checkInternalLists();
        
        getopts('Ddv', \%opts);
        
        ($port, $action) = parseOptions(@ARGV);
        
        if ($action eq "status") {
                printStatus($port);
                exit(0);
        }
        
        for ($l = 0; $l < 7; $l++) {
                if ("$statusArray[$l]" eq "$action") {
                        $a = $l + 1;
                        last;
                }
        }
        
        my $oid = "$sPDUOutletCtl.$port";
        $result = $session->set_request( -varbindlist => [$oid, INTEGER, $a] );
        
        if (!defined($result)) {
                print ("Error:  Action NOT successful $result.\n");
                exit(1);
        }
        
        exit (@States);
#______________________________________________________________________________
sub getPortNames {
        my $x;
        for ($x = 1; $x < 9; $x++) {
                my $oid = "$sPDUOutletCtlName.$x";
                my $result = $session->get_request(
                        -varbindlist => [$oid]
                );

                if (!defined($result)) {
                        printf("ERROR getting host names: %s.\n", $session->error);
                        $session->close;
                        exit 1;
                }
                $portNames{$x} = $result->{$oid};
        }
}
#______________________________________________________________________________
sub getOutletStatus {
        my $x;
        for ($x = 1; $x < 9; $x++) {
                my $oid = "$sPDUOutletCtl.$x";
                my $result = $session->get_request(
                        -varbindlist => [$oid]
                );

                if (!defined($result)) {
                        printf("ERROR getting outlet status: %s.\n", $session->error);
                        $session->close;
                        exit 1;
                }
                $portStatus{$x} = $result->{$oid};
        }
}
#______________________________________________________________________________
sub printStatus {
        my $x;
        my ($port) = $_[0];

        if ($port == 0) {
           for ($x = 1; $x < 9; $x++) {
                printStatus_port($x);
           }
        } else {
                printStatus_port($port);
        }
}
#______________________________________________________________________________
sub printStatus_port {

        my ($port) = @_;

        my $State = '';
        if ($portStatus{$port} == 1) {
            $State = 'ON ';
            $States[$port] = 1;
        } elsif ($portStatus{$port} == 2) {
            $State = 'Off';
            $States[$port] = 0;
        }
        print "P$port: $State\n";

    }
#______________________________________________________________________________



sub getStatus {

        return $statusArray[$_[0] - 1];

}
#______________________________________________________________________________

sub parseOptions {

        my @argv = @_;
        my $wport;
        my $waction;

        if ($#argv < 1 && $argv[0] ne "status") {
                usage();
        }

        my $action = $argv[0];
        my $object = $argv[1];
#
        if ($object =~ /p([1-8])/) {
                $wport = $1;
         } elsif ($object =~ /^[0-9]+\.[0-9]+\.[0-9]+\.([0-9]+)$/) {
                # it's an ip address.  take the last chunk.
                my $twhost;
                $twhost = getPortNameFromIP($1);
                if ($twhost eq "") {
                        print("No host match found for IP address $object\n");
                        exit 1;
                }
                $wport = getPortFromPortName($twhost);
                if ($wport eq "") {
                        print("Power switch doesn't know about this port.\n");
                        exit 1;
                }
        } elsif ($object =~ /^([0-9]{1,3})$/) {
                # it's an ip address.  take the last chunk.
                my $twhost;
                $twhost = getPortNameFromIP($1);
                if ($twhost eq "") {
                        print("No host match found for IP address $object\n");
                        exit 1;
                }
                $wport = getPortFromPortName($twhost);
                if ($wport eq "") {
                        print("Power switch doesn't know about this port.\n");
                        exit 1;
                }
        } else {
                $object =~ s/\..*//g;
                $wport = getPortFromPortName($object);
                if ($wport eq "" && $action ne "status") {
                        print("Power switch doesn't know about this port.\n");
                        exit 1;
                } elsif ($action eq "status") {
                        $wport = 0;
                }
        }

        # now figure out what action to take.

        if ($action eq "on") {
                if (! $opts{"d"}) {
                        verboseprint ("Turning port $wport on.\n");
                        $waction = "outletOn";
                } else {
                        verboseprint ("Turning port $wport on with delay.\n");
                        $waction = "outletOnWithDelay";
                }
        } elsif ($action eq "off") {
                if (! $opts{"d"}) {
                        verboseprint ("Turning port $wport off.\n");
                        $waction = "outletOff";
                } else {
                        verboseprint ("Turning port $wport off with delay.\n");
                        $waction = "outletOffWithDelay";
                }
        } elsif ($action eq "reboot" | $action eq "cycle") {
                if (! $opts{"d"}) {
                        verboseprint ("Rebooting port $wport.\n");
                        $waction = "outletReboot";
                } else {
                        verboseprint ("Rebooting port $wport with delay.\n");
                        $waction = "outletRebootWithDelay";
                }
        } elsif ($action eq "status") {
                $waction = "status";
        } else {
                print "Invalid action.\n";
                exit(1);
        }
        return ($wport, $waction);;

}
#______________________________________________________________________________

sub getPortNameFromIP {

        my $l;
        my $tmp = $_[0];

        foreach $l (keys(%portIPs)) {
                if ($portIPs{$l} == $tmp) {
                        return $l;
                }
        }
        return "";
}
#______________________________________________________________________________

sub getPortFromPortName {

        my $portname = $_[0];
        my $match = 0;
        my $l;
        my $tmp;

        foreach $l (keys(%portNames)) {
                if ($portNames{$l} =~ /^$portname$/i) {
                        return $l;
                }
        }
        return "";
}
#______________________________________________________________________________

sub usage {

print <<EOM;
usage: $0 [-dDv] action object
Options:
        -d        delay
        -D        debug
        -v        verbose

actions:
        on
        off
        delay
        status

objects:
        p<n>                port number n
        <n>                last IP address octet n
        xxx.xxx.xxx.<n>        IP address n
EOM

        exit(1);
}
#______________________________________________________________________________
sub dangerWillRobinson {

print <<EOM;
******************************************************************
* DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER *
******************************************************************
I have an internal list that translates hostnames to physical ports.
I checked the power switches against this list and they don't match.
This implies that you've made some changes and forgot to tell the power
switch about them, or forgot to tell me about them.

The problem is that I use the internal tables of the power switch in
order to figure out what goes where.  Because there is no consistency,
I will have to assume that things are not where I think they are.
Proceeding in these circumstances is dangerous.

Please fix either my internal lists, or the tables in the power
switch.

I'm aborting now.
******************************************************************
* DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER DANGER *
******************************************************************
EOM

        exit(1);
}
#______________________________________________________________________________
sub checkInternalLists {

        my $x;
        for ($x = 1; $x < 9; $x++) {
                if (lc($internallist{$x}) ne lc($portNames{$x})) {
                    print "$x} $portNames{$x}\n";
                         dangerWillRobinson();

                }
        }
}
#______________________________________________________________________________

sub debugprint {

        if ($opts{"D"}) {
                print $_[0];
        }
}
#______________________________________________________________________________
sub verboseprint {

        if ($opts{"v"}) {
                print $_[0];
        }
}
#______________________________________________________________________________


def Power(Action) :   # This is called by Connect.pm following a <POWER>   ON|OFF

        Session  = Globals.Stats['Session']
        Session2 = Globals.Stats['Session'] - 8;
        Delay    = 0                  # Future
        States   = []
        Cmd = ""
        Logs.Print_Log (1, "Power {} Session {}".format(Action,Session))
        Logs.Print_Log (11, "{} Power {}".format(Power_type,Action))
        if Power_type == 'manual' :
                Alert ('Please turn UUT Power ' + Action.upper + '!')
        elif Power_type == 'APC') :
                if Session < 9  :
                        Cmd = "powerswitch.pl {} {} ".format(Power_Switch_IP, Action.lower)
                        if Action.lower == 'off' or Action.lower == 'on' : Cmd = Cmd + ' p {}'.format(Session)
                        Logs.Print_Log (1, "Power Cmd: $Cmd")
                elif Session > 8 and Session < 17 and Globals.Power_Switch2_IP not == "" :
                        Cmd = "powerswitch.pl {} {}".format(Power_Switch2_IP,Action.lower)
                        if Action.lower == 'off' or Action.lower == 'on' : Cmd = Cmd + ' p{}'.format(Session2) 
                        Logs.Print_Log (1, "Power Cmd: $Cmd")
                else :
                        Alert ('Please turn UUT Power {} !'.format(Action.upper))
                Logs.Print_Log (11, "Exec'ing {}".format(Cmd))
#        print "Exec'ing $Cmd\n";
                if Power_Switch_IP eq '' :        Util.Exit (999, "No Power_Switch_IP")         
                try: 
                        open(APC,"r") "{}".format(Cmd)
                except:    
                        Util.Exit (999, "Can\'t start snmp session to APC switch {}".format(Power_Switch_IP));
                if Action == 'status' 
                        while <APC>) {
                                Util.chomp;
                                if (/^P(\d+): (.*)/) {
                        $States[$1] = ($2 eq 'ON ') ? 1
                    : ($2 eq 'Off') ? 0
                               : "";
                               } else {
                        die "Can't read APC power status";
                }
                        }
                        &Print_Status (@States);
                }
                close APC;

        } elsif ($Power_type eq 'LPT') {
                &LPT_Power ($Session, $Action);
        } else {
                die "Invalid entry in testctrl.cfg file Power_type = $Power_type";
        }
        $Stats {'Power'}++ if $Action eq 'ON';  #Count the number of power ups per test
        $TestData {'Power'}=$Power_type . "_" . $Action;
        return ($Erc);
# ? Is this what stats power is for
#    $Stats {'Power'} = $Action if $Action =~ /ON|OFF/;
}


#_______________________________________________________________________________
sub Print_Status {

        my (@States) = @_;
        return if $Quiet;

        my $Str_ON  ='';
        my $Str_OFF ='';
        foreach (1..8) {

            if ($States[$_]) {
                $Str_ON  .= ' ON ';
            $Str_OFF .= '    ';
            } else {
                $Str_ON  .= '    ';
            $Str_OFF .= 'Off ';
        }
    }
        print "\n$Power_type switch:\n\n\tBit:\t 1   2   3   4   5   6   7   8\n";
        print "\t\t$Str_ON\n\t\t$Str_OFF\n";

}
#_______________________________________________________________________________

from pysnmp.hlapi import *
def GetSNMPVers(IP='192.168.1.200')

errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
           CommunityData('public', mpModel=0),
           UdpTransportTarget((IP, 161)),
           ContextData(),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
)

if errorIndication:
        print(errorIndication)
elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
        for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))
#_______________________________________________________________________________
from pysnmp.hlapi import * 
def snmpwalk(IP='192.168.1.200'):
        """
        Preload PySNMP MIBs
        +++++++++++++++++++
        
        Send a series of SNMP GETNEXT requests using the following options:
        
        * with SNMPv3 with user 'usr-md5-des', MD5 auth and DES privacy protocols
        * over IPv4/UDP
        * to an Agent at demo.snmplabs.com:161
        * for all OIDs starting from 1.3.6
        * preload all Python MIB modules found in search path
        
        Functionally similar to:
        
        | $ snmpwalk -v3 -l authPriv -u usr-md5-des -A authkey1 -X privkey1 -m ALL demo.snmplabs.com:161 1.3.6
        
        """#
        
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in (
                                 
                                  UdpTransportTarget(('IP', 161)),
                                  ContextData(),
                                  ObjectType(ObjectIdentity('1.3.6').loadMibs())):
                
                #varBinds) in (SnmpEngine(),
                        #UsmUserData('usr-md5-des', 'authkey1', 'privkey1'),
                        #UdpTransportTarget(('IP', 161)),
                        #ContextData(),
                        #ObjectType(ObjectIdentity('1.3.6').loadMibs())):                
        
                if errorIndication:
                        print(errorIndication)
                        break
                elif errorStatus:
                        print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                        break
                else:
                        for varBind in varBinds:
                                print(' = '.join([x.prettyPrint() for x in varBind]))
#_______________________________________________________________________________

if __name__ == "__main__":
        main()