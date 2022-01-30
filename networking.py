from model import Singleton
import socket
from typing import Tuple
from message import Message, MessageSerializer
from typing import NamedTuple


class Peer(NamedTuple):
    host: str
    port: int


class Socket(Singleton):
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def ping(self, peer: Peer) -> None:
        self._socket.sendto(b'0', peer)

    def keep_alive(self, peer: Peer) -> None:
        self.ping(peer)

    def bind(self, address: Peer) -> None:
        self._socket.bind(address)

    def read(self, size: int) -> Tuple[Message, Peer]:
        message, peer = self._socket.recvfrom(size)
        message = MessageSerializer.deserialize(message)

        return message, Peer(peer[0], peer[1])

    def write(self, message: Message, peer: Peer) -> None:
        self._socket.sendto(MessageSerializer.serialize(message), peer)