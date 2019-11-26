#  PCAN-ISO-TP.py
#
#  ~~~~~~~~~~~~
#
#  PCAN-ISO-TP API
#
#  ~~~~~~~~~~~~
#
#  ------------------------------------------------------------------
#  Author : Keneth Wagner
#  Last change: 08.11.2011 Wagner
#
#  Language: Python 3.4
 
#

# Module Imports
#
from ctypes import *
#import ctypes
#///////////////////////////////////////////////////////////
# Type definitions
#///////////////////////////////////////////////////////////

TPCANHandle            = c_ubyte  # Represents a PCAN hardware channel handle
TPCANStatus            = int      # Represents a PCAN status/error code
TPCANParameter         = c_ubyte  # Represents a PCAN parameter to be read or set
TPCANDevice            = c_ubyte  # Represents a PCAN device
TPCANMessageType       = c_ubyte  # Represents the type of a PCAN message
TPCANType              = c_ubyte  # Represents the type of PCAN hardware to be initialized
TPCANMode              = c_ubyte  # Represents a PCAN filter mode
TPCANBaudrate          = c_ushort # Represents a PCAN Baud rate register value

#///////////////////////////////////////////////////////////
# Value definitions
#///////////////////////////////////////////////////////////

# Currently defined and supported PCAN channels
#
PCANTP_NONEBUS             = TPCANHandle(0x00)  # Undefined/default value for a PCAN bus

PCANTP_ISABUS1             = TPCANHandle(0x21)  # PCAN-ISA interface, channel 1
PCANTP_ISABUS2             = TPCANHandle(0x22)  # PCAN-ISA interface, channel 2
PCANTP_ISABUS3             = TPCANHandle(0x23)  # PCAN-ISA interface, channel 3
PCANTP_ISABUS4             = TPCANHandle(0x24)  # PCAN-ISA interface, channel 4
PCANTP_ISABUS5             = TPCANHandle(0x25)  # PCAN-ISA interface, channel 5
PCANTP_ISABUS6             = TPCANHandle(0x26)  # PCAN-ISA interface, channel 6
PCANTP_ISABUS7             = TPCANHandle(0x27)  # PCAN-ISA interface, channel 7
PCANTP_ISABUS8             = TPCANHandle(0x28)  # PCAN-ISA interface, channel 8
    
PCANTP_DNGBUS1             = TPCANHandle(0x31)  # PCAN-Dongle/LPT interface, channel 1
    
PCANTP_PCIBUS1             = TPCANHandle(0x41)  # PCAN-PCI interface, channel 1
PCANTP_PCIBUS2             = TPCANHandle(0x42)  # PCAN-PCI interface, channel 2
PCANTP_PCIBUS3             = TPCANHandle(0x43)  # PCAN-PCI interface, channel 3
PCANTP_PCIBUS4             = TPCANHandle(0x44)  # PCAN-PCI interface, channel 4
PCANTP_PCIBUS5             = TPCANHandle(0x45)  # PCAN-PCI interface, channel 5
PCANTP_PCIBUS6	         = TPCANHandle(0x46)  # PCAN-PCI interface, channel 6
PCANTP_PCIBUS7	         = TPCANHandle(0x47)  # PCAN-PCI interface, channel 7
PCANTP_PCIBUS8	         = TPCANHandle(0x48)  # PCAN-PCI interface, channel 8
    
PCANTP_USBBUS1             = TPCANHandle(0x51)  # PCAN-USB interface, channel 1
PCANTP_USBBUS2             = TPCANHandle(0x52)  # PCAN-USB interface, channel 2
PCANTP_USBBUS3             = TPCANHandle(0x53)  # PCAN-USB interface, channel 3
PCANTP_USBBUS4             = TPCANHandle(0x54)  # PCAN-USB interface, channel 4
PCANTP_USBBUS5             = TPCANHandle(0x55)  # PCAN-USB interface, channel 5
PCANTP_USBBUS6             = TPCANHandle(0x56)  # PCAN-USB interface, channel 6
PCANTP_USBBUS7             = TPCANHandle(0x57)  # PCAN-USB interface, channel 7
PCANTP_USBBUS8             = TPCANHandle(0x58)  # PCAN-USB interface, channel 8
    
