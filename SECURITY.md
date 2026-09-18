# Security policy

## Supported versions

| Version | Supported |
| :--- | :--- |
| 3.0.x | Yes |
| < 3.0 | No |

## Reporting security vulnerabilities

If you discover a potential vulnerability or security issue within the open-source CLI tools or documentation, please submit a responsible disclosure report to:
`contact@bitcoinrecovery.site`

Please do not disclose security vulnerabilities through public GitHub issues.

## Air-gap execution guidelines

For maximum security when recovering high-value Bitcoin wallets:
1. Download official setup packages exclusively from official GitHub Releases or verified mirrors (`https://bitcoinrecovery.site/`).
2. Verify the SHA-256 integrity hash before execution.
3. Disconnect network adapters or execute the recovery process inside an isolated, air-gapped workstation.
4. bitResurrector does not require an active internet connection to evaluate mnemonic checksums or query the local 256MB Bloom balance filter.
