#!/usr/bin/env python3
"""Test suite for crypto application"""

from crypto_app import HashEncoder, SymmetricCipher, AsymmetricCipher
import os
import tempfile

def test_hash_encoders():
    print("Testing Hash/Encode algorithms...")
    text = "Hello, World!"
    
    # Base64
    encoded = HashEncoder.base64_encode(text)
    decoded = HashEncoder.base64_decode(encoded)
    assert decoded == text, f"Base64 failed: {decoded} != {text}"
    print("  ✓ Base64 encode/decode")
    
    # MD5
    md5_hash = HashEncoder.md5(text)
    assert len(md5_hash) == 32, f"MD5 hash length incorrect"
    print(f"  ✓ MD5: {md5_hash}")
    
    # RIPEMD-160
    ripemd = HashEncoder.ripemd160(text)
    assert len(ripemd) == 40, f"RIPEMD-160 hash length incorrect"
    print(f"  ✓ RIPEMD-160: {ripemd}")
    
    # SHA1
    sha1 = HashEncoder.sha1(text)
    assert len(sha1) == 40, f"SHA1 hash length incorrect"
    print(f"  ✓ SHA1: {sha1}")
    
    # SHA256
    sha256 = HashEncoder.sha256(text)
    assert len(sha256) == 64, f"SHA256 hash length incorrect"
    print(f"  ✓ SHA256: {sha256}")
    
    # SHA512
    sha512 = HashEncoder.sha512(text)
    assert len(sha512) == 128, f"SHA512 hash length incorrect"
    print(f"  ✓ SHA512: {sha512}")
    
    print("All hash tests passed!\n")


def test_symmetric_ciphers():
    print("Testing Symmetric encryption algorithms...")
    text = "Secret Message 123!"
    password = "mypassword"
    
    # AES
    aes_enc = SymmetricCipher.aes_encrypt(text, password)
    aes_dec = SymmetricCipher.aes_decrypt(aes_enc, password)
    assert aes_dec == text, f"AES failed: {aes_dec} != {text}"
    print(f"  ✓ AES encrypt/decrypt")
    
    # DES
    des_enc = SymmetricCipher.des_encrypt(text, password)
    des_dec = SymmetricCipher.des_decrypt(des_enc, password)
    assert des_dec == text, f"DES failed: {des_dec} != {text}"
    print(f"  ✓ DES encrypt/decrypt")
    
    # RC4
    rc4_enc = SymmetricCipher.rc4_encrypt(text, password)
    rc4_dec = SymmetricCipher.rc4_decrypt(rc4_enc, password)
    assert rc4_dec == text, f"RC4 failed: {rc4_dec} != {text}"
    print(f"  ✓ RC4 encrypt/decrypt")
    
    print("All symmetric tests passed!\n")


def test_asymmetric_cipher():
    print("Testing Asymmetric encryption (RSA)...")
    text = "RSA Test Message"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate keys
        priv_key, pub_key = AsymmetricCipher.generate_keys(2048)
        priv_path, pub_path = AsymmetricCipher.save_keys(priv_key, pub_key, tmpdir)
        
        print(f"  ✓ RSA key pair generated (2048-bit)")
        
        # Encrypt
        rsa_enc = AsymmetricCipher.rsa_encrypt(text, pub_path)
        print(f"  ✓ RSA encrypt")
        
        # Decrypt
        rsa_dec = AsymmetricCipher.rsa_decrypt(rsa_enc, priv_path)
        assert rsa_dec == text, f"RSA failed: {rsa_dec} != {text}"
        print(f"  ✓ RSA decrypt")
    
    print("All asymmetric tests passed!\n")


if __name__ == '__main__':
    print("=" * 60)
    print("  CRYPTO APPLICATION - TEST SUITE")
    print("=" * 60 + "\n")
    
    try:
        test_hash_encoders()
        test_symmetric_ciphers()
        test_asymmetric_cipher()
        
        print("=" * 60)
        print("  ALL TESTS PASSED!")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
