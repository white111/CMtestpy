################################################################################
#
# Module:      Menu_Exit.py
#
# Author:      Paul Tindle ( mailto:Paul@Tindle.org )
#			   Joe White ( mailto:joe@stoke.com )
#
# Descr:      Menu execution
#
# Version:    (See below) $Id$
#
# Changes:    
#
# Still ToDo:
#
# License:   This software is subject to and may be distributed under the
#            terms of the GNU General Public License as described in the
#            file License.html found in this or a parent directory.
#            Forward any and all validated updates to Paul@Tindle.org
#
#            Copyright (c) 1993 - 2005 Paul Tindle. All rights reserved.
#            Copyright (c) 2005-2013 Stoke. All rights reserved.
#            Copyright (c) 2017 Joe White. All rights reserved.xx
#
################################################################################
VER = '0.1  09/20/17'; #             #Name Changes to Mavenir  1/29/15
CVS_VER = ' [ Git: $Id$ ]'
global CMtestVersion
if "CMtestVersion" not in globals() : CMtestVersion={}
CMtestVersion['cmtest1'] = VER + CVS_VER
#____________________________________________________________________________

import Globals
import Init_Product1   # Gen1 hardware

import Stats
import Util
import Logs
import Connect
import os.path
#use SSX2;   # Gen1 hardware
#use SSX3;   # Gen2 Hardware


def Get_Data(Key, Data):       # Called by &Screen_Data to parse the comm buffer

    Key = Key.title
    #print ("Get_Data $Key, $Data\n");
    if Key == 'Serial': Get_Serial_Info_Example()  # No need to pass $Data since we're
                                            # using global @Screen_Data
    if Key == 'ShowMFG' : Get_show_mfg_serial_Example()
    if Key == 'Board': Get_Board_Info_Example()  # No need to pass $Data since we're
    if Key == 'Chassis' : Get_Chassis_Info() 
    #&Get_SW55thlink  if $Key eq 'SW55thlink';
    #&Get_Volts if $Key eq 'Volts';
    #&Check_GLC_Thermal ($Data) if $Key eq 'GLC_Thermal';
    #&Check_GLC_Thermal_Display ($Data) if $Key eq 'GLC_Thermal_Display';
    #&Get_CPLD_data if $Key eq 'CPLD'; # No need to pass $Data since we're
    #&Check_IMC_0_Standby  ($Data) if $Key eq 'Check_IMC_0_Standby';
    #&Check_IMC_0_Standby_Prompt  ($Data) if $Key eq 'Check_IMC_0_Standby_Prompt'  ;
    #&Check_IMC_Clock  ($Data) if $Key eq 'IMC_Clock';
    #&Check_IMC_Clock_OS  ($Data) if $Key eq 'IMC_Clock_OS';
    #&Check_IMC_Clock_QNX  ($Data) if $Key eq 'IMC_Clock_QNX';
    #&Get_BootPrompt  ($Data) if $Key eq 'BootPrompt' ;
    #&Get_FistbootIMC  ($Data) if $Key eq 'Get_FistbootIMC';
    #&Get_MAC  ($Data) if $Key eq 'GetMAC' ;
    #&Get_Show_Env  ($Data) if $Key eq 'Show_Env' ;
    #&Get_Memory_size  ($Data) if $Key eq 'Memory_size';
    #&Get_Port_Counter_Det ($Data) if $Key eq 'Port_Counter_Det';
    #&Get_FPD ($Data) if $Key eq 'Get_FPD';
    #&Get_FPD ($Data) if $Key eq 'Get_DOS';
    #&Check_Chassis_FRU_TEST if $Key eq 'Check_Chassis_FRU_TEST';
    #&Check_Chassis_TACH($Key) if $Key =~ /^Check_Chassis_TACH/;
    #&Check_POST_INFO  ($Data) if $Key eq 'POST' ;
    #&Check_Potenita(%Potentia_0_GLC) if $Key eq 'Potentia_0_GLC';
    #&Check_Potenita(%Potentia_1_GLC) if $Key eq 'Potentia_1_GLC';
    #&Check_PSOC() if $Key eq 'PSOC';
    #&Verify_Chassis_LED($Key) if $Key =~ /^Verify_Chassis_LED/;
    #&Check_U200 if $Key eq 'U200';
    #####  XGLC Related ####
    ##Check_CRC32
    #&Check_CRC32  ($Data) if $Key eq 'Check_CRC32';
    #&Check_tftp_size  ($Data) if $Key eq 'Check_tftp_size';
    #&Check_XGLC_CPLD  ($Data) if $Key eq 'Check_XGLC_CPLD';
    #&Check_XGLC_CPLD_Diag  ($Data) if $Key eq 'Check_XGLC_CPLD_Diag';
    #&Check_tftp_Ping  ($Data) if $Key eq 'Check_tftp_Ping';
    #&Check_XGLC_Diag  ($Data) if $Key eq 'Check_XGLC_Diag';
        #&Check_XGLC_voltage  ($Data) if $Key eq 'Check_XGLC_voltage';
        #&Check_XGLC_voltage_Margin_low  ($Data) if $Key eq 'Check_XGLC_voltage_Margin_low';
        #&Check_XGLC_voltage_Margin_high  ($Data) if $Key eq 'Check_XGLC_voltage_Margin_high';
        #&Check_XGLC_BMR  ($Data) if $Key eq 'Check_XGLC_BMR';
        #&Check_XGLC_Thermal ($Data) if $Key eq 'Check_XGLC_Thermal';
    #&Check_bytecompare  ($Data) if $Key eq 'Check_bytecompare';
    #&Check_XGLC_Bench_Links  ($Data) if $Key eq 'Check_XGLC_Bench_Links';
    #&Check_XGLC_I2C  ($Data) if $Key eq 'Check_XGLC_I2C';
    #&Check_GLC_Redundancy  ($Data) if $Key eq 'Check_GLC_Redundancy';
    #&Check_GLC_Slot4_Enable  ($Data) if $Key eq 'Check_GLC_Slot4_Enable';
    #&Detect_SFP_1GIG  ($Data) if $Key eq 'Detect_SFP_1GIG';
    #&Detect_SFP_10GIG  ($Data) if $Key eq 'Detect_SFP_10GIG';
    #&Check_XGLC_HD_Copytime  ($Data) if $Key eq 'Check_XGLC_HD_Copytime';
    #&Get_SFP_HextoASCII  ($Data) if $Key eq 'Get_SFP_HextoASCII';
    #&Get_SFP  ($Data) if $Key eq 'Get_SFP';

    #

