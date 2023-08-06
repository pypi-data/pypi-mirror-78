import os
import socket
import threading



def get_worker_id(prefix=None):
    """worker_id = prefix:hostname:process-id:thread-id
    """
    worker_inner_id = "{}:{}:{}".format(socket.gethostname(), os.getpid(), threading.get_ident())
    if prefix:
        return prefix + ":" + worker_inner_id
    else:
        return worker_inner_id
