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


# ==========================
# MAIN PROGRAM
# ==========================

torrent_data, info_hash = load_torrent(
    "ubuntu-26.04-desktop-amd64.iso.torrent"
)

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
    "compact": 1
}

query_string = urllib.parse.urlencode(
    params,
    quote_via=urllib.parse.quote
)

tracker_url = announce + "?" + query_string

print("Tracker URL:")
print(tracker_url)

response = urllib.request.urlopen(tracker_url)

tracker_response = response.read()

print("\nRaw tracker response:")
print(type(tracker_response))
print(len(tracker_response))
print(tracker_response[:100])

print("\nDecoding tracker response...\n")

tracker_data, _ = decode(tracker_response)

print("Tracker response keys:")
for key in tracker_data.keys():
    print(key)

print("\nSeeders:", tracker_data.get(b'complete'))
print("Leechers:", tracker_data.get(b'incomplete'))
print("Interval:", tracker_data.get(b'interval'), "seconds")

print("\nPeers:\n")

peers = tracker_data[b'peers']

for peer in peers:
    ip = peer[b'ip'].decode()
    port = peer[b'port']

    if ":" in ip:
        print(f"[{ip}]:{port}")
    else:
        print(f"{ip}:{port}")