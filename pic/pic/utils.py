from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64


def b64_to_pic(b64: str, dir, file_name):
    data = b64[b64.index(',') + 1:]
    bin_pic = base64.b64decode(data)
    with open(dir + file_name, 'wb') as f:
        f.write(bin_pic)


suffix = b'LYsWlwTzDA0rB8c1'
key = 'IdTJq0HklpuI6mu8iB%OO@!vd^4K&uXW'
iv = b'$0v@krH7V2883346'


def aes_cbc_pk5_padding_dec(b64_data: str):
    aes = AES.new(key.encode(encoding='utf-8'), mode=AES.MODE_CBC, IV=iv)
    data = base64.b64decode(b64_data)
    return unpad(aes.decrypt(data), 16).decode(encoding='utf-8')


if __name__ == '__main__':
    print(aes_cbc_pk5_padding_dec('PFbixdjrzMpaviinhU6t3v4KEUyOvW2U1vHmk3I9Lvo='))
