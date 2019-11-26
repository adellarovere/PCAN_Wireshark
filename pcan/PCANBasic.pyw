######################################################################
#  PCAN-Basic Example
#
#  ~~~~~~~~~~~~
#
#  ------------------------------------------------------------------
#  Author : Keneth Wagner
#  Language: Python 2.6
#  ------------------------------------------------------------------
#
#  Copyright (C) 1999-2011  PEAK-System Technik GmbH, Darmstadt
######################################################################

from PCANBasic import *        ## PCAN-Basic library import

## Imports for UI
##
from Tkinter import *          ## TK UI library
import Tix                     ## TK extensions library

import tkMessageBox            ## Simple-Messages library
import traceback               ## Error-Tracing library

import string                  ## String functions
import tkFont                  ## Font-Management library

import time                    ## Time-related library
import threading               ## Threading-based Timer library

TCL_DONT_WAIT           = 1<<1
TCL_WINDOW_EVENTS       = 1<<2
TCL_FILE_EVENTS         = 1<<3
TCL_TIMER_EVENTS        = 1<<4
TCL_IDLE_EVENTS         = 1<<5
TCL_ALL_EVENTS          = 0


COL_TYPE = 0
COL_ID = 1
COL_LENGTH = 2
COL_DATA = 3
COL_COUNT = 4
COL_TIME = 5

###*****************************************************************
### Message Status structure used to show CAN Messages
### in a ListView
###*****************************************************************
class MessageStatus:
    def __init__(self, canMsg = TPCANMsg(), canTimestamp = TPCANTimestamp(), listIndex = -1):
        self.__m_Msg = canMsg
        self.__m_TimeStamp = canTimestamp
        self.__m_iIndex = listIndex
        self.__m_iCount = 1

    def getCANMessage(self):
        return self.__m_Msg

    def getTimestamp(self):
        return self.__m_TimeStamp

    def getPosition(self):
        return self.__m_iIndex

    def getCount(self):
        return self.__m_iCount

    def Actualize(self,canMsg,canTimestamp):
        self.__m_Msg = canMsg
        self.__m_TimeStamp = canTimestamp        
        self.__m_iCount = self.__m_iCount + 1
###*****************************************************************




###*****************************************************************
### PCAN-basic Example app
###*****************************************************************
class PCANBasicExample:
    ## Constructor
    ##
    def __init__(self, parent):
        # Parent's configuration       
        self.m_Parent = parent
        self.m_Parent.wm_title("PCAN-Basic Example")
        self.m_Parent.resizable(False,False)
        self.m_Parent.protocol("WM_DELETE_WINDOW",self.Form_OnClosing)
               
        # Frame's configuration
        self.m_Frame =Frame(self.m_Parent)
        self.m_Frame.grid(row=0, column=0, padx=5, pady=2, sticky="nwes")

        # Example's configuration
        self.InitializeBasicComponents()
        self.CenterTheWindow()
        self.InitializeWidgets()
        self.ConfigureLogFile()

        self.SetConnectionStatus(False)


    ## Destructor
    ##
    def destroy (self):
        self.m_Parent.destroy()        

        
    ## Message loop
    ##
    def loop(self):
        # This is an explict replacement for _tkinter mainloop()
        # It lets catch keyboard interrupts easier, and avoids
        # the 20 msec. dead sleep() which burns a constant CPU.
        while self.exit < 0:
            # There are 2 whiles here. The outer one lets you continue
            # after a ^C interrupt.
            try:
                # This is the replacement for _tkinter mainloop()
                # It blocks waiting for the next Tcl event using select.
                while self.exit < 0:
                    self.m_Parent.tk.dooneevent(TCL_ALL_EVENTS)
            except SystemExit:
                # Tkinter uses SystemExit to exit
                #print 'Exit'
                self.exit = 1
                return
            except KeyboardInterrupt:
                if tkMessageBox.askquestion ('Interrupt', 'Really Quit?') == 'yes':
                    # self.tk.eval('exit')
                    self.exit = 1
                    return
                continue
            except:
                # Otherwise it's some other error
                t, v, tb = sys.exc_info()
                text = ""
                for line in traceback.format_exception(t,v,tb):
                    text += line + '\n'
                try: tkMessageBox.showerror ('Error', text)
                except: pass
                self.exit = 1
                raise SystemExit, 1            

        
