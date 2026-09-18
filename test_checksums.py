import unittest
import unicodedata
import hmac
import hashlib

def get_electrum_v2_type(phrase):
    norm = unicodedata.normalize('NFKD', phrase.strip().lower()).encode('utf-8')
    d = hmac.new(b"Seed version", norm, hashlib.sha512).digest()
    b0, b1 = d[0], d[1]
    if b0 == 0x01:
        return 'standard'
    if b0 == 0x10 and (b1 & 0xF0) == 0x00:
        return 'segwit'
    return None

class TestChecksumMechanics(unittest.TestCase):
    def test_electrum_modern_segwit(self):
        sample = "click bus script make all record tomorrow fringe speed lobster judge garment"
        self.assertEqual(get_electrum_v2_type(sample), 'segwit')

    def test_electrum_invalid_seed(self):
        invalid_sample = "abandon ability able about above absent absorb abstract absurd abuse access accident"
        self.assertIsNone(get_electrum_v2_type(invalid_sample))

if __name__ == '__main__':
    unittest.main()
