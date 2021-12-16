#
# fedhm mockup server v1.3
# needs secp256k1, install with:
#     $ sudo pip install secp256k1
# run with:
#     $ python3 fedhm-mockup.py
# for options:
#     $ python3 fedhm-mockup.py -h
#
#
# example client test:
#
"""
guest@guest-thinkpad:~$ telnet localhost 9999
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
{"command":"version"}
{"errorcode": "0", "version": "1"}
"""
#
#

import json
import socketserver
import secp256k1
import binascii
import time
from optparse import OptionParser

version = 1

class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        global key
        global log
        global logseq, logtop
        global version
        # self.request is the TCP socket connected to the client
        self.data = self.rfile.readline().strip()
        print("[I] {} Received command:").format(self.client_address[0])
        print(self.data)
        out = {}
        out["errorcode"] = -2
        try:
            cmd = json.loads(self.data)
            # return version
            if cmd["command"] == "version":
                out["version"] = version
                out["errorcode"] = 0
            elif "version" not in cmd:
                out["errorcode"] = -4
                out["error"] = "You should provide 'version' field."
            elif cmd["version"] != version:
                out["errorcode"] = -666
                out["error"] = "Requested version " + cmd["version"] + " but the gateway version is " + version
            else:
                # sign bytes
                if cmd["command"] == "sign":
                    #sign message
                    sign_ecdsa = key.ecdsa_sign(binascii.unhexlify(cmd["message"]), raw=True)
                    sign_bytes = key.ecdsa_serialize(sign_ecdsa)
                    #generate log entry
                    logentry = {}
                    logentry["lastLogHash"] = "TODO"
                    logentry["logseq"] = "%d" % logseq
                    logentry["timestamp"] = "%d" % int(time.time()) # get timestamp
                    logentry["tick"] = 0
                    logseq += 1
                    #add log
                    log.append(logentry)
                    # Decode from DER
                    # Fourth byte has got the length of R, and R follows
                    # (First three bytes are: 30 - sequence follows, total length byte, 02 indicating
                    # number follows)
                    r_len = int(binascii.hexlify(sign_bytes[3:4]), 16)
                    rbytes = sign_bytes[4:4+r_len]
                    # Second byte after R has got the length of S, and S follows
                    # (first byte after R has got type of value that follows - 02 - number)
                    s_len = int(binascii.hexlify(sign_bytes[5+r_len:6+r_len]), 16)
                    sbytes = sign_bytes[6+r_len:6+r_len+s_len]

                    signature = {}
                    signature["r"]=binascii.hexlify(rbytes)
                    signature["s"]=binascii.hexlify(sbytes)
                    out["signature"] = signature
                    out["errorcode"] = 0
                # retrieve log
                if cmd["command"] == "getLog":
                    if logtop >= logseq:
                        out["errorcode"] = -3
                    else:
                        logentry = log[logtop]
                        out["lastBlockHast"] = logentry["lastBlockHash"]
                        out["lastLogHash"] = logentry["lastLogHash"]
                        out["logseq"] = "%d" % logseq
                        out["timestamp"] = logentry["timestamp"]
                        out["tick"] = logentry["tick"]
                        out["errorcode"] = 0
                # return public key
                if cmd["command"] == "getPubKey":
                    out["pubKey"] = binascii.hexlify(
                        key.pubkey.serialize(compressed=False))
                    out["errorcode"] = 0
        except Exception as e:
            print('[E] Error: ' + str(e))
            print(repr(e))
            out["error"] = 'unhandled exception with message ' + str(e)
            out["errorcode"] = -4
            logtop += 1
        self.request.sendall(json.dumps(out) + "\n")


if __name__ == "__main__":
    global key
    global log
    global logseq, logtop

    # options parsing
    usage = "usage: %prog [--bind Bind ip] [--port port]"
    parser = OptionParser()
    parser.add_option("-p","--port",dest="PORT",help="Listening port (default 9999)",default=9999)
    parser.add_option("-b","--bind",dest="HOST",help="IP to bind to. (default localhost)",default="localhost")
    parser.add_option("-k","--key",dest="KEY",help="Private KEY to load. (default 'key.secp256')",default="key.secp256")
    (options, args) = parser.parse_args()

    HOST=options.HOST
    PORT=int(options.PORT)
    filename=options.KEY

    # main loop
    log = []
    logseq = 0
    logtop = 0
    # Create/load a secp256 key
    print("[I] Loading key file %s" % filename)
    try:
        keyfile = open(filename, "rb")
        keybytes = keyfile.read(1000).rstrip()
        keyfile.close()
        key = secp256k1.PrivateKey()
        key.deserialize(keybytes)
        print("[I] Loaded.Privkey: %s" % key.serialize())
    except:
        print("[I] File not found, generating key...")
        key = secp256k1.PrivateKey(privkey=None)
        print("[I] Generated. Privkey: %s" % key.serialize())
        keyfile = open(filename, "wb")
        keybytes = keyfile.write(key.serialize())
        keyfile.close()
        print("[I] Key saved as %s" % filename)

    # Create the server, binding to HOST:PORT
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print("[I] Listening on %s:%d" % (HOST, PORT))
    server.serve_forever()
