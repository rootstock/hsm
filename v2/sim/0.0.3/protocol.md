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

For this operation, depending on the `keyId` parameter, there's two possible formats: the authorized and the non-authorized. Details follow.

##### Authorized format

This format is only valid for the BTC and tBTC key ids (see corresponding section for details).

```
{
    "command": "sign",
    "keyId": "xxxxx", // (*)
    "message": {
        tx: "hhhh", // (**)
        input: i // (***)
    },
    "auth": {
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
// See valid BIP44 paths below (BTC and tBTC for this format).
// (**) the fully serialized BTC transaction
// that needs to be signed.
// (***) the input index of the BTC transaction
// that needs to be signed.
```

##### Non-authorized format

This format is only valid for the RSK, MST, tRSK and tMST key ids (see corresponding section for details).

```
{
    "command": "sign",
    "keyId": "xxxxx", // (*)
    "message": {
        hash: "hhhh", // (**)
    },
    "version": 2
}

// (*) the given string must be the
// BIP44 path of the key to use for signing.
// See valid BIP44 paths below (RSK, MST, tBTC and tMST for this format).
// (**) the hash that needs to be signed.
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
- `-5`: Invalid key ID
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
- `-5`: Invalid key ID
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
