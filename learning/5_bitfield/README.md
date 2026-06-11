# Phase 5 - Bitfield Exchange

## Objective

Implement peer wire message handling for a BitTorrent client.

The goal of this phase was to maintain communication with peers after the BitTorrent handshake, receive peer messages, and determine which pieces of the torrent a peer possesses through bitfield and have messages.

---

## Concepts Learned

* Peer wire protocol messages
* Message framing using length prefixes
* Bitfield messages
* Have messages
* Keep-alive messages
* Piece availability advertisement
* Bit-level operations
* Parsing binary payloads
* Long-lived TCP peer connections
* Real-world peer behavior

---

## How It Works

1. Read and parse the `.torrent` file.

2. Compute the SHA-1 info hash from the raw `info` dictionary bytes.

3. Contact the tracker and obtain a list of peers participating in the torrent swarm.

4. Generate a 20-byte BitTorrent peer ID.

5. Select a peer from the discovered peer list.

6. Establish a TCP connection to the peer.

7. Perform the BitTorrent handshake and verify that both peers are participating in the same torrent swarm.

8. Keep the TCP connection open after the handshake.

9. Receive peer wire protocol messages by:

   * Reading the 4-byte message length prefix.
   * Reading the message ID.
   * Reading the corresponding payload.

10. Handle keep-alive messages when the length prefix is zero.

11. Parse bitfield messages to determine which pieces the peer possesses.

12. Parse have messages to identify individual pieces advertised by the peer.

13. Display information about the pieces announced by the peer.

---

## Peer Message Structure

```text
+------------------+--------------+-------------+
| 4 bytes          | 1 byte       | Variable    |
+------------------+--------------+-------------+
| Length Prefix    | Message ID   | Payload     |
+------------------+--------------+-------------+
```

---

## Relevant Message IDs

```text
0  -> choke
1  -> unchoke
2  -> interested
3  -> not interested
4  -> have
5  -> bitfield
6  -> request
7  -> piece
8  -> cancel
```

---

## Bitfield Structure

Each bit represents whether the peer possesses a particular piece.

Example:

```text
10110010
```

Interpretation:

```text
Piece 0 -> Present
Piece 1 -> Missing
Piece 2 -> Present
Piece 3 -> Present
Piece 4 -> Missing
Piece 5 -> Missing
Piece 6 -> Present
Piece 7 -> Missing
```

---

## Have Message Structure

```text
+------------------+--------------+-------------+
| 4 bytes          | 1 byte       | 4 bytes     |
+------------------+--------------+-------------+
| Length Prefix    | Message ID   | Piece Index |
+------------------+--------------+-------------+
```

Example:

```text
Message ID: 4
Piece Index: 16522
```

Meaning:

```text
Peer possesses piece #16522.
```

---

## Project Structure

```text
5_bitfield/
├── parser.py
├── tracker_client.py
├── handshake.py
├── bitfield.py
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
Found 8 peers

Skipping IPv6 peer: 2001:470:58de:ff:9e6b:ff:feac:8bad:55280

Trying 185.125.190.59:6907
Handshake successful!

Protocol: BitTorrent protocol
Peer ID: b'T03I--012K9Xgfo.BhTJ'

Received message ID 1, skipping...

Have: piece 16522
Have: piece 11426

Failed: Peer closed connection
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

The client skipped IPv6 peers and continued searching for compatible IPv4 peers.

---

### Peers Do Not Always Send Bitfields

While the BitTorrent protocol supports bitfield messages, not all peers send them immediately after the handshake.

Some peers instead advertised available pieces incrementally using have messages.

Others closed the connection before transmitting a bitfield.

This demonstrated that real-world peer behavior can vary significantly from simplified protocol examples.

---

## Outcome

Successfully maintained communication with real BitTorrent peers after the handshake phase.

The client received and parsed peer wire protocol messages, handled keep-alive messages, processed have messages announcing piece availability, and implemented support for bitfield parsing.

This phase introduced the concept of piece availability and established the foundation required for requesting and downloading actual torrent data.

---

## Key Milestone

With the completion of this phase, the client is now capable of:

* Parsing torrent metadata
* Computing torrent identifiers
* Discovering peers through trackers
* Establishing TCP connections with peers
* Performing the BitTorrent handshake protocol
* Receiving peer wire protocol messages
* Parsing bitfield messages
* Parsing have messages
* Determining which pieces peers possess

The next step is to request and download individual pieces from peers.