#__________________________________________________________________________
def Menu_Exit():
    Globals.Stats['Status'] = 'Exit'
    Stats.Update_All 
    Util.Exit(0,'') 
            #exit;
    return

#________________________________________________________________________

def Menusub_Exit(y):
    Globals.Stats['Status'] = 'Exit'
    Stats.Update_All 
    Util.Exit(0,'')
    Menu_main()
            #exit;
    return
#________________________________________________________________________    
def Menu_Add(Label, Desc, Cmd):  
    # Can't use a hash because of the ordering!...
    Globals.Menu_List.append(Label)
    #    push @Menu_List, &Pad ($Label, 20) . "[$Desc]";
    Globals.Menu_Desc.append(Desc)
    Globals.Menu_Cmd.append(Cmd)
    return

#______________________________________________________________________________________
def Menu_Exec(y):
    print( "Exec\'ing $Menu_List[{}]...\n".format(y))
        #  Added for Sub menus,  need to clear the lists
    Exec (Menu_Cmd [y])    # Find the sub [last arg in Menu_add_...]

    return
#______________________________________________________________________________
def Menu_Show(Menu):    #!!! Move this to

    print("\nTest Options:")
    for i,val in enumerate(Globals.Menu_List) :
        Desc = Globals.Menu_Desc[i-1]
        if not Desc == '' : 
            Desc = "[{}]".format(Desc) 
        print ( "\t{} {} {}\n".format(i+1,Globals.Menu_List[i],Globals.Menu_Desc[i]))
    print("\n")
    y=0
    
    if Globals.Regress == "null" :
        while ( y==0 or y > len(Globals.Menu_List) + 1) :
            y = int(Util.PETC('Select item #?'))
    
    y -=1                # We're base 0, not 1
    
    Globals.TestData['SW_Ver']= Init_Product1.Software_OS_release_gbl
    Globals.TestData['Diag_Ver'] = Init_Product1.diag_ver_gbl
    Globals.Stats['Status'] = 'Started'
    Stats.Update_All
    if Globals.Regress == "null" :
        print("Exec\'ing {}[{}]...\n".format(Globals.Menu_Cmd[y],y))
        #locals()[Globals.Menu_Cmd[y]]()
        #try:
        if Globals.Menu1 == '' :
            if Globals.Debug: print ("Exc Func Menu.{}".format(Globals.Menu_Cmd[y]+"()"))
            method = eval(Globals.Menu_Cmd[y])
            method()            
                #func = getattr(Menu,Globals.Menu_Cmd[y],"Menu_main")
            #else :
                #method = eval(Menu,Globals.Menu1)
                #method()            
                ##func = getattr(Menu,Globals.Menu1)
                
        #except AttributeError:
            #print ('function not found "%s" (%s)' % (Globals.Menu_Cmd[y], y))
            ##Run_Prog_Example()
        #else:
            #method = eval("Menu_main")
            #method()
        #&Exec ($Menu_Cmd [$y]);     # Find the sub [last arg in Menu_add_...]
    else:
        print("Regressing\'ing {}...\n".format(Globals.Regress+"()"))
        method = eval(Globals.Regress)
        method()       
    return

