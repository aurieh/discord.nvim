import socket
import uuid
import struct
import enum
import json
import os


class OP(enum.Enum):
    AUTHENTICATE = 0
    FRAME = 1
    CLOSE = 2


class Message:
    @staticmethod
    def authenticate(client_id, version=1):
        return {"v": version, "client_id": client_id}

    @staticmethod
    def set_activity(activity, nonce, pid=os.getpid()):
        return {
            "cmd": "SET_ACTIVITY",
            "args": {
                "activity": activity,
                "pid": pid
            },
            "nonce": nonce
        }


class Discord(object):
    def __init__(self):
        self.sock = None
        env_vars = ["XDG_RUNTIME_DIR", "TMPDIR", "TMP", "TEMP"]
        # Stolen from https://github.com/GiovanniMCMXCIX/PyDiscordRPC/blob/master/rpc.py
        path = next((os.environ.get(path, None) for path in env_vars if path in os.environ), '/tmp')
        self.ipc_path = f"{path}/discord-ipc-0"

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.ipc_path)
        return self.sock

    def send(self, op, payload):
        if isinstance(op, OP):
            op = op.value
        payload = json.dumps(payload).encode("utf8")
        body = struct.pack("<ii", op, len(payload)) + payload
        return self.sock.sendall(body)

    def recv(self):
        data = self.sock.recv(8)
        return struct.unpack("<ii", data)

    def handshake(self, client_id):
        self.send(OP.AUTHENTICATE, Message.authenticate(str(client_id)))
        op, length = self.recv()
        assert op == OP.FRAME.value
        body = json.loads(self.sock.recv(length).decode("utf8"))
        assert body["evt"] == "READY"
        return body

    def set_activity(self, activity, pid=None):
        nonce = str(uuid.uuid4())
        self.send(OP.FRAME, Message.set_activity(activity, nonce))
        op, length = self.recv()
        assert op == OP.FRAME.value
        body = json.loads(self.sock.recv(length).decode("utf8"))
        assert body["cmd"] == "SET_ACTIVITY"
        assert body["nonce"] == nonce
        return body

    def shutdown(self):
        self.send(OP.CLOSE, {})
