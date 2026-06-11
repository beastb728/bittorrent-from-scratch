# Phase 6 - Piece Download and Verification

## Objective

Implement piece downloading for a BitTorrent client.

The goal of this phase was to request actual torrent data from real peers, receive the requested blocks through the BitTorrent peer wire protocol, reconstruct complete pieces, and verify their integrity using SHA-1 hashes obtained from the torrent metadata.

---

## Concepts Learned

* Interested messages
* Choke and unchoke mechanisms
* Piece request messages
* Piece messages
* Block-based downloading
* Piece reconstruction
* SHA-1 piece verification
* Data integrity validation
* IPv6 peer support
* Real-world swarm interaction
* Sequential block transfers

---

## How It Works

1. Read and parse the `.torrent` file.

2. Compute the SHA-1 info hash from the raw `info` dictionary bytes.

3. Contact the tracker and obtain a list of peers participating in the torrent swarm.

4. Generate a 20-byte BitTorrent peer ID.

5. Select a peer from the discovered peer list.

6. Establish a TCP connection with either IPv4 or IPv6 peers.

7. Perform the BitTorrent handshake and verify that both peers are participating in the same torrent swarm.

8. Receive peer wire protocol messages and determine which pieces the peer possesses using bitfield and have messages.

9. Identify a piece available from the connected peer.

10. Send an interested message indicating the desire to download data from the peer.

11. Wait until the peer unchokes the client.

12. Divide the target piece into smaller blocks.

13. Request each block sequentially using request messages.

14. Receive piece messages containing the requested blocks.

15. Reconstruct the complete piece by appending all received blocks in order.

16. Compute the SHA-1 hash of the reconstructed piece.

17. Compare the computed hash against the expected hash stored in the torrent metadata.

18. Confirm successful verification of the downloaded piece.

---

## Interested Message Structure

```text
+------------------+--------------+
| 4 bytes          | 1 byte       |
+------------------+--------------+
| Length Prefix    | Message ID   |
+------------------+--------------+
|        1         |      2       |
+------------------+--------------+
```

Meaning:

```text
The client wishes to download data from the peer.
```

---

## Request Message Structure

```text
+------------------+--------------+-------------+-------------+-------------+
| 4 bytes          | 1 byte       | 4 bytes     | 4 bytes     | 4 bytes     |
+------------------+--------------+-------------+-------------+-------------+
| Length Prefix    | Message ID   | Piece Index | Begin       | Length      |
+------------------+--------------+-------------+-------------+-------------+
```

Where:

```text
Message ID = 6
```

Fields:

```text
Piece Index -> Piece being requested
Begin       -> Offset within the piece
Length      -> Number of bytes requested
```

---

## Piece Message Structure

```text
+------------------+--------------+-------------+-------------+-------------+
| 4 bytes          | 1 byte       | 4 bytes     | 4 bytes     | Variable    |
+------------------+--------------+-------------+-------------+-------------+
| Length Prefix    | Message ID   | Piece Index | Begin       | Block Data  |
+------------------+--------------+-------------+-------------+-------------+
```

Where:

```text
Message ID = 7
```

Meaning:

```text
Peer is sending the requested block data.
```

---

## Block-Based Downloading

Torrent pieces are downloaded in smaller blocks.

Example:

```text
Piece Length = 262144 bytes
Block Size  = 16384 bytes
```

Calculation:

```text
262144 ÷ 16384 = 16 blocks
```

Request sequence:

```text
Request Block 0
↓
Receive Block 0

Request Block 1
↓
Receive Block 1

...

Request Block 15
↓
Receive Block 15
```

After all blocks have been received:

```text
Complete Piece Reconstructed
```

---

## Piece Verification

Every torrent stores the SHA-1 hash of each piece.

Verification process:

```text
Downloaded Piece
↓
SHA-1 Hash Computation
↓
Compare Against Expected Hash
↓
Valid or Corrupt
```

Successful verification confirms that the piece has been transferred correctly and has not been tampered with.

---

## Project Structure

```text
6_download-piece/
├── parser.py
├── tracker_client.py
├── handshake.py
├── bitfield.py
├── peer_messages.py
├── downloader.py
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

Trying 2001:41d0:303:9b68::2:17005
Handshake successful!

Peer has 24868 pieces
Peer has piece 0

Sending interested...
Waiting for unchoke...

Peer unchoked us!

Downloaded 16384/262144 bytes
Downloaded 32768/262144 bytes
Downloaded 49152/262144 bytes
Downloaded 65536/262144 bytes
Downloaded 81920/262144 bytes
Downloaded 98304/262144 bytes
Downloaded 114688/262144 bytes
Downloaded 131072/262144 bytes
Downloaded 147456/262144 bytes
Downloaded 163840/262144 bytes
Downloaded 180224/262144 bytes
Downloaded 196608/262144 bytes
Downloaded 212992/262144 bytes
Downloaded 229376/262144 bytes
Downloaded 245760/262144 bytes
Downloaded 262144/262144 bytes

Successfully downloaded piece 0
Piece size: 262144 bytes
```

---

## Challenges Encountered

### IPv6 Peers

A significant portion of peers returned by the tracker used IPv6 addresses.

Initially, the client created only IPv4 sockets using:

```python
socket.AF_INET
```

which resulted in IPv6 peers being skipped.

The connection logic was updated to dynamically select:

```python
socket.AF_INET
```

for IPv4 peers and:

```python
socket.AF_INET6
```

for IPv6 peers.

This greatly increased the number of reachable peers within the swarm.

---

### Real-World Peer Behavior

Peers did not always behave exactly as simplified protocol examples suggested.

Observed behaviors included:

* Peers sending have messages instead of bitfields.
* Peers closing connections unexpectedly.
* Peers unchoking immediately after the handshake.
* Peers responding differently despite participating in the same swarm.

Handling these situations highlighted the importance of building resilient protocol implementations.

---

## Outcome

Successfully downloaded a complete piece from a real BitTorrent peer.

The client established a connection with a peer, exchanged protocol messages, requested piece blocks, reconstructed the piece from the received data, and verified its integrity using SHA-1 hashing.

Although the downloaded piece existed only in memory and was not yet written to disk, this phase demonstrated that the client could retrieve authentic torrent data from the public BitTorrent network.

---

## Key Milestone

With the completion of this phase, the client is now capable of:

* Parsing torrent metadata
* Computing torrent identifiers
* Discovering peers through trackers
* Establishing IPv4 and IPv6 peer connections
* Performing the BitTorrent handshake protocol
* Receiving peer wire protocol messages
* Determining which pieces peers possess
* Expressing download interest to peers
* Handling peer unchoking
* Requesting piece blocks
* Receiving piece data
* Reconstructing complete pieces
* Verifying downloaded data using SHA-1 hashes

The next step is to download all pieces of a torrent and reconstruct the original file on disk.
