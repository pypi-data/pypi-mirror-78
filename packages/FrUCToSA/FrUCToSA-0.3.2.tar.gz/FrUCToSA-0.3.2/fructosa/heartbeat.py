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

from fructosa.logs import setup_logging

from fructosa.constants import (
    HEARTBEAT_RECEIVE_MSG_TEMPLATE, HEARTBEAT_SEND_MSG_TEMPLATE,
    HEARTBEAT_INTERVAL_SECONDS
)


def encode_beat_number(num):
    return num.to_bytes(length=64, byteorder="big", signed=False)


def decode_beat_number(data):
    return int.from_bytes(data,  byteorder="big", signed=False)



class HeartbeatProtocolFactory:
    def __init__(self, protocol_class, logging_conf):
        self.logger = setup_logging(
            "Heartbeat",
            rotatingfile_conf=logging_conf
        )
        self._protocol_class = protocol_class
        
    def __call__(self):
        return self._protocol_class(self.logger)
        
        
class HeartbeatClientProtocol:
    _next_beat_number = 0 #  should be a descriptor?
    
    def __init__(self, logger):
        """Customers of this classs must await on on_complete to ensure 
        that the data has been dispatched:

        >>> protocol = HeartbeatClient(logger)
        >>> await protocol.on_complete
        """
        self.transport = None
        self.logger = logger
        self.on_complete = asyncio.get_running_loop().create_future()
            
    @property
    def beat_number(self):
        return self._next_beat_number
    
    @property
    def message(self):
        return encode_beat_number(self.beat_number)
    
    def connection_made(self, transport):
        self.transport = transport
        self.transport.sendto(self.message)
        log_msg = HEARTBEAT_SEND_MSG_TEMPLATE.format(
            message_number=self.beat_number)
        self.logger.info(log_msg)
        self.__class__._next_beat_number += 1
        self.on_complete.set_result(True)
        

class HeartbeatServerProtocol:
    def __init__(self, logger):
        self.logger = logger
        self.on_complete = asyncio.get_running_loop().create_future()
        
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        num = decode_beat_number(data)
        self.logger.info(
            HEARTBEAT_RECEIVE_MSG_TEMPLATE.format(
                host=addr, message_number=num
            )
        )


class HeartbeatBase:
    def __init__(self, host, port, logging_conf, protocol_class):
        self._host = host
        self._port = port
        self._hb_factory = HeartbeatProtocolFactory(
            protocol_class, logging_conf
        )
        self.addr_parameter_name = "addr"

    async def __call__(self):
        await self.create_datagram_endpoint()
        await self.complete()

    async def create_datagram_endpoint(self):
        loop = asyncio.get_running_loop()
        addr = {self.addr_parameter_name: (self._host, self._port)}
        transport, protocol = await loop.create_datagram_endpoint(
            self._hb_factory, **addr
        )
        self._transport = transport
        self._protocol = protocol

    def future(self):
        # This is a method to make the testing easier
        return self._protocol.on_complete
    
    async def complete(self):
        try:
            await self.future()
        finally:
            self._transport.close()
        
    
class HeartbeatSource(HeartbeatBase):
    def __init__(self, host, port, logging_conf):
        super().__init__(host, port, logging_conf, HeartbeatClientProtocol)
        self.addr_parameter_name = "remote_addr"
        
    async def __call__(self):
        await super().__call__()
        await asyncio.sleep(HEARTBEAT_INTERVAL_SECONDS)


class HeartbeatSink(HeartbeatBase):
    def __init__(self, host, port, logging_conf):
        super().__init__(host, port, logging_conf, HeartbeatServerProtocol)
        self.addr_parameter_name = "local_addr"
