from Crypto.Util.number import*
from hashlib import sha256
import socketserver
import signal
import string
import random
from secret import flag

banner = br'''
 .oooooo..o                             oooo  oooo  ooooooooooooo                     o8o              
d8P'    `Y8                             `888  `888  8'   888   `8                     `"'              
Y88bo.      ooo. .oo.  .oo.    .oooo.    888   888       888      oooo d8b  .oooo.   oooo  ooo. .oo.   
 `"Y8888o.  `888P"Y88bP"Y88b  `P  )88b   888   888       888      `888""8P `P  )88b  `888  `888P"Y88b  
     `"Y88b  888   888   888   .oP"888   888   888       888       888      .oP"888   888   888   888  
oo     .d8P  888   888   888  d8(  888   888   888       888       888     d8(  888   888   888   888  
8""88888P'  o888o o888o o888o `Y888""8o o888o o888o     o888o     d888b    `Y888""8o o888o o888o o888o 
'''

n0 = 30798082519452208630254982405300548841337042015746308462162479889627080155514391987610153873334549377764946092629701
g = 64146569863628228208271069055817252751116365290967978172021890038925428672043

def TrainHash(msg):
    n = n0
    msg = map(ord,msg)
    for i in msg :
        n = g * (n+i)
        n = n & (1<<383)
    return n - 0xf5e33dabb114514

table = string.ascii_letters+string.digits

MENU = br'''
<OPTION>
'''

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
        self.send(b"\nPlease give me 2 strings that are same when are hashed  =.=  ")
        string1 = self.recv().decode()
        string2 = self.recv().decode()

        if TrainHash(string1) == TrainHash(string2):
            self.send(b'\nJust do it!~ You can do more!')
            if string2.encode()[-50:] == string1.encode()[-50:]:
                self.send(flag)
        self.send(b"\nConnection has been closed  =.=  ")
        self.request.close()

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10012
    print("HOST:POST " + HOST+":" + str(PORT))
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()