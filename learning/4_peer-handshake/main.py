from tracker_client import get_peers
from handshake import connect_to_peer


filename = "ubuntu-26.04-desktop-amd64.iso.torrent"

peers, info_hash, peer_id = get_peers(
    filename
)

print(
    f"Found {len(peers)} peers"
)

for ip, port in peers:

    try:

        print(
            f"\nTrying {ip}:{port}"
        )

        result = connect_to_peer(
            ip,
            port,
            info_hash,
            peer_id
        )

        print(
            "Handshake successful!"
        )

        print(
            "Protocol:",
            result["protocol"].decode()
        )

        print(
            "Peer ID:",
            result["peer_id"]
        )

        break

    except Exception as e:

        print(
            f"Failed: {e}"
        )