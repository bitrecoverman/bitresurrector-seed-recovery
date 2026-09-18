# Mathematical specification of mnemonic entropy constraints

## Entropy bounds and combinatorial search space

A BIP-39 mnemonic phrase encodes a binary entropy sequence concatenated with a deterministic checksum:

$$\\text{Total bits} = E + \\frac{E}{32}$$

For a 12-word phrase ($E = 128$ bits):
* Entropy: 128 bits
* Checksum length: $128 / 32 = 4$ bits
* Total bit length: 132 bits
* Sliced into 12 blocks of 11 bits each ($2^{11} = 2048$)

The checksum is defined as:
$$\\text{CS} = \\text{SHA-256}(E)[0] \\gg 4$$

Because the 4-bit checksum is strictly deterministic, the probability that an arbitrary 12th word satisfies the checksum for a given 128-bit prefix is:
$$P(\\text{valid}) = \\frac{1}{2^4} = \\frac{1}{16} = 6.25\\%$$

Consequently, early bitwise verification rejects $93.75\\%$ of unviable candidates before key derivation.

## Electrum Modern v2 HMAC prefix filter

Modern Electrum seeds evaluate an HMAC-SHA512 digest:
$$\\text{Digest} = \\text{HMAC-SHA512}(\\text{Key}=\\text{"Seed version"}, \\text{Data}=\\text{Phrase})$$

Valid prefixes:
* Native SegWit (`bc1q`): Digest begins with `0x100` (byte 0 is `0x10`, high nibble of byte 1 is `0x00`).
* Standard Legacy (`1`): Digest begins with `0x01`.

This criterion enforces an early rejection rate of $255 / 256 \\approx 99.6\\%$.
