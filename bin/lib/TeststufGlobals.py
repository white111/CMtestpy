#!/usr/bin/python
################################################################################
#
# Module:     Globals.py
#
# Author:      Joe White
#			
# Descr:      Define Cmtest globals
#
# Version:    (See below) $Id: Globals.pm,v 1.9 2011/12/12 22:54:28 joe Exp $
#
# Changes:    Conversion from Globals.pm perl to Python
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
#            Copyright (c) 2005-2012 Stoke. All rights reserved.
#            Copyright (c) 2017 Joe White. All rights reserved.
#
################################################################################
VER= 'v0.1 5/4/2017'; #Conversion to Python
CVS_VER = ' [ CVS: $Id: Globals.pm,v 1.9 2011/12/12 22:54:28 joe Exp $ ]';
#CMtestVersion['Globals'] = VER + CVS_VER;
#______________________________________________________________________________


print ("Setting globals")

global Stats_Path; 
Stats_Path      = 'jack'
print(Stats_Path)

#__________________________________________________________________________
1;
