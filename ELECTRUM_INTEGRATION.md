# Electrum wallet asset reclamation protocol

## Restoring verified seed phrases

1. Launch official Electrum (version 4.0 or newer).
2. Select: **File** -> **New/Restore**.
3. Choose **Standard wallet** -> **I already have a seed**.
4. Enter the 12 verified words.
5. **Important for BIP-39 seeds:** Click **Options** and check **BIP39 seed**.
6. Select address type: Native SegWit (`p2wpkh`) or Legacy (`p2pkh`).
7. Electrum synchronizes on-chain balances and transaction histories.

## Importing discovered private keys (WIF)

1. In Electrum, navigate to: **File** -> **New/Restore**.
2. Select **Import Bitcoin addresses or private keys**.
3. Paste the WIF key string.
4. For Native SegWit addresses, prepend `p2wpkh:` (e.g. `p2wpkh:KxZ...`).
5. Set an encryption password and transfer assets to cold storage.
