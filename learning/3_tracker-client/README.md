# Phase 4 - Tracker Communication

## Objective

Implement tracker communication for a BitTorrent client.

The goal of this phase was to contact a real BitTorrent tracker, announce participation in a torrent swarm, and obtain a list of peers currently sharing or downloading the file.

---

## Concepts Learned

* BitTorrent trackers
* Tracker announce requests
* URL encoding
* Peer IDs
* Info hashes
* HTTP requests using Python
* Bencoded tracker responses
* Peer discovery

---

## How It Works

1. Read and parse the `.torrent` file.
2. Compute the SHA-1 info hash from the raw `info` dictionary bytes.
3. Generate a 20-byte BitTorrent peer ID.
4. Construct the tracker announce URL with the required parameters:

   * `info_hash`
   * `peer_id`
   * `port`
   * `uploaded`
   * `downloaded`
   * `left`
   * `compact`
5. Send an HTTP GET request to the tracker.
6. Decode the bencoded tracker response.
7. Extract and display:

   * Number of seeders
   * Number of leechers
   * Reannounce interval
   * Peer IP addresses and ports

---

## Project Structure

```text
tracker-client/
├── tracker_client.py
├── parser.py
├── README.md
└── ubuntu-26.04-desktop-amd64.iso.torrent
```

---

## Running the Program

```bash
python tracker_client.py
```

---

## Example Output

```text
Seeders: 2260
Leechers: 73
Interval: 1800 seconds

Peers:

[2a01:e0a:11d:9860:9209:d0ff:fe21:adb]:16881
185.125.190.59:6903
...
```

---

## Outcome

Successfully communicated with a real BitTorrent tracker and discovered active peers participating in the Ubuntu torrent swarm.

This marks the first phase in which the project interacts with the live BitTorrent network.