################################################################################################################################################
### Help functions
################################################################################################################################################

    ## Initializes app members
    ##
    def InitializeBasicComponents(self):
        self.m_Width =760
        self.m_Height = 600
        self.exit = -1        
        self.m_objPCANBasic = PCANBasic()
        self.m_PcanHandle = PCAN_NONEBUS
        self.m_LastMsgsList = []
        
        self.m_CHANNELS = {'PCAN_DNGBUS1':PCAN_DNGBUS1, 'PCAN_PCCBUS1':PCAN_PCCBUS1, 'PCAN_PCCBUS2':PCAN_PCCBUS2, 'PCAN_ISABUS1':PCAN_ISABUS1, 
                           'PCAN_ISABUS2':PCAN_ISABUS2, 'PCAN_ISABUS3':PCAN_ISABUS3, 'PCAN_ISABUS4':PCAN_ISABUS4, 'PCAN_ISABUS5':PCAN_ISABUS5,
                           'PCAN_ISABUS6':PCAN_ISABUS6, 'PCAN_ISABUS7':PCAN_ISABUS7, 'PCAN_ISABUS8':PCAN_ISABUS8, 'PCAN_PCIBUS1':PCAN_PCIBUS1,
                           'PCAN_PCIBUS2':PCAN_PCIBUS2, 'PCAN_PCIBUS3':PCAN_PCIBUS3, 'PCAN_PCIBUS4':PCAN_PCIBUS4, 'PCAN_PCIBUS5':PCAN_PCIBUS5,
                           'PCAN_PCIBUS6':PCAN_PCIBUS6, 'PCAN_PCIBUS7':PCAN_PCIBUS7, 'PCAN_PCIBUS8':PCAN_PCIBUS8, 'PCAN_USBBUS1':PCAN_USBBUS1,
                           'PCAN_USBBUS2':PCAN_USBBUS2, 'PCAN_USBBUS3':PCAN_USBBUS3, 'PCAN_USBBUS4':PCAN_USBBUS4, 'PCAN_USBBUS5':PCAN_USBBUS5,
                           'PCAN_USBBUS6':PCAN_USBBUS6, 'PCAN_USBBUS7':PCAN_USBBUS7, 'PCAN_USBBUS8':PCAN_USBBUS8}

        self.m_BAUDRATES = {'1 MBit/sec':PCAN_BAUD_1M, '800 kBit/sec':PCAN_BAUD_800K, '500 kBit/sec':PCAN_BAUD_500K, '250 kBit/sec':PCAN_BAUD_250K,
                            '125 kBit/sec':PCAN_BAUD_125K, '100 kBit/sec':PCAN_BAUD_100K, '95,238 kBit/sec':PCAN_BAUD_95K, '83,333 kBit/sec':PCAN_BAUD_83K,
                            '50 kBit/sec':PCAN_BAUD_50K, '47,619 kBit/sec':PCAN_BAUD_47K, '33,333 kBit/sec':PCAN_BAUD_33K, '20 kBit/sec':PCAN_BAUD_20K,
                            '10 kBit/sec':PCAN_BAUD_10K, '5 kBit/sec':PCAN_BAUD_5K}

        self.m_HWTYPES = {'ISA-82C200':PCAN_TYPE_ISA, 'ISA-SJA1000':PCAN_TYPE_ISA_SJA, 'ISA-PHYTEC':PCAN_TYPE_ISA_PHYTEC, 'DNG-82C200':PCAN_TYPE_DNG,
                         'DNG-82C200 EPP':PCAN_TYPE_DNG_EPP, 'DNG-SJA1000':PCAN_TYPE_DNG_SJA, 'DNG-SJA1000 EPP':PCAN_TYPE_DNG_SJA_EPP}

        self.m_IOPORTS = {'0100':0x100, '0120':0x120, '0140':0x140, '0200':0x200, '0220':0x220, '0240':0x240, '0260':0x260, '0278':0x278, 
                          '0280':0x280, '02A0':0x2A0, '02C0':0x2C0, '02E0':0x2E0, '02E8':0x2E8, '02F8':0x2F8, '0300':0x300, '0320':0x320,
                          '0340':0x340, '0360':0x360, '0378':0x378, '0380':0x380, '03BC':0x3BC, '03E0':0x3E0, '03E8':0x3E8, '03F8':0x3F8}

        self.m_INTERRUPTS = {'3':3, '4':4, '5':5, '7':7, '9':9, '10':10, '11':11, '12':12, '15':15}

        self.m_PARAMETERS = {'USBs Device Number':PCAN_DEVICE_NUMBER, 'USB/PC-Cards 5V Power':PCAN_5VOLTS_POWER,
                             'Auto-reset on BUS-OFF':PCAN_BUSOFF_AUTORESET, 'CAN Listen-Only':PCAN_LISTEN_ONLY,
                             'Debugs Log':PCAN_LOG_STATUS,'Receive Status':PCAN_RECEIVE_STATUS,
                             'CAN Controller Number':PCAN_CONTROLLER_NUMBER}

        
    ## Initializes the complete UI
    ##
    def InitializeWidgets(self):
        # Connection groupbox
        self.gbConnection = LabelFrame(self.m_Frame, height=70, width = 745, text=" Connection ")
        self.gbConnection.grid_propagate(0)
        self.gbConnection.grid(row=0, column = 0, padx=2, pady=2)
        self.InitializeConnectionWidgets()
        
        ## Message Filtering groupbox
        self.gbMsgFilter = LabelFrame(self.m_Frame, height=70, width = 745, text=" Message Filtering ")
        self.gbMsgFilter.grid_propagate(0)
        self.gbMsgFilter.grid(row=1, column = 0, padx=2, pady=2)
        self.InitializeFilteringWidgets()

        ## Configuration Parameters groupbox
        self.gbParameters = LabelFrame(self.m_Frame, height=70, width = 745, text=" Configuration Parameters ")
        self.gbParameters.grid_propagate(0)
        self.gbParameters.grid(row=2, column = 0, padx=2, pady=2)
        self.InitializeConfigurationWidgets()

        ## Messages Reading groupbox
        self.gbReading = LabelFrame(self.m_Frame, height=150, width = 745, text=" Messages Reading ")
        self.gbReading.grid_propagate(0)
        self.gbReading.grid(row=3, column = 0, padx=2, pady=2)
        self.InitializeReadingWidgets()

        ## Messages Writing groupbox
        self.gbWriting = LabelFrame(self.m_Frame, height=70, width = 745, text=" Write Messages ")
        self.gbWriting.grid_propagate(0)
        self.gbWriting.grid(row=4, column = 0, padx=2, pady=2)
        self.InitializeWritingWidgets()

        ## Information groupbox
        self.gbInfo = LabelFrame(self.m_Frame, height=140, width = 745, text=" Information ")
        self.gbInfo.grid_propagate(0)
        self.gbInfo.grid(row=5, column = 0, padx=2, pady=2)
        self.InitializeInformationWidgets()
        
        self.btnHwRefresh.invoke()


    ## Initializes controls and variables in the groupbox "Connection"
    ##
    def InitializeConnectionWidgets(self):
        Label(self.gbConnection, anchor=W, text="Hardware:").grid(row=0, sticky=W)
        self.cbbChannel = Tix.ComboBox(self.gbConnection, command=self.cbbChannel_SelectedIndexChanged)
        self.cbbChannel.subwidget('entry')['width'] = 16
        self.cbbChannel.subwidget('listbox')['width'] = 16
        self.cbbChannel.grid(row=1,column=0,sticky=W)        
        
        self.btnHwRefresh = Button(self.gbConnection, text="Refresh", command=self.btnHwRefresh_Click)
        self.btnHwRefresh.grid(row=1, column=1, sticky=W)

        Label(self.gbConnection, anchor=W, text="Baudrate:").grid(row=0, column=2, sticky=W)
        self.cbbBaudrates = Tix.ComboBox(self.gbConnection)
        self.cbbBaudrates.subwidget('entry')['width'] = 16
        self.cbbBaudrates.subwidget('listbox')['width'] = 16
        self.cbbBaudrates.grid(row=1,column=2,sticky=W)
        for name, value in self.m_BAUDRATES.iteritems(): self.cbbBaudrates.insert(Tix.END,name)
        self.cbbBaudrates['selection']='500 kBit/sec'
               
        Label(self.gbConnection, anchor=W, text="Hardware Type:").grid(row=0, column=3, sticky=W)
        self.cbbHwType = Tix.ComboBox(self.gbConnection)
        self.cbbHwType.subwidget('entry')['width'] = 16
        self.cbbHwType.subwidget('listbox')['width'] = 16        
        self.cbbHwType.grid(row=1,column=3,sticky=W)
        for name, value in self.m_HWTYPES.iteritems(): self.cbbHwType.insert(Tix.END,name)
        self.cbbHwType['selection']='ISA-82C200'
        
        Label(self.gbConnection, anchor=W, text="I/O Port:").grid(row=0, column=4, sticky=W)
        self.cbbIO = Tix.ComboBox(self.gbConnection)
        self.cbbIO.subwidget('entry')['width'] = 5
        self.cbbIO.subwidget('listbox')['width'] = 5
        self.cbbIO.grid(row=1,column=4,sticky=W)
        for name, value in self.m_IOPORTS.iteritems(): self.cbbIO.insert(Tix.END,name)
        self.cbbIO['selection']=self.cbbIO.pick(0)        
        
        Label(self.gbConnection, anchor=W,width=13, text="Interrupt:").grid(row=0, column=5, sticky=W)
        self.cbbInterrupt = Tix.ComboBox(self.gbConnection)
        self.cbbInterrupt.subwidget('entry')['width'] = 5
        self.cbbInterrupt.subwidget('listbox')['width'] = 5
        self.cbbInterrupt.grid(row=1,column=5, sticky=W)
        for name, value in self.m_INTERRUPTS.iteritems(): self.cbbInterrupt.insert(Tix.END,name)
        self.cbbInterrupt['selection']=self.cbbInterrupt.pick(0)

        self.btnInit = Button(self.gbConnection, width= 8, text="Initialize", command= self.btnInit_Click)
        self.btnInit.grid(row=1, padx = 5, column=6, sticky=W)

        self.btnRelease = Button(self.gbConnection, width= 8, state=DISABLED, text="Release", command= self.btnRelease_Click)
        self.btnRelease.grid(row=1, column=7, sticky=W)
  

    ## Initializes controls and variables in the groupbox "Message Filtering"
    ##
    def InitializeFilteringWidgets(self):
        # Control variables
        #
        self.m_FilteringRDB = IntVar(value=1)
        self.m_FilterExtCHB = IntVar(value=0);
        self.m_IdToNUD = StringVar(value="2047");
        self.m_IdFromNUD = StringVar(value="0");

        # Controls
        #
        Label(self.gbMsgFilter, anchor=W, text="From:").grid(row=0, column=4, sticky=W)
        Label(self.gbMsgFilter, anchor=W, width=16, text="To:").grid(row=0, column=5, sticky=W)
        
        self.chbFilterExt = Checkbutton(self.gbMsgFilter, text="Extended Frame", variable=self.m_FilterExtCHB, command=self.chbFilterExt_CheckedChanged)
        self.chbFilterExt.grid(row=1,column=0, padx=0, pady=2)

        self.rdbFilterOpen = Radiobutton(self.gbMsgFilter, text="Open", value = 1, variable=self.m_FilteringRDB)      
        self.rdbFilterOpen.grid(row=1,column=1, padx=0, pady=2)

        self.rdbFilterClose = Radiobutton(self.gbMsgFilter, text="Close", value = 0, variable=self.m_FilteringRDB)        
        self.rdbFilterClose.grid(row=1,column=2, padx=0, pady=2)

        self.rdbFilterCustom = Radiobutton(self.gbMsgFilter, anchor=W, width=20, text="Custom (expand)", value = 2, variable=self.m_FilteringRDB)
        self.rdbFilterCustom.grid(row=1,column=3, padx=0, pady=2, sticky=W)

        self.nudIdFrom = Spinbox(self.gbMsgFilter, width=10, from_=0, to=0x7FF, textvariable=self.m_IdFromNUD)
        self.nudIdFrom.grid(row=1, column=4,padx=0, pady=2)

        self.nudIdTo = Spinbox(self.gbMsgFilter, width=10, from_=0, to=0x7FF, textvariable=self.m_IdToNUD)
        self.nudIdTo.grid(row=1, column=5,padx=5, pady=2, sticky=W)

        self.btnFilterApply = Button(self.gbMsgFilter, width = 8, state=DISABLED, text = "Apply", command=self.btnFilterApply_Click)
        self.btnFilterApply.grid(row=1, padx = 5, column=6, sticky=W)

        self.btnFilterQuery = Button(self.gbMsgFilter, width = 8, state=DISABLED, text = "Query", command=self.btnFilterQuery_Click)
        self.btnFilterQuery.grid(row=1, column=7, sticky=W)

        self.rdbFilterOpen.select()


    ## Initializes controls and variables in the groupbox "Configuration Parameters"
    ##
    def InitializeConfigurationWidgets(self):
        # Control variables
        #        
        self.m_ConfigurationRDB = IntVar(value=1)
        self.m_DeviceIdNUD = StringVar(value="0");

        # Controls
        #        
        Label(self.gbParameters, anchor=W, text="Parameter:").grid(row=0, column=0, sticky=W)
        self.cbbParameter = Tix.ComboBox(self.gbParameters, command=self.cbbParameter_SelectedIndexChanged)
        self.cbbParameter.subwidget('entry')['width'] = 30
        self.cbbParameter.subwidget('listbox')['width'] = 30
        self.cbbParameter.subwidget('listbox')['height'] = 6
        self.cbbParameter.grid(row=1,column=0,sticky=W)
        for name, value in self.m_PARAMETERS.iteritems(): self.cbbParameter.insert(Tix.END,name)
        self.cbbParameter.bind("<<ComboboxSelected>>",self.cbbParameter_SelectedIndexChanged)
        self.cbbParameter['selection'] = 'Debugs Log'
        
        Label(self.gbParameters, anchor=W, text="Activation:").grid(row=0, column=1, sticky=W)
        self.rdbParamActive = Radiobutton(self.gbParameters, text="Active", value = 1, variable=self.m_ConfigurationRDB)
        self.rdbParamActive.grid(row=1,column=1, padx=0, pady=2, sticky=W)

        self.rdbParamInactive = Radiobutton(self.gbParameters, anchor=W,width = 20, text="Inactive", value = 0, variable=self.m_ConfigurationRDB)
        self.rdbParamInactive.grid(row=1,column=2, padx=0, pady=2, sticky=W)
        
        Label(self.gbParameters, anchor=W, width=20, text="Device ID:").grid(row=0, column=3, sticky=W)
        self.nudDeviceId = Spinbox(self.gbParameters, width=15, state=DISABLED, from_=0, to=0x7FF, textvariable=self.m_DeviceIdNUD)
        self.nudDeviceId.grid(row=1, column=3,padx=0, pady=2, sticky=W)

        self.btnParameterSet = Button(self.gbParameters, width = 8, state=ACTIVE, text = "Set", command=self.btnParameterSet_Click)
        self.btnParameterSet.grid(row=1, padx = 5, column=4, sticky=W)

        self.btnParameterGet = Button(self.gbParameters, width = 8, state=ACTIVE, text = "Get", command=self.btnParameterGet_Click)
        self.btnParameterGet.grid(row=1, column=5, sticky=W)


    ## Initializes controls and variables in the groupbox "Messages Reading"
    ##
    def InitializeReadingWidgets(self):
        # Control variables
        #
        self.m_ListColCaption = ["Type", "|ID", "|Length", "|Data", "|Count", "|RcvTime"]
        self.m_ListColSpace = [9, 10, 7, 25, 6, 10]        
        
        self.m_ListCaptionPadxSpaces = []
        for colText, colWidth in zip(self.m_ListColCaption, self.m_ListColSpace):            
            self.m_ListCaptionPadxSpaces.append(colWidth - len(colText))
        self.m_ListCaptionPadxSpaces[0] = self.m_ListCaptionPadxSpaces[0]-1
        
        self.m_ListFont = tkFont.Font(family="Lucida Console", size ="10")
        
        self.m_ReadingRDB = IntVar(value=0)
        self.m_showPeriodCHB = IntVar(value=1)

        self.tmrRead = threading.Timer(5.0,self.tmrRead_Tick)
        
        # Controls
        #          
        self.rdbTimer = Radiobutton(self.gbReading, text="Read using a Timer", value = 1, variable=self.m_ReadingRDB, command=self.rdbTimer_CheckedChanged)
        self.rdbTimer.grid(row=0,column=0, padx=5, pady=2, sticky=W)

        self.rdbEvent = Radiobutton(self.gbReading, text="Reading using an Event", value = 2, variable=self.m_ReadingRDB, command=self.rdbTimer_CheckedChanged)        
        self.rdbEvent.grid(row=0,column=1, padx=5, pady=2, sticky=W)

        self.rdbManual = Radiobutton(self.gbReading, text="Manual Read", value = 0, variable=self.m_ReadingRDB, command=self.rdbTimer_CheckedChanged)
        self.rdbManual.grid(row=0,column=2, padx=5, pady=2, sticky=W)

        self.chbShowPeriod = Checkbutton(self.gbReading, width=16, text="Timestamp as period", variable=self.m_showPeriodCHB)
        self.chbShowPeriod.grid(row=0,column=3, padx=5, pady=2)
        
        self.yReadScroll = Scrollbar(self.gbReading, orient=VERTICAL)
        self.yReadScroll.grid(row=1, column=4, rowspan=2, sticky=N+S)

        tempString = ""        
        for caption, spaces in zip(self.m_ListColCaption, self.m_ListCaptionPadxSpaces):
            tempString = tempString + "{0}{1}".format(caption," "*spaces)
        Label(self.gbReading, anchor=W, text=tempString, bg="#E2E2E3", fg="#000000", font=self.m_ListFont, relief=GROOVE).grid(row=1,column=0, columnspan=4, padx=5, sticky="nwes")
        
        self.lstMessages = Tix.TList(self.gbReading, relief=GROOVE, height = 6, orient="vertical", yscrollcommand=self.yReadScroll.set, itemtype ="text", font=self.m_ListFont, command=self.btnMsgClear_Click)
        self.lstMessages.grid(row=2, column=0, padx=5, columnspan=4, sticky="nwes")

        self.yReadScroll['command'] = self.lstMessages.yview

        Label(self.gbReading, width=1, text=" ").grid(row=0,  column=5)
        
        self.btnRead = Button(self.gbReading, width = 8, state=DISABLED, text = "Read", command=self.btnRead_Click)        
        self.btnRead.grid(row=1, column=6, padx = 4, sticky=NW)

        self.btnMsgClear = Button(self.gbReading, width = 8, state=ACTIVE, text = "Clear", command=self.btnMsgClear_Click)
        self.btnMsgClear.grid(row=1, column=7, sticky=NW)
        

    ## Initializes controls and variables in the groupbox "Write Messages"
    ##
    def InitializeWritingWidgets(self):
        # Control variables
        #        
        self.m_IDTXT = StringVar(value="000")
        self.m_ExtendedCHB = IntVar(value=0)
        self.m_RemoteCHB = IntVar(value=0)
        self.m_LengthNUD = StringVar(value="8")

        self.m_Data0TXT = StringVar(value="00")
        self.m_Data1TXT = StringVar(value="00")
        self.m_Data2TXT = StringVar(value="00")
        self.m_Data3TXT = StringVar(value="00")
        self.m_Data4TXT = StringVar(value="00")
        self.m_Data5TXT = StringVar(value="00")
        self.m_Data6TXT = StringVar(value="00")
        self.m_Data7TXT = StringVar(value="00")        

        # Controls
        #         
        Label(self.gbWriting, anchor=W, text="ID (Hex):").grid(row=0, column=0, sticky=W)
        self.txtID = Entry(self.gbWriting, width = 13, textvariable=self.m_IDTXT)
        self.txtID.bind("<FocusOut>",self.txtID_Leave)
        self.txtID.grid(row=1,column=0, padx = 5, pady = 0, sticky=W)

        self.chbExtended = Checkbutton(self.gbWriting, text="Extended", variable=self.m_ExtendedCHB, command=self.txtID_Leave)
        self.chbExtended.grid(row=1,column=1, padx=0, pady=2)

        Label(self.gbWriting, anchor=W, width=10, text="Length:").grid(row=0, column=2, sticky=W)
        self.nudLength = Spinbox(self.gbWriting, width=5, from_=0, to=8, textvariable=self.m_LengthNUD, command=self.nudLength_ValueChanged)
        self.nudLength.grid(row=1, column=2, padx=0, pady=2, sticky=W)

        Label(self.gbWriting, anchor=W, text="Data (0..7)").grid(row=0, column=3, sticky=W)
        self.chbRemote = Checkbutton(self.gbWriting, text="RTR", variable=self.m_RemoteCHB, command=self.chbRemote_CheckedChanged)
        self.chbRemote.grid(row=1,column=3, padx=0, pady=2, sticky=W)

        self.txtData0 = Entry(self.gbWriting, width = 4, textvariable=self.m_Data0TXT)        
        self.txtData0.grid(row=1,column=4, padx = 3, pady = 0, sticky=W)
        self.txtData0.bind("<FocusOut>",self.txtData0_Leave)

        self.txtData1 = Entry(self.gbWriting, width = 4, textvariable=self.m_Data1TXT)
        self.txtData1.grid(row=1,column=5, padx = 3, pady = 0, sticky=W)
        self.txtData1.bind("<FocusOut>",self.txtData0_Leave)

        self.txtData2 = Entry(self.gbWriting, width = 4, textvariable=self.m_Data2TXT)
        self.txtData2.grid(row=1,column=6, padx = 3, pady = 0, sticky=W)
        self.txtData2.bind("<FocusOut>",self.txtData0_Leave)

        self.txtData3 = Entry(self.gbWriting, width = 4, textvariable=self.m_Data3TXT)
        self.txtData3.grid(row=1,column=7, padx = 3, pady = 0, sticky=W)
        self.txtData3.bind("<FocusOut>",self.txtData0_Leave)

        self.txtData4 = Entry(self.gbWriting, width = 4, textvariable=self.m_Data4TXT)
        self.txtData4.grid(row=1,column=8, padx = 3, pady = 0, sticky=W)
        self.txtData4.bind("<FocusOut>",self.txtData0_Leave)

        self.txtData5 = Entry(self.gbWriting, width = 4, textvariable=self.m_Data5TXT)
        self.txtData5.grid(row=1,column=9, padx = 3, pady = 0, sticky=W)
        self.txtData5.bind("<FocusOut>",self.txtData0_Leave)

        self.txtData6 = Entry(self.gbWriting, width = 4, textvariable=self.m_Data6TXT)
        self.txtData6.grid(row=1,column=10, padx = 3, pady = 0, sticky=W)
        self.txtData6.bind("<FocusOut>",self.txtData0_Leave)

        self.txtData7 = Entry(self.gbWriting, width = 4, textvariable=self.m_Data7TXT)
        self.txtData7.grid(row=1,column=11, padx = 3, pady = 0, sticky=W)
        self.txtData7.bind("<FocusOut>",self.txtData0_Leave)

        Label(self.gbWriting, width=12, text=" ").grid(row=0, column=12)
        self.btnWrite = Button(self.gbWriting, width = 8, state=DISABLED, text = "Write", command=self.btnWrite_Click)
        self.btnWrite.grid(row=1, column=13, sticky=W)
        
        
    ## Initializes controls and variables in the groupbox "Information"
    ##
    def InitializeInformationWidgets(self):
        # Controls
        #         
        self.yInfoScroll = Scrollbar(self.gbInfo, orient=VERTICAL)
        self.yInfoScroll.grid(row=0, column=1, sticky=N+S)
       
        self.lbxInfo = Listbox(self.gbInfo, width=90, height=7, activestyle="none", yscrollcommand=self.yInfoScroll.set) 
        self.lbxInfo.grid(row=0, column = 0, padx=5, sticky="nwes")
        self.lbxInfo.bind("<Double-1>", self.btnInfoClear_Click)

        self.yInfoScroll['command'] = self.lbxInfo.yview        
        self.lbxInfo.insert(END,"Select a Hardware and a configuration for it. Then click ""Initialize"" button")
        self.lbxInfo.insert(END,"When activated, the Debug-Log file will be found in the same directory as this application")

        Label(self.gbInfo, width=2, text=" ").grid(row=0, column=2)
        
        self.btnGetVersions = Button(self.gbInfo, width = 8, state=DISABLED, text = "Versions", command=self.btnGetVersions_Click)
        self.btnGetVersions.grid(row=0, column=3, padx = 4, sticky=NW)

        self.btnInfoClear = Button(self.gbInfo, width = 8, state=ACTIVE, text = "Clear", command=self.btnInfoClear_Click)
        self.btnInfoClear.grid(row=0, column=4, sticky=NW)

        self.btnStatus = Button(self.gbInfo, width = 8, state=DISABLED, text = "Status", command=self.btnStatus_Click)
        self.btnStatus.grid(row=0, column=3, padx = 4, sticky=W)

        self.btnReset = Button(self.gbInfo, width = 8, state=DISABLED, text = "Reset", command=self.btnReset_Click)
        self.btnReset.grid(row=0, column=4, sticky=W)
           

    ## Centers the app from in the middle of the screen
    ##
    def CenterTheWindow(self):
        Desktop = self.m_Parent.winfo_toplevel()
        desktopWidth = Desktop.winfo_screenwidth()
        desktopHeight = Desktop.winfo_screenheight()
        
        self.m_Parent.geometry("{0}x{1}+{2}+{3}".format(self.m_Width,
                                                        self.m_Height,
                                                        (desktopWidth-self.m_Width)/2,
                                                        (desktopHeight-self.m_Height)/2))           


    ## Configures the Debug-Log file of PCAN-Basic
    ##
    def ConfigureLogFile(self):
        # Sets the mask to catch all events
        #
        iBuffer = LOG_FUNCTION_ALL

        # Configures the log file. 
        # NOTE: The Log capability is to be used with the NONEBUS Handle. Other handle than this will 
        # cause the function fail.
        #
        self.m_objPCANBasic.SetValue(PCAN_NONEBUS, PCAN_LOG_CONFIGURE, iBuffer)


    ## Help Function used to get an error as text
    ##
    def GetFormatedError(self, error):
        # Gets the text using the GetErrorText API function
        # If the function success, the translated error is returned. If it fails,
        # a text describing the current error is returned.
        #
        stsReturn = self.m_objPCANBasic.GetErrorText(error, 0)
        if stsReturn[0] != PCAN_ERROR_OK:
            return "An error occurred. Error-code's text ({0:X}h) couldn't be retrieved".format(error)
        else:
            return stsReturn[1]


    ## Includes a new line of text into the information Listview
    ##
    def IncludeTextMessage(self, strMsg):
        self.lbxInfo.insert(END, strMsg);
        self.lbxInfo.see(END)


    ## Gets the current status of the PCAN-Basic message filter
    ##
    def GetFilterStatus(self):
        # Tries to get the sttaus of the filter for the current connected hardware
        #
        stsResult = self.m_objPCANBasic.GetValue(self.m_PcanHandle, PCAN_MESSAGE_FILTER)

        # If it fails, a error message is shown
        #
        if stsResult[0] != PCAN_ERROR_OK:
            tkMessageBox.showinfo("Error!", self.GetFormatedError(stsResult[0]))
            return False,
        else:
            return True, stsResult[1]


    ## Activates/deaactivates the different controls of the form according
    ## with the current connection status
    ##
    def SetConnectionStatus(self, bConnected=True):
        # Gets the status values for each case
        #
        if bConnected:
            stsConnected = ACTIVE
            stsNotConnected = DISABLED
        else:
            stsConnected = DISABLED
            stsNotConnected = ACTIVE
            
        # Buttons
        #
        self.btnInit['state'] = stsNotConnected
        if (self.m_ReadingRDB.get() == 0) and bConnected:
            self.btnRead['state'] = ACTIVE
        else:
            self.btnRead['state'] = DISABLED
        self.btnWrite['state'] = stsConnected;
        self.btnRelease['state'] = stsConnected
        self.btnFilterApply['state'] = stsConnected
        self.btnFilterQuery['state'] = stsConnected
        self.btnGetVersions['state'] = stsConnected
        self.btnHwRefresh['state'] = stsNotConnected
        self.btnStatus['state'] = stsConnected
        self.btnReset['state'] = stsConnected

        # ComboBoxs
        #
        self.cbbBaudrates['state'] = stsNotConnected;
        self.cbbChannel['state'] = stsNotConnected;
        self.cbbHwType['state'] = stsNotConnected;
        self.cbbIO['state'] = stsNotConnected;
        self.cbbInterrupt['state'] = stsNotConnected;

        # Hardware configuration and read mode
        #
        if not bConnected:
            self.cbbChannel_SelectedIndexChanged(self.cbbChannel['value'])
        else:
            self.rdbTimer_CheckedChanged()


    ## Creates and returns an input line for a received message with the messages-receive            
    ## Listview format
    ##
    def FormatCANMessage(self, msg, time):
        msgStringEntry = ""
        newMsg = msg.getCANMessage()
        bIsRTR = (newMsg.MSGTYPE & PCAN_MESSAGE_RTR.value) == PCAN_MESSAGE_RTR.value
      
        if (newMsg.MSGTYPE & PCAN_MESSAGE_EXTENDED.value) == PCAN_MESSAGE_EXTENDED.value:
            if bIsRTR:
                strTemp = "EXT/RTR "
            else:
                strTemp = "EXTENDED"
            msgStringEntry = msgStringEntry + (strTemp + " "*(self.m_ListColSpace[COL_TYPE] - len(strTemp)))
            strTemp = "{0:08X}".format(newMsg.ID)
            msgStringEntry = msgStringEntry + (strTemp + " "*(self.m_ListColSpace[COL_ID] - len(strTemp)))
        else:
            if bIsRTR:
                strTemp = "STD/RTR "
            else:
                strTemp = "STANDARD"
            msgStringEntry = msgStringEntry + (strTemp + " "*(self.m_ListColSpace[COL_TYPE] - len(strTemp)))
            strTemp = "{0:03X}".format(newMsg.ID)
            msgStringEntry = msgStringEntry + (strTemp + " "*(self.m_ListColSpace[COL_ID] - len(strTemp)))

        strTemp = str(newMsg.LEN)
        msgStringEntry = msgStringEntry + (strTemp + " "*(self.m_ListColSpace[COL_LENGTH] - len(strTemp)))

        if bIsRTR:
            strTemp = "Remote Request"
        else:
            strTemp = ""
            for i in range(newMsg.LEN):
                if strTemp != "":
                    strTemp = strTemp + " "
                strTemp = strTemp + "{0:02X}".format(newMsg.DATA[i])
            msgStringEntry = msgStringEntry + (strTemp + " "*(self.m_ListColSpace[COL_DATA] - len(strTemp)))

        strTemp = str(msg.getCount())
        msgStringEntry = msgStringEntry + (strTemp + " "*(self.m_ListColSpace[COL_COUNT] - len(strTemp)))
        msgStringEntry = msgStringEntry + (time + " "*(self.m_ListColSpace[COL_TIME] - len(time)))

        return msgStringEntry    

