# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 07:56:06 2020

@author: ThomasBitskyJr
(C) Copyright 2019-2020 Automated Design Corp. All Rights Reserved.

Flexible software trigger for use with DAQ applications. Supprts
RISING EDGE, FALLING EDGE, ABOVE LEVEL and BELOW LEVEL triggers.
Uses hysteresys to avoid false triggers.
"""



import logging

from enum import Enum
from time import perf_counter as pc
import numpy as np



class TriggerMode(Enum):
    Single:int = 0,				# the trigger will run disable itself after being triggered once
    Repeating:int = 1			# the trigger will remain enabled until disabled
    FiniteRepeating:int = 2    	# the trigger will remain enabled until disabled... for a set amount of times.
    Continuous:int = 10			# the trigger will always signal that it's true

    
class TriggerSensitivity(Enum):
    RisingEdge:int = 0
    FallingEdge:int = 1
    AboveLevel:int = 2
    BelowLevel:int = 3
    EQLevel:int = 4
    NELevel:int = 5
    HighLevel:int = 6
    LowLevel:int = 7
    

class SoftwareTrigger:
    
    
    def __init__(self):
        self.mode:TriggerMode = TriggerMode.Repeating
        self.sensitivity:TriggerSensitivity = TriggerSensitivity.RisingEdge
        self.setPoint:float = 0.0
        
        # dead time to ignore a trigger after it's been activated.
        self.deadTimeSec:int = 1
        
        # set number of seconds to timeout waiting for a trigger to happen.
        self.timeoutSec:int = 30;
        
        self.isDeadTimeActive:bool = False
        
        self.deadTimeStart = pc()
        self.timeoutStart = pc()
        
        self.isTriggered:bool = False
        
        self.captureLength:int = 1000
        self.preTriggerLength:int = 10
        
        self.isEnabled:bool = False
        
        # Index of the column in the data to monitor
        self.columnIndex = -1
        
        self.npData = None
        self.pretrigger_buffer = None

        self.hysteresis_rows:int = 100
        
           
    def enable(self):
        """ Activate the trigger to start monitoring the values
        """
        
        
        self.timeoutStart = pc()
        self.isTriggered = False
        self.isEnabled = True
        
        # @todo emit an enabled signal
        
    def disable(self):
        """Stop the trigger from monitoring values.
        """
        
        self.isEnabled = False
        
        self.isDeadTimeActive = False
        self.isTriggered = False
        
        # @todo: emit disabled signal
        
        
    def process(self, data : np.array ) -> bool:
        """Check and update the status of the trigger.
        
            Returns True if capture is complete and 
            data should be exported.
        """
        
        if not self.isEnabled or self.columnIndex < 0:
            logging.debug("Trigger not enabled")
            return False
        
        ret:bool = False
                
        # Do no re-trigger during dead time, but don't start counting
        # the dead time until the trigger has become false.
        if self.isDeadTimeActive:
            if self.check_trigger(data) < 0:
                
                logging.debug("Trigger value lost...")
                
                timeSpan = pc() - self.deadTimeStart
                
                if ( timeSpan >= self.deadTimeSec ):
                    logging.debug("Dead time no longer active.")
                    self.isDeadTimeActive = False
                    
                    
            else:
                # don't start counting the dead time until we lose trigger
                # condition
                self.deadTimeStart = pc()
        
        else:
            
            if not self.isTriggered:
                idx = self.check_trigger(data)
                
                if idx >= 0:
                    logging.debug(f"Appending data from {idx}")
                    ret = self.append_data(idx, data)
                
            else:
                ret = self.append_data(0,data)

        # buffer for the pre-trigger in case the triggger event
        # happens early in the next block of data
        # we copy a slice of the last data row that should cover the length of the pre-trigger
        self.pretrigger_buffer = np.array(data[-(self.preTriggerLength):])


        return ret


    def check_positive_hysteresis(self, data:np.array) -> int:
        """ Evaluate a trigger transitioning to the positive
        direction with hysteresis considered.

        If hysteresis_rows member is <= 0, then hysteresis is ignored
        and only a simple check is performed.
        """

        ret:int = -1
        idx:np.array = np.argwhere(data[:,self.columnIndex] > self.setPoint)

        if self.hysteresis_rows > 0:
            invidx:np.array = np.argwhere(data[:,self.columnIndex] <= self.setPoint)
            invdiff:np.array = np.diff(invidx).flatten()
            invhys:np.array = np.argwhere(invdiff >= self.hysteresis_rows)


            if ( np.shape(invhys)[0] > 0 ):
                ret = invhys[0][0]
            else:
                if np.shape(idx)[0] > 0 and np.shape(invidx)[0] > 0:
                    if ( (idx[-1][0] - invidx[-1][0]) >= self.hysteresis_rows ):
                        ret = invidx[-1][0] + 1
                elif np.shape(idx)[0] > 0: 
                    #no noise, just solid signal
                    ret = idx[0][0]

        else:
            if idx.size > 0:
                logging.debug(f"Trigger Index: {idx[0][0]} {data[idx[0][0]][self.columnIndex]}")
                ret = idx[0][0]


        return ret



    def check_negative_hysteresis(self, data:np.array) -> int:
        """ Evaluate a trigger transitioning to the positive
        direction with hysteresis considered.

        If hysteresis_rows member is <= 0, then hysteresis is ignored
        and only a simple check is performed.
        """

        ret:int = -1
        idx:np.array = np.argwhere(data[:,self.columnIndex] < self.setPoint)

        if self.hysteresis_rows > 0:
            invidx:np.array = np.argwhere(data[:,self.columnIndex] >= self.setPoint)
            invdiff:np.array = np.diff(invidx).flatten()
            invhys:np.array = np.argwhere(invdiff >= self.hysteresis_rows)


            if ( np.shape(invhys)[0] > 0 ):
                ret = invhys[0][0]
            else:
                if np.shape(idx)[0] > 0 and np.shape(invidx)[0] > 0:
                    if ( (idx[-1][0] - invidx[-1][0]) >= self.hysteresis_rows ):
                        ret = invidx[-1][0] + 1
                elif np.shape(idx)[0] > 0: 
                    #no noise, just solid signal
                    ret = idx[0][0]

        else:
            if idx.size > 0:
                logging.debug(f"Trigger Index: {idx[0][0]} {data[idx[0][0]][self.columnIndex]}")
                ret = idx[0][0]


        return ret



    
    def check_trigger(self, data:np.array) -> int:
        """Checks for a value having passed the trigger based
            upon the sensitivity type.
            
            Returns index if trigger has occurred, -1 if not.
        """
        
        idx = np.array([0])
        
        if self.sensitivity == TriggerSensitivity.RisingEdge:     

            #idx = np.argwhere(data[:,self.columnIndex] > self.setPoint)
            return self.check_positive_hysteresis(data)

        elif self.sensitivity == TriggerSensitivity.FallingEdge:            

            #idx = np.argwhere(data[:,self.columnIndex] < self.setPoint)
            return self.check_negative_hysteresis(data)

        elif self.sensitivity == TriggerSensitivity.AboveLevel:

            if not self.isTriggered:
                #idx = np.argwhere(data[:,self.columnIndex] > self.setPoint)
                return self.check_positive_hysteresis(data)
            else:
                #idx = np.argwhere(data[:,self.columnIndex] < self.setPoint)
                return self.check_negative_hysteresis(data)

        elif self.sensitivity == TriggerSensitivity.BelowLevel:

            if not self.isTriggered:
                #idx = np.argwhere(data[:,self.columnIndex] < self.setPoint)
                return self.check_negative_hysteresis(data)
            else:
                #idx = np.argwhere(data[:,self.columnIndex] > self.setPoint)            
                return self.check_positive_hysteresis(data)

        else:
            raise NotImplementedError(
                "Selected trigger not supported at this time."
                )
            
        raise "!!Unexpected behavior!!"
        """
        if idx.size > 0:
            logging.debug(f"Trigger Index: {idx[0][0]} {data[idx[0][0]][self.columnIndex]}")
            return idx[0][0]
        
        else:
            logging.debug(f"Nothing found!: {idx}") 
            return -1           
            
        """
     
        

    def append_data(self, start: int, data:np.array) -> bool:
        """Append data to the internal buffer.
        
        Slices the incoming numpy array, accounting
        for pretrigger and capacity settings. The hope is that this
        will be faster and more straight-forward than a traditional
        ring-buffer.
        
        This function should manage the isTriggered member. It will set the
        value true when starting data anew, then turn it off when all data
        has been captured. This allows us to properly manage the pre-trigger.
        
        Note that the slice command returns a VIEW of the original
        Numpy array, not a new copy. We need to make sure that we make a
        copy of that slice so that, after this function returns and the data
        is changed, our underlying values aren't affected.
        """       
        
        
        dataRowCount = np.shape(data)[0]
        
        trigger_done = False
        
        if not self.isTriggered:

            print( f"Starting trigger at: {start}  {data[start]}")

            triggerIndex = start

            start = start - self.preTriggerLength
           

            # if start - self.preTriggerLength < 0:
            #     start = 0
            # else:
            #     start = start - self.preTriggerLength


            print(f"Sensitivity {self.sensitivity}")


            if self.sensitivity == TriggerSensitivity.AboveLevel \
                or self.sensitivity == TriggerSensitivity.BelowLevel:     

                # marks as triggered to the check_trigger function
                # works in the opposite direction
                self.isTriggered = True

                MINIMUM_CAPTURE_LEN = 100

                # check for the end of data in this data block
                idx = self.check_trigger(data[triggerIndex + MINIMUM_CAPTURE_LEN :])

                if ( idx >= 0 ):
                    # end of data found
                    end = (triggerIndex + MINIMUM_CAPTURE_LEN + idx)

                    if ( start < 0 ):
                        self.npData = np.append(self.pretrigger_buffer[start:], np.array(data[0:end]),axis=0)
                    else:
                        self.npData = np.array(data[start:end])

                    trigger_done = True
                    print( f"Ending trigger immediately  at: {end} {data[end]} {np.shape(self.npData)}")

                else:
                    # there is no end to the data in this data block
                    # add it all
                    if ( start < 0 ):
                        self.npData = np.append(self.pretrigger_buffer[start:], np.array(data[0:]),axis=0)
                    else:
                        self.npData = np.array(data[start:])

            else:
                end = start + self.captureLength
                
                if end > (dataRowCount - 1):
                    end = dataRowCount
                else:
                    trigger_done = True
                    
                self.npData = np.array(data[start:end])
                
                #print(f"create {np.shape(self.npData)}")
                
                self.isTriggered = True
            
        else:
            

            if self.sensitivity == TriggerSensitivity.AboveLevel \
                or self.sensitivity == TriggerSensitivity.BelowLevel:

                print ( f"datasize {np.shape(data)} buffersize {np.shape(self.npData)}")
                idx = self.check_trigger(data)

                

                if ( idx >= 0 ):
                    # end of data found
                    print ( f"index at end: {idx}  {data[idx]}")
                    self.npData = np.append(self.npData, np.array(data[0:idx]),axis=0)
                    trigger_done = True
                    print( f"Ending trigger finally at: {idx} {data[idx]} {np.shape(self.npData)}")
                else:
                    # there is no end to the data in this data block
                    # add it all
                    self.npData = np.append(self.npData, np.array(data),axis=0)


            else:
                nRemaining = self.captureLength - np.shape(self.npData)[0]
                self.npData = np.append(self.npData, np.array(data[0:nRemaining]),axis=0)

                if np.shape(self.npData)[0] >= self.captureLength:
                    trigger_done = True
            
            #print(f"append {nRemaining}  {np.shape(self.npData)}")
            
            
        
        ret:bool = False
        
        if self.isTriggered:
            
            if trigger_done:
                
                self.isTriggered = False
                
                # we've collected all data. activate the dead time
                self.deadTimeStart = pc()
                self.isDeadTimeActive = True
                
                if self.mode == TriggerMode.Single:
                    self.isEnabled = False                
                
                ret = True
            
        return ret        
            
            
        
        
        
        
        
        