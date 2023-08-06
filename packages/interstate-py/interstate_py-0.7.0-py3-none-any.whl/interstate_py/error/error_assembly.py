import json
import sys
import traceback
from typing import List

from interstate_py.interstate_message import InterstateWireMessage, InterstateWireMessageType
from interstate_py.multiplex_message import MultiplexMessage


class ErrorAssembly:
    """
    Converts multiplex messages that contains exceptions to an on_error interstate message carrying the exception
    """

    @staticmethod
    def to_on_error(multiplex_message: MultiplexMessage) -> InterstateWireMessage:
        if multiplex_message.type != InterstateWireMessageType.ERROR:
            raise Exception("Only error message can be converted")
        carried_exception = multiplex_message.payload

        error_type = carried_exception.__class__.__name__
        error_message = ErrorAssembly.exc_message(carried_exception)
        stacktrace = ErrorAssembly._get_stacktrace(10)

        return InterstateWireMessage(multiplex_message.identity.encode(), InterstateWireMessageType.header("error"),
                                     json.dumps({
                                         "errorType": error_type,
                                         "errorMessage": error_message,
                                         "stacktrace": stacktrace
                                     }).encode())

    @staticmethod
    def exc_message(exception: Exception) -> str:
        """
        Extracts the message from the given exception. Some exceptions carry the message within a 'message' field while
        others does not.
        :param exception:
        :return:
        """
        if hasattr(exception, 'message'):
            return exception.message
        else:
            return repr(exception)

    @staticmethod
    def _get_stacktrace(limit: int) -> List[str]:
        (_, _, s) = sys.exc_info()
        return traceback.format_list(traceback.extract_tb(s, limit=limit))