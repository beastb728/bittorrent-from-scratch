from parser import decode
import urllib.parse
import urllib.request
import parser
import hashlib
import random


def load_torrent(filename):
    with open(filename, "rb") as f:
        data = f.read()

    torrent_data, _ = decode(data)

    info_bytes = data[parser.INFO_START:parser.INFO_END]

    info_hash = hashlib.sha1(info_bytes).digest()

    return torrent_data, info_hash


def generate_peer_id():
    random_digits = ''.join(
        str(random.randint(0, 9))
        for _ in range(12)
    )

    peer_id = "-PC0001-" + random_digits

    return peer_id.encode()


def get_peers(filename):

    torrent_data, info_hash = load_torrent(filename)

    peer_id = generate_peer_id()

    announce = torrent_data[b'announce'].decode()

    left = torrent_data[b'info'][b'length']

    params = {
        "info_hash": info_hash,
        "peer_id": peer_id,
        "port": 6881,
        "uploaded": 0,
        "downloaded": 0,
        "left": left,
        "compact": 0
    }

    query_string = urllib.parse.urlencode(
        params,
        quote_via=urllib.parse.quote
    )

    tracker_url = announce + "?" + query_string

    try:

        response = urllib.request.urlopen(
            tracker_url,
            timeout=10
        )

    except Exception as e:

        raise ConnectionError(
            f"Tracker request failed: {e}"
        )

    tracker_response = response.read()

    tracker_data, _ = decode(tracker_response)

    peers = []

    for peer in tracker_data[b'peers']:

        ip = peer[b'ip'].decode()

        port = peer[b'port']

        peers.append((ip, port))

    return peers, info_hash, peer_id