#_____________________________________________________________________________

def Menu_main():
    #Init_Product1.Globals_Product1;
    Globals.Menu_List = []
    Globals.Menu_Desc = []
    Globals.Menu_Cmd  = []
    if (Globals.Debug_UUT == 1 or Globals.Development == 1) : Globals.User_Level = 0
    Globals.CmdFilePath = os.path.join(Globals.GP_Path , "cmdfiles","SSX","Gen1")
    #use Init_SSX;  # <- Stoke Specific Globals defined here
    #Init_Product1.Globals_Product1

    Menu_Add ('Exit', '', 'Menu_Exit')
    if (Globals.GlobalVar['User_Level'] > 1  or Globals.User_Level == 0): Menu_Add ('CMTEST1', 'CMTEST1', 'CMtest1_Menu_main') 
    if (Globals.GlobalVar['User_Level'] > 1  or Globals.User_Level == 0): Menu_Add ('CMTEST2', 'CMTEST2', 'CMtest2_Menu_main') 

    if ( Globals.Menu1 != '') : 
        Menu_Add ('Test', 'Regression test vehicle', 'Run_Test')

    Menu_Show ( 'Main' )
  
#______________________________________________________________________________________

def CMtest1_Menu_main():
    #Globals_Product1;
    Globals.Menu_List = []
    Globals.Menu_Desc = []
    Globals.Menu_Cmd  = []
    if (Globals.Debug_UUT == 1 or Globals.Development == 1) : Globals.User_Level = 0
    Globals.CmdFilePath = os.path.join(Globals.GP_Path , "cmdfiles","SSX","Gen1")
    #use Init_SSX;  # <- Stoke Specific Globals defined here
    #Globals_Product1

    Menu_Add ('Exit', '', 'Menu_Exit');
    if Globals.GlobalVar['User_Level'] > 1  or Globals.User_Level == 0: Menu_Add ('Gen 1', 'Test 1 Gig interface product', 'Cmtest1_Menu1') 
    if Globals.GlobalVar['User_Level'] > 1  or Globals.User_Level == 0: Menu_Add ('Gen 2', 'Test 10 Gig interface product', 'Cmtest1_Menu2') 

    if ( Globals.Menu1 != '') : 
        Menu_Add ('Test', 'Regression test vehicle', 'Run_Test')

    Menu_Show ( 'Main' )
    return()
#__________________________________________________________________________
def CMtest2_Menu_main():
    #Globals_Product1;
    Globals.Menu_List = []
    Globals.Menu_Desc = []
    Globals.Menu_Cmd  = []
    if (Globals.Debug_UUT == 1 or Globals.Development == 1) : Globals.User_Level = 0
    Globals.CmdFilePath = os.path.join(Globals.GP_Path , "cmdfiles","SSX","Gen1")
    #use Init_SSX;  # <- Stoke Specific Globals defined here
    #Globals_Product1

    Menu_Add ('Exit', '', 'Menu_Exit');
    if Globals.GlobalVar['User_Level'] > 1  or Globals.User_Level == 0: Menu_Add ('Gen 1', 'Test 1 Gig interface product', 'Cmtest1_Menu1') 
    if Globals.GlobalVar['User_Level'] > 1  or Globals.User_Level == 0: Menu_Add ('Gen 2', 'Test 10 Gig interface product', 'Cmtest1_Menu2') 

    if ( Globals.Menu1 != '') : 
        Menu_Add ('Test', 'Regression test vehicle', 'Run_Test')

    Menu_Show ( 'Main' )
    return()
