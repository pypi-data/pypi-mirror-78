# -*- coding: utf-8 -*-
#
#   UDP: User Datagram Protocol
#
#                                Written in 2020 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2020 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

from abc import ABC, abstractmethod
from typing import Optional

from .status import ConnectionStatus
from .connection import Connection
from .filter import HubFilter


class HubListener(ABC):

    @property
    def filter(self) -> Optional[HubFilter]:
        return None

    @abstractmethod
    def data_received(self, data: bytes, source: tuple, destination: tuple) -> Optional[bytes]:
        """
        New data package arrived

        :param data:        UDP data received
        :param source:      remote IP and port
        :param destination: local IP and port
        :return: response to the source address
        """
        raise NotImplemented

    # @abstractmethod
    def status_changed(self, connection: Connection, old_status: ConnectionStatus, new_status: ConnectionStatus):
        """
        Status changed

        :param connection:
        :param old_status:
        :param new_status:
        """
        pass
