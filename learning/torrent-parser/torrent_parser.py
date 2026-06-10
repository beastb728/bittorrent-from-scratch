```python
from parser import decode


# ============================================================
# READING THE TORRENT FILE
# ============================================================

with open("ubuntu-26.04-desktop-amd64.iso.torrent", "rb") as f:
    data = f.read()

torrent_data, next_index = decode(data)


# ============================================================
# TOP LEVEL STRUCTURE OF THE .TORRENT FILE
# ============================================================

print(type(torrent_data))
# <class 'dict'>

print(torrent_data.keys())

'''
dict_keys([
    b'announce',
    b'announce-list',
    b'comment',
    b'created by',
    b'creation date',
    b'info'
])

This means:
The whole .torrent file is represented as a dictionary.
'''


# ============================================================
# ANNOUNCE
# ============================================================

print(type(torrent_data[b'announce']))
# <class 'bytes'>

print(torrent_data[b'announce'])

'''
Primary tracker URL.

Example output:
b'https://torrent.ubuntu.com/announce'
'''


# ============================================================
# ANNOUNCE LIST
# ============================================================

print(type(torrent_data[b'announce-list']))
# <class 'list'>

print(torrent_data[b'announce-list'])

'''
List of trackers.

Example output:
[
    [b'https://torrent.ubuntu.com/announce'],
    [b'https://ipv6.torrent.ubuntu.com/announce']
]
'''


# ============================================================
# COMMENT
# ============================================================

print(type(torrent_data[b'comment']))
# <class 'bytes'>

print(torrent_data[b'comment'])

'''
Example output:

b'Ubuntu CD releases.ubuntu.com'
'''


# ============================================================
# CREATED BY
# ============================================================

print(torrent_data[b'created by'].decode())

'''
Software that generated the torrent file.

Example output:

mktorrent 1.1
'''


# ============================================================
# CREATION DATE
# ============================================================

print(type(torrent_data[b'creation date']))
# <class 'int'>

print(torrent_data[b'creation date'])

'''
Unix timestamp.

Represents:
Number of seconds since January 1, 1970.
'''


# ============================================================
# INFO DICTIONARY
# ============================================================

print(type(torrent_data[b'info']))
# <class 'dict'>

print(torrent_data[b'info'].keys())

'''
dict_keys([
    b'length',
    b'name',
    b'piece length',
    b'pieces'
])

The info field itself contains another dictionary.
'''


# ============================================================
# ACTUAL FILE INFORMATION
# ============================================================

info = torrent_data[b'info']

print("Name:", info[b'name'].decode())
print("Size:", info[b'length'])
print("Piece Length:", info[b'piece length'])

'''
Name          -> actual filename being shared
Size          -> total size in bytes
Piece Length  -> size of each torrent piece
'''


# ============================================================
# SHA1 PIECES
# ============================================================

print("Total SHA1 bytes:", len(info[b'pieces']))

print("Number of pieces:", len(info[b'pieces']) // 20)

'''
Each SHA1 hash occupies 20 bytes.

The pieces field stores:

SHA1(piece0) + SHA1(piece1) + SHA1(piece2) + ...

Therefore:

number_of_pieces = len(pieces) // 20
'''
```