#__________________________________________________________________________
def Cmtest1_Menu1():
    Globals.Menu_List = []
    Globals.Menu_Desc = []
    Globals.Menu_Cmd  = []
    if (Globals.Debug_UUT == 1 or Globals.Development == 1) : User_Level = 0 
    Menu_Add ('Exit', '', 'Menu_main')
    Globals.CmdFilePath = os.path.join(Globals.GP_Path , "cmdfiles","SSX","Gen1")
    if Globals.GlobalVar['User_Level'] > 1  or Globals.User_Level == 0 : Menu_Add ('Bench Program', 'Initial PCB bringup Programming', 'Run_Prog_Example')
    if Globals.GlobalVar['User_Level'] > 2  or Globals.User_Level == 0 : Menu_Add ('Bench Test', 'Initial PCB bringup', 'Run_Bench_Test_Example') 
    if Globals.GlobalVar['User_Level'] > 3 or Globals.User_Level == 0: Menu_Add ('Chassis Pre BI', 'Chassis Test IMC and GLC Pre-BI', 'Run_Chassis_Test_Pre_BI_Example') 
    if Globals.GlobalVar['User_Level'] > 4 or Globals.User_Level == 0: Menu_Add ('Chassis BI', '12 Hour BI test', 'Run_Chassis_BI_Example') 
    if Globals.GlobalVar['User_Level'] > 5 or Globals.User_Level == 0: Menu_Add ('Chassis POST BI', 'Chassis Test IMC and GLC POST-BI', 'Run_Chassis_Test_Post_BI_Example') 
    if Globals.GlobalVar['User_Level'] > 7 or Globals.User_Level == 0: Menu_Add ('Chassis Config', 'Chassis Configuration', 'Run_Chassis_Config_Example') 
    if Globals.GlobalVar['User_Level'] > 7 or Globals.User_Level == 0: Menu_Add ('Chassis Extended', 'Long term system tests', 'Run_Chassis_Extended_Example') 
    if Globals.GlobalVar['User_Level'] > 7 or Globals.User_Level == 0: Menu_Add ('Chassis ORT', 'MTBF Validation', 'Run_Chassis_ORT_Example') 
    if Globals.GlobalVar['User_Level'] > 7 or Globals.User_Level == 0: Menu_Add ('Chassis Program', 'Chassis Program', 'Run_Chassis_Prog_Example')
    if Globals.GlobalVar['User_Level'] > 7 or Globals.User_Level == 0: Menu_Add ('Chassis TEST Pre BI', 'Chassis TEST', 'Run_Chassis_TEST_PRE_Example') 
    if Globals.GlobalVar['User_Level'] > 7 or Globals.User_Level == 0: Menu_Add ('Chassis TEST Post BIProgram', 'Chassis TEST', 'Run_Chassis_TEST_POST_Example')
    if Globals.GlobalVar['User_Level'] > 7 or Globals.User_Level == 0: Menu_Add ('Chassis TEST Functionl Full', 'Chassis TEST', 'Run_Chassis_Functional_Full_Example') 
    if Globals.GlobalVar['User_Level'] > 7 or Globals.User_Level == 0: Menu_Add ('Order Entry', 'Enter Sales Order', 'Run_GetOrder_Example')
    if Globals.GlobalVar['User_Level'] > 7 or Globals.User_Level == 0: Menu_Add ('Debug', 'Debug Sub menu', 'Cmtest1_Debug_Menu1') 
    
    if ( Globals.Menu1 != ''):
        Menu_Add ('Test', 'Regression test vehicle', 'Run_Test');
#        &Menu_Add ('Test_ssh', 'Regression test vehicle', 'Run_Test_ssh');

    Menu_Show ( 'Main' )
 
    return()

#__________________________________________________________________________

