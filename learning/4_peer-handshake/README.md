# Phase 5 - Peer Handshake

## Objective

Implement peer-to-peer communication for a BitTorrent client.

The goal of this phase was to establish direct TCP connections with real BitTorrent peers, perform the BitTorrent handshake protocol, and verify participation in the same torrent swarm.

---

## Concepts Learned

* TCP peer connections
* BitTorrent wire protocol
* Handshake messages
* Peer IDs
* Info hash verification
* Binary protocol construction
* Socket communication in Python
* Receiving fixed-length messages
* Peer validation

---

## How It Works

1. Read and parse the `.torrent` file.

2. Compute the SHA-1 info hash from the raw `info` dictionary bytes.

3. Contact the tracker and obtain a list of peers participating in the torrent swarm.

4. Generate a 20-byte BitTorrent peer ID.

5. Select a peer from the discovered peer list.

6. Establish a TCP connection to the peer.

7. Construct the 68-byte BitTorrent handshake message containing:

   * Protocol string length
   * Protocol identifier (`BitTorrent protocol`)
   * Reserved bytes
   * Torrent info hash
   * Client peer ID

8. Send the handshake to the peer.

9. Receive the peer's handshake response.

10. Parse and validate the response by verifying that the returned info hash matches the requested torrent.

11. Display the peer's client identifier upon successful handshake.

---

## Handshake Structure

```text
+------------+-----------------------+-----------+-------------+----------+
| 1 byte     | 19 bytes              | 8 bytes   | 20 bytes    | 20 bytes |
+------------+-----------------------+-----------+-------------+----------+
| pstrlen    | BitTorrent protocol   | Reserved  | Info Hash   | Peer ID  |
+------------+-----------------------+-----------+-------------+----------+
```

Total size:

```text
68 bytes
```

---

## Project Structure

```text
peer-handshake/
├── parser.py
├── tracker_client.py
├── handshake.py
├── main.py
├── README.md
└── ubuntu-26.04-desktop-amd64.iso.torrent
```

---

## Running the Program

```bash
python main.py
```

---

## Example Output

```text
Found 24 peers

Trying 2a03:3b40:2c:1::3:48389
Failed: Address family for hostname not supported

Trying 185.125.190.59:6918
Handshake successful!

Protocol: BitTorrent protocol
Peer ID: b'T03I--012FoWJsWlSeGz'
```

---

## Challenges Encountered

### IPv6 Peers

Many peers returned by the tracker used IPv6 addresses.

Since the client currently creates IPv4 sockets using:

```python
socket.AF_INET
```

attempts to connect to IPv6 peers failed with:

```text
Address family for hostname not supported
```

The client continued iterating through the peer list until a compatible IPv4 peer was found.

---

## Outcome

Successfully established direct communication with a real BitTorrent peer on the public internet.

The client constructed and transmitted a valid BitTorrent handshake, received the peer's response, and verified participation in the same torrent swarm using the torrent's info hash.

This marks the first phase in which the project communicates directly with other BitTorrent clients rather than intermediary trackers.

At this point, the project has evolved from metadata processing into an actual BitTorrent protocol implementation.

---

## Key Milestone

With the completion of this phase, the client is now capable of:

* Parsing torrent metadata
* Computing torrent identifiers
* Discovering peers through trackers
* Establishing TCP connections with peers
* Performing the BitTorrent handshake protocol

The next step is to exchange bitfields and determine which pieces each peer possesses.
