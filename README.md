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

### Build macOS App

**Prerequisites:**

```bash
# 1. Install Xcode from App Store, then:
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch

# 2. Install CocoaPods
brew install cocoapods
```

**Build:**

```bash
./build_macos.sh
```

The app will be in `build/macos/` directory.

### Build APK (Android)

```bash
# Requires Java JDK
./build_apk.sh
```

Or run manually:

```bash
export SSL_CERT_FILE=/opt/homebrew/etc/openssl@3/cert.pem
flet build apk
```

APK output: `build/android/app/outputs/apk/release/app-release.apk`

### Programmatic Usage

```python
from main_flet import CryptoEngine

e = CryptoEngine()

# Hash
print(e.sha256("Hello"))

# Symmetric
enc = e.aes_encrypt("Secret", "password")
dec = e.aes_decrypt(enc, "password")

# RSA
priv, pub = e.generate_rsa_keys()
enc = e.rsa_encrypt_text("Hi", pub)
dec = e.rsa_decrypt_text(enc, priv)
```

## Running Tests

```bash
python3 test_crypto.py
```

## Project Structure

```
CryptoTool/
├── main_flet.py       # Flet GUI application
├── crypto_app.py      # CLI application
├── test_crypto.py     # Test suite
├── flet.toml          # Flet build configuration
├── build_macos.sh     # macOS build script
├── build_apk.sh       # Android APK build script
├── requirements.txt   # Dependencies
└── README.md         # This file
```