def CMtest1_Debug_Menu1():
    Globals.Menu_List = []
    Globals.Menu_Desc = []
    Globals.Menu_Cmd  = []
    if (Globals.Debug_UUT == 1 or Globals.Development == 1) : User_Level = 0
    Globals.CmdFilePath = os.path.join(Globals.GP_Path , "cmdfiles","SSX","Gen1")
    Menu_Add ('Exit', '', 'Menu_main');
    if Globals.GlobalVar['User_Level'] == 0: Menu_Add ('Debug', 'Temporary', "Run_Debug") 
    if Globals.GlobalVar['User_Level'] == 0: Menu_Add ('Debug', 'Power Cycle GLC on Bench', "Run_Debug_GLC_Bench_Power") 
    if Globals.GlobalVar['User_Level'] == 0: Menu_Add ('Debug', 'Power Cycle IMC on Bench', "Run_Debug_IMC_Bench_Power")  
    if Globals.GlobalVar['User_Level'] == 0: Menu_Add ('Debug', 'BI Debug', "Run_Debug_Chassis_BI")  

    if ( Globals.Menu1 != '') :
        Menu_Add ('Test', 'Regression test vehicle', 'Run_Test');

    Menu_Show ( 'Main' );

    return()

#__________________________________________________________________________

def Cmtest1_Menu2 ():   # Gen 2 boards
    Globals.Menu_List = []
    Globals.Menu_Desc = []
    Globals.Menu_Cmd  = []
    Globals.CmdFilePath = os.path.join(Globals.GP_Path , "cmdfiles","SSX","Gen2")
    if (Globals.Debug_UUT == 1 or Globals.Development == 1) : User_Level = 0 
    Menu_Add ('Exit', '', 'Menu_main');
    if Globals.GlobalVar['User_Level'] > 1  or Globals.User_Level == 0: Menu_Add ('Bench Program XGLC', 'Initial PCB bringup Programming', 'Run_Prog2_Example')
    if Globals.GlobalVar['User_Level'] > 2  or Globals.User_Level == 0: Menu_Add ('Bench Test XGLC', 'Initial PCB bringup', 'Run_Bench_Test2_Example') 
    if Globals.GlobalVar['User_Level'] > 3  or Globals.User_Level == 0: Menu_Add ('Chassis Pre BI XGLC', 'Chassis Test IMC and XGLC Pre-BI', 'Run_Chassis_Test_Pre_BI_XGLC_Example') 
    if Globals.GlobalVar['User_Level'] > 4  or Globals.User_Level == 0: Menu_Add ('Chassis BI XGLC', 'Chassis Test IMC and XGLC BI', 'Run_Chassis_Test_BI_XGLC_Example') 
    if Globals.GlobalVar['User_Level'] > 5  or Globals.User_Level == 0: Menu_Add ('Chassis POST BI XGLC', 'Chassis Test IMC and XGLC POST-BI', 'Run_Chassis_Test_Post_BI_XGLC_Example') 
    if Globals.GlobalVar['User_Level'] > 6  or Globals.User_Level == 0: Menu_Add ('Chassis Config XGLC', 'Chassis Test Config', 'Run_Chassis_Test_Config_XGLC_Example') 
    if Globals.GlobalVar['User_Level'] > 7  or Globals.User_Level == 0: Menu_Add ('Chassis Extended XGLC', 'Long term system tests', 'Run_Chassis_Extended_XGLC_Example') 
    if Globals.GlobalVar['User_Level'] > 7  or Globals.User_Level == 0: Menu_Add ('Chassis ORT XGLC', 'Long term system tests', 'Run_Chassis_ORT_XGLC_Example') 
    if Globals.GlobalVar['User_Level'] > 7  or Globals.User_Level == 0: Menu_Add ('Chassis Program', 'Program chassis', 'Run_Chassis_Prog_gen2_Example') 
    if Globals.GlobalVar['User_Level'] > 7  or Globals.User_Level == 0: Menu_Add ('Chassis TEST Pre BI', 'Chassis TEST', 'Run_Chassis_TEST_PRE_gen2_Example') 
    if Globals.GlobalVar['User_Level'] > 7  or Globals.User_Level == 0: Menu_Add ('Chassis TEST Post BIProgram', 'Chassis TEST', 'Run_Chassis_TEST_POST_gen2_Example') 
    if Globals.GlobalVar['User_Level'] > 7  or Globals.User_Level == 0: Menu_Add ('Debug Gen 2', 'Debug Sub menu', '_Debug_Menu2_Example') 

    if ( Globals.Menu1 != ''):
        Menu_Add ('Test', 'Regression test vehicle', 'Run_Test');
