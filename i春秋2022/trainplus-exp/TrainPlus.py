def Md00Plus(message: bytes):
    h0 = 0x114514ab
    h1 = 0x1919810a
    h2 = 0xa0189191
    h3 = 0xba415411

    R = (7, 12, 17, 22) * 4 + (5, 9, 14, 20) * 4 + (4, 11, 16, 23) * 4 + (6, 10, 15, 21) * 4
    K = (0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
         0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8,
         0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193,
         0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340, 0x265e5a51,
         0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
         0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905,
         0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681,
         0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60,
         0xbebfbc70, 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
         0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244,
         0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92,
         0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314,
         0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391)

    F = lambda x, y, z: ((x & y) | ((~x) & z))
    G = lambda x, y, z: ((x & z) | (y & (~z)))
    H = lambda x, y, z: (x ^ y ^ z)
    I = lambda x, y, z: (y ^ (x | (~z)))

    L = lambda x, n: ((x << n) | (x >> (32 - n))) & 0xffffffff
    W = lambda i4, i3, i2, i1: (i1 << 24) | (i2 << 16) | (i3 << 8) | i4
    reverse = lambda x: (x << 24) & 0xff000000 | (x << 8) & 0x00ff0000 | \
                        (x >> 8) & 0x0000ff00 | (x >> 24) & 0x000000ff

    ascii_list = list(map(lambda x: x, message))
    msg_length = len(ascii_list) * 8
    ascii_list.append(128)

    while (len(ascii_list) * 8 + 64) % 512 != 0:
        ascii_list.append(1)

    for i in range(8):
        ascii_list.append((msg_length >> (8 * i)) & 0xff)

    for i in range(len(ascii_list) // 64):
        a, b, c, d = h0, h1, h2, h3
        for j in range(64):
            if 0 <= j <= 15:
                f = F(b, c, d) & 0xffffffff
                g = j
            elif 16 <= j <= 31:
                f = G(b, c, d) & 0xffffffff
                g = ((5 * j) + 1) % 16
            elif 32 <= j <= 47:
                f = H(b, c, d) & 0xffffffff
                g = ((3 * j) + 5) % 16
            else:
                f = I(b, c, d) & 0xffffffff
                g = (7 * j) % 16
            aa, dd, cc = d, c, b
            s = i * 64 + g * 4
            w = W(ascii_list[s], ascii_list[s + 1], ascii_list[s + 2], ascii_list[s + 3])
            bb = (L((a + f + K[j] + w) & 0xffffffff, R[j]) + b) & 0xffffffff
            a, b, c, d = aa, bb, cc, dd
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
    h0, h1, h2, h3 = reverse(h0), reverse(h1), reverse(h2), reverse(h3)
    digest = (h0 << 96) | (h1 << 64) | (h2 << 32) | h3
    return hex(digest)[2:].rjust(32, '0'),ascii_list

def md5ex(hash,message: bytes):
    reverse = lambda x: (x << 24) & 0xff000000 | (x << 8) & 0x00ff0000 | \
                        (x >> 8) & 0x0000ff00 | (x >> 24) & 0x000000ff
    hash = int(hash,16)
    h3 = reverse(hash&0xffffffff)
    hash >>= 32
    h2 = reverse(hash&0xffffffff)
    hash >>= 32
    h1 = reverse(hash&0xffffffff)
    hash >>= 32
    h0 = reverse(hash&0xffffffff)

    R = (7, 12, 17, 22) * 4 + (5, 9, 14, 20) * 4 + (4, 11, 16, 23) * 4 + (6, 10, 15, 21) * 4
    K = (0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
         0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8,
         0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193,
         0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340, 0x265e5a51,
         0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
         0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905,
         0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681,
         0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60,
         0xbebfbc70, 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
         0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244,
         0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92,
         0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314,
         0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391)

    F = lambda x, y, z: ((x & y) | ((~x) & z))
    G = lambda x, y, z: ((x & z) | (y & (~z)))
    H = lambda x, y, z: (x ^ y ^ z)
    I = lambda x, y, z: (y ^ (x | (~z)))

    L = lambda x, n: ((x << n) | (x >> (32 - n))) & 0xffffffff
    W = lambda i4, i3, i2, i1: (i1 << 24) | (i2 << 16) | (i3 << 8) | i4

    ascii_list = list(map(lambda x: x, message))
    msg_length = len(ascii_list) * 8 + 512
    ascii_list.append(128)

    while (len(ascii_list) * 8 + 64) % 512 != 0:
        ascii_list.append(1)

    for i in range(8):
        ascii_list.append((msg_length >> (8 * i)) & 0xff)

    for i in range(len(ascii_list) // 64):
        a, b, c, d = h0, h1, h2, h3
        for j in range(64):
            if 0 <= j <= 15:
                f = F(b, c, d) & 0xffffffff
                g = j
            elif 16 <= j <= 31:
                f = G(b, c, d) & 0xffffffff
                g = ((5 * j) + 1) % 16
            elif 32 <= j <= 47:
                f = H(b, c, d) & 0xffffffff
                g = ((3 * j) + 5) % 16
            else:
                f = I(b, c, d) & 0xffffffff
                g = (7 * j) % 16
            aa, dd, cc = d, c, b
            s = i * 64 + g * 4
            w = W(ascii_list[s], ascii_list[s + 1], ascii_list[s + 2], ascii_list[s + 3])
            bb = (L((a + f + K[j] + w) & 0xffffffff, R[j]) + b) & 0xffffffff
            a, b, c, d = aa, bb, cc, dd
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
    h0, h1, h2, h3 = reverse(h0), reverse(h1), reverse(h2), reverse(h3)
    digest = (h0 << 96) | (h1 << 64) | (h2 << 32) | h3
    return hex(digest)[2:].rjust(32, '0'),ascii_list

from pwn import*
import string
from pwnlib.util.iters import mbruteforce
from hashlib import*
table = string.ascii_letters+string.digits

io = remote("127.0.0.1",10114)

def pow1():
    io.recvuntil(b'XXXX+')
    suffix = io.recv(16).decode("utf8")
    io.recvuntil(b'== ')
    cipher = io.recvline().strip().decode("utf8")
    proof = mbruteforce(lambda x: sha256((x + suffix).encode()).hexdigest() ==
                        cipher, table, length=4, method='fixed')
    io.sendlineafter(b'XXXX :', proof.encode())
    return cipher
pow1()

io.recvuntil(b'Thing:')
GreatThing = io.recv(16)

from Crypto.Util.number import*
io.recvuntil(b'REATTHING:')
Md00 = io.recv(32)
H = md5ex(Md00.decode(),GreatThing)[0].encode()
for i in range(1,26):
    Pad = Md00Plus(i*b'a')[1][i:]
    MSG = bytes(Pad) + GreatThing
    s = hex(bytes_to_long(MSG))[2:].encode()+b','+ hex(bytes_to_long(H))[2:].encode()
    io.sendline(s)
    print(i,io.recv())
    msg = io.recv()
    if b'flag' in msg:
        print(msg)
        break
io.interactive()