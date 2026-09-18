# System architecture and hardware pipeline

## Execution pipeline overview

The bitResurrector framework employs a decoupled multi-stage execution pipeline designed to isolate cryptographic computation from user interface latency:

1. **Positional Constraint Parser:** Validates user input across 12-slot visual grids, compiling wildcard masks, length constraints, and dictionary sub-lists into bitwise bitmasks.
2. **L1/L2 Permutation Streamer:** Generates lexicographic permutations directly in CPU cache registers without dynamic memory allocation overhead.
3. **AVX2 / OpenCL Checksum Barrier:** Discards $93.75\\%$ (BIP-39) to $99.6\\%$ (Electrum) of candidate phrases in SIMD registers prior to PBKDF2.
4. **PBKDF2-HMAC-SHA512 Derivation Engine:** Derives 512-bit binary seeds across multi-core CPU threads or GPU OpenCL compute kernels.
5. **secp256k1 Elliptic Curve Multiplier:** Computes public keys via native optimized C++ libraries.
6. **In-Memory Bloom Filter Query ($O(1)$):** Queries the 256MB memory-mapped address index within 40 nanoseconds without network access.