#        &Menu_Add ('Test_ssh', 'Regression test vehicle', 'Run_Test_ssh');

    Menu_Show ( 'Main' )

    return()

#_______________________________________________________________________________

def Cmtest1_Debug_Menu2():   # Gen 2 boards
    Globals.Menu_List = []
    Globals.Menu_Desc = []
    Globals.Menu_Cmd  = []
    Globals.CmdFilePath = os.path.join(Globals.GP_Path , "cmdfiles","SSX","Gen2")
    if (Globals.Debug_UUT == 1 or Globals.Development == 1): Globals.User_Level = 0 
    Menu_Add ('Exit', '', 'Menu_main')
    if Globals.GlobalVar['User_Level'] > 5  or Globals.User_Level == 0: Menu_Add ('Debug Bench Test XGLC', 'Debug', 'Run_Bench_Debug')
    if Globals.GlobalVar['User_Level'] > 1  or Globals.User_Level == 0: Menu_Add ('Bench Flash XGLC', 'Flash Programming', 'Run_Prog_Flash2') 
    if Globals.GlobalVar['User_Level'] > 5  or Globals.User_Level == 0: Menu_Add ('StokeOS Reload', 'StokeOS startup Stability', 'Run_Debug_XGLC_StokeOSReload')
    if Globals.GlobalVar['User_Level'] > 5  or Globals.User_Level == 0: Menu_Add ('Debug Temp', 'Debug XGLC', 'Run_Debug_XGLC') 
    if Globals.GlobalVar['User_Level'] > 5  or Globals.User_Level == 0: Menu_Add ('Debug', 'Debug Reboot XLP', 'Run_Debug_Reboot_XLP')
    if Globals.GlobalVar['User_Level'] > 5  or Globals.User_Level == 0: Menu_Add ('Debug', 'Debug Power Cycle XGLC', 'Run_Debug_Bench_XGLC_PowerCycle') 
    if Globals.GlobalVar['User_Level'] > 5  or Globals.User_Level == 0: Menu_Add ('Debug', 'Debug Power Cycle XGLC Selct margin', 'Run_Debug_Bench_XGLC_PowerCycle_Select_Margin') 
    if Globals.GlobalVar['User_Level'] > 5  or Globals.User_Level == 0: Menu_Add ('Debug', 'Debug Power Cycle XGLC GPP DRAM', 'Run_Debug_Bench_XGLC_PowerCycle_GPP_DRAM') 
    if Globals.GlobalVar['User_Level'] > 5  or Globals.User_Level == 0: Menu_Add ('Debug', 'Debug Reboot XGLC', 'Run_Debug_Bench_XGLC_Reboot') 
    if Globals.GlobalVar['User_Level'] > 5  or Globals.User_Level == 0: Menu_Add ('Debug', 'Debug XGLC Flashimage', 'Run_Debug_Flashimage_XGLC') 
    if Globals.GlobalVar['User_Level'] > 5  or Globals.User_Level == 0: Menu_Add ('Debug', 'Debug', 'Run_Debug_Gen2') 

    if (Globals.Menu1 != '') :
        Menu_Add ('Test', 'Regression test vehicle', 'Run_Test');
#        &Menu_Add ('Test_ssh', 'Regression test vehicle', 'Run_Test_ssh');

    Menu_Show ( 'Main' )

    return()

#__________________________________________________________________________
def Run_Debug_GLC_Bench_Power_Example():
            #caller(0))[3];

    Cmd_File = os.path.join(Globals.CmdFilePath,"Debug_Bench_GLC_Powercyle.dat");
    print("Debug")
    Globals.TestData['TID'] = 'DEBUG'
    Globals.Exit_On_Timeout = 1

    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Global.Cmd_File );

    Final()
    returm(0)
#__________________________________________________________________________
def Run_Debug_IMC_Bench_Power_Example():
            #caller(0))[3];

    Cmd_File = os.path.join(Globals.CmdFilePath,"Debug_Bench_IMC_Powercyle.dat");
    print("Debug")
    Globals.TestData['TID'] = 'DEBUG'
    Globals.Exit_On_Timeout = 1
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Global.Cmd_File );
    Final()
    returm(0)
