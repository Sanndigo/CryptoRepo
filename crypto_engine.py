#!/usr/bin/env python3
"""
Crypto Engine - All cryptographic operations
"""

import base64
import hashlib
import os

from Crypto.Cipher import AES, DES, PKCS1_OAEP, ARC4
from Crypto.PublicKey import RSA as RSAKey
from Crypto.Util.Padding import pad, unpad


class CryptoEngine:
    """All crypto operations"""

    # ===== HASH / ENCODE (no key required) =====

    @staticmethod
    def base64_encode(text: str) -> str:
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')

    @staticmethod
    def base64_decode(text: str) -> str:
        return base64.b64decode(text.encode('utf-8')).decode('utf-8')

    @staticmethod
    def md5(text: str) -> str:
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    @staticmethod
    def ripemd160(text: str) -> str:
        return hashlib.new('ripemd160', text.encode('utf-8')).hexdigest()

    @staticmethod
    def sha1(text: str) -> str:
        return hashlib.sha1(text.encode('utf-8')).hexdigest()

    @staticmethod
    def sha256(text: str) -> str:
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    @staticmethod
    def sha512(text: str) -> str:
        return hashlib.sha512(text.encode('utf-8')).hexdigest()

    # ===== SYMMETRIC (password required) =====

    @staticmethod
    def _get_key_aes(password: str) -> bytes:
        return hashlib.sha256(password.encode('utf-8')).digest()

    @staticmethod
    def _get_key_des(password: str) -> bytes:
        return hashlib.sha256(password.encode('utf-8')).digest()[:8]

    @staticmethod
    def aes_encrypt(text: str, password: str) -> str:
        key = CryptoEngine._get_key_aes(password)
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
        return base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')

    @staticmethod
    def aes_decrypt(ciphertext: str, password: str) -> str:
        key = CryptoEngine._get_key_aes(password)
        raw = base64.b64decode(ciphertext.encode('utf-8'))
        iv = raw[:AES.block_size]
        ct = raw[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')

    @staticmethod
    def des_encrypt(text: str, password: str) -> str:
        key = CryptoEngine._get_key_des(password)
        cipher = DES.new(key, DES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), DES.block_size))
        return base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')

    @staticmethod
    def des_decrypt(ciphertext: str, password: str) -> str:
        key = CryptoEngine._get_key_des(password)
        raw = base64.b64decode(ciphertext.encode('utf-8'))
        iv = raw[:DES.block_size]
        ct = raw[DES.block_size:]
        cipher = DES.new(key, DES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), DES.block_size).decode('utf-8')

    @staticmethod
    def rc4_encrypt(text: str, password: str) -> str:
        key = hashlib.sha256(password.encode('utf-8')).digest()
        cipher = ARC4.new(key)
        ct = cipher.encrypt(text.encode('utf-8'))
        return base64.b64encode(ct).decode('utf-8')

    @staticmethod
    def rc4_decrypt(ciphertext: str, password: str) -> str:
        key = hashlib.sha256(password.encode('utf-8')).digest()
        cipher = ARC4.new(key)
        ct = base64.b64decode(ciphertext.encode('utf-8'))
        return cipher.decrypt(ct).decode('utf-8')

    # ===== ASYMMETRIC (RSA) =====

    @staticmethod
    def generate_rsa_keys(bits: int = 2048) -> tuple[str, str]:
        key = RSAKey.generate(bits)
        return key.export_key().decode('utf-8'), key.publickey().export_key().decode('utf-8')

    @staticmethod
    def rsa_encrypt_text(text: str, public_key_pem: str) -> str:
        public_key = RSAKey.import_key(public_key_pem)
        cipher = PKCS1_OAEP.new(public_key)
        ct = cipher.encrypt(text.encode('utf-8'))
        return base64.b64encode(ct).decode('utf-8')

    @staticmethod
    def rsa_decrypt_text(ciphertext: str, private_key_pem: str) -> str:
        private_key = RSAKey.import_key(private_key_pem)
        cipher = PKCS1_OAEP.new(private_key)
        ct = base64.b64decode(ciphertext.encode('utf-8'))
        return cipher.decrypt(ct).decode('utf-8')

    @staticmethod
    def save_keys(private_key: str, public_key: str, directory: str = '.') -> tuple[str, str]:
        priv_path = os.path.join(directory, 'private.pem')
        pub_path = os.path.join(directory, 'public.pem')

        with open(priv_path, 'w') as f:
            f.write(private_key)
        with open(pub_path, 'w') as f:
            f.write(public_key)

        return priv_path, pub_path

    @staticmethod
    def load_public_key(public_key_path: str) -> RSAKey.RsaKey:
        with open(public_key_path, 'r') as f:
            return RSAKey.import_key(f.read())

    @staticmethod
    def load_private_key(private_key_path: str) -> RSAKey.RsaKey:
        with open(private_key_path, 'r') as f:
            return RSAKey.import_key(f.read())