################################################################################################################################################
### Message-proccessing functions
################################################################################################################################################

    ## Modifies a message entry in the Message-ListView
    ##
    def ModifyMsgEntry(self, msgStsCurrentMessage, theMsg, itsTimeStamp):
        # Update and format the new time information
        #
        lastTimeStamp = msgStsCurrentMessage.getTimestamp()
        fTime = itsTimeStamp.millis + (itsTimeStamp.micros / 1000.0)       
        if self.m_showPeriodCHB.get():
            fTime = fTime - (lastTimeStamp.millis + (lastTimeStamp.micros / 1000.0))
            
        # Update the values associated with the message
        #
        msgStsCurrentMessage.Actualize(theMsg, itsTimeStamp)
        msgStringEntry = self.FormatCANMessage(msgStsCurrentMessage,str(fTime))

        # Refresh the line-entry in the listview
        #
        self.lstMessages.delete(msgStsCurrentMessage.getPosition())
        self.lstMessages.insert(msgStsCurrentMessage.getPosition(),text=msgStringEntry)


    ## Inserts a new entry for a new message in the Message-ListView
    ##
    def InsertMsgEntry(self, theMsg, itsTimeStamp):
        # Format the new time information
        #
        if self.m_showPeriodCHB.get() == 0:
            strTime = "{0},{1}".format(timeStamp.millis, timeStamp.micros)
        else:
            strTime = ""

        # The status values associated with the new message are created
        #
        lastMsg = MessageStatus(theMsg,itsTimeStamp,len(self.m_LastMsgsList))
        self.m_LastMsgsList.append(lastMsg)

        # We add this status in the last message list
        msgStringEntry = self.FormatCANMessage(lastMsg,strTime)
        self.lstMessages.insert(END,text=msgStringEntry)


    ## Processes a received message, in order to show it in the Message-ListView
    ##
    def ProcessMessage(self, *args):
        bFound = False
        
        # Split the arguments. [0] TPCANMsg, [1] TPCANTimestamp
        #
        theMsg = args[0][0]
        itsTimeStamp = args[0][1]    

        # We search if a message (Same ID and Type) is 
        # already received or if this is a new message
        #
        for msgStsCurrentMessage in self.m_LastMsgsList:
            if msgStsCurrentMessage.getCANMessage().ID == theMsg.ID:
                if msgStsCurrentMessage.getCANMessage().MSGTYPE == theMsg.MSGTYPE:
                    bFound = True
                    break        

        if bFound:
            # Messages of this kind are already received; we do an update
            #
            self.ModifyMsgEntry(msgStsCurrentMessage, theMsg, itsTimeStamp)
        else:
            # Messages of this kind are not received; we create a new entry
            #
            self.InsertMsgEntry(theMsg, itsTimeStamp)


