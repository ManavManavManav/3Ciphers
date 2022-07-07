#!/usr/bin/python3

import sys

mx = sys.maxsize*2+2


def reverseShuffle(block, firstKeystream):# loads an initial keystream and generates the following 16, to recreate a reverse shuffle order
    temp2 = []
    temp2.append(firstKeystream)
    for i in range(16):
        temp2.append(lcg(temp2[i-1]))
    for i in range(16):
        temp = str(hex(temp2[15-i]))

        if(len(temp) < 4):
            first = 0
            second = int(temp[-1], 16)
        else:
            first = int(temp[-2], 16)
            second = int(temp[-1], 16)

        one = block[first]
        two = block[second]
        block[second] = one
        block[first] = two
    return block


def byteShuffle(block, recordedKeystream): #loads an initial keystream and generates the following 16, shuffles based on stream hex 0xNM swapping N and M
    temp2 = []
    temp2.append(recordedKeystream)
    for i in range(16):
        temp2.append(lcg(temp2[i-1]))
    for i in range(16):
        temp = str(hex(temp2[i]))

        if(len(temp) < 4):
            first = 0
            second = int(temp[-1], 16)
        else:
            first = int(temp[-2], 16)
            second = int(temp[-1], 16)

        one = block[first]
        two = block[second]
        block[second] = one
        block[first] = two
    return block


def lcg(rand):  # linear congruential generator takes a prev seed and generates a new seed(single vals<256)
    a = 1103515245
    c = 12345
    m = 2**8
    return ((a*rand + c) % m)


def pseudoOverflow(value):  # mimick C overflow in py
    return value % mx


def passwordSeed(password):  # generates seed from given password text
    hash = 0
    for x in password:
        hash = ord(x)+pseudoOverflow(hash << 6) + \
            pseudoOverflow(hash << 16)-pseudoOverflow(hash)
        hash = pseudoOverflow(hash)
    return hash


def main():
    #arg len check
    if(len(sys.argv) != 4):
        print("Invalid Arg count")
        exit(1)

    password = sys.argv[1]
    file1 = open(sys.argv[2], "rb")
    file2 = open(sys.argv[3], "wb")
    # encrypt or decrypt
    
    #tracks padding
    padding = 0
    seed = passwordSeed(password)
    lastBlock = [int(x) for x in str(seed)]
    lastBlock=lastBlock[0:16]
    keystream=lcg(seed)
    for i in range(16):
        lastBlock[i]= keystream
        keystream=lcg(keystream)

    pbyte = bytes(1)

    cipherByteArray = bytearray()
    while(pbyte):
        recordedKeystream = keystream
        pbyte = file1.read(16)
        plainList = list(pbyte)

        if padding == 0 and len(plainList) == 0:
            for i in range(16):
                plainList.append(16)
        elif padding > 0 and len(plainList) == 0:
            break
        else:
            padding = 16-len(plainList)
            for i in range(padding):
                plainList.append(padding)



        tempByteArray = bytearray()
        for i in range(16):
            tempByteArray += (lastBlock[i] ^ plainList[i]
                                ).to_bytes(1, sys.byteorder)
        # lastBlock=tempByteArray


        tempByteArray = byteShuffle(tempByteArray, recordedKeystream)

        tempBlock = list(tempByteArray)
        tempByteArray = bytearray()

        for i in range(16):
            tempByteArray += (tempBlock[i] ^
                                keystream).to_bytes(1, sys.byteorder)
            keystream = lcg(keystream)
        
        for i in range(16):
            lastBlock[i]=tempByteArray[i]


        cipherByteArray += tempByteArray
    
    file2.write(bytes(cipherByteArray))

main()