#__________________________________________________________________________
def Run_Debug_Chassis_BI_Example():

    Cmd_File = os.path.join(Globals.CmdFilePath,"Debug_Chassis_BI.dat")
    print("Debug")
    Globals.TestData['TID'] = 'DEBUG'
    Globals.Exit_On_Timeout = 1
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Global.Cmd_File );
    Final()
    returm(0)
#__________________________________________________________________________
def Run_GetOrder_Example():

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Order_entry.dat")

    Globals.TestData['TID']= 'SO'
    Globals.Exit_On_Timeout = 0
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File );

    Final()
    return()
#__________________________________________________________________________
def Run_Chassis_Extended_Example():

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_Extended.dat")
    Globals.TestData['TID'] = 'EXT'
    Globals.Exit_On_Timeout = 0
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File );
    Final()
    return()

#__________________________________________________________________________
def Run_Chassis_TEST_PRE_Example():
    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_test.dat")


    Globals.TestData['TID'] = 'CHP'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )
    Final()
    return()
#__________________________________________________________________________
def Run_Chassis_TEST_PRE_gen2_Example():
    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_test_gen2.dat")

    Globals.TestData['TID'] = 'CHP'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________
def Run_Chassis_TEST_POST_Example():
    Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_test.dat")

    Globals.TestData['TID'] = 'CHF'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File );
    Final()
    return()
#__________________________________________________________________________
def Run_Chassis_TEST_POST_gen2_Example():
    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_test_gen2.dat")
    Globals.TestData['TID'] = 'CHF'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File );
    Final()
    return()
#__________________________________________________________________________
def Run_Chassis_Config_Example():

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_Config.dat")
    TestData['TID'] = 'SHIP'
    Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File );
    Final()
    return()
#__________________________________________________________________________
def Run_Chassis_Prog_Example():

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_Prog.dat")
    Globals.TestData['TID'] = 'Program'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stokee
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )
    Final()
    return()

#__________________________________________________________________________
def Run_Chassis_Prog_gen2_Example():

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_Prog_gen2.dat")
    Globals.TestData['TID'] = 'Program'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File );

    Final()
    return()
#__________________________________________________________________________
def Run_Chassis_Functional_Full_Example():
    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_Functional_Full.dat");
    Globals.TestData['TID'] = 'CHA'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )
    Final()
    return()
#__________________________________________________________________________

def Run_Chassis_Test_Post_BI_Example():
    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_Post_BI.dat")
    Globals.TestData['TID'] = 'FST'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________
def Run_Chassis_BI_Example():
    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_BI.dat")
    TestData['TID'] = 'BI'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )
    Final()
    return()
#__________________________________________________________________________
def Run_Chassis_ORT_Example():
    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_ORT.dat")
    Globals.TestData['TID'] = 'ORT'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globasl.ComPort, Globals.Cmd_File )
    Final()
    return()
#__________________________________________________________________________
def Run_Chassis_Test_Pre_BI_Example():

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_Pre_BI.dat");

    Globals.TestData['TID'] = 'IST'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globsl.Cmd_File )
    Final()
    final()
#__________________________________________________________________________
def Run_Bench_Test_Example():
    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Bench.dat")
    Globals.TestData['TID'] = 'Bench'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stokee
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________

def Run_Prog_Example():      #GLC Generation

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Bench_Prog.dat")
    Globals.TestData['TID'] = 'Program';
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()

#__________________________________________________________________________
def Run_Prog2_Example():          #XGLC Generation(gen2)

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Bench_Prog.dat")
    print ("Command File path:  "+Globals.CmdFilePath)
    Globals.Baud = "115200"    #  Gen 2 currently runs at 115200 buad
    Globals.TestData['TID'] = 'Program'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()

#__________________________________________________________________________
def Run_Prog_Flash2_Example():         #XGLC Generation(gen2)

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Bench_Prog_Flash.dat")
    print ("Command File path:  $CmdFilePath\n");
    Globals.Baud = "115200"    #  Gen 2 currently runs at 115200 buad
    Globals.TestData['TID'] = 'DEBUG'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()

#__________________________________________________________________________
def Run_Bench_Test2_Example():         #XGLC Generation(gen2)

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Bench.dat")
    print ("Command File path:  "+Globals.CmdFilePath)
    Globals.Baud = "115200"    #  Gen 2 currently runs at 115200 buad
    Globals.TestData['TID'] = 'Bench'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________
