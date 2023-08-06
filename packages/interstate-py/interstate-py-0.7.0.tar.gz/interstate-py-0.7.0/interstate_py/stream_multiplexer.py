from asyncio import Queue

from interstate_py.connection_agent import ConnectionAgentBase
from interstate_py.control.worker_task import AIOWorkerTask
from interstate_py.error.error_assembly import ErrorAssembly
from interstate_py.interstate_message import InterstateWireMessageType, InterstateWireMessage
from interstate_py.log_factory import LogFactory
from interstate_py.multiplex_message import MultiplexMessage
from interstate_py.serialization.serialization import Serialization


class StreamMultiplexer(AIOWorkerTask):
    """
    Multiplexes stream by simply passing MultiplexMessages from the outbound_queue to the raw_outbound_queue and turning
    them into InterstateWireMessages during the process.

    If a serialization object is passed, the payload will be serialized to bytes.
    """
    _log = LogFactory.get_logger(__name__)

    def __init__(self,
                 outbound_queue: Queue,
                 raw_outbound_queue: Queue,
                 con_agent: ConnectionAgentBase,
                 serialization: Serialization):  # TODO: interceptor
        super().__init__()
        self._outbound_queue = outbound_queue
        self._raw_outbound_queue = raw_outbound_queue
        self._con_agent = con_agent
        self._serialization = serialization

    async def do_work(self):
        multiplex_message = await self._outbound_queue.get()
        identity = multiplex_message.identity
        connection = self._con_agent.get(identity)

        # TODO: generify and decrease rx1 coupling
        if multiplex_message.type == InterstateWireMessageType.NEXT:
            self._log.info("[OUT][NEXT] - {}".format(multiplex_message))
            message = await self._serialize_message(multiplex_message)
            await self._raw_outbound_queue.put(message)
        elif multiplex_message.type == InterstateWireMessageType.ERROR:
            self._log.info("[OUT][ERROR] - {}".format(multiplex_message))
            self._log.warn("[OUT][ERROR] - Propagating error: %s", ErrorAssembly.exc_message(multiplex_message.payload))
            await self._raw_outbound_queue.put(ErrorAssembly.to_on_error(multiplex_message))
            connection.close_outbound()
        elif multiplex_message.type == InterstateWireMessageType.COMPLETE:
            self._log.info("[OUT][COMPLETED] - {}".format(multiplex_message))
            await self._raw_outbound_queue.put(
                InterstateWireMessage(multiplex_message.identity.encode(), InterstateWireMessageType.header("complete"),
                                      bytes(0))
            )
            connection.close_outbound()
        elif multiplex_message.type == InterstateWireMessageType.PONG:
            self._log.info("[OUT][PONG] - {}".format(multiplex_message))
            await self._raw_outbound_queue.put(
                InterstateWireMessage(multiplex_message.identity.encode(), InterstateWireMessageType.header("pong"),
                                      bytes(0))
            )
        else:
            self._log.info("Can not handle message: {}".format(multiplex_message))

        self._outbound_queue.task_done()

    async def _serialize_message(self, multiplex_message: MultiplexMessage) -> InterstateWireMessage:
        """
        Serializes a messages using the given serializer. If something is going wrong during serialization an
        on_error message is sent.

        :param multiplex_message:
        :return:
        """
        try:
            serialized_payload = self._serialization.serialize(multiplex_message.payload)
            return InterstateWireMessage(multiplex_message.identity.encode(), InterstateWireMessageType.header("next"),
                                         serialized_payload)
        except Exception as e:
            self._log.error("Something went wrong during serialization")
            await self._raw_outbound_queue.put(ErrorAssembly.to_on_error(
                MultiplexMessage(multiplex_message.identity, InterstateWireMessageType.ERROR, e)))
