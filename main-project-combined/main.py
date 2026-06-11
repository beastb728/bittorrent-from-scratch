from bittorrent.client import (
    download_torrent
)

TORRENT_FILE = (
    "torrents/"
    "ubuntu-26.04-desktop-"
    "amd64.iso.torrent"
)

download_torrent(
    TORRENT_FILE
)