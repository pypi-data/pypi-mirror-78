#!/bin/env python3

#######################################################################
#
# Copyright (C) 2020 David Palao
#
# This file is part of FrUCToSA.
#
#  FrUCToSA is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  FrUCToSA is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with FrUCToSA.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

import asyncio
import pickle
import struct
#from asyncio import open_connection

from fructosa.fructosad import FructosaD
from fructosa.conf import LMasterConf
from fructosa.maind import generic_main
from .lmessage import LMessage, LMessageError
from .heartbeat import HeartbeatSink

from .constants import (
    PROTO_STARTING_PROGRAM_MSG, PROTO_STOPPED_PROGRAM_MSG, PROTO_CANT_STOP_MSG,
    START_STOP_ERROR, NOT_RUNNING_MESSAGE, LMASTER_PROGRAM, PROTO_MEASUREMENT_MSG,
    SERVING_PROTO_MESSAGE, INITIAL_LMASTER_SERVER_PACKET_SIZE,
    PROTO_MEASUREMENT_RECEIVED_MSG, LAGENT_TO_LMASTER_DATA_PORT_KEY,
    LMASTER_HOST_KEY, GRAPHITE_HOST_KEY, GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY,
    PROTO_MSG_TO_GRAPHITE, TO_GRAPHITE_CONNECTING_MSG,
    TO_GRAPHITE_CONNECTED_MSG, TO_GRAPHITE_RETRY_MSG,
    HEARTBEAT_LISTENING_MSG_TEMPLATE, HEARTBEAT_PORT,
)

LMASTER_STARTING_MESSAGE = PROTO_STARTING_PROGRAM_MSG.format(program=LMASTER_PROGRAM)
LMASTER_STOP_MESSAGE = PROTO_STOPPED_PROGRAM_MSG.format(program=LMASTER_PROGRAM)
LMASTER_CANT_STOP_MESSAGE = PROTO_CANT_STOP_MSG.format(program=LMASTER_PROGRAM)


class LMaster(FructosaD):
    _starting_message = LMASTER_STARTING_MESSAGE
    _stopped_message = LMASTER_STOP_MESSAGE
    _cant_stop_message = LMASTER_CANT_STOP_MESSAGE

    def run(self):
        """LMaster.run is the place to submit asyncio tasks: that is
        the reason why the messages come from LAgent instances to
        LMaster: because LMaster might have instructions to dispatch
        messages to different locations.
        """
        server = self._create_server()
        self._run_server(server)
        self.submit_task(self.heartbeats_sink)
        #self.submit_task(self._send_to_graphite)
        #  More tasks can be added here
        super().run()
    
    def _create_server(self):
        host = self._conf.lmaster[LMASTER_HOST_KEY]
        port = self._conf.lmaster[LAGENT_TO_LMASTER_DATA_PORT_KEY]
        return asyncio.start_server(
            self._handle_connection, host, port, loop=self._event_loop
        )

    def _run_server(self, server_coroutine):
        self.server = self._event_loop.run_until_complete(server_coroutine)
        self.logger.info(
            SERVING_PROTO_MESSAGE.format(self.server.sockets[0].getsockname())
        )
        
    async def _handle_connection(self, reader, writer):
        addr = writer.get_extra_info('peername')
        while True:
            data = await reader.read(INITIAL_LMASTER_SERVER_PACKET_SIZE)
            await self._to_graphite_queue.put(data)
            message = pickle.loads(data)
            log_msg = PROTO_MEASUREMENT_RECEIVED_MSG.format(addr, message)
            self.logger.debug(log_msg)

    def _clean_up(self):
        self.server.close()
        self._event_loop.run_until_complete(self.server.wait_closed())
        super()._clean_up()


    async def heartbeats_sink(self):
        host = self._conf.lmaster[LMASTER_HOST_KEY]
        port = HEARTBEAT_PORT
        self.logger.info(
            HEARTBEAT_LISTENING_MSG_TEMPLATE.format(
                master=host, hb_port=port
            )
        )
        hb_sink = HeartbeatSink(
            host=host, port=port, logging_conf=self._conf.logging
        )
        await hb_sink()
        
    # async def heartbeats_sink(self): #  ?
    #     # print("Starting UDP server")

    #     # # Get a reference to the event loop as we plan to use
    #     # # low-level APIs.
    #     # loop = asyncio.get_running_loop()

    #     # One protocol instance will be created to serve all
    #     # client requests.
    #     from .constants import HEARTBEAT_PORT
    #     from .heartbeat import HeartbeatProtocolFactory, HeartbeatServerProtocol
    #     import traceback
    #     import sys
    #     host = self._conf.lmaster[LMASTER_HOST_KEY]
    #     self.logger.debug("Enter the dragon")
    #     try:
    #         transport, protocol = await self._event_loop.create_datagram_endpoint(
    #             HeartbeatProtocolFactory(HeartbeatServerProtocol, self._conf.logging),
    #             local_addr=(host, HEARTBEAT_PORT))
    #         for t in asyncio.all_tasks():
    #             self.logger.info("{}".format(t))
    #         self.logger.info("/"*80)
    #     except:
    #         msg = traceback.format_exception(*sys.exc_info())
    #         for l in msg:
    #             self.logger.error(l)
    #     self.logger.debug("datagram created")
    #     try:
    #         await asyncio.sleep(3600)  # Serve for 1 hour.
    #         # instead, mimick what is done in LAgent: await on a never done future
    #     finally:
    #         transport.close()


    
def main():
    generic_main(LMasterConf, LMaster)

