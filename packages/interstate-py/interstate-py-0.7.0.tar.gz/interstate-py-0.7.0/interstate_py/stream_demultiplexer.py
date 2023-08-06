from asyncio import Queue

from interstate_py.connection_agent import ConnectionAgentBase
from interstate_py.control.worker_task import AIOWorkerTask
from interstate_py.error.deserialization_exception import DeserializationException
from interstate_py.error.error_assembly import ErrorAssembly
from interstate_py.interstate_message import InterstateWireMessageType
from interstate_py.log_factory import LogFactory
from interstate_py.multiplex_message import MultiplexMessage
from interstate_py.serialization.serialization import Serialization


class StreamDemultiplexer(AIOWorkerTask):
    """
    Demultiplexes a messages by extracting its identity and calling the according emitter method on
    the corresponding connection provided by the connection agent.
    """
    _log = LogFactory.get_logger(__name__)

    def __init__(self, raw_inbound_queue: Queue,
                 outbound_queue: Queue,
                 con_agent: ConnectionAgentBase,
                 serialization: Serialization):  # TODO: interceptor
        super().__init__()
        self._raw_inbound_queue = raw_inbound_queue
        self._outbound_queue = outbound_queue
        self._con_agent = con_agent
        self._serialization = serialization

    async def do_work(self):
        message = await self._raw_inbound_queue.get()
        identity = message.identity.decode()
        connection = self._con_agent.get(identity)

        # TODO: generify and decrease rx1 coupling
        if message.type == InterstateWireMessageType.NEXT:
            self._log.info("[IN][NEXT] - {}".format(message))
            try:
                deserialized_payload = self._serialization.deserialize(message.payload)
                connection.inbound_stream().on_next(deserialized_payload)
            except Exception as e:
                self._log.warn("[IN][NEXT] - Could not deserialize incoming message: %s", ErrorAssembly.exc_message(e))
                await self._outbound_queue.put(
                    MultiplexMessage(message.identity.decode(), InterstateWireMessageType.ERROR,
                                     DeserializationException("Could not deserialize:" + e.__repr__())))
        elif message.type == InterstateWireMessageType.ERROR:
            self._log.info("[IN][ERROR] - {}".format(message))
            connection.inbound_stream().on_error(Exception("Error"))
            connection.close_inbound()
        elif message.type == InterstateWireMessageType.COMPLETE:
            self._log.info("[IN][COMPLETED] - {}".format(message))
            connection.inbound_stream().on_completed()
            connection.close_inbound()
        elif message.type == InterstateWireMessageType.PING:
            # TODO: find a better way via interceptors or another mechanism
            self._log.info("[IN][PING] - {}".format(message))
            await self._outbound_queue.put(MultiplexMessage(identity, InterstateWireMessageType.PONG, "pong".encode()))
        else:
            self._log.info("Can not handle message: {}".format(message))

        self._raw_inbound_queue.task_done()
