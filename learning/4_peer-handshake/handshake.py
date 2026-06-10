import socket


def build_handshake(info_hash, peer_id):

    protocol = b"BitTorrent protocol"

    pstrlen = len(protocol).to_bytes(1, 'big')

    reserved = b'\x00' * 8

    handshake = (
        pstrlen +
        protocol +
        reserved +
        info_hash +
        peer_id
    )

    return handshake


def recv_exact(sock, n):

    data = b''

    while len(data) < n:

        chunk = sock.recv(n - len(data))

        if not chunk:
            raise ConnectionError(
                "Peer closed connection"
            )

        data += chunk

    return data


def parse_handshake(data):

    pstrlen = data[0]

    protocol = data[1:1 + pstrlen]

    reserved_start = 1 + pstrlen

    info_start = reserved_start + 8

    peer_start = info_start + 20

    info_hash = data[info_start:peer_start]

    peer_id = data[peer_start:peer_start + 20]

    return {
        "protocol": protocol,
        "info_hash": info_hash,
        "peer_id": peer_id
    }


def connect_to_peer(ip, port,
                    info_hash,
                    peer_id):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(10)

    sock.connect((ip, port))

    handshake = build_handshake(
        info_hash,
        peer_id
    )

    sock.sendall(handshake)

    response = recv_exact(sock, 68)

    result = parse_handshake(response)

    if result["info_hash"] != info_hash:

        sock.close()

        raise ValueError(
            "Info hash mismatch"
        )

    sock.close()

    return result