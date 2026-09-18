import itertools
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

def solve_adjacent_swaps(words):
    if len(words) != 12:
        return []
    valid = []
    for choices in itertools.product([False, True], repeat=6):
        w = list(words)
        for pair_idx in range(6):
            if choices[pair_idx]:
                i = pair_idx * 2
                w[i], w[i+1] = w[i+1], w[i]
        p_str = " ".join(w)
        etype = get_electrum_v2_type(p_str)
        if etype:
            valid.append((choices, etype, p_str))
    return valid

if __name__ == '__main__':
    if len(sys.argv) < 13:
        print("Usage: python pairwise_swap_solver.py word1 word2 ... word12")
        sys.exit(1)
    res = solve_adjacent_swaps(sys.argv[1:13])
    print(f"Tested 64 adjacent swap permutations. Found {len(res)} valid:")
    for choices, etype, phrase in res:
        print(f"  Swap pattern {choices} ({etype}): {phrase}")