PCANTP_PCCBUS1             = TPCANHandle(0x61)  # PCAN-PC Card interface, channel 1
PCANTP_PCCBUS2             = TPCANHandle(0x62)  # PCAN-PC Card interface, channel 2

# Baud rate codes = BTR0/BTR1 register values for the CAN controller.
# You can define your own Baud rate with the BTROBTR1 register.
# Take a look at www.peak-system.com for our free software "BAUDTOOL" 
# to calculate the BTROBTR1 register for every baudrate and sample point.
#
PCAN_BAUD_1M             = TPCANBaudrate(0x0014) #   1 MBit/s
PCAN_BAUD_800K           = TPCANBaudrate(0x0016) # 800 kBit/s
PCAN_BAUD_500K           = TPCANBaudrate(0x001C) # 500 kBit/s
PCAN_BAUD_250K           = TPCANBaudrate(0x011C) # 250 kBit/s
PCAN_BAUD_125K           = TPCANBaudrate(0x031C) # 125 kBit/s
PCAN_BAUD_100K           = TPCANBaudrate(0x432F) # 100 kBit/s
PCAN_BAUD_95K            = TPCANBaudrate(0xC34E) #  95,238 kBit/s
PCAN_BAUD_83K            = TPCANBaudrate(0x4B14) #  83,333 kBit/s
PCAN_BAUD_50K            = TPCANBaudrate(0x472F) #  50 kBit/s
PCAN_BAUD_47K            = TPCANBaudrate(0x1414) #  47,619 kBit/s
PCAN_BAUD_33K            = TPCANBaudrate(0x1D14) #  33,333 kBit/s
PCAN_BAUD_20K            = TPCANBaudrate(0x532F) #  20 kBit/s
PCAN_BAUD_10K            = TPCANBaudrate(0x672F) #  10 kBit/s
PCAN_BAUD_5K             = TPCANBaudrate(0x7F7F) #   5 kBit/s

# Supported No-Plug-And-Play Hardware types
#
PCAN_TYPE_ISA            = TPCANType(0x01)  # PCAN-ISA 82C200
PCAN_TYPE_ISA_SJA        = TPCANType(0x09)  # PCAN-ISA SJA1000
PCAN_TYPE_ISA_PHYTEC     = TPCANType(0x04)  # PHYTEC ISA 
PCAN_TYPE_DNG            = TPCANType(0x02)  # PCAN-Dongle 82C200
PCAN_TYPE_DNG_EPP        = TPCANType(0x03)  # PCAN-Dongle EPP 82C200
PCAN_TYPE_DNG_SJA        = TPCANType(0x05)  # PCAN-Dongle SJA1000
PCAN_TYPE_DNG_SJA_EPP    = TPCANType(0x06)  # PCAN-Dongle EPP SJA1000
    
# Represent the PCAN-TP error and status codes 
#
PCANTP_ERROR_OK                    = TPCANStatus(0x00000)  # No error 
PCANTP_ERROR_NOT_INITIALIZED       = TPCANStatus(0x00001)  # Transmit buffer in CAN controller is full
PCANTP_ERROR_ALREADY_INITIALIZED   = TPCANStatus(0x00002)  # CAN controller was read too late
PCANTP_ERROR_NO_MEMORY             = TPCANStatus(0x00003)  # Bus error: an error counter reached the 'light' limit
PCANTP_ERROR_OVERFLOW              = TPCANStatus(0x00004)  # Bus error: an error counter reached the 'heavy' limit
PCANTP_ERROR_TIMEOUT               = TPCANStatus(0x00005)  # Bus error: the CAN controller is in bus-off state
PCANTP_ERROR_NO_MESSAGE            = TPCANStatus(0x00007)  # Mask for all bus errors
PCANTP_ERROR_WRONG_PARAM           = TPCANStatus(0x00008)
PCANTP_ERROR_BUSLIGHT              = TPCANStatus(0x00009)
PCANTP_ERROR_BUSHEAVY              = TPCANStatus(0x0000A)
PCANTP_ERROR_BUSOFF                = TPCANStatus(0x0000B)
PCANTP_ERROR_CAN_ERROR             = TPCANStatus(0x80000000)



