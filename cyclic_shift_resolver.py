import sys
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

def resolve_cyclic_shifts(words):
    if len(words) != 12:
        return []
    valid = []
    for shift in range(12):
        rotated = words[shift:] + words[:shift]
        p_str = " ".join(rotated)
        etype = get_electrum_v2_type(p_str)
        if etype:
            valid.append((shift, etype, p_str))
    return valid

if __name__ == '__main__':
    if len(sys.argv) < 13:
        print("Usage: python cyclic_shift_resolver.py word1 word2 ... word12")
        sys.exit(1)
    input_words = sys.argv[1:13]
    res = resolve_cyclic_shifts(input_words)
    print(f"Tested 12 rotations. Found {len(res)} valid orientations:")
    for shift, etype, phrase in res:
        print(f"  Shift +{shift} ({etype}): {phrase}")
