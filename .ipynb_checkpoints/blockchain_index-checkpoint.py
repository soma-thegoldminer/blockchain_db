
from struct import unpack

from btc_utils import BTCUtils as Utils

BLOCK_HAVE_DATA = 8
BLOCK_HAVE_UNDO = 16


def _read_varint(raw_hex):
    """
    Reads the weird format of VarInt present in src/serialize.h of bitcoin core
    and being used for storing data in the leveldb.
    This is not the VARINT format described for general bitcoin serialization
    use.
    """
    n = 0
    pos = 0
    while True:
        data = raw_hex[pos]
        pos += 1
        n = (n << 7) | (data & 0x7f)
        if data & 0x80 == 0:
            return n, pos
        n += 1


class DBBlockIndex(object):
    def __init__(self, blk_hash, raw_hex):
        self.hash = blk_hash
        pos = 0
        n_version, i = _read_varint(raw_hex[pos:])
        pos += i
        self.height, i = _read_varint(raw_hex[pos:])
        pos += i
        self.status, i = _read_varint(raw_hex[pos:])
        pos += i
        self.n_tx, i = _read_varint(raw_hex[pos:])
        pos += i
        if self.status & (BLOCK_HAVE_DATA | BLOCK_HAVE_UNDO):
            self.file, i = _read_varint(raw_hex[pos:])
            pos += i
        else:
            self.file = -1

        if self.status & BLOCK_HAVE_DATA:
            self.data_pos, i = _read_varint(raw_hex[pos:])
            pos += i
        else:
            self.data_pos = -1
        if self.status & BLOCK_HAVE_UNDO:
            self.undo_pos, i = _read_varint(raw_hex[pos:])
            pos += i

        assert(pos + 80 == len(raw_hex))
        self.version, p, m, time, bits, self.nonce = unpack(
            "<I32s32sIII",
            raw_hex[-80:])
        
        self.prev_hash = Utils.format_hash(p)
        self.merkle_root = Utils.format_hash(m)

    def __repr__(self):
        return "DBBlockIndex(%s, height=%d, file_no=%d, file_pos=%d)" \
               % (self.hash, self.height, self.file, self.data_pos)
    
    def to_json(self):
        return {
            'blk_hash': self.hash,
            'prev_hash': self.prev_hash,
            'height': self.height,
            'file': self.file,
            'nTxns': self.n_tx,
            'status': self.status,
            'data_posn': self.data_pos,
            'merkle_root' : self.merkle_root,
            'version': self.version,
            'nounce':self.nonce
        }