def Run_Chassis_Test_Pre_BI_XGLC_Example(): 

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_Pre_BI_XGLC.dat")
    Globals.TestData['TID'] = 'IST'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________

def Run_Chassis_Test_BI_XGLC_Example(): 

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_BI_XGLC.dat")
    Globals.TestData['TID'] = 'BI'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________

def Run_Chassis_Test_Post_BI_XGLC_Example(): 

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_Post_BI_XGLC.dat")
    Globals.TestData['TID'] = 'FST'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )
    Final()
    return()
#__________________________________________________________________________

def Run_Chassis_Test_Config_XGLC_Example(): 

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_Config_XGLC.dat")
    Globals.TestData['TID'] = 'SHIP'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________

def Run_Chassis_Extended_XGLC_Example(): 

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_Extended_XGLC.dat")
    Globals.TestData['TID'] = 'EXT'
    Globals.Exit_On_Timeout = 0;
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________

def Run_Chassis_ORT_XGLC_Example():     #xglc

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Chassis_ORT_XGLC.dat")
    Globals.TestData['TID'] = 'ORT'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________
def Run_Bench_Debug_Example():         #XGLC Generation(gen2)

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Debug_Bench.dat")
    print ("Command File path:  $CmdFilePath\n");
    Globals.Baud = "115200"    #  Gen 2 currently runs at 115200 buad
    Globals.TestData['TID'] = 'DEBUG'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________

def Run_Debug_XGLC_StokeOSReload_Example(): 

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Debug_Boot_StokeOS_Loop.dat")
    Globals.TestData['TID'] = 'DEBUG';
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
    #__________________________________________________________________________
#Run_Debug_Reboot_XLP
def Run_Debug_Bench_XGLC_PowerCycle_Example(): 

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Debug_Bench_XGLC_PowerCycle.dat");
    Globals.Baud = "115200"    #  Gen 2 currently runs at 115200 buad
    Globals.TestData['TID'] = 'DEBUG'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
    #__________________________________________________________________________
    #Run_Debug_Reboot_XLP
def Run_Debug_Bench_XGLC_PowerCycle_Select_Margin_Example(): 

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Debug_Bench_XGLC_PowerCycle_select_margin.dat");
    Globals.Baud = "115200";    #  Gen 2 currently runs at 115200 buad
    Globals.TestData['TID'] = 'DEBUG'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
    #__________________________________________________________________________
#Run_Debug_Reboot_XLP
def Run_Debug_Bench_XGLC_PowerCycle_GPP_DRAM_Example(): 

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Debug_Bench_XGLC_PowerCycle_GPP_DRAM.dat");
    Globals.Baud = "115200";    #  Gen 2 currently runs at 115200 buad
    Globals.TestData['TID'] = 'DEBUG'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________
#Run_Debug_Reboot_XLP
def Run_Debug_Bench_XGLC_Reboot_Example(): 

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Debug_Bench_XGLC_Reboot.dat");
    Globals.Baud = "115200";    #  Gen 2 currently runs at 115200 buad
    Globals.TestData['TID'] = 'DEBUG'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________
def Run_Debug_Flashimage_XGLC_Example(): 

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Debug_Flashimage_XGLC.dat");
    Globals.Baud = "115200";    #  Gen 2 currently runs at 115200 buad
    Globals.TestData['TID'] = 'DEBUG'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________
def Run_Debug_Gen2_Example(): 

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Debug.dat");
    Globals.Baud = "9600"    #  Gen 2 currently runs at 115200 buad
    Globals.TestData['TID'] = 'DEBUG'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________
#Run_Debug_Reboot_XLP
def Run_Debug_Reboot_XLP_Example(): 

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Debug_XLP_Reboot.dat");
    Globals.Baud = "115200"    #  Gen 2 currently runs at 115200 buad
    Globals.TestData['TID'] = 'DEBUG'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________
def Run_Debug_XGLC_Example(): 

    Globals.Cmd_File = os.path.join(Globals.CmdFilePath,"Debug.dat");
    Globals.Baud = "9600"    #  Gen 2 currently runs at 115200 buad
    Globals.TestData['TID'] = 'DEBUG'
    Globals.Exit_On_Timeout = 1
    Logs.XML_Header() # Added JSW - Stoke
    Connect.Cmd_Expect( 'Serial', Globals.ComPort, Globals.Cmd_File )

    Final()
    return()
#__________________________________________________________________________

