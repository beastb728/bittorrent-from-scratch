from bittorrent.tracker_client import (
    load_torrent,
    get_peers
)

from bittorrent.file_manager import (
    create_output_file,
    save_piece
)

from bittorrent.handshake import (
    connect_to_peer
)

from bittorrent.bitfield import (
    parse_bitfield,
    parse_have
)

from bittorrent.peer_messages import (
    recv_message,
    send_interested,
    wait_for_unchoke
)

from bittorrent.downloader import (
    download_piece
)


def get_peer_pieces(sock):

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
                    message["payload"]
                )
            )

            print(
                f"Peer has "
                f"{len(pieces)} "
                f"pieces"
            )

            return pieces

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
                f"Received "
                f"message ID "
                f"{message['id']}, "
                "skipping..."
            )


def download_torrent(filename):

    torrent_data, torrent = (
        load_torrent(filename)
    )

    filepath = create_output_file(
        torrent_data,
        torrent
    )

    peers, info_hash, peer_id = (
        get_peers(filename)
    )

    total_pieces = len(
        torrent["pieces"]
    )

    completed = set()

    print(
        f"Found {len(peers)} peers"
    )

    print(
        f"Need to download "
        f"{total_pieces} pieces"
    )

    for ip, port in peers:

        sock = None

        try:

            print(
                f"\nTrying "
                f"{ip}:{port}"
            )

            sock, _ = connect_to_peer(
                ip,
                port,
                info_hash,
                peer_id
            )

            print(
                "Handshake successful!"
            )

            pieces = get_peer_pieces(
                sock
            )

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

            print(
                f"Received "
                f"{len(pieces)} "
                f"pieces from peer"
            )

            for piece_index in sorted(pieces):

                if piece_index in completed:

                    continue

                print(
                    f"\nDownloading "
                    f"piece "
                    f"{piece_index}"
                )

                piece_data = (
                    download_piece(
                        sock,
                        torrent,
                        piece_index
                    )
                )

                save_piece(
                    filepath,
                    piece_index,
                    torrent[
                        "piece_length"
                    ],
                    piece_data
                )

                completed.add(
                    piece_index
                )

                print(
                    f"Completed "
                    f"{len(completed)}/"
                    f"{total_pieces}"
                )

                progress = (
                    len(completed) /
                    total_pieces
                ) * 100

                print(
                    f"Progress: "
                    f"{progress:.2f}%"
                )

                if (
                    len(completed)
                    == total_pieces
                ):

                    print(
                        "\nTorrent "
                        "download complete!"
                    )

                    return (
                        torrent,
                        filepath,
                        peers,
                        info_hash,
                        peer_id,
                        completed,
                        total_pieces
                    )

        except Exception as e:

            print(
                f"Failed: {e}"
            )

            continue

        finally:

            if sock:

                sock.close()

    if len(completed) == 0:

        print(
            "Could not download "
            "from any peer."
        )

    elif (
        len(completed)
        < total_pieces
    ):

        print(
            f"\nIncomplete "
            f"download: "
            f"{len(completed)}/"
            f"{total_pieces} "
            f"pieces."
        )

    else:

        print(
            "\nDownload "
            "completed "
            "successfully!"
        )

    return (
        torrent,
        filepath,
        peers,
        info_hash,
        peer_id,
        completed,
        total_pieces
    )
