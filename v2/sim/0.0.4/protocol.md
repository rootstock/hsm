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
This operation can return generic errors only. See the error codes section for details.

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
This operation can return `0`, `-101`, `-102`, `-103`, and generic errors. See the error codes section for details.

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
This operation can return `0`, `-103`, and generic errors. See the error codes section for details.

### Error and success codes

The following are all the possible error and success codes:

#### Success codes
- `0`: Ok

#### Authorization-related errors (< `100`)
- `-101`: Wrong authorization
- `-102`: Invalid message
- `-103`: Invalid or unauthorized key ID

#### Generic errors (< `900`).

These errors can be returned by all operations.

- `-901`: Format error
- `-902`: Invalid request
- `-903`: Command unknown
- `-904`: Wrong version
- `-905`: Device error (unspecified)
- `-906`: Unknown error

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
