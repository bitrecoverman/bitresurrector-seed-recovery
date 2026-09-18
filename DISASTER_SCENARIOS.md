# Physical disaster recovery casebook

This casebook outlines 7 real-world physical failure scenarios affecting mnemonic storage media and their algorithmic solutions:

## Case 1: Torn paper edge
* **Pattern:** Missing final two words (positions 11 and 12).
* **Search Space:** 4194304 dictionary pairs.
* **Resolution:** Bitwise checksum reduces search to 262144 BIP-39 candidates and 16000 Electrum candidates, resolved in 1.5 to 4 seconds.

## Case 2: Fluid stain
* **Pattern:** Single word blurred with known first letter and character count.
* **Resolution:** Mask constraints (e.g. `p*****`) reduce candidate words from 2048 to 38, resolved in under 0.05 seconds.

## Case 3: Circular metal disc
* **Pattern:** Words stamped around a ring without a start index.
* **Resolution:** The cyclic group solver tests all 12 rotations in 0.002 seconds.

## Case 4: Two-column notebook layout (2x6)
* **Pattern:** Ambiguity between horizontal (row-wise) and vertical (column-wise) reading order.
* **Resolution:** Evaluates 64 row-alternating trajectories in less than 1 millisecond.

## Case 5: Charred paper note
* **Pattern:** Multiple burn holes with partial letter fragments.
* **Resolution:** Positional multi-slot wildcard masks eliminate non-matching words in L1 cache.

## Case 6: Handwriting ambiguity and typos
* **Pattern:** Cursive ambiguity and phonetic non-dictionary spellings.
* **Resolution:** Levenshtein distance fuzzy matcher restores correct dictionary entries.

## Case 7: Quadrant paper split
* **Pattern:** Sheet separated into 4 distinct quadrants along fold creases.
* **Resolution:** Block permutation engine reconstructs 12-word strings from 3-word chunks in 0.05 seconds.
