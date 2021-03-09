# Changes

Changes from version 0.1.4:

## Features/enhancements

- Added support for Iris network upgrade (by default activated from block 3,000,000 for mainnet and 2,000,000 for testnet -- final values TBD).
- Merge mining merkle proof maximum size set to 960 bytes from Iris onwards.
- Added three new unauthorized signing paths (see [the protocol documentation](./protocol.md) for details). The corresponding old paths are now deprecated.
- Added network 'regtest' with activation block numbers set to zero for testing purposes (`-n regtest` command line option).
- The build is now a `.tgz` bundle archive that contains the binary (`sim.tgz`). The docker runner build takes care of the extraction. Manual extraction is required to run outside of the given docker image.

## Fixes

- BTC transactions are now unsigned before computing the sighash (this mimics the actual ledger signer behavior).
- The build is now compatible with older glibc versions (2.24+)
