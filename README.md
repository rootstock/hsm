
# HSM

## Usage

Make sure you have Python 3 install.

Also, make sure you have pip installed with Python 3.

You will probably need to create a Python venv (virtual environment) with `python3 -m venv <env_name>`, to install the dependencies like:

> python3 -m venv my_env

Install `secp256k1` with:

> sudo pip install secp256k1

Run with:

> python3 fedhm-mockup.py

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
