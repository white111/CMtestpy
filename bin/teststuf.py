#!/usr/bin/python
"Sources parametric data from a file like:"
"logFile = /tmp/log.txt"
"Returns the # found"
File=r"m:\python\CMtestpy\bin\cfgfiles\testctrl.defaults.cfg"
try:
    print("Read_Cfg_File trying to open: %s" % File)
    with open (File, 'r') as fh :
        print("Read_Cfg_File opened: %s" % File)
        for line in fh:
            print("Read_Cfg_File line: %s" % line)
            yield line
            #if re.search("^$", line): next # Blank line
            #chomp()
            #Param = re.sub("\s+", '', Param)    #Remove any white spaces
            #Data  = re.sub("^\s+", '', Data)    #Remove any leading/trailing white spaces
            #Data  = re.sub("\s+$", '', Data)    #Remove any leading/trailing white spaces
            #if Param == '' : next 
            #if Param == 'CmdFilePath' : next 
            #if re.search("\w+\s*\[\d+\]",Param) : 
                #Param1,Param2 = Data.split()
                #Globals.GlobalVar[Param1][Param2] = Data
            #else :
                    #Globals.GlobalVar[Param] = Data
except:
    print("Read_Cfg_File failed to read %s" % File)
   

fh.close()

