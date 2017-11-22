#!/usr/bin/python
################################################################################
#
# Module:      power.py(Depreciated, folded into powerswitch
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
# Set port 6 snmp v1 on ex: cmdgen.CommandGenerator().setCmd( cmdgen.CommunityData('private', 'private', 0), 
#                      cmdgen.UdpTransportTarget(("192.168.1.201", "161")),  (oid, rfc1902.Integer(str(1))))
# Set port 6 snmp v1 off ex: cmdgen.CommandGenerator().setCmd( cmdgen.CommunityData('private', 'private', 0), 
#                      cmdgen.UdpTransportTarget(("192.168.1.201", "161")),  (oid, rfc1902.Integer(str(2))))
# Set port 6 snmp v1 cycle ex: cmdgen.CommandGenerator().setCmd( cmdgen.CommunityData('private', 'private', 0), 
#                      cmdgen.UdpTransportTarget(("192.168.1.201", "161")),  (oid, rfc1902.Integer(str(3))))
################################################################################
VER= 'v0.1 11/6/2017'; # Conversion to Python from Perl 050917 JSW
CVS_VER = ' [ CVS: $Id: Logs.pm,v 1.10 2011/01/21 18:38:56 joe Exp $ ]';
global CMtestVersion; 
if not "CMtestVersion" in globals() : CMtestVersion={}
CMtestVersion['power'] = VER + CVS_VER;

# http://henrysmac.org you need SNMP v1 enabled and user public able to read and user private able to write+.)
import Globals
#from Globals import *
import Util
import Init
import FileOp
import Logs
from pysnmp.entity.rfc3413.oneliner import cmdgen  
from pysnmp.proto import rfc1902
import logging
import os
import os.path
from os.path import isfile, join
from os.path import expanduser
import socket
import ipaddress
from optparse import OptionParser

#______________________________________________________________________________

def main():
    usage = "usage: %prog session#"
    parser = OptionParser(usage)
    parser.add_option("-d", "--debug", action="count",  dest="Debug", default=0,
                      help="Turn on Debug Stetments")
    parser.add_option("-v", "--verbose", action="count",  dest="Verbose", default=0,
                      help="Turn on more output") 
    parser.add_option("-c", "--control",  dest="Control", default="",
                      help="[ON|OFF|Reboot" )
    parser.add_option("-i", "--ip",  dest="Ip", default=Globals.GlobalVar['Power_Switch_IP'],
                      help="format IP/Name [ON|OFF|Cycle Outlet Number" )    
    parser.add_option("-p", "--port",  dest="Port", type="int", default=0,
                      help=" Outlet Number" )
    parser.add_option("-m", "--monitor", dest="Monitor", type="int", default=0,
                      help="Monitor Power Ports, loop until keypress")
    
    (options, args) = parser.parse_args()
    #if not options.Session :
        #parser.error("-s session# required")
    Globals.Debug += options.Debug
    Globals.Verbose += options.Verbose
    Control = options.Control
    Ip = options.Ip
    Port = options.Port
    Monitor = options.Monitor
    
    if Ip : #check fora valid Ip address/name
        try:
            ipaddress.ip_address(socket.getaddrinfo(Ip, 80)[0][4][0])
        except:
            Util.Exit(0, "Option -i Invalid Ip address or name {}".format(Ip))
    
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
    
    if "lib" in Globals.GP_Path : Globals.GP_Path,_ = os.path.split(Globals.GP_Path)
    if Globals.GP_Path == '': Globals.GP_Path = ".."
    if Globals.Debug : print ("OS path detected is: %s " % Globals.GP_Path)
    
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
    
    
    Globals.CmdFilePath = r"../" + PPATH +r"/cmdfiles"
    
    Util.ASCIIColor('reset')
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
    
    pdu = PDU()
    if not Monitor and not Ip : pdu.print_status_with_names()
    if Ip : 
        pdu.Ip = Ip
        print("Set PDU IP to: {}".format(pdu.Ip))
        #pdu.get_Ip()
    pdu.print_status_with_names()
    if Control == "on" and Port > 0 and Port < 9 :      
        print("Turn on Port {}".format(Port))
        pdu.outletnumbers[Port](1)
    elif  Control == "off" and Port > 0 and Port < 9 : 
        pdu.outletnumbers[Port](0)
    elif  Control == "reboot" and Port > 0 and Port < 9 : 
        pdu.outletnumbers[Port](2)    
    else: 
        Exit(0, "Invlaid request for control {} or port {}".formt(Control,Port))
        
    pdu.print_status_with_names()
