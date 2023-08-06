import asyncio
from asyncio import Future, Queue
from typing import Any

from rx import Observer

from interstate_py.interstate_message import InterstateWireMessage, InterstateWireMessageType
from interstate_py.log_factory import LogFactory
from interstate_py.multiplex_message import MultiplexMessage


class SendingObserver(Observer):
    """
    Subscribes to the Observable provided by the 'evaluation function' Callable[[Subject], Observable] and dispatches
    messages received from the upstream observable to the specific queues.
    """
    _log = LogFactory.get_logger(__name__)

    def __init__(self, identity: str, outbound_queue: Queue):
        self._identity = identity
        self._outbound_queue = outbound_queue

    def on_next(self, value):
        self._dispatch_internal(MultiplexMessage(
            self._identity, InterstateWireMessageType.NEXT, value
        ))

    def on_error(self, error):
        self._dispatch_internal(MultiplexMessage(
            self._identity, InterstateWireMessageType.ERROR, error
        ))

    def on_completed(self):
        self._dispatch_internal(MultiplexMessage(
            self._identity, InterstateWireMessageType.COMPLETE, bytes(0)
        ))

    def _dispatch_internal(self, message: MultiplexMessage):
        return self._dispatch(self._outbound_queue, message)

    def _dispatch_wire(self, value: InterstateWireMessage) -> Future:
        return self._dispatch(self._outbound_queue, value)

    def _dispatch(self, queue: Queue, message: Any) -> Future:
        async def _put_on_queue(q: Queue, m: Any):
            await q.put(m)

        return asyncio.ensure_future(_put_on_queue(queue, message))
