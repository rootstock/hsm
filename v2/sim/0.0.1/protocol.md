# FedHM protocol definition v2.x

## Definitions

- `xxxxx`: String
- `hhhhh`: Hex string
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
    "message": {
        tx: "hhhhh", // (**)
        input: i // (***)
    },
    "auth": {
        rsk_block_header: "hhhhh",
        receipt: "hhhhh",
        receipt_merkle_proof: [
            "hhhhh", "hhhhh", ..., "hhhhh"
        ]
    },
    "version": 2
}

// (*) the given string must be the
// BIP44 path of the key to use for signing.

// (**) the fully serialized BTC transaction
// that needs to be signed.

// (***) the input index of the BTC transaction
// that needs to be signed.
```

#### Response
```
{
    "signature": {
        "r": "hhhhh",
        "s": "hhhhh"
    },
    "errorcode": i
}
```

**Error codes:**
- `0`: Ok
- `-1`: Wrong auth
- `-2`: Generic error (device not ready)
- `-3`: Invalid message
- `-10`: Wrong version

### Get public key

#### Request
```
{
    "command": "getPubKey",
    "keyId": "xxxxx", // (**)
    "auth": "xxxxx", (***)
    "version": 2
}

// (**) the given string must be the
// BIP44 path of the key of which to retrieve
// the public key.
//
// (***) not in use at the moment, no need to send.
```

#### Response
```
{
    "pubKey": "hhhhh",
    "errorcode": i
}
```

**Error codes:**
- `0`: Ok
- `-1`: Wrong auth
- `-2`: Generic error (device not ready)
- `-10`: Wrong version

### Generic error codes

The following are error codes that can apply to any request. The are numbers lower than `900`.

- `-901`: Format error
- `-902`: Invalid request
- `-903`: Command unknown
