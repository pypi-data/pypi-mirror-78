# -*- coding: utf-8 -*-
#
#   TCP: Transmission Control Protocol
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


class Pool(ABC):

    """
        Memory cache for received data
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """

    @property
    def is_full(self) -> bool:
        """
        Check whether cache is full

        :return: true on full
        """
        return False

    @abstractmethod
    def cache(self, data: bytes) -> Optional[bytes]:
        """
        Add received data to data

        :param data: received data
        :return: ejected data when cache pool full
        """
        raise NotImplemented

    @abstractmethod
    def received(self) -> Optional[bytes]:
        """
        Check received  data (not remove)

        :return: received data
        """
        raise NotImplemented

    @abstractmethod
    def receive(self, length: int) -> Optional[bytes]:
        """
        Received data from pool with length (remove)

        :param length: data length to remove
        :return: remove data from the pool and return it
        """
        raise NotImplemented
