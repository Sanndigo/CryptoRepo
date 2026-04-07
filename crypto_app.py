#!/usr/bin/env python3
"""
Crypto Application - Text Encryption/Decryption Tool

Supported algorithms:
- Hash/Encode: Base64, MD5, RIPEMD-160, SHA1, SHA256, SHA512
- Symmetric: AES, DES, RC4
- Asymmetric: RSA
"""

import base64
import hashlib
import sys
import os
from typing import Optional

from Crypto.Cipher import AES, DES, PKCS1_OAEP, ARC4
from Crypto.PublicKey import RSA as RSAKey
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class HashEncoder:
    """Hash and encoding algorithms (no key required)"""

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


class SymmetricCipher:
    """Symmetric encryption algorithms (requires password/key)"""

    @staticmethod
    def _get_key_aes(password: str) -> bytes:
        return hashlib.sha256(password.encode('utf-8')).digest()

    @staticmethod
    def _get_key_des(password: str) -> bytes:
        key = hashlib.sha256(password.encode('utf-8')).digest()[:8]
        return key

    @staticmethod
    def aes_encrypt(text: str, password: str) -> str:
        key = SymmetricCipher._get_key_aes(password)
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
        return base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')

    @staticmethod
    def aes_decrypt(ciphertext: str, password: str) -> str:
        key = SymmetricCipher._get_key_aes(password)
        raw = base64.b64decode(ciphertext.encode('utf-8'))
        iv = raw[:AES.block_size]
        ct = raw[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')

    @staticmethod
    def des_encrypt(text: str, password: str) -> str:
        key = SymmetricCipher._get_key_des(password)
        cipher = DES.new(key, DES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), DES.block_size))
        return base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')

    @staticmethod
    def des_decrypt(ciphertext: str, password: str) -> str:
        key = SymmetricCipher._get_key_des(password)
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


class AsymmetricCipher:
    """Asymmetric encryption (RSA)"""

    @staticmethod
    def generate_keys(bits: int = 2048) -> tuple[str, str]:
        key = RSAKey.generate(bits)
        private_key = key.export_key().decode('utf-8')
        public_key = key.publickey().export_key().decode('utf-8')
        return private_key, public_key

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

    @staticmethod
    def rsa_encrypt(text: str, public_key_path: str) -> str:
        public_key = AsymmetricCipher.load_public_key(public_key_path)
        cipher = PKCS1_OAEP.new(public_key)
        ct = cipher.encrypt(text.encode('utf-8'))
        return base64.b64encode(ct).decode('utf-8')

    @staticmethod
    def rsa_decrypt(ciphertext: str, private_key_path: str) -> str:
        private_key = AsymmetricCipher.load_private_key(private_key_path)
        cipher = PKCS1_OAEP.new(private_key)
        ct = base64.b64decode(ciphertext.encode('utf-8'))
        return cipher.decrypt(ct).decode('utf-8')


def print_menu():
    print("\n" + "=" * 60)
    print("  CRYPTO APPLICATION")
    print("=" * 60)
    print("\n  HASH / ENCODE (No key required):")
    print("  1.  Base64 Encode")
    print("  2.  Base64 Decode")
    print("  3.  MD5")
    print("  4.  RIPEMD-160")
    print("  5.  SHA1")
    print("  6.  SHA256")
    print("  7.  SHA512")
    print("\n  SYMMETRIC (Password required):")
    print("  8.  AES Encrypt")
    print("  9.  AES Decrypt")
    print("  10. DES Encrypt")
    print("  11. DES Decrypt")
    print("  12. RC4 Encrypt")
    print("  13. RC4 Decrypt")
    print("\n  ASYMMETRIC (RSA key pair required):")
    print("  14. Generate RSA Key Pair")
    print("  15. RSA Encrypt")
    print("  16. RSA Decrypt")
    print("\n  0.  Exit")
    print("=" * 60)


def main():
    hash_enc = HashEncoder()
    symm = SymmetricCipher()
    asymm = AsymmetricCipher()

    while True:
        print_menu()
        choice = input("\nSelect option: ").strip()

        if choice == '0':
            print("Exiting...")
            break

        try:
            # Hash/Encode operations
            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                text = input("Enter text: ")
                
                if choice == '1':
                    result = hash_enc.base64_encode(text)
                    print(f"\nBase64 Encoded: {result}")
                elif choice == '2':
                    result = hash_enc.base64_decode(text)
                    print(f"\nBase64 Decoded: {result}")
                elif choice == '3':
                    result = hash_enc.md5(text)
                    print(f"\nMD5: {result}")
                elif choice == '4':
                    result = hash_enc.ripemd160(text)
                    print(f"\nRIPEMD-160: {result}")
                elif choice == '5':
                    result = hash_enc.sha1(text)
                    print(f"\nSHA1: {result}")
                elif choice == '6':
                    result = hash_enc.sha256(text)
                    print(f"\nSHA256: {result}")
                elif choice == '7':
                    result = hash_enc.sha512(text)
                    print(f"\nSHA512: {result}")

            # Symmetric operations
            elif choice in ['8', '9', '10', '11', '12', '13']:
                password = input("Enter password: ")
                
                if choice in ['8', '10', '12']:
                    text = input("Enter text to encrypt: ")
                else:
                    text = input("Enter ciphertext: ")

                if choice == '8':
                    result = symm.aes_encrypt(text, password)
                    print(f"\nAES Encrypted: {result}")
                elif choice == '9':
                    result = symm.aes_decrypt(text, password)
                    print(f"\nAES Decrypted: {result}")
                elif choice == '10':
                    result = symm.des_encrypt(text, password)
                    print(f"\nDES Encrypted: {result}")
                elif choice == '11':
                    result = symm.des_decrypt(text, password)
                    print(f"\nDES Decrypted: {result}")
                elif choice == '12':
                    result = symm.rc4_encrypt(text, password)
                    print(f"\nRC4 Encrypted: {result}")
                elif choice == '13':
                    result = symm.rc4_decrypt(text, password)
                    print(f"\nRC4 Decrypted: {result}")

            # Asymmetric operations
            elif choice in ['14', '15', '16']:
                if choice == '14':
                    bits = int(input("Key size in bits (default 2048): ") or "2048")
                    priv_key, pub_key = asymm.generate_keys(bits)
                    priv_path, pub_path = asymm.save_keys(priv_key, pub_key)
                    print(f"\nRSA Key Pair Generated ({bits}-bit)")
                    print(f"Private key saved to: {priv_path}")
                    print(f"Public key saved to: {pub_path}")
                    print("\n--- PUBLIC KEY ---")
                    print(pub_key)
                    print("--- PUBLIC KEY ---")
                elif choice == '15':
                    pub_path = input("Enter public key file path: ")
                    text = input("Enter text to encrypt: ")
                    result = asymm.rsa_encrypt(text, pub_path)
                    print(f"\nRSA Encrypted: {result}")
                elif choice == '16':
                    priv_path = input("Enter private key file path: ")
                    text = input("Enter ciphertext: ")
                    result = asymm.rsa_decrypt(text, priv_path)
                    print(f"\nRSA Decrypted: {result}")
            else:
                print("Invalid option. Please try again.")

        except Exception as e:
            print(f"\nError: {e}")

        input("\nPress Enter to continue...")


if __name__ == '__main__':
    main()
