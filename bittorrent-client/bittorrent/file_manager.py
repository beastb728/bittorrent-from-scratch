import os

def create_output_file(
    torrent_data,
    torrent,
    output_dir="downloads"
):

    filename = (
        torrent_data[b'info'][b'name']
        .decode()
    )

    filepath = os.path.join(
        output_dir,
        filename
    )

    total_size = torrent[
        "length"
    ]

    with open(filepath, "wb") as f:

        f.truncate(total_size)

    return filepath

    
def save_piece(
    filepath,
    piece_index,
    piece_length,
    piece_data
):

    offset = (
        piece_index *
        piece_length
    )

    with open(
        filepath,
        "r+b"
    ) as f:

        f.seek(offset)

        f.write(piece_data)