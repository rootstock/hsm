
# HSM

## Usage

Make sure you have Python 3 install.

Also, make sure you have pip installed with Python 3.

Needs secp256k1, install with:

> sudo pip install secp256k1

Run with:

> python3 fedhm-mockup.py

You may need to create a file named `key.secp256` manually and put the generated private key in it.

For options:

> python3 fedhm-mockup.py -h

To quickly test the client, make sure you have `telnet` install and in a new command line run:

> telnet localhost 9999

You should see a response like this:

```
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
```
