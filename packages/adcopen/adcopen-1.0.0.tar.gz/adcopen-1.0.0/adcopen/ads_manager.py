# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 14:35:58 2018

@author: ThomasBitskyJr
(C) Copyright 2018-2020 Autoamted Design Corp. All Rights Reserved.

Combines a Beckhoff ADS client with loosely-coupled events for
easy integration into a larger program.

"""

#from ads_client import AdsClient
from adcopen.ads_client import AdsClient
from adcopen.events import Events
import pyads
import asyncio
import sys, traceback
import time
import os

import logging, logging.handlers
import configparser
    
# remote connection
#options_ = {"AmsNetId": "192.168.127.1.1.1", "port": 851}     
# local connection
options_ = {}        



class AdsManager():
    """Combines a Beckhoff ADS client with loosely-coupled events for
    easy integration into a larger program.
    """

    def __init__(self, options : configparser.ConfigParser) -> None:
        """Constructor"""
        self.options:configparser.ConfigParser = options
        self.ads_client:AdsClient = None


    def configure_signals(self) -> None:
        """Create the slots for the loosely-coupled API and
        attach to the signals.
        """

        async def on_subscribe_tag(args) -> None:
            """Slot
            
            Request to register a tag for on-change notification.
            """
            if ( not type(args) is dict ):
                arg = {"name": args}
                self.ads_client.addTag(arg)
                await self.ads_client.refresh(args)
            else:       
                self.ads_client.addTag(args)
                await self.ads_client.refresh(args["name"])




        async def on_refresh_all(args) -> None:
            """Slot
            
            Request to re-broadcast the current value for all registerd tags.
            """            
            await self.ads_client.refreshAll()

        async def on_refresh_tag(args):
            """Slot
            
            Request to re-broadcast the current value for a specific tag.
            """                 

            try:
                if ( not type(args) is dict ):
                    arg = {"name": args}
                    await self.ads_client.refresh(arg)
                else:       
                    await self.ads_client.refresh(args["name"])

            except:
                print("Failed to refresh requested tag.")


        async def on_tag_write(args:dict) -> None:
            """Slot
            
            Request to re-broadcast the current value for all registerd tags.
            """                 
            if type(args) is dict:
                await self.ads_client.writeTag(args.get("name"), args.get("value"))
            else:
                logging.warning("AdsManager::on_tag_write - invalid argument.")


        async def on_data_change(args:dict) -> None:
            """Callback from Ads Client. Notification from the remote
            controller that the value of a tag has changed.
            """            
            try:
                # publish the tag value under the tag name
                Events.publish(args.get("name"), args.get("value"))
            except Exception:
                print( "Exception on publish {0}  {1}".format(args.get("name"), args.get("value")))


        Events.subscribe_method("ads-dataChange", on_data_change)
        Events.subscribe_method("ads-subscribe-tag", on_subscribe_tag)
        Events.subscribe_method("ads-refresh-all", on_refresh_all)
        Events.subscribe_method("ads-refresh-tag", on_refresh_tag)
        Events.subscribe_method('ads-tag-write', on_tag_write )


    def start(self) -> None:
        """Configure the ads manager and start a connection out to
        the configured PLC.
        """

        self.configure_signals()

        # Create an ads client instance, passing in the connection properties.
        self.ads_client = AdsClient(self.options["ADS"])

        try:
            # start the connection to the server

            print( "Connecting to ADS server.. ")
            print( "Note: If not connected to machine or local instance, this will block ")
            print( "and you will not be able to test.")

            self.ads_client.connect()
        except pyads.pyads.ADSError as ex:

            logging.exception(ex)
            raise ex

        except Exception as ex:

            logging.exception(ex)
            raise ex       


    def stop(self) -> None:
        """Disconnect the ADS client and unregister all tags.
        """
        if not self.ads_client is None:
            self.ads_client.unloadTags()
            self.ads_client.close()   


    async def start_async(self) -> None:
        """
        A callback that starts the server. Used when starting this class as a Windows Service or daemon.

        Usage:
        asyncio.run_coroutine_threadsafe(adsManagerInst.start_async(), loop)
        """

        self.start()            


if __name__ == '__main__':
    """ If this script is executed as the "main" file .

    Used only for testing. Not very useful.
    """

    @Events.subscribe("GIO.xbControlPower")
    async def onControlPowerChanged(value):
        print(f"Control Power is now {value}")

    CONFIG_FILE_NAME:str = "adsmantest.ini"
    config = configparser.ConfigParser()
    if os.path.isfile(CONFIG_FILE_NAME):
        config.read(CONFIG_FILE_NAME)
    else:
        config['ADS'] = {
            "AmsNetId": "", 
            "port": "851"
        }

        with open(CONFIG_FILE_NAME, 'w') as configfile:
            config.write(configfile)

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:

        manager:AdsManager = AdsManager(config)
        manager.start()

        manager.ads_client.addTag({"name":"GIO.xbControlPower"})

        print( "Press CTRL-C to stop.")  

        loop.run_forever()

    except KeyboardInterrupt:
        
        print( "Closing from keyboard request.")  


    except Exception as ex:

        print( f"AdsManager exception: {ex}")  
        print(ex)
            
    finally:
        

        manager.stop()       
        
        loop.stop()

        print( "Goodbye.")
