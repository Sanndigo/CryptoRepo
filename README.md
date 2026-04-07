![Python](https://img.shields.io/badge/python-3.13-blue?logo=python&logoColor=white)
![Cryptography](https://img.shields.io/badge/Crypto-Library-green?logo=fortinet&logoColor=white)
# Crypto Application

A cross-platform GUI app for text encryption, decryption, and hashing built with Flet.

## Features

### Hash/Encode (No key required)
- Base64
- MD5
- RIPEMD-160
- SHA1
- SHA256
- SHA512

### Symmetric Encryption (Password required)
- AES (Rijndael)
- DES
- RC4

### Asymmetric Encryption (RSA key pair required)
- RSA (2048-bit default)

## Installation

```bash
pip3 install -r requirements.txt
```

## Usage

### Desktop GUI

```bash
python3 main_flet.py
```

### Build APK

```bash
# Install Flet CLI
pip3 install flet

# Build for Android
flet build apk

# The APK will be in build/ directory
```

### Programmatic Usage

```python
from crypto_app import HashEncoder, SymmetricCipher, AsymmetricCipher

# Hash/Encode
hash_val = HashEncoder.sha256("Hello, World!")
print(hash_val)

# Symmetric (AES)
encrypted = SymmetricCipher.aes_encrypt("Secret text", "password")
decrypted = SymmetricCipher.aes_decrypt(encrypted, "password")

# Asymmetric (RSA)
priv_key, pub_key = AsymmetricCipher.generate_keys(2048)
AsymmetricCipher.save_keys(priv_key, pub_key)
encrypted = AsymmetricCipher.rsa_encrypt("Secret", "./public.pem")
decrypted = AsymmetricCipher.rsa_decrypt(encrypted, "./private.pem")
```

## Running Tests

```bash
python3 test_crypto.py
```

## Project Structure

```
Crypto/
├── main_flet.py       # Flet GUI application
├── crypto_app.py      # CLI application
├── test_crypto.py     # Test suite
├── flet.toml          # Flet build configuration
├── requirements.txt   # Dependencies
└── README.md         # This file
```