################################################################################################################################################
### Event Handlers
################################################################################################################################################        

    ## Form-Closing Function / Finish function
    ##
    def Form_OnClosing(self, event=None):
        # Releases the used PCAN-Basic channel
        #
        self.m_objPCANBasic.Uninitialize(self.m_PcanHandle)
        """Quit our mainloop."""
        self.exit = 0


    ## Button btnHwRefresh handler
    ##
    def btnHwRefresh_Click(self):

        # Clears the Channel comboBox and fill it again with 
        # the PCAN-Basic handles for no-Plug&Play hardware and
        # the detected Plug&Play hardware
        #        
        items = []
        myText = self.cbbChannel.subwidget('listbox').delete(0,Tix.END)
        for name, value in self.m_CHANNELS.iteritems():
            # Includes all no-Plug&Play Handles
            #
            if (value <= PCAN_DNGBUS1):
                items.append(name)
            else:
                # Checks for a Plug&Play Handle and, according with the return value, includes it
                # into the list of available hardware channels.
                #                
                result =  self.m_objPCANBasic.GetValue(value, PCAN_CHANNEL_CONDITION)
                if  (result[0] == PCAN_ERROR_OK) and (result[1] == PCAN_CHANNEL_AVAILABLE):
                    items.append(name)                    

        items.sort()
        self.cbbChannel
        for name in items:
            self.cbbChannel.insert(Tix.END, name)
        self.cbbChannel['selection'] = self.cbbChannel.pick(Tix.END)


    ## Button btnInit handler
    ##
    def btnInit_Click(self):
        # gets the connection values
        #
        baudrate = self.m_BAUDRATES[self.cbbBaudrates['selection']]
        hwtype = self.m_HWTYPES[self.cbbHwType['selection']]
        ioport = int(self.cbbIO['selection'],16)
        interrupt = int(self.cbbInterrupt['selection'])

        # Connects a selected PCAN-Basic channel
        #
        result =  self.m_objPCANBasic.Initialize(self.m_PcanHandle,baudrate,hwtype,ioport,interrupt)

        if result != PCAN_ERROR_OK:
            tkMessageBox.showinfo("Error!", self.GetFormatedError(result[0]))

        # Sets the connection status of the form
        #
        self.SetConnectionStatus(result == PCAN_ERROR_OK)


    ## Button btnRelease handler
    ##
    def btnRelease_Click(self):
        # Releases a current connected PCAN-Basic channel
        #
        self.m_objPCANBasic.Uninitialize(self.m_PcanHandle)
