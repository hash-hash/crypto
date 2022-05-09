from MD_Train import MD00Plus
from hashlib import sha256
import socketserver
import signal
import string
import random
import os
from secret import flag


banner = br'''
ooooooooooooo                     o8o              ooooooooo.   oooo                       
8'   888   `8                     `"'              `888   `Y88. `888                       
     888      oooo d8b  .oooo.   oooo  ooo. .oo.    888   .d88'  888  oooo  oooo   .oooo.o 
     888      `888""8P `P  )88b  `888  `888P"Y88b   888ooo88P'   888  `888  `888  d88(  "8 
     888       888      .oP"888   888   888   888   888          888   888   888  `"Y88b.  
     888       888     d8(  888   888   888   888   888          888   888   888  o.  )88b 
    o888o     d888b    `Y888""8o o888o o888o o888o o888o        o888o  `V88V"V8P' 8""888P' 
'''
table = string.ascii_letters+string.digits
sec = os.urandom(random.randrange(1,26))
GreatThing = os.urandom(16)

class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'\n'
            self.request.sendall(msg)
        except:
            pass

    def recv(self, prompt=b'SERVER <INPUT>: '):
        self.send(prompt, newline=False)
        return self._recvall()

    def proof_of_work(self):
        proof = (''.join([random.choice(table)for _ in range(20)])).encode()
        sha = sha256(proof).hexdigest().encode()
        self.send(b"[+] sha256(XXXX+" + proof[4:] + b") == " + sha )
        XXXX = self.recv(prompt = b'[+] Plz Tell Me XXXX :')
        if len(XXXX) != 4 or sha256(XXXX + proof[4:]).hexdigest().encode() != sha:
            return False
        return sha.decode()

    def handle(self):
        signal.alarm(30)
        FirstBlockHash = self.proof_of_work()
        if not FirstBlockHash:
            self.request.close()


        self.send(banner)
        self.send(b":) My Great Thing:" + GreatThing )
        self.send(b":) The MD00Plus of my GREATTHING:" + MD00Plus(sec).encode())

        for i in range(25):
            self.send(b"Please tell me the msg ")
            msg = self.recv()
            self.send(b"Please tell me the hash you can forcast.")
            msg,Hash = msg.split(b',')
            msg = bytes.fromhex(msg.decode())
            Hash = bytes.fromhex(Hash.decode())
            if GreatThing not in msg:
                self.send(b"[!]INVALID!")
                continue
            elif MD00Plus(sec + msg).encode() == Hash:
                self.send(flag)
                break
            else:
                self.send(b'You Wrong!')

        self.request.close()

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10114
    print("HOST:POST " + HOST+":" + str(PORT))
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
