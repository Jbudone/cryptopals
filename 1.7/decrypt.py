from Crypto.Cipher import AES

key = "YELLOW SUBMARINE"
file = open('7.txt', 'r').read().replace('\n', '').decode('base64')
plaintext = ''

blocks = [file[i:i+16] for i in range(0, len(file), 16)]
aes = AES.new(key, AES.MODE_ECB)
for block in blocks:
    plaintext += aes.decrypt(block)

print plaintext

