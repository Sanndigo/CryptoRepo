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

## Running Tests

```bash
python3 test_crypto.py
```
