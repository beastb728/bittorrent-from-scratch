from tracker_client import get_peers
from handshake import connect_to_peer
from bitfield import (
    recv_message,
    parse_bitfield,
    parse_have
)

filename = "ubuntu-26.04-desktop-amd64.iso.torrent"

peers, info_hash, peer_id = get_peers(
    filename
)

print(
    f"Found {len(peers)} peers"
)

for ip, port in peers:

    try:

        if ':' in ip:

            print(
                f"\nSkipping IPv6 peer: "
                f"{ip}:{port}"
            )

            continue

        print(
            f"\nTrying {ip}:{port}"
        )

        sock, result = connect_to_peer(
            ip,
            port,
            info_hash,
            peer_id
        )

        print(
            "Handshake successful!"
        )

        print(
            "Protocol:",
            result["protocol"].decode()
        )

        print(
            "Peer ID:",
            result["peer_id"]
        )

        pieces = set()

        while True:

            message = recv_message(
                sock
            )

            if message["id"] is None:

                print(
                    "Keep-alive received"
                )

                continue

            elif message["id"] == 5:

                pieces.update(
                    parse_bitfield(
                        message["payload"]
                    )
                )

                print(
                    f"Peer has "
                    f"{len(pieces)} pieces"
                )

                print(
                    "First 20 pieces:"
                )

                print(
                    sorted(pieces)[:20]
                )

                sock.close()

                break

            elif message["id"] == 4:

                piece = parse_have(
                    message["payload"]
                )

                pieces.add(piece)

                print(
                    f"Have: piece "
                    f"{piece}"
                )

            else:

                print(
                    f"Received message ID "
                    f"{message['id']}, "
                    "skipping..."
                )

        break

    except Exception as e:

        print(
            f"Failed: {e}"
        )

else:

    print(
        "Could not connect to any peer."
    )