# PCAN message types
#
PCANTP_MESSAGE_UNKNOWN              = TPCANMessageType(0x00)  # The PCAN message is a CAN Standard Frame (11-bit identifier)
PCANTP_MESSAGE_DIAGNOSTIC           = TPCANMessageType(0x01)  # The PCAN message is a CAN Remote-Transfer-Request Frame
PCANTP_MESSAGE_REMOTE_DIAGNOSTIC    = TPCANMessageType(0x02)  # The PCAN message is a CAN Extended Frame (29-bit identifier)
PCANTP_MESSAGE_REQUEST_CONFIRMATION = TPCANMessageType(0x03)  # The PCAN message represents a PCAN status message
PCANTP_MESSAGE_INDICATION           = TPCANMessageType(0x04)

# Frame Type / Initialization Mode
#
PCAN_MODE_STANDARD       = TPCANType(0x01)  
PCAN_MODE_EXTENDED       = TPCANType(0x02)  


# Message definition
#
class TPCANTPMsg (Structure):
    """
    Represents a PCAN message
    """
    _fields_ = [ ("SA",      c_ubyte),
                 ("TA",      c_ubyte),
                 ("TA_TYPE", c_ubyte),
                 ("RA",      c_ubyte),
                 ("IDTYPE",  c_ubyte),
                 ("MSGTYPE", c_ubyte),
                 ("FORMAT",  c_ubyte),
                 ("DATA",    c_ubyte * 4095),      # Data of the message (DATA[0]..DATA[7])
                 ("LEN",     c_ushort),
                 ("RESULT",  c_ubyte)]

# Represents a timestamp of a received PCAN message
# Total Microseconds = micros + 1000 * millis + 0xFFFFFFFF * 1000 * millis_overflow
#
class TPCANTPTimestamp (Structure):
    """
    Represents a timestamp of a received PCAN message
    Total Microseconds = micros + 1000 * millis + 0xFFFFFFFF * 1000 * millis_overflow
    """
    _fields_ = [ ("millis", c_ulong),           # Base-value: milliseconds: 0.. 2^32-1
                 ("millis_overflow", c_ushort), # Roll-arounds of millis
                 ("micros", c_ushort) ]         # Microseconds: 0..999

#///////////////////////////////////////////////////////////
# PCAN-Basic API function declarations
#///////////////////////////////////////////////////////////

