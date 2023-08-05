"""
Simple symmetric encryption based on rc4
"""

import base64

def _rc4Crypt(data, key):
    """rc4 encryption"""

    S = list(range(256))
    j = 0
    out = []

    #KSA Phase
    for i in range(256):
        j = (j + S[i] + ord( key[i % len(key)] )) % 256
        S[i] , S[j] = S[j] , S[i]

    #PRGA Phase
    i = j = 0
    for char in data:
        i = ( i + 1 ) % 256
        j = ( j + S[i] ) % 256
        S[i] , S[j] = S[j] , S[i]
        out.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))

    return ''.join(out)

# function that encrypts data with RC4 and encodes it in base64 as default
# for other types of data encoding use a different encode parameter
# Use None for no encoding
def encrypt(data, key, encode=base64.b64encode):
    """encrypt"""

    data = _rc4Crypt(data, key)

    if encode:
        data = encode(data.encode())

    return data

#function that decrypts data with RC4 and decodes it in base64 as default
# for other types of data encoding use a different decode parameter
# Use None for no decoding
def decrypt(data, key, decode=base64.b64decode):
    """decrypt"""

    if decode:
        data = decode(data).decode()

    return _rc4Crypt(data, key)
