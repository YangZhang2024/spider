from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os
from pymongo import MongoClient
import logging


# data URI scheme
# https://en.wikipedia.org/wiki/Data_URI_scheme#:~:text=The%20data%20URI%20scheme%20is,file%20literal%20or%20here%20document.

def b64_to_pic(b64: str, file_path):
    if b64.startswith('data:'):
        meta = b64[:b64.index(',')]
        file_extension = meta.split(';')[0][meta.index('/') + 1:]
        if not file_path.endswith(file_extension):
            file_path += '.' + file_extension
        content = b64[b64.index(',') + 1:]
    else:
        content = b64
        pass

    bin_pic = base64.b64decode(content)
    with open(file_path, 'wb') as f:
        f.write(bin_pic)


def save_pictures(directory, pic_set_name, file_names, b64_contents):
    dir_exists = os.path.exists(directory)
    if not dir_exists:
        os.mkdir(directory)

    for i in range(len(file_names)):
        try:
            file_path = os.path.normpath(os.path.join(directory, file_names[i]))
            b64_to_pic(b64_contents[i], file_path)
        except Exception as e:
            logging.error(f'save pic error {pic_set_name}', e)


key = b'IdTJq0HklpuI6mu8iB%OO@!vd^4K&uXW'
iv = b'$0v@krH7V2883346'


def aes_cbc_pk5_padding_dec(b64_data: str):
    aes = AES.new(key, mode=AES.MODE_CBC, IV=iv)
    data = base64.b64decode(b64_data)
    return unpad(aes.decrypt(data), 16).decode(encoding='utf-8')

client = MongoClient("localhost", 27017)
scrtv = client.pic['4scrtv']


if __name__ == '__main__':
    print(aes_cbc_pk5_padding_dec('PFbixdjrzMpaviinhU6t3v4KEUyOvW2U1vHmk3I9Lvo='))
