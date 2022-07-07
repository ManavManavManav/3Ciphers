#!/usr/bin/python3

import sys

k = open(sys.argv[1], "rb")
c = open(sys.argv[2], "rb")
p = open(sys.argv[3], "wb")

keyByteArray = bytearray()
kbyte = bytes(1)
while(kbyte):
    kbyte = k.read(1)
    keyByteArray += kbyte

cipherByteArray = bytearray()
cbyte = bytes(1)
while(cbyte):
    cbyte = c.read(1)
    cipherByteArray += cbyte



plainByteArray=bytearray()
for i in range(len(cipherByteArray)):
    x = (cipherByteArray[i]-keyByteArray[i % len(keyByteArray)] +256)% 256
    if x<0:
        x=256+x

    x=x.to_bytes(1,sys.byteorder)
    plainByteArray+=x


p.write(bytes(plainByteArray))