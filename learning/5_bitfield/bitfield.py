from handshake import recv_exact


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


def parse_bitfield(payload):

    pieces = []

    piece_index = 0

    for byte in payload:

        for bit in range(8):

            has_piece = (
                byte >> (7 - bit)
            ) & 1

            if has_piece:

                pieces.append(
                    piece_index
                )

            piece_index += 1

    return pieces


def count_pieces(payload):

    return len(
        parse_bitfield(payload)
    )


def parse_have(payload):

    return int.from_bytes(
        payload,
        'big'
    )