#!/usr/bin/env python3
"""
Crypto Application - Flet GUI
"""

import flet as ft
import base64
import hashlib
import os
import tempfile
from typing import Optional

from Crypto.Cipher import AES, DES, PKCS1_OAEP, ARC4
from Crypto.PublicKey import RSA as RSAKey
from Crypto.Util.Padding import pad, unpad


class CryptoEngine:
    """All crypto operations"""

    # --- Hash/Encode ---
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

    # --- Symmetric ---
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

    # --- Asymmetric (RSA) ---
    @staticmethod
    def generate_rsa_keys(bits: int = 2048) -> tuple[str, str]:
        key = RSAKey.generate(bits)
        private_key = key.export_key().decode('utf-8')
        public_key = key.publickey().export_key().decode('utf-8')
        return private_key, public_key

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


def main(page: ft.Page):
    page.title = "Crypto Tool"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window_width = 500
    page.window_height = 900

    engine = CryptoEngine()

    # --- State ---
    page.session_set("rsa_private_key", "")
    page.session_set("rsa_public_key", "")

    # --- Components ---
    # Tabs
    tab_hash = ft.Tab()
    tab_symmetric = ft.Tab()
    tab_rsa = ft.Tab()

    # ===== HASH/ENCODE TAB =====
    input_hash = ft.TextField(label="Input text", multiline=True, min_lines=2, max_lines=4)
    output_hash = ft.TextField(label="Result", readonly=True, multiline=True, min_lines=2, max_lines=4)

    def run_hash(e):
        text = input_hash.value
        if not text:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Enter text first!")))
            return
        algo = hash_dropdown.value
        try:
            if algo == "Base64 Encode":
                result = engine.base64_encode(text)
            elif algo == "Base64 Decode":
                result = engine.base64_decode(text)
            elif algo == "MD5":
                result = engine.md5(text)
            elif algo == "RIPEMD-160":
                result = engine.ripemd160(text)
            elif algo == "SHA1":
                result = engine.sha1(text)
            elif algo == "SHA256":
                result = engine.sha256(text)
            elif algo == "SHA512":
                result = engine.sha512(text)
            else:
                result = "Unknown algorithm"
            output_hash.value = result
        except Exception as ex:
            output_hash.value = f"Error: {ex}"
        page.update()

    hash_dropdown = ft.Dropdown(
        label="Algorithm",
        options=[
            ft.dropdown.Option("Base64 Encode"),
            ft.dropdown.Option("Base64 Decode"),
            ft.dropdown.Option("MD5"),
            ft.dropdown.Option("RIPEMD-160"),
            ft.dropdown.Option("SHA1"),
            ft.dropdown.Option("SHA256"),
            ft.dropdown.Option("SHA512"),
        ],
        value="Base64 Encode",
    )

    btn_hash = ft.ElevatedButton("Process", on_click=run_hash, expand=True)

    btn_copy_hash = ft.ElevatedButton(
        "📋 Copy",
        on_click=lambda e: (page.set_clipboard(output_hash.value), page.show_snack_bar(ft.SnackBar(content=ft.Text("Copied!")))),
    )

    tab_hash.content = ft.Column([
        ft.Text("Hash / Encode", size=24, weight=ft.FontWeight.BOLD),
        input_hash,
        hash_dropdown,
        ft.Row([btn_hash, btn_copy_hash]),
        output_hash,
    ], spacing=15, scroll=ft.ScrollMode.AUTO)

    # ===== SYMMETRIC TAB =====
    input_sym = ft.TextField(label="Input text", multiline=True, min_lines=2, max_lines=4)
    password_sym = ft.TextField(label="Password", password=True, can_reveal_password=True)
    output_sym = ft.TextField(label="Result", readonly=True, multiline=True, min_lines=2, max_lines=4)

    sym_algo = ft.Dropdown(
        label="Algorithm",
        options=[
            ft.dropdown.Option("AES Encrypt"),
            ft.dropdown.Option("AES Decrypt"),
            ft.dropdown.Option("DES Encrypt"),
            ft.dropdown.Option("DES Decrypt"),
            ft.dropdown.Option("RC4 Encrypt"),
            ft.dropdown.Option("RC4 Decrypt"),
        ],
        value="AES Encrypt",
    )

    def run_symmetric(e):
        text = input_sym.value
        password = password_sym.value
        if not text or not password:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Enter text and password!")))
            return
        algo = sym_algo.value
        try:
            if algo == "AES Encrypt":
                result = engine.aes_encrypt(text, password)
            elif algo == "AES Decrypt":
                result = engine.aes_decrypt(text, password)
            elif algo == "DES Encrypt":
                result = engine.des_encrypt(text, password)
            elif algo == "DES Decrypt":
                result = engine.des_decrypt(text, password)
            elif algo == "RC4 Encrypt":
                result = engine.rc4_encrypt(text, password)
            elif algo == "RC4 Decrypt":
                result = engine.rc4_decrypt(text, password)
            else:
                result = "Unknown algorithm"
            output_sym.value = result
        except Exception as ex:
            output_sym.value = f"Error: {ex}"
        page.update()

    btn_sym = ft.ElevatedButton("Process", on_click=run_symmetric, expand=True)

    btn_copy_sym = ft.ElevatedButton(
        "📋 Copy",
        on_click=lambda e: (page.set_clipboard(output_sym.value), page.show_snack_bar(ft.SnackBar(content=ft.Text("Copied!")))),
    )

    tab_symmetric.content = ft.Column([
        ft.Text("Symmetric Encryption", size=24, weight=ft.FontWeight.BOLD),
        input_sym,
        password_sym,
        sym_algo,
        ft.Row([btn_sym, btn_copy_sym]),
        output_sym,
    ], spacing=15, scroll=ft.ScrollMode.AUTO)

    # ===== RSA TAB =====
    rsa_pub_display = ft.TextField(label="Public Key (PEM)", readonly=True, multiline=True, min_lines=3, max_lines=5, text_size=10)
    rsa_priv_display = ft.TextField(label="Private Key (PEM)", readonly=True, multiline=True, min_lines=3, max_lines=5, text_size=10, password=True, can_reveal_password=True)

    rsa_input = ft.TextField(label="Input text", multiline=True, min_lines=2, max_lines=4)
    rsa_output = ft.TextField(label="Result", readonly=True, multiline=True, min_lines=2, max_lines=4)

    rsa_algo = ft.Dropdown(
        label="Operation",
        options=[
            ft.dropdown.Option("Generate Keys"),
            ft.dropdown.Option("RSA Encrypt"),
            ft.dropdown.Option("RSA Decrypt"),
        ],
        value="Generate Keys",
    )

    def run_rsa(e):
        algo = rsa_algo.value
        try:
            if algo == "Generate Keys":
                priv, pub = engine.generate_rsa_keys(2048)
                page.session_set("rsa_private_key", priv)
                page.session_set("rsa_public_key", pub)
                rsa_pub_display.value = pub
                rsa_priv_display.value = priv
                rsa_output.value = "Keys generated! Save them."
                page.show_snack_bar(ft.SnackBar(content=ft.Text("RSA Keys Generated!")))
            elif algo == "RSA Encrypt":
                text = rsa_input.value
                pub_key = page.session_get("rsa_public_key")
                if not text or not pub_key:
                    page.show_snack_bar(ft.SnackBar(content=ft.Text("Enter text and generate keys first!")))
                    return
                result = engine.rsa_encrypt_text(text, pub_key)
                rsa_output.value = result
            elif algo == "RSA Decrypt":
                text = rsa_input.value
                priv_key = page.session_set("rsa_private_key", page.session_get("rsa_private_key"))
                priv_key = page.session_get("rsa_private_key")
                if not text or not priv_key:
                    page.show_snack_bar(ft.SnackBar(content=ft.Text("Enter ciphertext and generate keys first!")))
                    return
                result = engine.rsa_decrypt_text(text, priv_key)
                rsa_output.value = result
        except Exception as ex:
            rsa_output.value = f"Error: {ex}"
        page.update()

    btn_rsa = ft.ElevatedButton("Process", on_click=run_rsa, expand=True)

    btn_copy_rsa = ft.ElevatedButton(
        "📋 Copy",
        on_click=lambda e: (page.set_clipboard(rsa_output.value), page.show_snack_bar(ft.SnackBar(content=ft.Text("Copied!")))),
    )

    tab_rsa.content = ft.Column([
        ft.Text("Asymmetric (RSA)", size=24, weight=ft.FontWeight.BOLD),
        rsa_algo,
        ft.Row([btn_rsa, btn_copy_rsa]),
        ft.Text("Keys (stored in session):", size=14, weight=ft.FontWeight.W_500),
        rsa_pub_display,
        rsa_priv_display,
        rsa_input,
        rsa_output,
    ], spacing=10, scroll=ft.ScrollMode.AUTO)

    # ===== Tabs =====
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(text="Hash", content=tab_hash.content),
            ft.Tab(text="Symmetric", content=tab_symmetric.content),
            ft.Tab(text="RSA", content=tab_rsa.content),
        ],
        expand=True,
    )

    page.add(tabs)


ft.app(target=main)
