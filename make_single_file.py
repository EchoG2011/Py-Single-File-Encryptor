# make_single_file.py
import base64
import hashlib
import os
import zlib
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

PWD = b"YourPassword123"   # ← 修改密码
ITS = 500_000

def derive_key(pwd, salt):
    return hashlib.pbkdf2_hmac('sha256', pwd, salt, ITS, dklen=32)

def encrypt_data(data: bytes) -> bytes:
    salt = get_random_bytes(32)
    key = derive_key(PWD, salt)
    cipher = AES.new(key, AES.MODE_GCM)
    ct, tag = cipher.encrypt_and_digest(data)
    return salt + cipher.nonce + tag + ct

def make_single_decryptor(py_file, out_file):
    src = Path(py_file).read_bytes()
    # 1. 加密
    salt = get_random_bytes(32)
    key = derive_key(PWD, salt)
    cipher = AES.new(key, AES.MODE_GCM)
    ct, tag = cipher.encrypt_and_digest(src)
    blob = salt + cipher.nonce + tag + ct   # 固定：32+16+16+len(ct)

    # 2. 一行 base64（无换行）
    b64 = base64.b64encode(blob).decode()

    template = f'''# 内存解密器（单文件）
import base64, hashlib, sys
from Crypto.Cipher import AES

PWD = b"{PWD.decode()}"
ITS = {ITS}

def derive_key(pwd, salt):
    return hashlib.pbkdf2_hmac('sha256', pwd, salt, ITS, dklen=32)

def decrypt_resource():
    blob = base64.b64decode("{b64}")
    salt, nonce, tag, ct = blob[:32], blob[32:48], blob[48:64], blob[64:]
    key = derive_key(PWD, salt)
    return AES.new(key, AES.MODE_GCM, nonce).decrypt_and_verify(ct, tag)

exec(compile(decrypt_resource(), '<memory>', 'exec'))
'''

    Path(out_file).write_text(template, encoding='utf-8')
    print(f"✅ 单文件解密器已生成：{out_file}")

if __name__ == "__main__":
    import tkinter.filedialog
    src = tkinter.filedialog.askopenfilename(title="选择要加密的 .py", filetypes=[("Python", "*.py")])
    if src:
        dst = Path(src).with_name("decryptor_single.py")
        make_single_decryptor(src, dst)
