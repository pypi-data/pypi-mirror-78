import os
import socket
import inspect
from functools import wraps

from log.server_log_config import SERVER_LOG
# from log.client_log_config import CLIENT_LOG


class Log:
    """Debug info logger class for tracing wrapped function calls."""

    def __init__(self, raiseable=False):
        """Set a flag in case wrapped function can potentially raise an exception."""

        self.raiseable = raiseable

    def __call__(self, func):
        """Select a logger and generate debugging information to store."""

        @wraps(func)
        def wrapped(*args, **kwargs):
            full_name, function_name = self._inspect_caller()
            file_name = os.path.split(full_name)[1]
            logger = SERVER_LOG
            logger.debug(f'function "{func.__name__}" called from "{function_name}", params = {args}, {kwargs}')
            if not self.raiseable:
                res = func(*args, **kwargs)
                # logger.debug(f'function "{func.__name__} returned: {res}')
            else:
                try:
                    res = func(*args, **kwargs)
                    # logger.debug(f'function "{func.__name__} returned: {res}')
                except Exception as e:
                    logger.error(f'function "{func.__name__}" raised an exception "{type(e).__name__}" {e.args}')
                    raise e
            return res
        return wrapped

    @staticmethod
    def _inspect_caller():
        """Gets caller file and called function names from frame inspecting."""

        prev_frame = inspect.currentframe().f_back.f_back
        (file_name, line_number, function_name, lines, index) = inspect.getframeinfo(prev_frame)

        return file_name, function_name


def login_required(func):
    """Decorator for checking that the client is authorized on the server.

    Checks whether the socket object is within a client list, unless the auth procedure is running.
    Generates TypeError otherwise.
    """

    def checker(*args, **kwargs):
        from server.core import MessageProcessor
        from common.constants import JIM
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            for arg in args:
                if isinstance(arg, dict):
                    if JIM.ACTION in arg and arg[JIM.ACTION] == JIM.Actions.PRESENCE:
                        found = True

            if not found:
                raise TypeError
        return func(*args, **kwargs)

    return checker
