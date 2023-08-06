from typing import Callable, Any

from rx import Observable

from interstate_py.interstate_server import InterstateServer
from interstate_py.log_factory import LogFactory
from interstate_py.serialization.serialization import Serialization, PassthroughSerialization
from interstate_py.zeromq.aio_zmq_server import AIOZMQServer


class Interstate:
    """
    The main entry point for the interstate server
    """
    _log = LogFactory.get_logger(__name__)

    @staticmethod
    def transformer_server(transformer: Callable[[Observable], Observable],
                           port: int = 8077,
                           serialization: Serialization = PassthroughSerialization()) -> InterstateServer:

        def _try_eager() -> Callable[[Observable], Observable]:
            """
            Tries if the transformer function does raise an exception when applied. This is considered invalid
            and should kill the server immediately and not during runtime when the first message arrives.
            :return:
            """
            try:
                transformer(Observable.empty())
                return transformer
            except Exception as e:
                Interstate._log.error(
                    "Unfortunately the given transformer function does raise an Exception. This prevents the server from starting - please check your transformer function:")
                raise e

        server = AIOZMQServer(port, _try_eager(), serialization)
        server.start_server()

        return server

    @staticmethod
    def request_response_server(req_res_handler: Callable[[Any], Any], port: int = 8077,
                                serialization: Serialization = PassthroughSerialization()) -> InterstateServer:
        def transformer(obs: Observable) -> Observable:
            return obs.map(req_res_handler)

        server = AIOZMQServer(port, transformer, serialization)
        server.start_server()

        return server

    @staticmethod
    def request_stream(req_stream: Callable[[Any], Observable], port: int = 8077,
                       serialization: Serialization = PassthroughSerialization()) -> InterstateServer:
        def transformer(obs: Observable) -> Observable:
            return obs.flat_map(req_stream)

        server = AIOZMQServer(port, transformer, serialization)
        server.start_server()

        return server
