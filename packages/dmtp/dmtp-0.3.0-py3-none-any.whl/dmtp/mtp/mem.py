# -*- coding: utf-8 -*-
#
#   MTP: Message Transfer Protocol
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

"""
    Pool
    ~~~~

    Tasks cache pool
"""

import threading
import time
from typing import Optional

from .protocol import TransactionID
from .protocol import Command, CommandRespond
from .protocol import Message, MessageRespond, MessageFragment
from .package import Package
from .task import Departure, Arrival, Assemble
from .pool import Pool


class MemPool(Pool):

    """
        1. Departure task should be expired after 2 minutes when receive no response.
        2. Assembling task should be expired after 2 minutes when receive nothing.
    """
    EXPIRES = 120  # seconds

    def __init__(self):
        super().__init__()
        # waiting list for responding
        self.__departures = []
        self.__departures_lock = threading.Lock()
        # waiting list for processing
        self.__arrivals = []
        self.__arrivals_lock = threading.Lock()
        # waiting list for assembling
        self.__fragments = {}  # TransactionID -> Assemble
        self.__fragments_lock = threading.Lock()

    def is_departure_expired(self, task: Departure) -> bool:
        return (task.last_time + self.EXPIRES) < time.time()

    def is_assemble_expired(self, assemble: Assemble) -> bool:
        return (assemble.last_time + self.EXPIRES) < time.time()

    #
    #   Departures
    #
    def shift_expired_departure(self) -> Optional[Departure]:
        with self.__departures_lock:
            if len(self.__departures) > 0:
                if self.is_departure_expired(task=self.__departures[0]):
                    return self.__departures.pop(0)

    def append_departure(self, task: Departure) -> bool:
        if task.max_retries < 0:
            return False
        task.update_last_time()
        task.max_retries -= 1
        with self.__departures_lock:
            self.__departures.append(task)
        return True

    def __del_entire_task(self, sn: TransactionID, destination: tuple) -> bool:
        count = 0
        with self.__departures_lock:
            pos = len(self.__departures)
            while pos > 0:
                pos -= 1
                task = self.__departures[pos]
                assert isinstance(task, Departure), 'departure task error: %s' % task
                if task.sn != sn:
                    # transaction ID not match
                    continue
                elif task.destination != destination:
                    # destination not match
                    continue
                assert task.data_type in [Command, Message], 'task error: %s' % task
                # Got it!
                self.__departures.pop(pos)
                count += 1
                # break
        return count > 0

    def __del_task_fragment(self, sn: TransactionID, pages: int, offset: int, destination: tuple) -> bool:
        count = 0
        with self.__departures_lock:
            pos = len(self.__departures)
            while pos > 0:
                pos -= 1
                task = self.__departures[pos]
                assert isinstance(task, Departure), 'departure task error: %s' % task
                if task.sn != sn:
                    # transaction ID not match
                    continue
                elif task.destination != destination:
                    # destination not match
                    continue
                assert task.data_type == MessageFragment, 'task error: %s' % task
                packages = task.packages
                pos2 = len(packages)
                while pos2 > 0:
                    pos2 -= 1
                    pack = packages[pos2]
                    assert isinstance(pack, Package), 'package error: %s' % packages
                    assert pack.head.sn == sn, 'task fragment error: %s' % pack.head
                    assert pack.head.data_type == MessageFragment, 'task error: %s' % pack.head
                    assert pack.head.pages == pages, 'pages not match: %d, %s' % (pages, pack.head)
                    if pack.head.offset == offset:
                        # Got it!
                        packages.pop(pos2)
                        break
                if len(packages) == 0:
                    # all fragment sent, remove this task
                    self.__departures.pop(pos)
                    count += 1
                else:
                    # update receive time
                    task.update_last_time()
                break
        return count > 0

    def delete_departure(self, response: Package, destination: tuple, source: tuple) -> bool:
        head = response.head
        body = response.body
        body_len = body.length
        data_type = head.data_type
        trans_id = head.sn
        if data_type == CommandRespond:
            # response for Command
            assert body_len == 0 or body.get_bytes(end=2) == b'OK', 'CommandRespond error: %s' % body
            return self.__del_entire_task(sn=trans_id, destination=destination)
        elif data_type == MessageRespond:
            # response for Message or Fragment
            if body_len >= 8:
                # MessageFragment
                assert body_len == 8 or body.get_bytes(start=8) == b'OK', 'MessageRespond error: %s' % body
                # get pages count and index
                pages = body.get_uint32_value(start=0)
                offset = body.get_uint32_value(start=4)
                assert pages > 1 and pages > offset, 'pages error: %d, %d' % (pages, offset)
                return self.__del_task_fragment(sn=trans_id, pages=pages, offset=offset, destination=destination)
            elif body_len == 0 or body.get_bytes() == b'OK':
                # Message
                return self.__del_entire_task(sn=trans_id, destination=destination)
            else:
                # respond for split message
                assert body.get_bytes() == b'AGAIN', 'MessageRespond error: %s' % body
                # TODO: resend all fragments of this message
        else:
            assert False, 'data type should be a Respond: %s' % data_type

    #
    #   Arrivals
    #
    def arrivals_count(self) -> int:
        with self.__arrivals_lock:
            return len(self.__arrivals)

    def shift_first_arrival(self) -> Optional[Arrival]:
        with self.__arrivals_lock:
            if len(self.__arrivals) > 0:
                return self.__arrivals.pop(0)

    def append_arrival(self, task: Arrival) -> bool:
        with self.__arrivals_lock:
            self.__arrivals.append(task)
        return True

    #
    #   Fragments Assembling
    #
    def insert_fragment(self, fragment: Package, source: tuple, destination: tuple) -> Optional[Package]:
        pack = None
        with self.__fragments_lock:
            trans_id = fragment.head.sn
            assemble = self.__fragments.get(trans_id)
            if assemble is None:
                # TODO: check incomplete message (fragment missed) from this source address
                #       if too many waiting fragments, deny receiving new message here
                # create new assemble
                assemble = Assemble(fragment=fragment, source=source, destination=destination)
                self.__fragments[trans_id] = assemble
            else:
                assert isinstance(assemble, Assemble), 'fragments error: %s' % assemble
                # insert fragment and check whether completed
                if assemble.insert(fragment=fragment, source=source, destination=destination):
                    if assemble.is_completed:
                        pack = Package.join(packages=assemble.fragments)
                        self.__fragments.pop(trans_id)
        return pack

    def discard_fragments(self) -> list:
        """
        Remove all expired fragments

        :return:
        """
        array = []
        with self.__fragments_lock:
            keys = list(self.__fragments.keys())
            for trans_id in keys:
                assemble = self.__fragments.get(trans_id)
                assert isinstance(assemble, Assemble), 'fragments error: %s' % assemble
                if self.is_assemble_expired(assemble=assemble):
                    # remove expired fragments
                    array.append(assemble)
                    self.__fragments.pop(trans_id)
        return array
