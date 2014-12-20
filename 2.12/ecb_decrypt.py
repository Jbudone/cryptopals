from Crypto.Cipher import AES
import random
import math




# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%           ENCRYPTION           %%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


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

def encrypt_ecb(plaintext, aes):
    blocks = [plaintext[i:i+16] for i in range(0, len(plaintext), 16)]
    ciphertext = ''
    for block in blocks:
        plain = block
        cipher = aes.encrypt(plain)
        ciphertext += cipher
    return ciphertext

def encrypt_cbc(plaintext, key):
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


def encryption_oracle(plaintext, aes, always_ecb):
    plaintext = padding(plaintext)

    mode = random.randint(1,2)
    if always_ecb:
        mode = 1

    if mode == 1:
        return encrypt_ecb(plaintext, aes)
    else:
        print "CBC"
        return encrypt_cbc(plaintext, aes)




# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%       BLOCK SIZE DETECTION       %%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Check increments between ciphertext lengths to detect block size
def detect_block_size(aes):
    last_size = 0
    for i in range(1, 128):
        plain = 'A'*i
        ciphertext = encryption_oracle(plain, aes, True)
        if last_size == 0:
            last_size = len(ciphertext)
        elif last_size != len(ciphertext):
            return abs(last_size - len(ciphertext))
    return -1





# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%       ECB DETECTION       %%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%       Decrypt       %%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def decryptChar(block, postfix, i, blocksize, aes):
    findPlain = 'A'*(blocksize-1-i) + postfix + block + 'A'
    findCipher = encrypt_ecb(findPlain, aes)
    for i in range(0, 256):
        print "Testing: "+str(chr(i))
        plain = 'A'*(blocksize-1-i) + postfix + chr(i) + block
        print ('A'*(blocksize-1-i) + postfix + chr(i))
        print str(len(('A'*(blocksize-1-i) + postfix + chr(i))))
        cipher = encrypt_ecb(plain, aes)
        if cipher == findCipher:
            return chr(i)
    return '\0'



def decrypt(blocksize, plaintext, aes):
    blocks = [plaintext[i:i+blocksize] for i in range(0, len(plaintext), blocksize)]
    plain = ''
    block = blocks[0]
    findcipher = ''
    postfix = ''
    for i in range(blocksize-1, 0, -1):
        prefix = 'A'*i
        plaintext = prefix + block + 'A'*(len(postfix)+1)
        cipher = encrypt_ecb(plaintext, aes)
        findcipher = cipher[0:16]
        for k in range(0, 256):
            cipher = encrypt_ecb(prefix + block[0:len(postfix)] + chr(k) + block[len(postfix):] + 'A'*len(postfix), aes)
            cipher = cipher[0:16]
            #print prefix + block[0:len(postfix)] + chr(k) + block[len(postfix):]
            if cipher == findcipher:
                postfix = postfix + chr(k)
                #print "Found char: " + str(k)
                break
        #print "Sure hope we found one.."
    return postfix


key = rand_key()
aes = AES.new(key, AES.MODE_ECB)
plaintext = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK".decode('base64')
#plaintext = "LOL WHAT WHAT WHAT?!"

blocksize = detect_block_size(aes)
print "Blocksize is: " + str(blocksize)

plainCheck = "testing testing testing testing testing testing testing testing testing testing testin"
ciphertext = encryption_oracle(plainCheck, aes, True)
detection(ciphertext)


decrypted = decrypt(blocksize, plaintext, aes)
print decrypted







#key = 'A'*16
#aes = AES.new(key, AES.MODE_ECB)
#plaintext = 'A'*16 + 'A'*8 + 'B'*8
#print plaintext
##encrypted = encrypt_ecb(plaintext, aes)
#encrypted = aes.encrypt(plaintext)
#blocks = [encrypted[i:i+16] for i in range(0, len(encrypted), 16)]
#print blocks
##decrypted = decrypt(blocksize, plaintext, aes)
##print decrypted
