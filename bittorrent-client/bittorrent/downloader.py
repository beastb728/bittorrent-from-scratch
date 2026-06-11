import hashlib

from bittorrent.peer_messages import (
    send_request,
    receive_piece
)


BLOCK_SIZE = 16 * 1024


def verify_piece(
    torrent,
    piece_index,
    piece_data
):

    expected = torrent[
        "pieces"
    ][piece_index]

    actual = hashlib.sha1(
        piece_data
    ).digest()

    return expected == actual


def download_piece(
    sock,
    torrent,
    piece_index
):

    piece_length = torrent[
        "piece_length"
    ]

    total_length = torrent[
        "length"
    ]

    total_pieces = len(
        torrent["pieces"]
    )

    if (
        piece_index ==
        total_pieces - 1
    ):

        remaining = (
            total_length -
            (
                piece_length *
                (total_pieces - 1)
            )
        )

        expected_size = (
            remaining
        )

    else:

        expected_size = (
            piece_length
        )

    piece_data = bytearray()

    offset = 0

    while offset < expected_size:

        request_length = min(
            BLOCK_SIZE,
            expected_size -
            offset
        )

        send_request(
            sock,
            piece_index,
            offset,
            request_length
        )

        response = receive_piece(
            sock
        )

        if (
            response[
                "piece_index"
            ] != piece_index
        ):

            raise ValueError(
                "Received wrong "
                "piece index"
            )

        if (
            response["begin"]
            != offset
        ):

            raise ValueError(
                "Unexpected block "
                "offset"
            )

        piece_data.extend(
            response["block"]
        )

        offset += len(
            response["block"]
        )

        print(
            f"Downloaded "
            f"{offset}/"
            f"{expected_size} "
            f"bytes"
        )

    piece_data = bytes(
        piece_data
    )

    if not verify_piece(
        torrent,
        piece_index,
        piece_data
    ):

        raise ValueError(
            "Piece hash "
            "verification failed"
        )

    return piece_data