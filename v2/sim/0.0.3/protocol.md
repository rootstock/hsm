# FedHM protocol definition v2.x

## Definitions

- `xxxxx`: String
- `hhhh`: Hex string
- `i`: Integer

## Commands

### Get version

#### Request
```
{
    "command": "version"
}
```

#### Response
```
{
    "version": 2,
    "errorcode": i
}
```

**Error codes:**
- `0`: Ok
- `-2`: Generic error (device not ready)

### Sign

#### Request
```
{
    "command": "sign",
    "keyId": "xxxxx", // (*)
    "message": { // (**)
        tx: "hhhh", // (x)
        input: i, // (xx)
        hash: "hhhh", // (xxx)
    },
    "auth": { // (***)
        rsk_block_header: "hhhh",
        receipt: "hhhh",
        receipt_merkle_proof: [
            "hhhh", "hhhh", ..., "hhhh"
        ]
    },
    "version": 2
}

// (*) the given string must be the
// BIP44 path of the key to use for signing.
// See valid BIP44 paths below.

// (**) fields required in this object depend on the given key id.
// For the BTC (tBTC) key id, only fields "tx" and "input" are expected.
// For the RSK (tRSK) and MST (tMST) key ids, only the field "hash" is expected.

// (***) only needed if signing with the BTC (tBTC) key.

// (x) the fully serialized BTC transaction
// that needs to be signed.
// (xx) the input index of the BTC transaction
// that needs to be signed.
// (xxx) the hash that needs to be signed by
// either the RSK or MST key.
```

#### Response
```
{
    "signature": {
        "r": "hhhh",
        "s": "hhhh"
    },
    "errorcode": i
}
```

**Error codes:**
- `0`: Ok
- `-1`: Wrong auth
- `-2`: Generic error (device not ready)
- `-3`: Invalid message
- `-4`: Invalid key ID
- `-10`: Wrong version

### Get public key

#### Request
```
{
    "command": "getPubKey",
    "keyId": "xxxxx", // (*)
    "version": 2
}

// (*) the given string must be the
// BIP44 path of the key of which to retrieve
// the public key. See valid BIP44 paths below.
```

#### Response
```
{
    "pubKey": "hhhh",
    "errorcode": i
}
```

**Error codes:**
- `0`: Ok
- `-1`: Wrong auth
- `-2`: Generic error (device not ready)
- `-4`: Invalid key ID
- `-10`: Wrong version

### Generic error codes

The following are error codes that can apply to any request. The are numbers lower than `900`.

- `-901`: Format error
- `-902`: Invalid request
- `-903`: Command unknown

### Valid BIP44 paths

For any operation that requires a `keyId` parameter, the following are the
only accepted BIP44 paths:

- BTC key id - `m/44'/0'/0'/0/0`
- RSK key id - `m/44'/137'/0'/0/0` (\*)
- MST key id - `m/44'/137'/0'/0/1` (\*)
- tBTC key id - `m/44'/1'/0'/0/0`
- tRSK key id - `m/44'/1'/0'/0/1` (\*)
- tMST key id - `m/44'/1'/0'/0/2` (\*)

(\*) Sign operations using these keys don't require authorization.
