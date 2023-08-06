# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 14:48:13 2020

@author: ThomasBitskyJr
(C) Copyright 2020 Automated Design Corp. All Rights Reserved.

A simple one-to-many pub/sub class for supporting global events
and loose coupling of APIs. Uses asyncio for non-blocking publication
of events. 

Adapted from basicevents by agalera
Licensed under the GPL.
"""

import asyncio
import logging
import traceback
from typing import AnyStr, Callable

class Events(object):
    """A simple one-to-many pub/sub class for supporting global events.
    Requires asyncio
    
    @Usage:
        
        Asynchronous:
        
        @Events.subscribe("hello")
        async def example(*args, **kwargs):
            print ("recv signal, values:", args, kwargs)
        
        @Events.subscribe("hello")
        async def moreexample(*args, **kwargs):
            print ("I also recv signal, values:", args, kwargs)
            
        Events.publish("hello", "There")
        
        >>> recv signal, values: ("There",) {}
        >> I also recv signal, values: ("There",) {}
        
        
        Blocking:
        @Events.subscribe("hello")
        def example(*args, **kwargs):
            print ("recv signal, values:", args, kwargs)
        
        @Events.subscribe("hello")
        def moreexample(*args, **kwargs):
            print ("I also recv signal, values:", args, kwargs)
            
        Events.publishSync("hello", "There")
        
        >>> recv signal, values: ("There",) {}
        >> I also recv signal, values: ("There",) {}            
            
        
    """
    
    
    subs = {}


    @staticmethod
    def add_subscribe(event:str, func):
        if event not in Events.subs:
            Events.subs[event] = []

        loop = asyncio.get_event_loop()
        Events.subs[event].append({"func": func, "loop": loop})

    @staticmethod
    def subscribe_method(event:str, func:Callable) -> None:
        """Subscribe the method of a class instance to an event id.
        Can't use a decororator for this because 'self' won't be created.

        Not required for static methods. In that case, use the subscribe decorator.

        Parameters
        ----------
        event : str
            ID of the event
            
        func : function        
            The method/slot to call back. 
        """
        Events.add_subscribe(event,func)

    @staticmethod
    def subscribe(event:str) -> None:
        """Subscribe a function  to an event ID. 
        
        Parameters
        ----------
        event : str
            ID of the event
                
        """
               
        def wrap_function(func:Callable):

            Events.add_subscribe(event, func)
            return func
        return wrap_function


    @staticmethod
    def publish(event:str, *args, **kwargs):
        """Signal or publish values to all subscribers of the specified
        event ID. Asynchrnous. Returns immediately.
        
        """
        try:
            for ev in Events.subs[event]:
                try:
                    loop = ev["loop"] #asyncio.get_event_loop()

                    if loop.is_running():
                        asyncio.run_coroutine_threadsafe(
                            ev["func"](*args, **kwargs), loop
                            )
                    else:
                        #blocking
                        #print(f"event id {event} blocking with loop of {loop}")
                        #ev["func"](*args, **kwargs)
                        
                        try:
                            loop = asyncio.get_event_loop()
                            asyncio.run_coroutine_threadsafe(
                                ev["func"](*args, **kwargs), loop
                                )                        
                            ev["loop"] = loop
                        except:
                            logging.warning(f"event id {event} blocking with loop of {ev['loop']}")
                            ev["func"](*args, **kwargs)
                            

                    
                except:
                    logging.warning(traceback.format_exc())
        except:
            pass
        
        
    @staticmethod
    def publishSync(event:str, *args, **kwargs):
        """Signal or publish values to all subscribers of the specified
        event ID. SYNCHRNOUS AND BLOCKING.
        
        """
        try:
            for ev in Events.subs[event]:
                try:
                    ev["func"](*args, **kwargs)
                except:
                    Events.logger(traceback.format_exc())
        except:
            pass
        
        
"""
# avoids having to import Events
add_subscribe = Events.add_subscribe
subscribe = Events.subscribe
send = Events.send
send_queue = Events.send_queue
send_thread = Events.send_thread
send_blocking = Events.send_blocking
"""
    