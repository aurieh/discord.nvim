from contextlib import suppress, contextmanager
import enum
import json
import os
import socket
import struct
import tempfile
import uuid

IPC_SOCKET_NAME = "discord-ipc-0"


@contextmanager
def reconnect_on_failure(discord):
    try:
        yield
    except (socket.error, BrokenPipeError, ConnectionResetError):
        discord.reconnect()


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


class DiscordError(Exception):
    pass


class NoDiscordClientError(DiscordError):
    pass


class ReconnectError(DiscordError):
    pass


class Discord(object):
    def __init__(self, client_id, reconnect_threshold=5):
        # Reconnect props
        self.reconnect_threshold = reconnect_threshold
        self.reconnect_counter = 0

        # Sockets
        self.sock = None

        # Discord
        self.client_id = client_id

        self.ipc_directories = []
        xdg_runtime_dir = os.getenv("XDG_RUNTIME_DIR")
        if xdg_runtime_dir:
            self.ipc_directories.extend([
                xdg_runtime_dir,
                # Flatpak
                os.path.join(xdg_runtime_dir, "app/com.discordapp.Discord"),
                os.path.join(xdg_runtime_dir, "app/com.discordapp.DiscordCanary"),
                # Snap
                os.path.join(xdg_runtime_dir, "snap.discord"),
                os.path.join(xdg_runtime_dir, "snap.discord-canary"),
            ])
        self.ipc_directories.append(tempfile.gettempdir())

    def connect(self, client_id=None):
        self.client_id = self.client_id or client_id
        for ipc_dir in self.ipc_directories:
            path = os.path.join(ipc_dir, IPC_SOCKET_NAME)
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                sock.connect(path)
            except (FileNotFoundError, ConnectionAbortedError, ConnectionRefusedError):
                sock.close()
                continue
            else:
                self.sock = sock
                break
        else:
            raise NoDiscordClientError()
        self.handshake()

    def disconnect(self):
        with suppress(OSError):
            self.sock.close()
        self.sock = None

    def send(self, op, payload):
        if isinstance(op, OP):
            op = op.value
        payload = json.dumps(payload).encode("utf8")
        body = struct.pack("<ii", op, len(payload)) + payload
        with reconnect_on_failure(self):
            return self.sock.sendall(body)
        return None

    def set_activity(self, activity, pid=os.getpid()):
        nonce = str(uuid.uuid4())
        self.send(OP.FRAME, Message.set_activity(activity, nonce, pid))
        op, length = self.recv()
        if not op and not length:
            # There was a successful reconnect attempt
            return self.set_activity(activity, pid)
        body = self.recv_body(length)
        if not body:
            return self.set_activity(activity, pid)
        assert body["cmd"] == "SET_ACTIVITY"
        assert body["nonce"] == nonce

    def shutdown(self):
        with suppress(socket.error, OSError, BrokenPipeError):
            self.send(OP.CLOSE, {})
        self.disconnect()

    def recv(self):
        with reconnect_on_failure(self):
            return struct.unpack("<ii", self.sock.recv(8))
        return (None, None)

    def recv_body(self, length):
        with reconnect_on_failure(self):
            body = json.loads(self.sock.recv(length).decode("utf8"))
            if body["evt"] == "ERROR":
                raise DiscordError(body["data"]["message"])
            return body
        return None

    def handshake(self):
        self.send(OP.AUTHENTICATE, Message.authenticate(str(self.client_id)))
        op, length = self.recv()
        assert op == OP.FRAME.value
        body = self.recv_body(length)
        assert body["evt"] == "READY"
        return body

    def reconnect(self):
        if self.reconnect_counter > self.reconnect_threshold:
            raise ReconnectError("reconnect_counter > reconnect_threshold")
        self.disconnect()
        self.reconnect_counter += 1
        self.connect(self.client_id)
