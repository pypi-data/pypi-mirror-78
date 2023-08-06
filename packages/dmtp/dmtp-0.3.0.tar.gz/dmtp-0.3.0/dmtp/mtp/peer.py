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
    Peer
    ~~~~

    Network Node
"""

import threading
import time
import weakref
from typing import Optional

from .tlv import Data, MutableData, UInt32Data

from .protocol import Command, CommandRespond
from .protocol import Message, MessageRespond, MessageFragment
from .package import Package
from .task import Departure, Arrival, Assemble
from .pool import Pool
from .mem import MemPool
from .handler import PeerHandler, PeerDelegate


"""
    Topology:

        +-----------------------------------------------+
        |                      APP                      |
        |                 (Peer Handler)                |
        +-----------------------------------------------+
                            |       A
                            |       |
                            V       |
        +---+--------+----------------------------------+
        |   |  Pool  |                                  |        pool:
        |   +--------+         Peer        +--------+   |          -> departures
        |                (Hub Listener)    | Filter |   |          -> arrivals
        +----------------------------------+--------+---+          -> assembling
                            |       A
                            |       |
                            V       |
        +-----------------------------------------------+
        |                      HUB                      |
        +-----------------------------------------------+
"""


class Peer(threading.Thread):

    def __init__(self, pool: Pool=None):
        super().__init__()
        self.__running = False
        self.__delegate: weakref.ReferenceType = None
        self.__handler: weakref.ReferenceType = None
        if pool is None:
            pool = MemPool()
        self.__pool = pool

    @property
    def pool(self) -> Pool:
        return self.__pool

    @property
    def delegate(self) -> Optional[PeerDelegate]:
        if self.__delegate is not None:
            return self.__delegate()

    @delegate.setter
    def delegate(self, value: PeerDelegate):
        if value is None:
            self.__delegate = None
        else:
            self.__delegate = weakref.ref(value)

    @property
    def handler(self) -> Optional[PeerHandler]:
        if self.__handler is not None:
            return self.__handler()

    @handler.setter
    def handler(self, value: PeerHandler):
        if value is None:
            self.__handler = None
        else:
            self.__handler = weakref.ref(value)

    def start(self):
        if self.isAlive():
            return
        self.__running = True
        super().start()

    def stop(self):
        self.__running = False

    def run(self):
        while self.__running:
            try:
                pool = self.pool
                handler = self.handler
                # first, process all arrivals
                done = self.__clean_arrivals()
                # second, get one departure task
                task = pool.shift_expired_departure()
                if task is None:
                    # third, if no departure task, remove expired fragments
                    assembling = pool.discard_fragments()
                    for item in assembling:
                        assert isinstance(item, Assemble), 'assemble error: %s' % item
                        handler.recycle_fragments(fragments=item.fragments,
                                                  source=item.source, destination=item.destination)
                    if done == 0:
                        # all jobs done, have a rest. ^_^
                        time.sleep(0.1)
                else:
                    # redo this departure task
                    self.__send(task=task)
            except Exception as error:
                print('Peer.run error: %s' % error)

    def __clean_arrivals(self) -> int:
        """
        Process the received packages in waiting list

        :return: finished tasks count
        """
        pool = self.pool
        total = pool.arrivals_count()
        done = 0
        while done < total:
            task = pool.shift_first_arrival()
            if task is None:
                # no data now
                break
            self.__handle(task=task)
            done += 1
        return done

    def __handle(self, task: Arrival):
        pack = Package.parse(data=task.payload)
        if pack is None:
            # assert False, 'package error: %s' % task.payload
            self.handler.received_error(data=task.payload, source=task.source, destination=task.destination)
            return False
        head = pack.head
        data_type = head.data_type
        if data_type == CommandRespond:
            # command response
            trans_id = head.sn
            if self.pool.delete_departure(response=pack, destination=task.source, source=task.destination):
                # if departure task is deleted, means it's finished
                self.handler.send_command_success(sn=trans_id, destination=task.source, source=task.destination)
            return None
        elif data_type == MessageRespond:
            # message response
            trans_id = head.sn
            if self.pool.delete_departure(response=pack, destination=task.source, source=task.destination):
                # if departure task is deleted, means it's finished
                self.handler.send_message_success(sn=trans_id, destination=task.source, source=task.destination)
            return None
        elif data_type == Command:
            # handle command
            ok = self.handler.received_command(cmd=pack.body, source=task.source, destination=task.destination)
        elif data_type == Message:
            # handle message
            ok = self.handler.received_message(msg=pack.body, source=task.source, destination=task.destination)
        else:
            # handle message fragment
            assert data_type == MessageFragment, 'data type error: %s' % data_type
            ok = self.handler.check_fragment(fragment=pack, source=task.source, destination=task.destination)
            if ok:
                # assemble fragments
                msg = self.pool.insert_fragment(fragment=pack, source=task.source, destination=task.destination)
                if msg is not None:
                    # all fragments received
                    self.handler.received_message(msg=msg.body, source=task.source, destination=task.destination)
        # respond to the sender
        if ok:
            self.__respond(pack=pack, remote=task.source, local=task.destination)

    def __respond(self, pack: Package, remote: tuple, local: tuple):
        head = pack.head
        data_type = head.data_type
        if data_type == Command:
            data_type = CommandRespond
            body = Data(data=b'OK')
        elif data_type == Message:
            data_type = MessageRespond
            body = Data(data=b'OK')
        elif data_type == MessageFragment:
            data_type = MessageRespond
            pages = UInt32Data(value=head.pages)
            offset = UInt32Data(value=head.offset)
            body = MutableData(capacity=10)
            body.append(pages)
            body.append(offset)
            body.append(b'OK')
        else:
            raise TypeError('data type error: %s' % data_type)
        if head.body_length < 0:
            # UDP (unlimited)
            response = Package.new(data_type=data_type, sn=head.sn, body_length=-1, body=body)
        else:
            # TCP
            response = Package.new(data_type=data_type, sn=head.sn, body_length=body.length, body=body)
        # send response directly, don't add this task to waiting list
        res = self.delegate.send_data(data=response, destination=remote, source=local)
        assert res == response.length, 'failed to respond %s: %s' % (remote, data_type)

    #
    #   Sending
    #
    def __send(self, task: Departure):
        if self.pool.append_departure(task=task):
            # treat the task as a bundle of packages
            delegate = self.delegate
            packages = task.packages
            for item in packages:
                assert isinstance(item, Package), 'package error: %s' % item
                res = delegate.send_data(data=item, destination=task.destination, source=task.source)
                assert res == item.length, 'failed to resend packs (%d) to: %s' % (len(packages), task.destination)
        else:
            # mission failed
            data_type = task.data_type
            trans_id = task.sn
            if data_type == Command:
                self.handler.send_command_timeout(sn=trans_id, destination=task.destination, source=task.source)
            elif data_type == Message:
                self.handler.send_message_timeout(sn=trans_id, destination=task.destination, source=task.source)
            else:
                raise AssertionError('data type error: %s' % data_type)

    def send_command(self, pack: Package, destination: tuple, source: tuple) -> Departure:
        # send command as single package
        task = Departure(packages=[pack], destination=destination, source=source)
        self.__send(task=task)
        return task

    def send_message(self, pack: Package, destination: tuple, source: tuple) -> Departure:
        if pack.body.length <= Package.OPTIMAL_BODY_LENGTH or pack.head.data_type == MessageFragment:
            packages = [pack]
        else:
            # split packages for large message
            packages = pack.split()
        task = Departure(packages=packages, destination=destination, source=source)
        self.__send(task=task)
        return task
