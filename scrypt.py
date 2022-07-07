#!/usr/bin/python3

import sys

#mimicking C overflow
mx = sys.maxsize*2+2
def int_overflow(val):
    # only covers left shifts use commented code for both

    # right+left bit shift case
    #   if not -sys.maxsize-1 <= val <= sys.maxsize:
    #     val = (val + (sys.maxsize + 1)) % (2 * (sys.maxsize + 1)) - sys.maxsize - 1
    return val % mx


def lcg(rand):
  a = 1103515245
  c = 12345
  m = 2**8
  return ((a*rand + c)%m)

def passToSeed(pas):
  hash = 0
  for x in pas:
    hash = ord(x)+int_overflow(hash << 6) +int_overflow(hash << 16)-int_overflow(hash)
    hash = int_overflow(hash)
  return hash


if(len(sys.argv)!=4):
  print("Invalid Arg count")
  exit(1)


pas = sys.argv[1]
p=open(sys.argv[2],"rb")
c=open(sys.argv[3],"wb")


plainByteArray = bytearray()
pbyte = bytes(1)
while(pbyte):
    pbyte = p.read(1)
    plainByteArray += pbyte


cipherByteArray=bytearray()

t=lcg(passToSeed(pas))
for i in range(len(plainByteArray)):
  x = plainByteArray[i]^t
  x=x.to_bytes(1,sys.byteorder)
  cipherByteArray+=x
  t=lcg(t)

c.write(bytes(cipherByteArray))