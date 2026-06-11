from tracker_client import (
    get_peers,
    load_torrent
)

from handshake import connect_to_peer

from bitfield import (
    parse_bitfield,
    parse_have
)

from peer_messages import (
    recv_message,
    send_interested,
    wait_for_unchoke
)

from downloader import (
    download_piece
)


filename = (
    "ubuntu-26.04-desktop-"
    "amd64.iso.torrent"
)

# Easier to test initially
target_piece = 0


_, torrent = load_torrent(
    filename
)

peers, info_hash, peer_id = (
    get_peers(filename)
)

print(
    f"Found {len(peers)} peers"
)


for ip, port in peers:

    try:

        print(
            f"\nTrying {ip}:{port}"
        )


        sock, result = (
            connect_to_peer(
                ip,
                port,
                info_hash,
                peer_id
            )
        )

        print(
            "Handshake successful!"
        )

        pieces = set()

        while True:

            message = recv_message(
                sock
            )

            if message["id"] is None:

                continue

            elif message["id"] == 5:

                pieces.update(
                    parse_bitfield(
                        message[
                            "payload"
                        ]
                    )
                )

                print(
                    f"Peer has "
                    f"{len(pieces)} "
                    f"pieces"
                )

            elif message["id"] == 4:

                piece = parse_have(
                    message[
                        "payload"
                    ]
                )

                pieces.add(
                    piece
                )

                print(
                    f"Have: piece "
                    f"{piece}"
                )

            else:

                print(
                    f"Received "
                    f"message ID "
                    f"{message['id']}, "
                    "skipping..."
                )

            if (
                target_piece
                in pieces
            ):

                print(
                    f"Peer has "
                    f"piece "
                    f"{target_piece}"
                )

                break

        print(
            "Sending interested..."
        )

        send_interested(
            sock
        )

        print(
            "Waiting for unchoke..."
        )

        wait_for_unchoke(
            sock
        )

        print(
            "Peer unchoked us!"
        )

        piece_data = (
            download_piece(
                sock,
                torrent,
                target_piece
            )
        )

        print(
            f"\nSuccessfully "
            f"downloaded "
            f"piece "
            f"{target_piece}"
        )

        print(
            f"Piece size: "
            f"{len(piece_data)} "
            f"bytes"
        )

        sock.close()

        break

    except Exception as e:

        print(
            f"Failed: {e}"
        )

else:

    print(
        "Could not connect "
        "to any suitable peer."
    )