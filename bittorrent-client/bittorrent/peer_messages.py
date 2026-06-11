from bittorrent.handshake import recv_exact


def recv_message(sock):

    length_bytes = recv_exact(sock, 4)

    length = int.from_bytes(
        length_bytes,
        'big'
    )

    if length == 0:

        return {
            "id": None,
            "payload": b''
        }

    message_id = recv_exact(
        sock,
        1
    )[0]

    payload = recv_exact(
        sock,
        length - 1
    )

    return {
        "id": message_id,
        "payload": payload
    }


def send_interested(sock):

    message = (
        (1).to_bytes(4, 'big') +
        bytes([2])
    )

    sock.sendall(message)


def wait_for_unchoke(sock):

    while True:

        message = recv_message(sock)

        if message["id"] is None:

            continue

        elif message["id"] == 1:

            return

        elif message["id"] == 0:

            print(
                "Peer is choking us..."
            )

            continue

        else:

            print(
                f"Received message "
                f"{message['id']} "
                f"while waiting for "
                f"unchoke"
            )


def send_request(
    sock,
    piece_index,
    begin,
    length
):

    payload = (
        piece_index.to_bytes(
            4,
            'big'
        ) +
        begin.to_bytes(
            4,
            'big'
        ) +
        length.to_bytes(
            4,
            'big'
        )
    )

    message = (
        (13).to_bytes(
            4,
            'big'
        ) +
        bytes([6]) +
        payload
    )

    sock.sendall(message)


def receive_piece(sock):

    while True:

        message = recv_message(sock)

        if message["id"] is None:

            continue

        elif message["id"] == 7:

            payload = message[
                "payload"
            ]

            piece_index = (
                int.from_bytes(
                    payload[:4],
                    'big'
                )
            )

            begin = (
                int.from_bytes(
                    payload[4:8],
                    'big'
                )
            )

            block = payload[8:]

            return {
                "piece_index":
                    piece_index,
                "begin":
                    begin,
                "block":
                    block
            }

        else:

            print(
                f"Ignoring message "
                f"{message['id']}"
            )