#______________________________________________________________________________
class PduError(Exception):
    None
    
class PDU():
    class __PduParameters():
        def __init__(self):
            logging.basicConfig(filename=os.path.expanduser('~/pdu.log'),
                                format='%(levelname)s:%(asctime)s %(message)s',
                                level=logging.DEBUG)
            #Fill in your own IP below
            self.ip = '192.168.1.201'  #'10.10.30.230'
            #Can give each outlet a name:
            self.outlet_names = {1:'Outlet1',
                                 2:'Outlet2',
                                 3:'Outlet3',
                                 4:'Outlet4',
                                 5:'Outlet5',
                                 6:'Outlet6',
                                 7:'Outlet7',
                                 8:'Outlet8'}
            self.community = 'private'
            self.port = 161
            self.retries = 5
            self.timeout = 1
            self.getStatusAllOutlets = (1,3,6,1,4,1,318,1,1,4,2,2,0)
            self.outletBaseOID = [1,3,6,1,4,1,318,1,1,4,4,2,1,3]
            self.setOutletStates = {'On':1,'Off':2,'Reboot':3}
            logging.info('PDU started up on '+socket.gethostname()+' with:')
            logging.info('    IP = '+self.ip)
            keys = sorted(self.outlet_names.keys())
            #keys.sort()
            for curkey in keys:
                logging.info('    Port '+str(curkey)+' = '+self.outlet_names[curkey])
            
    def __init__(self):
        self.__pdu_params = self.__PduParameters()
        self.outletsnames = {}
        self.outletnumbers = {}
        #create each outlet and attach it to its appropriate outlet name as a functions
        for cur_outlet_number in self.__pdu_params.outlet_names.keys():
            cur_outlet_name = self.__pdu_params.outlet_names[cur_outlet_number]
            if cur_outlet_name == None:
                cur_outlet_name = 'outlet'+str(cur_outlet_number)
                self.__pdu_params.outlet_names[cur_outlet_number] = cur_outlet_name
            new_outlet = self.__PduOutlet( self.__pdu_params, 
                                           cur_outlet_number, 
                                           cur_outlet_name, self.status )
            self.outletsnames[cur_outlet_name] = new_outlet
            self.outletnumbers[cur_outlet_number] =new_outlet
        #self.print_status_with_names()

    #def __call__(self):
        #self.print_status_with_names()
        #return self.status()
    @property
    def Ip(self):
        print("proprety ip:{}".format(self.__pdu_params.ip))  
        return self.__pdu_params.ip
   
    @Ip.setter
    def Ip(self,ipval) :
        print("setting ip:{}".format(ipval))
        self.__pdu_params.ip=ipval        

    def print_status_with_names(self):
        _outletnames = []
        _outletnumbers = []
        _outletstatus = []
        max_name_length = max([len(a) for 
                               a in self.__pdu_params.outlet_names.values()])
        for i,status in enumerate(self.status()):
            outlet_number = i+1
            if os.name == 'posix':
                reset_color_string = '\033[0;0m'
                if status == 'On':  
                    color_string = '\033[1;32m'
                elif status == 'Off':
                    color_string = '\033[0;31m'
                else:
                    color_string = ''
            elif os.name == 'nt':  # these colors sequences not supported in cygwin
                color_string = ''
                reset_color_string = ''
            else:
                color_string = ''
                reset_color_string = ''
            print ( color_string + str(outlet_number)+' '+
                    (('%'+str(max_name_length)+'s') % 
                     self.__pdu_params.outlet_names[outlet_number]) + 
                    ' ' + status + reset_color_string + " | ", end='')
            _outletnumbers.append(outlet_number)
            _outletnames.append(self.__pdu_params.outlet_names[outlet_number])
            _outletstatus.append(status)
        print()
        #print("{}".format(_outletnumbers))
        #print ("{}".format(_outletnames))
        #print ("{}".format(_outletstatus))

    def status(self):
        logging.info('status request')
        return self.__snmpGet__(self.__pdu_params.getStatusAllOutlets)
    
    def __snmpGet__(self,oid):
        ( errorIndication, errorStatus, 
          errorIndex, varBinds ) = cmdgen.CommandGenerator().getCmd(
            cmdgen.CommunityData('test-agent', 'public'),
            cmdgen.UdpTransportTarget((self.__pdu_params.ip,
                                       self.__pdu_params.port)),
            oid,(('SNMPv2-MIB', 'sysObjectID'), 0))
        if errorIndication:
            raise PduError(errorIndication)
        else:
            if errorStatus:
                raise PduError('%s at %s\n' % 
                               (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex)-1] or '?'))
            else:
                for name, val in varBinds:
                    if name == oid:
                        return str(val).split()

    class __PduOutlet():
        def __init__(self, pdu_params, outlet_number, outlet_name, status_function):
            self.__pdu_params = pdu_params
            self.outlet_number = outlet_number
            self.outlet_name = outlet_name
            self.__all_outlet_status_function = status_function
            
        def __call__(self,request=None):
            print("Request {}".format(request))
            if request != None:
                if request == 1:
                    self.on()
                elif request == 0:
                    self.off()
                elif request == 2 :
                    self.reboot()
                else:
                    raise PduError("undefined power change request")  
            #return self.status()
        
        def __snmpSet__(self,oid,val):
            errorIndication, errorStatus, \
                errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(
                cmdgen.CommunityData('private', 'private', 1), 
                cmdgen.UdpTransportTarget((self.__pdu_params.ip, self.__pdu_params.port)), 
                (oid, rfc1902.Integer(str(val))))
            if errorIndication:
                raise PduError(errorIndication)
            else:
                if errorStatus:
                    raise PduError('%s at %s\n' % 
                                   (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex)-1] or '?'))
                else:
                    for name, val in varBinds:
                        if name == oid:
                            return str(val).split()

        def on(self):
            logging.info("ON requested for "+self.outlet_name+
                         " on outlet # "+str(self.outlet_number))
            self.__snmpSet__(self.__pdu_params.outletBaseOID+[self.outlet_number],
                             self.__pdu_params.setOutletStates['On'])
            #return self.status()
        
        def off(self):
            logging.info("OFF requested for "+self.outlet_name+
                         " on outlet # "+str(self.outlet_number))
            self.__snmpSet__(self.__pdu_params.outletBaseOID+[self.outlet_number],
                             self.__pdu_params.setOutletStates['Off'])
            #return self.status()
        def reboot(self):
            logging.info("Reboot requested for "+self.outlet_name+
                         " on outlet # "+str(self.outlet_number))
            self.__snmpSet__(self.__pdu_params.outletBaseOID+[self.outlet_number],
                             self.__pdu_params.setOutletStates['Reboot'])
            #return self.status()        

        def status(self):
            outlet_status = self.__all_outlet_status_function()[self.outlet_number - 1]
            if outlet_status == 'On':
                return True
            elif outlet_status == 'Off':
                return False
            raise PduError("Unrecognized PDU state error")

if __name__ == '__main__':
    print("Power Self Test")
    main()
    


1;

