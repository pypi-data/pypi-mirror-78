# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 21:49:50 2018

@author: ThomasBitskyJr


Uses pyads:
https://pyads.readthedocs.io/en/latest/quickstart.html#usage


Usage:
    
    from ads import AdsClient
    
    tags_ = [{"name": "GM.trayHomeOffsetWidth", "type": pyads.PLCTYPE_REAL},
         {"name": "GM.manualPressureCommand", "type": pyads.PLCTYPE_INT},
         {"name": "GM.isControlPower", "type": pyads.PLCTYPE_BOOL},
         {"name": "GM.intSim", "type": pyads.PLCTYPE_INT},
         {"name": "GM.floatSim", "type": pyads.PLCTYPE_REAL},
         {"name": "GM.dblSim", "type": pyads.PLCTYPE_LREAL}]
    
    
    
"""

import time

import pyads
import pyads.filetimes

from ctypes import memmove, addressof
import struct

from ctypes import pointer, c_ubyte, c_ulong, c_ushort, sizeof, c_char_p, Structure, \
    c_bool, c_byte, c_int8, c_uint8, c_int16, c_uint16, \
    c_int32, c_uint32, c_float, c_double, c_char, c_short, c_int64, c_uint64, \
    c_int64

from struct import Struct

import numpy as np

import asyncio
from adcopen.events import Events
import logging

import configparser






# stores the notification handles of a tag
#handles_ = []

#plc_ = pyads.Connection("5.38.60.194.1.1", 851)
#plc_.open()

class SAdsSymbolEntry(Structure):

    """
    ADS symbol information
    :ivar entryLength: length of complete symbol entry
    :ivar iGroup: indexGroup of symbol: input, output etc.
    :ivar iOffs: indexOffset of symbol
    :ivar size: size of symbol (in bytes, 0=bit)
    :ivar dataType: adsDataType of symbol
    :ivar flags: symbol flags
    :ivar nameLength: length of symbol name
    :ivar typeLength: length of type name
    :ivar commentLength: length of comment
    """
    _pack_ = 1
    _fields_ = [("entryLength", c_ulong),
                ("iGroup", c_ulong),
                ("iOffs", c_ulong),
                ("size", c_ulong),
                ("dataType", c_ulong),
                ("flags", c_ulong),
                ("nameLength", c_ushort),
                ("typeLength", c_ushort),
                ("commentLength", c_ushort)]



'''
' ADS Constants for data types.
'''
ADST_VOID     = 0
ADST_INT8     = 16
ADST_UINT8    = 17
ADST_INT16    = 2
ADST_UINT16   = 18
ADST_INT32    = 3
ADST_UINT32   = 19
ADST_INT64    = 20
ADST_UINT64   = 21
ADST_REAL32   = 4
ADST_REAL64   = 5
ADST_BIGTYPE  = 65
ADST_STRING   = 30
ADST_WSTRING  = 31
ADST_REAL80   = 32
ADST_BIT      = 33



ADST_TYPE_TO_PLC_TYPE:dict = {
    ADST_VOID : None,
    ADST_BIT: pyads.PLCTYPE_BOOL,    
    ADST_INT8: pyads.PLCTYPE_SINT,
    ADST_UINT8 : pyads.PLCTYPE_USINT,
    ADST_INT16: pyads.PLCTYPE_INT,
    ADST_UINT16: pyads.PLCTYPE_UINT,
    ADST_INT32: pyads.PLCTYPE_DINT,
    ADST_UINT32: pyads.PLCTYPE_UDINT,
    ADST_UINT64: pyads.PLCTYPE_ULINT,
    ADST_INT64: c_int64,
    ADST_REAL32: pyads.PLCTYPE_REAL,
    ADST_REAL64: pyads.PLCTYPE_LREAL,
    ADST_STRING: pyads.PLCTYPE_STRING,
    ADST_WSTRING: pyads.PLCTYPE_STRING,
    ADST_REAL80: pyads.PLCTYPE_LREAL ,
    ADST_BIGTYPE: None
}


class AdsClient():
    
    # constructor
    def __init__(self, options:configparser.ConfigParser=configparser.ConfigParser()) -> None:
        if "AmsNetId" in options:
            # connect to TwinCAT on a remote machine
            amsNetId = options.get("AmsNetId")
        else:
            # connect to local machine instance
            amsNetId ="127.0.0.1.1.1"

        if len(amsNetId) <= 0:
            # pyads doesn't handle empty strings properly
            amsNetId ="127.0.0.1.1.1"
            
        if "port" in options:
            port = options.getint("port")
        else:
            # The default PLC port
            port = 851


        self.handles_ = {}
        self.handlesByName_ = {}


        self.plc_ = pyads.Connection(amsNetId, port)




        self.rootLogger_ = logging.getLogger('')


    """
    async def asyncHandleDataReceived(self, name, value, timestamp):
        print(
                '{0}: received new notitifiction for variable "{1}", value: {2}'
                .format(timestamp, name, value)
        )
        if "name" in self.handlesByName_.keys():
            self.handlesByName_[name].set("value", value)
        
        # await Event.publish(name, value)
        args = {"name": name, "value": value}
        Events.publish("ads-dataChange", args)

    def handleDataReceived(self, name, value, timestamp):

        print(f"handleDataReceived {name} {value}")

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        task = loop.create_task(self.asyncHandleDataReceived(name, value, timestamp))
        loop.run_until_complete(task)

        #asyncio.run_coroutine_threadsafe(asyncHandleDataReceived(name, value, timestamp), loop)
    """

    def handleDataReceived(self, name, value, timestamp):

        args = {"name": name, "value": value}
        Events.publish("ads-dataChange", args)


    def datachange_callback(self, notification, data):
        """A generic callback to receive datachange notitications from pyads.
        Uses the handle data_type information we already have to use the pyads
        parse_notification method.
        """

        #print(f"Datachange callback {data}")

        handle = self.handlesByName_[data]

        handle, timestamp, value = self.plc_.parse_notification(notification, handle["type"])
        self.handleDataReceived(data, value, timestamp)

    def addTag(self, tag, notify=True):

        '''
        if (not 'type' in tag.keys() or
            not 'name' in tag.keys() ):
                return
        '''

        if not isinstance(tag, dict):
            raise "Tag argument must be a dict."
        
        if not 'name' in tag.keys():
            raise "Tag name required!"

        '''
        ' Don't re-register if this tag was already requested.
        ' Not an error, so just return gracefully.
        '''
        if tag.get('name') in self.handlesByName_.keys():
            logging.info( "Tag {0} already registered. Ya' basic.". format(tag.get("name")))
            return


        # cycle time should be a real number that comes in milliseconds

        if 'cycleTime' in tag.keys():

            cycleTime = tag.get('cycleTime')
            # print( "cycleTIme {0} tag {1}".format(cycleTime, tag.get("name")))


        else:
            # our interface shouldn't need anything over 100ms
            # If a tag needs more update, send in a cycleTime of 0
            cycleTime = 100


        try:
            tagInfo = self.readSymbol(tag.get("name"))
        except:
            logging.error( "The request tag name {0} does not exist. Dick.".format(tag.get("name")))
            return
             


        '''
        ADST_INT8     = 16
        ADST_UINT8    = 17
        ADST_INT16    = 2
        ADST_UINT16   = 18
        ADST_INT32    = 3
        ADST_UINT32   = 19
        ADST_INT64    = 20
        ADST_UINT64   = 21
        ADST_REAL32   = 4
        ADST_REAL64   = 5
        ADST_BIGTYPE  = 65
        ADST_STRING   = 30
        ADST_WSTRING  = 31
        ADST_REAL80   = 32
        ADST_BIT      = 33
        '''

      

        handle = -1
        user = -1
        tagType = None


        logging.info( "adding notification: {0} {1}".format(tag.get("name"), tagInfo.dataType )) 

        if tagInfo.dataType in ADST_TYPE_TO_PLC_TYPE:
            tagType = ADST_TYPE_TO_PLC_TYPE[tagInfo.dataType]
        else:
            raise "This type is unsupported."
        

        if notify:
            """API changes in pyads:
            - cycle_time and max_delay are now in milliseconds
            - arguments of datachange_callback have changed.
            """

            handle, user = self.plc_.add_device_notification(
                    tag.get("name"), 
                    pyads.NotificationAttrib(sizeof(tagType), cycle_time=cycleTime, max_delay=cycleTime), 
                    self.datachange_callback
                    )

            logging.info(f"added notify: {handle} {user} {sizeof(tagType)}")
            
        self.handles_[handle] = ({"handle": handle, "user": user, "name": tag.get("name"), 
            "value": 0, "type": tagType })
        self.handlesByName_[tag.get("name")] = self.handles_[handle]    


    
    #tags is an array of dictionaries
    def loadTags(self,tags):
        
        logging.info( "Adding tags from dictionay..." )
        
        shouldExit = False

        while not shouldExit:
            try:
                '''
                handle = -1
                user = -1
                for i in range(len(tags)):
                    if tags[i].get("type") == pyads.PLCTYPE_BOOL:
                        handle, user = self.plc_.add_device_notification(
                                tags[i].get("name"), 
                                pyads.NotificationAttrib(1), 
                                AdsClient.dataChange_bool)
            
                    elif tags[i].get("type") == pyads.PLCTYPE_INT:
                        handle, user = self.plc_.add_device_notification(
                                tags[i].get("name"), 
                                pyads.NotificationAttrib(2), 
                                AdsClient.dataChange_int)
            
                    elif tags[i].get("type") == pyads.PLCTYPE_REAL:
                        handle, user = self.plc_.add_device_notification(
                                tags[i].get("name"), 
                                pyads.NotificationAttrib(4), 
                                AdsClient.dataChange_real)
                        
                    elif tags[i].get("type") == pyads.PLCTYPE_LREAL:
                        handle, user = self.plc_.add_device_notification(
                                tags[i].get("name"), 
                                pyads.NotificationAttrib(8), 
                                AdsClient.dataChange_lreal)
            
                    #handles_.append({"handle": handle, "user": user})
                    handles_[handle] = ({"handle": handle, "user": user, "name": tags[i].get("name")})
                    '''

                for i in range(len(tags)):

                    self.addTag(tags[i])
                    shouldExit = True

            except pyads.pyads_ex.ADSError:
                logging.warning( "Communication error. Retrying...")
                time.sleep(2)
            except:
                raise Exception("Critical communications error.")


            

    # handles provides an array of notification handles
    def unloadTags(self):
        
        logging.info( "Removing tags...")
        
        for key, value in self.handles_.items():

            if ( value.get("handle") > 0 ):
                logging.info ( "removing handle {0} {1}"
                    .format(value.get("handle"), value.get("user") )
                    )               
                self.plc_.del_device_notification(value.get("handle"), value.get("user"))
            
            
        logging.info( "Handles are removed...")


    '''
    ' Refresh any stale values for registered notification tags by
    ' doing a synchrnous read of the tag in the plc.
    '''
    async def refreshAll(self):
        
        for key, value in self.handlesByName_.items():

            try:
                logging.info( "refresh {0} {1}".format(key, value.get("type")))
                value = self.plc_.read_by_name(key, value.get("type"))
            except:
                value = 0

            args = {"name": key, "value": value}
            await Events.publish("ads-dataChange", args)


    async def refresh(self, tagName):

        if tagName in self.handlesByName_.keys():
            tag = self.handlesByName_[tagName]

            try:
                value = self.plc_.read_by_name(tagName, tag.get("type"))

                args = {"name": tagName, "value": value}
                await Events.publish("ads-dataChange", args)            

            except:
                logging.error( "Failure to refresh tag {0}".format(tagName))


     
    # start a connection to the remote server
    def connect(self):
        self.plc_.open()


    def close(self):
        self.plc_.close()



    def readSymbol(self, name):

        err_code = 0

        try:

            address = self.plc_._adr

            '''
            ' Updated 2018 08 22
            ' Newer version of pyads changed the api to use AdsSyncReadWriteReqEx2 instead
            ' of AdsSyncReadWriteReq, and also changed the name of the file, so pyads.pyads becomes
            ' pyads.pyads_ex
            '''
            adsSyncReadWriteReqFct = pyads.pyads_ex._adsDLL.AdsSyncReadWriteReqEx2


            ADSIGRP_SYM_INFOBYNAMEEX = 0xF009
            #bufferSize = 0xFFFF
            # rdata =  c_ulong * bufferSize  # bytearray(0xFFFF)
            rdata = SAdsSymbolEntry()


            pAmsAddr = pointer(address.amsAddrStruct())
            nIndexGroup = c_ulong(ADSIGRP_SYM_INFOBYNAMEEX)
            nIndexOffset = c_ulong(0)

            #readData = plcReadDataType()
            nReadLength = c_ulong(sizeof(rdata))


            # We got the name as unicode string (python 3)
            # we have to convert it to ascii
            ascii_string = name.encode()
            data = c_char_p(ascii_string)
            data_length = len(name) + 1


            '''
            ' Updated 2018 08 22
            ' Newer version of pyads changed the api to use AdsSyncReadWriteReqEx2 instead
            ' of AdsSyncReadWriteReq, so we have to send the port number return by adsOpenPortEx
            ' as the first argument.
            '''
            port = self.plc_._port
            # print( "port: {0}".format(port))



            '''
            ' Updated 2018 08 22
            ' Newer version of pyads changed the api to use AdsSyncReadWriteReqEx2 instead
            ' of AdsSyncReadWriteReq. It returns the number of bytes returned in a pointer
            ' as the last argument.
            '''
            pcbReturn = c_ulong(0)

            err_code = adsSyncReadWriteReqFct(
                port,
                pAmsAddr, 
                nIndexGroup, 
                nIndexOffset, 
                nReadLength, 
                pointer(rdata),
                data_length, 
                data,
                pointer(pcbReturn)
            )

            # print ( "err_code: {0}".format(err_code))

        except:
            self.rootLogger_.exception("reading symbol information")
            
            

        if err_code:
            raise pyads.ADSError(err_code)
        else:            
            # print("Datatype: {0} nameLength: {1}".format(rdata.dataType, rdata.nameLength) ) 
            return rdata


    async def writeTag( self, tagName, value):

        if not tagName in self.handlesByName_.keys():

            try:
                # Fetch the tag properties, but don't register for notify.
                tagArg = {"name": tagName}
                self.addTag(tagArg, False)
            except:
                logging.error( "Failed to write tag {0} b/c I couldn't get it's information.".format(tagName))                



        if not tagName in self.handlesByName_.keys():
            logging.error( "Tag {0} was not found in PLC.".format(tagName))
            return
        
        tag = self.handlesByName_[tagName]

        try:
            #print( "{0} Value {1}   {2}".format(tagName, value, type(value)))
            self.plc_.write_by_name(tagName, value, tag.get("type"))
        except:
            logging.error( f"Failed to write tag {tagName} {value}")

        
    '''
    ' Flatten the array
    ' The matrix columns must match the order of the
    ' 2D array columns in TwinCAT
    '''
    async def write2dArray( self, tagName, matrix ):

        matRows = matrix.shape[0]
        matCols = matrix.shape[1]

        nLimit = matRows * matCols

        rc = np.zeros(nLimit)

        index = 0
        for i in range(matRows):
            for j in range(matCols):
                rc[index] = matrix.item(i,j)
                index += 1

        # @TODO: the library picks out the data type
        self.plc_.write_by_name(tagName, rc, pyads.PLCTYPE_ARR_LREAL(nLimit) )






'''
A script for testing this individual file. Only runs of the program is
started from this script.
'''
if __name__ == '__main__':


    def main_loop():
        while 1:
            # do your stuff...
            # print (plc.read_by_name("GM.trayHomeOffsetWidth", pyads.PLCTYPE_REAL))
            time.sleep(0.1)
        
    
    tags_ = [{"name": "GM.trayHomeOffsetWidth", "type": pyads.PLCTYPE_REAL},
             {"name": "GM.manualPressureCommand", "type": pyads.PLCTYPE_INT},
             {"name": "GM.isControlPower", "type": pyads.PLCTYPE_BOOL},
             {"name": "GM.intSim", "type": pyads.PLCTYPE_INT},
             {"name": "GM.floatSim", "type": pyads.PLCTYPE_REAL},
             {"name": "GM.dblSim", "type": pyads.PLCTYPE_LREAL}]
    
    try:
        
        # options = {"AmsNetId": "127.0.0.1.1.1", "port": 851}
        options = {}
        
        client = AdsClient(options)
        client.connect()

        val = client.plc_.read_by_name('GIO.AXIS_TT_Z.axis.position', pyads.PLCTYPE_LREAL)
        print( "Value {0}".format(val) )


        # client.loadTags(tags_)
        
        client.readSymbol("GIO.AXIS_TT_Z.axis.position")
        #client.addTag({"name":"GM.trayHomeOffsetWidth"})

        main_loop()
    except KeyboardInterrupt:
        print ( '\nExiting by user request.\n' )
        client.unloadTags()
        
        print ( '\nClosing the PLC....\n' )
        client.close()
        

