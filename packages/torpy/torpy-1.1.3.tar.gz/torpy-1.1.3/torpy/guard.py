# Copyright 2019 James Brown
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
import functools

from torpy.cells import CellRelay, CellDestroy, CellCreatedFast, CellCreated2, CellRelayTruncated
from torpy.utils import retry, log_retry
from torpy.circuit import TorReceiver, CircuitsManager, CellTimeoutError, CellHandlerManager, CircuitExtendError
from torpy.cell_socket import TorCellSocket

logger = logging.getLogger(__name__)


class GuardState:
    Disconnecting = 1
    Disconnected = 2
    Connecting = 3
    Connected = 4


def cell_to_circuit(func):
    def wrapped(_self, cell, *args, **kwargs):
        circuit = _self._circuits_manager.get_by_id(cell.circuit_id)
        if not circuit:
            if _self._state != GuardState.Connected:
                logger.debug('Ignore not found circuits on %r state', _self._state)
                return
            raise Exception('Circuit #{:x} not found'.format(cell.circuit_id))
        args_new = [_self, cell, circuit] + list(args)
        return func(*args_new, **kwargs)

    return wrapped


class TorSender:
    def __init__(self, tor_socket):
        self._tor_socket = tor_socket

    def send(self, cell):
        self._tor_socket.send_cell(cell)


class TorGuard:
    def __init__(self, router, consensus=None, auth_data=None):
        self._router = router
        self._consensus = consensus
        self._auth_data = auth_data

        self._state = GuardState.Connecting
        logger.info('Connecting to guard node %s...', self._router)
        self.__tor_socket = TorCellSocket(self._router)
        self.__tor_socket.connect()

        self._sender = TorSender(self.__tor_socket)
        self._circuits_manager = CircuitsManager(self._router, self._sender, self._consensus, self._auth_data)

        self._handler_mgr = CellHandlerManager()
        self._handler_mgr.subscribe_for(CellDestroy, self._on_destroy)
        self._handler_mgr.subscribe_for([CellCreatedFast, CellCreated2], self._on_cell)
        self._handler_mgr.subscribe_for(CellRelay, self._on_relay)

        self._receiver = TorReceiver(self.__tor_socket, self._handler_mgr)
        self._receiver.start()

        self._state = GuardState.Connected

    def __enter__(self):
        """Return Guard object."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Disconnect from Guard node."""
        self.close()

    def close(self):
        logger.info('Closing guard connections...')
        self._state = GuardState.Disconnecting
        self._destroy_all_circuits()
        self._receiver.stop()
        self.__tor_socket.close()
        self._state = GuardState.Disconnected

    def _destroy_all_circuits(self):
        logger.debug('Destroying all circuits...')
        for circuit in list(self._circuits_manager.circuits()):
            self.destroy_circuit(circuit)

    @cell_to_circuit
    def _on_destroy(self, cell, circuit):
        logger.info('On destroy: circuit #%x', cell.circuit_id)
        send_destroy = isinstance(cell, CellRelayTruncated)
        self.destroy_circuit(circuit, send_destroy=send_destroy)

    @cell_to_circuit
    def _on_cell(self, cell, circuit):
        circuit.handle_cell(cell)

    @cell_to_circuit
    def _on_relay(self, cell: CellRelay, circuit):
        circuit.handle_relay(cell)

    @retry(
        3, (CircuitExtendError, CellTimeoutError), log_func=functools.partial(log_retry, msg='Retry circuit creation')
    )
    def create_circuit(self, hops_count, extend_routers=None):
        if self._state != GuardState.Connected:
            raise Exception('You must connect to guard node first')

        circuit = self._circuits_manager.create_new()
        try:
            circuit.create(self)

            circuit.build_hops(hops_count)

            if extend_routers:
                for router in extend_routers:
                    circuit.extend(router)
        except Exception:
            # We must close here because we didn't enter to circuit yet to guard by context manager
            circuit.close()
            raise

        return circuit

    def destroy_circuit(self, circuit, send_destroy=True):
        logger.info('Destroy circuit #%x', circuit.id)
        circuit.destroy(send_destroy=send_destroy)
        self._circuits_manager.remove(circuit.id)

    def register(self, sock_or_stream, events, callback):
        return self._receiver.register(sock_or_stream, events, callback)

    def unregister(self, sock_or_stream):
        self._receiver.unregister(sock_or_stream)
