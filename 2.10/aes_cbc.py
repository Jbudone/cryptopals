from Crypto.Cipher import AES
import math

encrypt = True
file = open("10.txt").read().decode('base64')
plain = "Testing testing, 123"

iv = "\x00" * 16
key = "YELLOW SUBMARINE"
aes = AES.new(key, AES.MODE_ECB)

def xor(block, key):
    xored = ""
    for i in range(0, len(block)):
        xored += chr( ord(block[i]) ^ ord(key[i]) )
    return xored

def padding(plaintext):
    missing = int(math.ceil(len(plaintext) / 16.0)) * 16 - len(plaintext)
    pad = chr(missing)
    return plaintext + pad * missing

def encrypt(plaintext, iv):
    plaintext = padding(plaintext)
    blocks = [plaintext[i:i+16] for i in range(0, len(plaintext), 16)]
    cipher = iv
    ciphertext = ''
    for i in range(0, len(blocks)):
        block = blocks[i]
        plain = xor(block, cipher)
        cipher = aes.encrypt(plain)
        ciphertext += cipher
    return ciphertext

def decrypt(ciphertext, iv):
    blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    xored = iv
    plain = ''
    for i in range(0, len(blocks)):
        block = blocks[i]
        decrypted = aes.decrypt(block)
        plain += xor(decrypted, xored)
        xored = block
    return plain


plaintext = ""
ciphertext = ""

plaintext = decrypt(file, iv)
print plaintext