##        tmrRead.enabled = false;
##        if thread ...:
##            thread.abort()
##            thread.Join()
##            thread =0
        # Sets the connection status of the main-form
        #
        self.SetConnectionStatus(False)


    ## Button btnFilterApply handler
    ##
    def btnFilterApply_Click(self):
        if self.m_FilterExtCHB.get():
            filterMode = PCAN_MODE_EXTENDED
        else:
            filterMode = PCAN_MODE_STANDARD

        # Gets the current status of the message filter
        #
        filterRet = self.GetFilterStatus()

        if not filterRet[0]:
            return 

        # Configures the message filter for a custom range of messages
        #
        if self.m_FilteringRDB.get() == 2:
            # Sets the custom filter
            #
            result = self.m_objPCANBasic.FilterMessages(self.m_PcanHandle,
                                                        int(self.m_IdFromNUD.get()),
                                                        int(self.m_IdToNUD.get()),
                                                        filterMode)
            # If success, an information message is written, if it is not, an error message is shown
            #
            if result == PCAN_ERROR_OK:
                self.IncludeTextMessage("The filter was customized. IDs from {0:X} to {1:X} will be received".format(int(self.m_IdFromNUD.get()),int(self.m_IdToNUD.get())))
            else:
                tkMessageBox.showinfo("Error!", self.GetFormatedError(result))

            return

        # The filter will be full opened or complete closed
        #
        if self.m_FilteringRDB.get() == 0:
            filterMode = PCAN_FILTER_CLOSE
            textEnd = "closed"
        else:
            filterMode = PCAN_FILTER_OPEN
            textEnd = "opened"

        # The filter is configured
        #
        result = self.m_objPCANBasic.SetValue(self.m_PcanHandle,
                                              PCAN_MESSAGE_FILTER,
                                              filterMode)
        
        # If success, an information message is written, if it is not, an error message is shown
        #
        if result == PCAN_ERROR_OK:
            self.IncludeTextMessage("The filter was successfully "+ textEnd)
        else:
            tkMessageBox.showinfo("Error!", self.GetFormatedError(result))


    ## Button btnFilterQuery handler
    ##
    def btnFilterQuery_Click(self):
        # Queries the current status of the message filter
        #
        filterRet = self.GetFilterStatus()

        if filterRet[0]:
            if filterRet[1] == PCAN_FILTER_CLOSE:
                self.IncludeTextMessage("The Status of the filter is: closed.")
            elif filterRet[1] == PCAN_FILTER_OPEN:
                self.IncludeTextMessage("The Status of the filter is: full opened.")
            elif filterRet[1] == PCAN_FILTER_CUSTOM:
                self.IncludeTextMessage("The Status of the filter is: customized.")
            else:
                self.IncludeTextMessage("The Status ofself.tmrRead the filter is: Invalid.")
                

    ## Button btnParameterSet handler
    ##
    def btnParameterSet_Click(self):
        currentVal = self.cbbParameter['selection']
        iVal = self.m_PARAMETERS[currentVal]

        if self.m_ConfigurationRDB.get() == 1:
            iBuffer = PCAN_PARAMETER_ON
            lastStr = "activated"
            lastStr2 = "ON"
        else:
            iBuffer = PCAN_PARAMETER_OFF
            lastStr = "deactivated"
            lastStr2 = "OFF"

        # The Device-Number of an USB channel will be set
        #
        if iVal == PCAN_DEVICE_NUMBER:
            iBuffer = int(self.m_DeviceIdNUD.get())
            result = self.m_objPCANBasic.SetValue(self.m_PcanHandle,PCAN_DEVICE_NUMBER,iBuffer)
            if result == PCAN_ERROR_OK:
                self.IncludeTextMessage("The desired Device-Number was successfully configured")

        # The 5 Volt Power feature of a PC-card or USB will be set
        #        
        elif iVal == PCAN_5VOLTS_POWER:
            result = self.m_objPCANBasic.SetValue(self.m_PcanHandle,PCAN_5VOLTS_POWER,iBuffer)
            if result == PCAN_ERROR_OK:
                self.IncludeTextMessage("The USB/PC-Card 5 power was successfully " + lastStr)
            
        # The feature for automatic reset on BUS-OFF will be set
        #        
        elif iVal == PCAN_BUSOFF_AUTORESET:
            result = self.m_objPCANBasic.SetValue(self.m_PcanHandle,PCAN_BUSOFF_AUTORESET,iBuffer)
            if result == PCAN_ERROR_OK:
                self.IncludeTextMessage("The automatic-reset on BUS-OFF was successfully " + lastStr)
            
        # The CAN option "Listen Only" will be set
        #        
        elif iVal == PCAN_LISTEN_ONLY:
            result = self.m_objPCANBasic.SetValue(self.m_PcanHandle,PCAN_LISTEN_ONLY,iBuffer)
            if result == PCAN_ERROR_OK:
                self.IncludeTextMessage("The CAN option ""Listen Only"" was successfully " + lastStr)

        # The feature for logging debug-information will be set
        #
        elif iVal == PCAN_LOG_STATUS:
            result = self.m_objPCANBasic.SetValue(PCAN_NONEBUS,PCAN_LOG_STATUS,iBuffer)
            if result == PCAN_ERROR_OK:
                self.IncludeTextMessage("The feature for logging debug information was successfully " + lastStr)

        # The channel option "Receive Status" will be set
        #        
        elif iVal == PCAN_RECEIVE_STATUS:
            result = self.m_objPCANBasic.SetValue(self.m_PcanHandle,PCAN_RECEIVE_STATUS,iBuffer)
            if result == PCAN_ERROR_OK:
                self.IncludeTextMessage("The channel option ""Receive Status"" was set to  " + lastStr2)
                
        # The current parameter is invalid
        #
        else:
            stsResult = PCAN_ERROR_UNKNOWN
            tkMessageBox.showinfo("Error!", "Wrong parameter code.")

        # If the function fail, an error message is shown
        #
        if result != PCAN_ERROR_OK:
            tkMessageBox.showinfo("Error!", self.GetFormatedError(result))


    ## Button btnParameterGet handler
    ##
    def btnParameterGet_Click(self):
        currentVal = self.cbbParameter['selection']
        iVal = self.m_PARAMETERS[currentVal]

        # The Device-Number of an USB channel will be retrieved
        #
        if iVal == PCAN_DEVICE_NUMBER:
            iBuffer = int(self.m_DeviceIdNUD.get())
            result = self.m_objPCANBasic.GetValue(self.m_PcanHandle,PCAN_DEVICE_NUMBER)
            if result[0] == PCAN_ERROR_OK:
                self.IncludeTextMessage("The configured Device-txtData0_LeaveNumber is {0:X}h".format(result[1]))

        # The activation status of the 5 Volt Power feature of a PC-card or USB will be retrieved
        #
        elif iVal == PCAN_5VOLTS_POWER:
            result = self.m_objPCANBasic.GetValue(self.m_PcanHandle,PCAN_5VOLTS_POWER)
            if result[0] == PCAN_ERROR_OK:
                if result[1] == PCAN_PARAMETER_ON:
                    lastStr = "ON"
                else:
                    lastStr = "OFF"
                self.IncludeTextMessage("The 5-Volt Power of the USB/PC-Card is " + lastStr)
                
        # The activation status of the feature for automatic reset on BUS-OFF will be retrieved
        #
        elif iVal == PCAN_BUSOFF_AUTORESET:
            result = self.m_objPCANBasic.GetValue(self.m_PcanHandle,PCAN_BUSOFF_AUTORESET)
            if result[0] == PCAN_ERROR_OK:
                if result[1] == PCAN_PARAMETER_ON:
                    lastStr = "ON"
                else:
                    lastStr = "OFF"
                self.IncludeTextMessage("The automatic-reset on BUS-OFF is " + lastStr)

        # The activation status of the CAN option "Listen Only" will be retrieved
        #
        elif iVal == PCAN_LISTEN_ONLY:
            result = self.m_objPCANBasic.GetValue(self.m_PcanHandle,PCAN_LISTEN_ONLY)
            if result[0] == PCAN_ERROR_OK:
                if result[1] == PCAN_PARAMETER_ON:
                    lastStr = "ON"
                else:
                    lastStr = "OFF"
                self.IncludeTextMessage("The CAN option ""Listen Only"" is " + lastStr)

        # The activation status for the feature for logging debug-information will be retrieved
        #
        elif iVal == PCAN_LOG_STATUS:
            result = self.m_objPCANBasic.GetValue(PCAN_NONEBUS,PCAN_LOG_STATUS)
            if result[0] == PCAN_ERROR_OK:
                if result[1] == PCAN_PARAMETER_ON:
                    lastStr = "ON"
                else:
                    lastStr = "OFF"
                self.IncludeTextMessage("The feature for logging debug information is " + lastStr)

        # The activation status of the channel option "Receive Status"  will be retrieved
        #
        elif iVal == PCAN_RECEIVE_STATUS:
            result = self.m_objPCANBasic.GetValue(self.m_PcanHandle,PCAN_RECEIVE_STATUS)
            if result[0] == PCAN_ERROR_OK:
                if result[1] == PCAN_PARAMETER_ON:
                    lastStr = "ON"
                else:
                    lastStr = "OFF"
                self.IncludeTextMessage("The channel option ""Receive Status"" is " + lastStr)

        # The Number of the CAN-Controller used by a PCAN-Channel
        #
        elif iVal == PCAN_CONTROLLER_NUMBER:
            result = self.m_objPCANBasic.GetValue(self.m_PcanHandle,PCAN_CONTROLLER_NUMBER)
            if result[0] == PCAN_ERROR_OK:
                self.IncludeTextMessage("The CAN Controller number is {0}".format(result[1]))
                
        # The current parameter is invalid
        #
        else:
            stsResult = PCAN_ERROR_UNKNOWN,
            tkMessageBox.showinfo("Error!", "Wrong parameter code.")

         #If the function fail, an error message is shown
        #
        if result[0] != PCAN_ERROR_OK:
            tkMessageBox.showinfo("Error!", self.GetFormatedError(result[0]))


    ## Button btnRead handler
    ##
    def btnRead_Click(self):
        # We execute the "Read" function of the PCANBasic
        #
        result = self.m_objPCANBasic.Read(self.m_PcanHandle)

        if result[0] == PCAN_ERROR_OK:
            # We show the received message
            #
            self.ProcessMessage(result[1:])
        else:
            # If an error occurred, an information message is included
            #
            self.IncludeTextMessage(self.GetFormatedError(result[0]))


    ## Button btnGetVersions handler
    ##
    def btnGetVersions_Click(self):
        # We get the vesion of the PCAN-Basic API
        #
        result = self.m_objPCANBasic.GetValue(PCAN_NONEBUS, PCAN_API_VERSION)
        if result[0] ==PCAN_ERROR_OK:
            self.IncludeTextMessage("API Version: " + result[1])
            # We get the driver version of the channel being used
            #
            result = self.m_objPCANBasic.GetValue(self.m_PcanHandle, PCAN_CHANNEL_VERSION)
            if result[0] == PCAN_ERROR_OK:
                # Because this information contains line control characters (several lines)
                # we split this also in several entries in the Information List-Box
                #
                lines = string.split(result[1],'\n')
                self.IncludeTextMessage("Channel/Driver Version: ")
                for line in lines:
                    self.IncludeTextMessage("     * " + line)

        # If an error ccurred, a message is shown
        #
        if result[0] != PCAN_ERROR_OK:
            tkMessageBox.showinfo("Error!", self.GetFormatedError(result[0]))


    ## Button btnMsgClear handler
    ##
    def btnMsgClear_Click(self, *args):
        # The information contained in the messages List-View
        # is cleared
        #
        self.lstMessages.delete(0,END)
        self.m_LastMsgsList = []


    ## Button btnInfoClear handler
    ##
    def btnInfoClear_Click(self, event=None):
        # The information contained in the Information List-Box 
        # is cleared
        #
        self.lbxInfo.delete(0,END)


    ## Button btnWrite handler
    ##
    def btnWrite_Click(self):
        edits = [self.m_Data0TXT, self.m_Data1TXT, self.m_Data2TXT, self.m_Data3TXT, self.m_Data4TXT, self.m_Data5TXT, self.m_Data6TXT, self.m_Data7TXT]
        iCount = int(self.m_LengthNUD.get())
        
        if self.m_ExtendedCHB.get():
            msgType = PCAN_MESSAGE_EXTENDED
        else:
            msgType = PCAN_MESSAGE_STANDARD

        # We create a TPCANMsg message structure
        #
        CANMsg = TPCANMsg()

        # We configurate the Message.  The ID,
        # Length of the Data, Message Type and the data
        #
        CANMsg.ID = int(self.m_IDTXT.get(),16)
        CANMsg.LEN = int(self.m_LengthNUD.get())
        CANMsg.MSGTYPE = msgType

        # If a remote frame will be sent, the data bytes are not important.
        #
        if self.m_RemoteCHB.get():
            CANMsg.MSGTYPE = msgType | PCAN_MESSAGE_RTR
        else:
            # We get so much data as the Len of the message
            #
            for i in range(iCount):
                CANMsg.DATA[i] = int(edits[i].get(),16)

        # The message is sent to the configured hardware
        #
        result = self.m_objPCANBasic.Write(self.m_PcanHandle, CANMsg)

        # The message was successfully sent
        #
        if result == PCAN_ERROR_OK:
            self.IncludeTextMessage("Message was successfully SENT")
        else:
            # An error occurred.  We show the error.
            #
            tkMessageBox.showinfo(self.GetFormatedError(result))


    ## Button btnReset handler
    ##
    def btnReset_Click(self):
        # Resets the receive and transmit queues of a PCAN Channel.
        #
        result = self.m_objPCANBasic.Reset(self.m_PcanHandle)

        # If it fails, a error message is shown
        #
        if result != PCAN_ERROR_OK:
            tkMessageBox.showinfo("Error!", self.GetFormatedTex(result))
        else:
            self.IncludeTextMessage("Receive and transmit queues successfully reset")


    ## Button btnStatus handler
    ##            
    def btnStatus_Click(self):
        # Gets the current BUS status of a PCAN Channel.
        #
        result = self.m_objPCANBasic.GetStatus(self.m_PcanHandle)

        # Switch On Error Name
        #
        if result == PCAN_ERROR_INITIALIZE:
            errorName = "PCAN_ERROR_INITIALIZE"
        elif result == PCAN_ERROR_BUSLIGHT:
            errorName = "PCAN_ERROR_BUSLIGHT"
        elif result == PCAN_ERROR_BUSHEAVY:
            errorName = "PCAN_ERROR_BUSHEAVY"
        elif result == PCAN_ERROR_BUSOFF:
            errorName = "PCAN_ERROR_BUSOFF"
        elif result == PCAN_ERROR_OK:
            errorName = "PCAN_ERROR_OK"
        else:
            errorName = "See Documentation"

        # Display Message
        #
        self.IncludeTextMessage("Status: {0} ({1:X}h)".format(errorName, result))


    ## Combobox cbbChannel handler
    ##          
    def cbbChannel_SelectedIndexChanged(self, currentValue):
        # Get the handle from the text being shown
        #
        self.m_PcanHandle = self.m_CHANNELS[currentValue]
        # Determines if the handle belong to a No Plug&Play hardware
        #
        if self.m_PcanHandle < PCAN_DNGBUS1:
            putItActive = NORMAL
        else:
            putItActive = DISABLED

        # Activates/deactivates configuration controls according with the 
        # kind of hardware
        #
        self.cbbHwType['state'] = putItActive
        self.cbbIO['state'] = putItActive
        self.cbbInterrupt['state'] = putItActive


    ## Combobox cbbParameter handler
    ##     
    def cbbParameter_SelectedIndexChanged(self, currentValue=None):
        # Activates/deactivates controls according with the selected 
        # PCAN-Basic parameter
        #
        bIsRB = currentValue != 'USBs Device Number'
        if bIsRB:
            self.rdbParamActive['state'] = ACTIVE
            self.rdbParamInactive['state'] = ACTIVE
            self.nudDeviceId['state'] = DISABLED
        else:
            self.rdbParamActive['state'] = DISABLED
            self.rdbParamInactive['state'] = DISABLED
            self.nudDeviceId['state'] = NORMAL

            
    ## Checkbox chbRemote handler
    ## 
    def chbRemote_CheckedChanged(self):
        edits = [self.txtData0, self.txtData1, self.txtData2, self.txtData3, self.txtData4, self.txtData5, self.txtData6, self.txtData7]

        # Determines the status for the textboxes
        # according wiht the cehck-status
        #
        if self.m_RemoteCHB.get():
            newStatus = DISABLED
            iCount = 8
        else:
            newStatus = NORMAL
            iCount = int(self.m_LengthNUD.get())        

        # If the message is a RTR, no data is sent. The textboxes for data 
        # will be disabled
        #
        for i in range(iCount):
            edits[i]['state'] = newStatus


    ## Checkbox chbFilterExt handler
    ##             
    def chbFilterExt_CheckedChanged(self):
        # Determines the maximum value for a ID
        # according with the Filter-Type
        #
        if self.m_FilterExtCHB.get():
            self.nudIdTo['to'] = 0x1FFFFFFF
            self.nudIdFrom['to'] = 0x1FFFFFFF
        else:
            self.nudIdTo['to'] = 0x7FF
            self.nudIdFrom['to'] = 0x7FF

        # We check that the maximum value for a selected filter 
        # mode is used
        #
        if int(self.m_IdToNUD.get()) > self.nudIdTo['to']:
            self.m_IdToNUD.set(iMaxValue)
        if int(self.m_IdFromNUD.get()) > self.nudIdFrom['to']:
            self.m_IdFromNUD.set(iMaxValue)


    ## Radiobutton rdbTimer handler
    ##              
    def rdbTimer_CheckedChanged(self):
        if self.btnRelease['state'] == DISABLED:
            return

        # According with the kind of reading, a timer, a thread or a button will be enabled
        #
        if self.m_ReadingRDB.get() == 1:
            tkMessageBox.showinfo(message="TODO (rdbTimer_CheckedChanged): Reading with a TIMER")

        if self.m_ReadingRDB.get() == 2:
            tkMessageBox.showinfo(message="TODO (rdbTimer_CheckedChanged): Reading using an EVENT")
            
        if (self.btnRelease['state'] == ACTIVE) and (self.m_ReadingRDB.get() == 0):
            self.btnRead['state'] = ACTIVE
        else:
            self.btnRead['state'] = DISABLED        

       
    ## Entry txtID OnLeave handler
    ##                   
    def txtID_Leave(self,*args):
        # Calculates the text length and Maximum ID value according
        # with the Message Typ
        #
        if self.m_ExtendedCHB.get():
            iTextLength = 8
            uiMaxValue = 0x1FFFFFFF
        else:
            iTextLength = 3
            uiMaxValue = 0x7FF
        
        try:
            iValue = int(self.m_IDTXT.get(),16)       
        except ValueError:
            iValue = 0
        finally:
            # The Textbox for the ID is represented with 3 characters for 
            # Standard and 8 characters for extended messages.
            # We check that the ID is not bigger than current maximum value
            #
            if iValue > uiMaxValue:
                iValue = uiMaxValue            
            self.m_IDTXT.set("{0:0{1}X}".format(iValue,iTextLength))
            return True
        

    ## Entry txtData0 OnLeave handler
    ##   
    def txtData0_Leave(self,*args):        
        edits = [self.m_Data0TXT, self.m_Data1TXT, self.m_Data2TXT, self.m_Data3TXT, self.m_Data4TXT, self.m_Data5TXT, self.m_Data6TXT, self.m_Data7TXT]
        for i in range(8):
            # The format of all Textboxes Data fields are checked.
            #
            self.txtData0_LeaveHelper(edits[i])

    ## Helper function for the above funciton
    #
    def txtData0_LeaveHelper(self, editVar):
        try:
            iValue = int(editVar.get(),16)       
        except ValueError:
            iValue = 0
        finally:
            # All the Textbox Data fields are represented with 2 characters.
            # The maximum value allowed is 255 (0xFF)
            #
            if iValue > 255:
                iValue = 255
            editVar.set("{0:0{1}X}".format(iValue,2))
        

    # Spinbutton nudLength handler
    def nudLength_ValueChanged(self):
        edits = [self.txtData0, self.txtData1, self.txtData2, self.txtData3, self.txtData4, self.txtData5, self.txtData6, self.txtData7]
        iCount = int(self.m_LengthNUD.get())

        # The Textbox Data fields are enabled or disabled according
        # with the desaired amount of data
        #
        for i in range(8):
            if i < iCount:
                edits[i]['state'] = NORMAL
            else:
                edits[i]['state'] = DISABLED
                
                             
    def tmrRead_Tick(self):
        print "AJA"
###*****************************************************************

        


###*****************************************************************
### ROOT
###*****************************************************************

### Loop-Functionallity  
def RunMain(root):
    global basicExl

    # Creates a PCAN-Basic application
    #
    basicExl = PCANBasicExample(root)
    
    # Runs the Application / loop-start
    #
    basicExl.loop()
    
    # Application's destrution / loop-end
    #
    basicExl.destroy()


if __name__ == '__main__':
    # Creates the Tkinter-extension Root
    #
    root = Tix.Tk()
    # Uses the root to launch the PCAN-Basic Example application
    #
    RunMain(root)
###*****************************************************************

