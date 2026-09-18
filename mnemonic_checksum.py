import hashlib
import hmac
import sys
import unicodedata

def is_valid_bip39(words, wordlist):
    if len(words) not in (12, 15, 18, 21, 24):
        return False
    word_to_idx = {w: i for i, w in enumerate(wordlist)}
    total_val = 0
    for w in words:
        idx = word_to_idx.get(w)
        if idx is None:
            return False
        total_val = (total_val << 11) | idx
    cs_len = len(words) // 3
    ent_len = len(words) * 11 - cs_len
    ent_int = total_val >> cs_len
    cs_val = total_val & ((1 << cs_len) - 1)
    ent_bytes = ent_int.to_bytes(ent_len // 8, 'big')
    expected_cs = hashlib.sha256(ent_bytes).digest()[0] >> (8 - cs_len)
    return cs_val == expected_cs

def get_electrum_v2_type(phrase):
    norm = unicodedata.normalize('NFKD', phrase.strip().lower()).encode('utf-8')
    d = hmac.new(b"Seed version", norm, hashlib.sha512).digest()
    b0, b1 = d[0], d[1]
    if b0 == 0x01:
        return 'standard'
    if b0 == 0x10 and (b1 & 0xF0) == 0x00:
        return 'segwit'
    if b0 == 0x10 and (b1 & 0xF0) == 0x10:
        return '2fa'
    return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python mnemonic_checksum.py "word1 word2 ... word12"")
        sys.exit(1)
    raw = " ".join(sys.argv[1:])
    el_t = get_electrum_v2_type(raw)
    print(f"Electrum v2 type: {el_t if el_t else 'Invalid / Non-Electrum'}")
