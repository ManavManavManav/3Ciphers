#!/usr/bin/python3

import sys

k = open(sys.argv[1], "rb")
p = open(sys.argv[2], "rb")
c = open(sys.argv[3], "wb")

keyByteArray = bytearray()
kbyte = bytes(1)
while(kbyte):
    kbyte = k.read(1)
    keyByteArray += kbyte

plainByteArray = bytearray()
pbyte = bytes(1)
while(pbyte):
    pbyte = p.read(1)
    plainByteArray += pbyte


cipherByteArray=bytearray()

for i in range(len(plainByteArray)):
    x = (plainByteArray[i]+keyByteArray[i % len(keyByteArray)]) % 256
    x=x.to_bytes(1,sys.byteorder)
    cipherByteArray+=x

c.write(bytes(cipherByteArray))

k.close(),p.close(),c.close()
