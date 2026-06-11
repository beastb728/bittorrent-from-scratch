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


def parse_have(payload):

    return int.from_bytes(
        payload,
        'big'
    )