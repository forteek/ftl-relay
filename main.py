from networking import Socket, Peer
from message import MessageSerializer, MessageEvent, Message
from typing import Dict, List


def main(host: str, port: int):
    sock = Socket()
    sock.bind(Peer(host, port))
    print(f'Relay listening for connections on {host}:{port}')
    known_files: Dict[str, List[Peer]] = {}

    while True:
        data, peer = sock.read(1024)

        if data.event == MessageEvent.HAS:
            filename = data.content
            if filename in known_files:
                if peer not in known_files[filename]:
                    known_files[filename].append(peer)
            else:
                known_files[data.content] = [peer]

        elif data.event == MessageEvent.NEED:
            filename = data.content
            if filename in known_files:
                for peer in known_files[filename]:
                    sock.write(
                        Message(MessageEvent.NEED, filename),
                        peer
                    )

        print(known_files)


if __name__ == '__main__':
    main('0.0.0.0', 62012)
