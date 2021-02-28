
from binascii import hexlify
import hashlib, codecs
from configparser import ConfigParser
from bson.binary import Binary as BsonBinary

class BTCUtils(object):
    
    @staticmethod
    def load_config(config_file, section_name):
        config = ConfigParser()
        config.read(config_file)
        return config[section_name]
    
    @staticmethod
    def b2x(b):
        return b.hex();
    
    @staticmethod
    def s2x(s):
        return hexlify(bytes(s, 'utf-8'))
    
    @staticmethod
    def x2b(x):
        return codecs.decode(x, 'hex')
    
    @staticmethod
    def x2bson(x):
        return BsonBinary(BTCUtils.x2b(x), 5)
    
    @staticmethod
    def s2bson(s):
        return BTCUtils.x2bson(BTCUtils.s2x(s))
    
    @staticmethod
    def i2x(i,nBits):
        return hex(i)[2:].zfill(nBits);
    
    @staticmethod
    def seed2pvk(s_str, nHash=1):
        seed_b = s.encode('utf8') #converts string to bytes
        for x in range(nHash):
            sha_pvk = hashlib.sha256(seed_b)
            seed_b = sha_pvk;
        pvk_b = sha_pvk.digest()
        return pvk_b
    
    @staticmethod
    def btc_ripemd160(data):
        h1 = hashlib.sha256(data).digest()
        r160 = hashlib.new("ripemd160")
        r160.update(h1)
        return r160.digest()

    @staticmethod
    def double_sha256(data):
        return hashlib.sha256(hashlib.sha256(data).digest()).digest()

    @staticmethod
    def format_hash(hash_):
        return str(hexlify(hash_[::-1]).decode("utf-8"))

    @staticmethod
    def decode_uint32(data):
        assert(len(data) == 4)
        return struct.unpack("<I", data)[0]

    @staticmethod
    def decode_uint64(data):
        assert(len(data) == 8)
        return struct.unpack("<Q", data)[0]

    @staticmethod
    def decode_varint(data):
        assert(len(data) > 0)
        size = int(data[0])
        assert(size <= 255)

        if size < 253:
            return size, 1

        if size == 253:
            format_ = '<H'
        elif size == 254:
            format_ = '<I'
        elif size == 255:
            format_ = '<Q'
        else:
            # Should never be reached
            assert 0, "unknown format_ for size : %s" % size

        size = struct.calcsize(format_)
        return struct.unpack(format_, data[1:size+1])[0], size + 1
    
    @staticmethod
    def format_json(json_obj, indent=2):
        json_formatted_str = json.dumps(json.load(json_obj), indent=indent)
        return json_formatted_str
    
    @staticmethod
    def val_non_satoshi(val_satoshi):
        return val_satoshi/100000000
    
    @staticmethod
    def val_satoshi(val_non_satoshi):
        return val_non_satoshi * 100000000

