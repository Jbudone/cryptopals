from Crypto.Cipher import AES
import random
import math

def rand_key():
    key = ''
    for i in range(0, 16):
        key += chr( random.randint(0, 255) )
    return key

def randPadding():
    num = random.randint(5, 10)
    pad = ''
    for i in range(1, num):
       pad += chr( random.randint(0, 255) )
    return pad

def padding(plaintext):
    missing = int(math.ceil(len(plaintext) / 16.0)) * 16 - len(plaintext)
    pad = chr(missing)
    return plaintext + pad * missing


def xor(block, key):
    xored = ""
    for i in range(0, len(block)):
        xored += chr( ord(block[i]) ^ ord(key[i]) )
    return xored

def encrypt_ecb(plaintext):
    key = rand_key()
    aes = AES.new(key, AES.MODE_ECB)
    blocks = [plaintext[i:i+16] for i in range(0, len(plaintext), 16)]
    ciphertext = ''
    for block in blocks:
        plain = block
        cipher = aes.encrypt(plain)
        ciphertext += cipher
    return ciphertext

def encrypt_cbc(plaintext):
    key = rand_key()
    iv = rand_key()
    aes = AES.new(key, AES.MODE_ECB)
    blocks = [plaintext[i:i+16] for i in range(0, len(plaintext), 16)]
    cipher = iv
    ciphertext = ''
    for block in blocks:
        plain = xor(block, cipher)
        cipher = aes.encrypt(plain)
        ciphertext += cipher
    return ciphertext


# Return the number of patterns between these two blocks
def scoreBlocks(blockA, blockB):
    score = 0
    for i in range(0, 16):
        if (blockA[i] == blockB[i]):
            score += 1
    return score

# Score a line by checking for any repetitions between blocks (of 16 bytes) in the line
def scoreLine(line):
    blocks = [list(line[i:i+16]) for i in range(0, len(line), 16)]
    score = 0
    for i in range(1, len(blocks)):
        for j in range(0, i):
            score += scoreBlocks(blocks[i], blocks[j])
    return score


def encryption_oracle(plaintext):
    plaintext = randPadding() + plaintext + randPadding()
    plaintext = padding(plaintext)

    mode = random.randint(1,2)
    if mode == 1:
        print "ECB"
        return encrypt_ecb(plaintext)
    else:
        print "CBC"
        return encrypt_cbc(plaintext)

def detection(ciphertext):
    score = scoreLine(ciphertext)
    numBlocks = len(ciphertext) / 16
    minScorePerBlock = 2
    minScore = numBlocks * minScorePerBlock
    print score
    print numBlocks
    if score > minScore:
        print "Its totally an ECB, bro"
    else:
        print "I smell an CBC crypto"

plaintext = "Testing, testing.. 123. Testing, testing, testing, testing testing 12..1....1....123Testing, testing.. 123. Testing, testing, testing, testing testing 12..1....1....12Testing, testing.. 123. Testing, testing, testing, testing testing 12..1....1....12Testing, testing.. 123. Testing, testing, testing, testing testing 12..1....1....12Testing, testing.. 123. Testing, testing, testing, testing testing 12..1....1....12Testing, testing.. 123. Testing, testing, testing, testing testing 12..1....1....1233333"

ciphertext = encryption_oracle(plaintext)
print ciphertext
detection(ciphertext)
