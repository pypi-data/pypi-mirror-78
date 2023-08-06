from typing import Tuple

from .abstract_handler import AbstractExProtoHandler
from emqx.erlport.erlterms import Pid
from emqx.erlport import erlang
from .connection import Connection, ConnectionInfo
from .message import Message


OK = 0
ERROR = 1

EXPROTO_CLASS: AbstractExProtoHandler = None

##--------------------------------------------------------------------
## Connection level

def init(conn, conninfo):
    global EXPROTO_CLASS
    connection = Connection(pid=conn)
    connection_info = ConnectionInfo(conninfo)
    EXPROTO_CLASS.on_connect(connection, connection_info)
    state = 0
    return (OK, state)

def received(conn, data, state):
    global EXPROTO_CLASS
    connection = Connection(pid=conn)
    EXPROTO_CLASS.on_received(connection, data, state)
    return (OK, state+1)

def terminated(conn, reason, state):
    global EXPROTO_CLASS
    connection = Connection(pid=conn)
    EXPROTO_CLASS.on_terminated(connection, reason, state)
    return

##--------------------------------------------------------------------
## Protocol/Session level

def deliver(conn, msgs, state):
    global EXPROTO_CLASS
    connection = Connection(pid=conn)
    msg_list = Message.parse(msgs)
    EXPROTO_CLASS.on_deliver(connection, msg_list)
    return (OK, state+1)

##--------------------------------------------------------------------
## APIs
##--------------------------------------------------------------------

def send(conn, data):
    erlang.call(Atom(b'emqx_exproto'), Atom(b'send'), [conn, data])
    return

def close(conn):
    erlang.call(Atom(b'emqx_exproto'), Atom(b'close'), [conn])
    return

def register(conn, clientinfo):
    erlang.call(Atom(b'emqx_exproto'), Atom(b'register'), [conn, clientinfo])
    return

def publish(conn, message):
    erlang.call(Atom(b'emqx_exproto'), Atom(b'publish'), [conn, message])
    return

def subscribe(conn, topic, qos):
    erlang.call(Atom(b'emqx_exproto'), Atom(b'subscribe'), [conn, topic, qos])
    return
