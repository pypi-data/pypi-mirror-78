#!/bin/env python

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

from fructosa.fructosad import FructosaD
from fructosa.conf import LAgentConf
from fructosa.constants import (
    PROTO_STARTING_PROGRAM_MSG, PROTO_STOPPED_PROGRAM_MSG, PROTO_CANT_STOP_MSG,
    START_STOP_ERROR, NOT_RUNNING_MESSAGE, LAGENT_PROGRAM, PROTO_MEASUREMENT_MSG,
    LAGENT_TO_LMASTER_DATA_PORT_KEY, LMASTER_HOST_KEY,
    LAGENT_TO_LMASTER_CONNECTING_MSG, LAGENT_TO_LMASTER_CONNECTED_MSG,
    HEARTBEAT_START_SENDING_MSG_TEMPLATE, HEARTBEAT_PORT, HEARTBEAT_INTERVAL_SECONDS, #  ?
)
from fructosa.maind import generic_main
from fructosa.heartbeat import HeartbeatSource


LAGENT_STARTING_MESSAGE = PROTO_STARTING_PROGRAM_MSG.format(program=LAGENT_PROGRAM)
LAGENT_STOP_MESSAGE = PROTO_STOPPED_PROGRAM_MSG.format(program=LAGENT_PROGRAM)
LAGENT_CANT_STOP_MESSAGE = PROTO_CANT_STOP_MSG.format(program=LAGENT_PROGRAM)


class LAgent(FructosaD):
    _starting_message = LAGENT_STARTING_MESSAGE
    _stopped_message = LAGENT_STOP_MESSAGE
    _cant_stop_message = LAGENT_CANT_STOP_MESSAGE

    def _create_queues(self):
        super()._create_queues()
        self._sensors_queue = asyncio.Queue()
        
    @property
    def sensors(self):
        return self._conf.sensors
    
    def run(self):
        self.submit_task(self.heartbeating)
        for sensor in self.sensors:
            self.submit_task(sensor, self._sensors_queue)
        self.submit_task(self.report_data)
        self.submit_task(self._send_to_graphite)
        super().run()

    async def report_data(self):
        while True:
            value = await self._sensors_queue.get()
            self.logger.debug(PROTO_MEASUREMENT_MSG.format(value))
            await self._to_graphite_queue.put(pickle.dumps(value))

    async def heartbeating(self):
        host = self._conf.lmaster[LMASTER_HOST_KEY]
        port = HEARTBEAT_PORT
        self.logger.info(
            HEARTBEAT_START_SENDING_MSG_TEMPLATE.format(
                master=host, hb_port=port
            )
        )
        hb = HeartbeatSource(
            host=host, port=port, logging_conf=self._conf.logging
        )
        while True:
            await hb()

    ############################################################################
    
    # old idea:
    
    # async def heartbeating(self): #  ?
    #     host = self._conf.lmaster[LMASTER_HOST_KEY] #  ?
    #     port = HEARTBEAT_PORT #  ?
    #     self.logger.info( #  ?
    #         HEARTBEAT_START_SENDING_MSG_TEMPLATE.format( #  ?
    #             master=host, hb_port=port #  ?
    #         ) #  ?
    #     ) #  ?
    #     hb_proto_factory = HeartbeatProtocolFactory(
    #         HeartbeatClientProtocol, self._conf.logging) #  ?
    #     while True: #  ?
    #         await self._send_one_heartbeat(hb_proto_factory, host, port)

    # async def _send_one_heartbeat(self, factory, host, port):
    #     transport, protocol = await self._event_loop.create_datagram_endpoint(
    #         factory, remote_addr=(host, port)
    #     )
    #     # try: #  ?
    #     #     await protocol.on_sent #  ?
    #     # finally: #  ?
    #     #     transport.close() #  ?
    #     # await asyncio.sleep(HEARTBEAT_INTERVAL_SECONDS) #  ?

    async def send_to_master(self):
        """This coroutine is not used for now since the data are sent to 
        Graphite directly.
        It remains here in case it is used in the future (or a variation of it)
        """
        host = self._conf.lmaster[LMASTER_HOST_KEY]
        port = self._conf.lmaster[LAGENT_TO_LMASTER_DATA_PORT_KEY]
        self.logger.info(
            LAGENT_TO_LMASTER_CONNECTING_MSG.format(
                host_key=LMASTER_HOST_KEY, host=host,
                port_key=LAGENT_TO_LMASTER_DATA_PORT_KEY, port=port,
            )
        )
        reader, writer = await asyncio.open_connection(
            host, port, loop=self._event_loop,
        )
        self.logger.info(LAGENT_TO_LMASTER_CONNECTED_MSG)
        while True:
            message = await self._to_master_queue.get()
            writer.write(message)
        #writer.close()# not needed (?) review the protocol; is this correct?
        #              # I think I should factorize this functionality in a client class

def main():
    generic_main(LAgentConf, LAgent)
