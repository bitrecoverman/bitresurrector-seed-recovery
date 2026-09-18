import math
import hashlib

class BloomFilterDemo:
    def __init__(self, size_bytes=1048576, num_hashes=7):
        self.size_bits = size_bytes * 8
        self.bit_array = bytearray(size_bytes)
        self.num_hashes = num_hashes

    def _get_hashes(self, item_bytes):
        h1 = int.from_bytes(hashlib.sha256(item_bytes).digest()[:8], 'big')
        h2 = int.from_bytes(hashlib.sha256(item_bytes + b'\x01').digest()[:8], 'big')
        for i in range(self.num_hashes):
            yield (h1 + i * h2) % self.size_bits

    def add(self, item_bytes):
        for bit_idx in self._get_hashes(item_bytes):
            byte_pos = bit_idx >> 3
            bit_mask = 1 << (bit_idx & 7)
            self.bit_array[byte_pos] |= bit_mask

    def contains(self, item_bytes):
        for bit_idx in self._get_hashes(item_bytes):
            byte_pos = bit_idx >> 3
            bit_mask = 1 << (bit_idx & 7)
            if not (self.bit_array[byte_pos] & bit_mask):
                return False
        return True

if __name__ == '__main__':
    bf = BloomFilterDemo(size_bytes=65536, num_hashes=7)
    test_addr = b"bc1qtestaddressdemonstrationvector"
    bf.add(test_addr)
    print("Address added to Bloom filter.")
    print(f"Query added address: {bf.contains(test_addr)}")
    print(f"Query unknown address: {bf.contains(b'bc1qunknownsampleaddress')}")
