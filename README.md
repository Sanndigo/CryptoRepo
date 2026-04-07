# Crypto Application

A CLI tool for text encryption, decryption, and hashing.

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

### Interactive Mode

```bash
python3 crypto_app.py
```

You'll be presented with a menu to choose operations.

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
├── crypto_app.py      # Main application
├── test_crypto.py     # Test suite
├── requirements.txt   # Dependencies
└── README.md         # This file
```