# PCAN-Basic API class implementation
#
class PCANISOTP:
    """
      PCAN-Basic API class implementation
    """      
    def __init__(self):
        # Loads the PCANBasic.dll
        #     
        self.__m_dllBasic = windll.LoadLibrary(".\PCAN-ISO-TP.dll")
        #self.__m_dllBasic = windll.LoadLibrary("PCANBasic.dll")        
        #print (self.__m_dllBasic)
        if self.__m_dllBasic == None:
            print ("Exception: The PCAN-ISO-TP DLL couldn't be loaded!")

    # Initializes a PCAN Channel
    #
    def CANTP_Initialize(
        self,
        Channel,   
        Btr0Btr1,  
        HwType = TPCANType(0),  
        IOPort = c_uint(0),
        Interrupt = c_ushort(0)):
        
        """
          Initializes a PCAN Channel

        Parameters:
          Channel  : A TPCANHandle representing a PCAN Channel
          Btr0Btr1 : The speed for the communication (BTR0BTR1 code)
          HwType   : NON PLUG&PLAY: The type of hardware and operation mode
          IOPort   : NON PLUG&PLAY: The I/O address for the parallel port
          Interrupt: NON PLUG&PLAY: Interrupt number of the parallel port
        
        Returns:
          A TPCANStatus error code
        """
        try:
            res = self.__m_dllBasic.CANTP_Initialize(Channel,Btr0Btr1,HwType,IOPort,Interrupt)
            return TPCANStatus(res)
        except:
            print ("Exception on PCANISPTP.Initialize")
            raise
        
    #  Uninitializes one or all PCAN Channels initialized by CAN_Initialize
    #
    def CANTP_Uninitialize(
        self,
        Channel):

        """
          Uninitializes one or all PCAN Channels initialized by CAN_Initialize
          
        Remarks:
          Giving the TPCANHandle value "PCAN_NONEBUS", uninitialize all initialized channels
          
        Parameters:
          Channel  : A TPCANHandle representing a PCAN Channel
        
        Returns:
          A TPCANStatus error code
        """
        try:
            res = self.__m_dllBasic.CANTP_Uninitialize(Channel)
            return TPCANStatus(res)
        except:
            print ("Exception on PCANISPTP.Uninitialize")
            raise

    #  Resets the receive and transmit queues of the PCAN Channel
    #
    def CANTP_Reset(
        self,
        Channel):

        """
          Resets the receive and transmit queues of the PCAN Channel
          
        Remarks:
          A reset of the CAN controller is not performed
          
        Parameters:
          Channel  : A TPCANHandle representing a PCAN Channel
        
        Returns:
          A TPCANStatus error code
        """
        try:
            res = self.__m_dllBasic.CANTP_Reset(Channel)
            return TPCANStatus(res)
        except:
            print ("Exception on PCANISPTP.Reset")
            raise
            
    #  Gets the current status of a PCAN Channel
    #
    def CANTP_GetStatus(
        self,
        Channel):

        """
          Gets the current status of a PCAN Channel
          
        Parameters:
          Channel  : A TPCANHandle representing a PCAN Channel
        
        Returns:
          A TPCANStatus error code
        """
        try:
            res = self.__m_dllBasic.CANTP_GetStatus(Channel)
            return TPCANStatus(res)
        except:
            print ("Exception on PCANISPTP.GetStatus")
            raise

    # Reads a CAN message from the receive queue of a PCAN Channel
    #
    def CANTP_Read(
        self,
        Channel,
        MessageBuffer,
        TimestampBuffer):

        """
          Reads a CAN message from the receive queue of a PCAN Channel

        Remarks:
          The return value of this method is a 3-touple, where 
          the first value is the result (TPCANStatus) of the method.
          The order of the values are:
          [0]: A TPCANStatus error code
          [1]: A TPCANMsg structure with the CAN message read
          [2]: A TPCANTimestamp structure with the time when a message was read
          
        Parameters:
          Channel  : A TPCANHandle representing a PCAN Channel
        
        Returns:
          A touple with three values
        """
        try:
            msg = TPCANTPMsg()
            timestamp = TPCANTPTimestamp()
            res = self.__m_dllBasic.CANTP_Read(Channel,byref(msg),byref(timestamp))
            return TPCANStatus(res),msg,timestamp
        except:
            print ("Exception on PCANISPTP.Read")
            raise           

    # Transmits a CAN message 
    #
    def CANTP_Write(
        self,
        Channel,
        MessageBuffer):

        """
          Transmits a CAN message 
          
        Parameters:
          Channel      : A TPCANHandle representing a PCAN Channel
          MessageBuffer: A TPCANMsg representing the CAN message to be sent
        
        Returns:
          A TPCANStatus error code
        """
        try:
            res = self.__m_dllBasic.CANTP_Write(Channel,byref(MessageBuffer))
            return TPCANStatus(res)
        except:
            print ("Exception on PCANISPTP.Write")
            raise


    # Retrieves a PCAN Channel value 
    #
    def CANTP_GetValue(
        self,
        Channel,
        Parameter,
        Buffer,
        BufferLength):

        """
          Retrieves a PCAN Channel value

        Remarks:
          Parameters can be present or not according with the kind
          of Hardware (PCAN Channel) being used. If a parameter is not available,
          a PCAN_ERROR_ILLPARAMTYPE error will be returned.
          
          The return value of this method is a 2-touple, where 
          the first value is the result (TPCANStatus) of the method and
          the second one, the asked value 
          
        Parameters:
          Channel   : A TPCANHandle representing a PCAN Channel
          Parameter : The TPCANParameter parameter to get
        
        Returns:
          A touple with 2 values
        """        
        try:
            if Parameter == PCAN_API_VERSION or Parameter == PCAN_CHANNEL_VERSION or Parameter == PCAN_LOG_LOCATION:
                mybuffer = create_string_buffer(256)
            else:
                mybuffer = c_int(0)

            res = self.__m_dllBasic.CAN_GetValue(Channel,Parameter,byref(mybuffer),sizeof(mybuffer))
            return TPCANStatus(res),mybuffer.value
        except:
            print ("Exception on PCANISPTP.GetValue")
            raise            

    # Returns a descriptive text of a given TPCANStatus
    # error code, in any desired language
    #
    def CANTP_SetValue(
        self,
        Channel,
        Parameter,
        Buffer,
        BufferLength):

        """
          Returns a descriptive text of a given TPCANStatus error
          code, in any desired language

        Remarks:
          Parameters can be present or not according with the kind
          of Hardware (PCAN Channel) being used. If a parameter is not available,
          a PCAN_ERROR_ILLPARAMTYPE error will be returned.
          
        Parameters:
          Channel      : A TPCANHandle representing a PCAN Channel
          Parameter    : The TPCANParameter parameter to set
          Buffer       : Buffer with the value to be set
          BufferLength : Size in bytes of the buffer
        
        Returns:
          A TPCANStatus error code
        """        
        try:
            if Parameter == PCAN_LOG_LOCATION or Parameter == PCAN_LOG_TEXT:
                mybuffer = create_string_buffer(256)
            else:
                mybuffer = c_int(0)

            mybuffer.value = Buffer
            res = self.__m_dllBasic.CAN_SetValue(Channel,Parameter,byref(mybuffer),sizeof(mybuffer))
            return TPCANStatus(res)
        except:
            print ("Exception on PCANISPTP.SetValue")
            raise

    def CANTP_GetErrorText(
        self,
        Error,
        Language = 0):

        """
          Configures or sets a PCAN Channel value

        Remarks:

          The current languages available for translation are:
          Neutral (0x00), German (0x07), English (0x09), Spanish (0x0A),
          Italian (0x10) and French (0x0C)          

          The return value of this method is a 2-touple, where 
          the first value is the result (TPCANStatus) of the method and
          the second one, the error text
          
        Parameters:
          Error    : A TPCANStatus error code
          Language : Indicates a 'Primary language ID' (Default is Neutral(0))
        
        Returns:
          A touple with 2 values
        """  
        try:
            mybuffer = create_string_buffer(256)
            res = self.__m_dllBasic.CAN_GetErrorText(Error,Language,byref(mybuffer))
            return TPCANStatus(res),mybuffer.value
        except:
            print ("Exception on PCANISPTP.GetErrorText")
            raise            


    def CANTP_AddMapping(
        self,
        Channel,
        canId,
        canIDResponse,
        canIdType,
        formatType,
        msgType,
        sourceAddr,
        targetAddr,
        targetType,
        remoteAddr):
        try:
            res = self.__m_dllBasic.CANTP_AddMapping(Channel,canId,canIDResponse,canIdType,formatType,msgType,sourceAddr,targetAddr,targetType,remoteAddr)
        except:
            print ("Exception on PCANISPTP.CANTP_AddMapping")
            raise

    def CANTP_RemoveMapping(
        self,
        Channel,
        canId):
        try:
            res = self.__m_dllBasic.CANTP_RemoveMapping(Channel,canId)
        except:
            print ("Exception on PCANISPTP.CANTP_RemoveMapping")
            raise




























