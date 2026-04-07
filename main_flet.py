#!/usr/bin/env python3
"""
Crypto Application - Flet GUI
"""

import flet as ft
import base64
import hashlib

from Crypto.Cipher import AES, DES, PKCS1_OAEP, ARC4
from Crypto.PublicKey import RSA as RSAKey
from Crypto.Util.Padding import pad, unpad


class CryptoEngine:
    """All crypto operations"""

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


def main(page: ft.Page):
    page.title = "Crypto Tool"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.window_width = 480
    page.window_height = 850

    engine = CryptoEngine()

    def copy_result(value, label=""):
        page.clipboard.set(data=value)
        page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Copied {label}!")))

    # ===== HASH TAB =====
    input_hash = ft.TextField(label="Input text", multiline=True, min_lines=2, max_lines=3)
    output_hash = ft.TextField(label="Result", read_only=True, multiline=True, min_lines=2, max_lines=3)
    hash_dropdown = ft.Dropdown(
        label="Algorithm",
        options=[ft.dropdown.Option(x) for x in [
            "Base64 Encode", "Base64 Decode", "MD5", "RIPEMD-160", "SHA1", "SHA256", "SHA512"
        ]],
        value="Base64 Encode",
    )

    def run_hash(e):
        text = input_hash.value
        if not text:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Enter text first!")))
            return
        try:
            fn = {
                "Base64 Encode": engine.base64_encode,
                "Base64 Decode": engine.base64_decode,
                "MD5": engine.md5,
                "RIPEMD-160": engine.ripemd160,
                "SHA1": engine.sha1,
                "SHA256": engine.sha256,
                "SHA512": engine.sha512,
            }[hash_dropdown.value]
            output_hash.value = fn(text)
        except Exception as ex:
            output_hash.value = f"Error: {ex}"
        page.update()

    hash_view = ft.Column([
        ft.Text("Hash / Encode", size=22, weight=ft.FontWeight.BOLD),
        ft.Text("No key required", size=12, color=ft.Colors.GREY_400),
        input_hash,
        hash_dropdown,
        ft.Row([
            ft.ElevatedButton("Process", on_click=run_hash, expand=True),
            ft.ElevatedButton("Copy", on_click=lambda e: copy_result(output_hash.value, "result")),
        ]),
        output_hash,
    ], spacing=12, scroll=ft.ScrollMode.AUTO)

    # ===== SYMMETRIC TAB =====
    input_sym = ft.TextField(label="Input text", multiline=True, min_lines=2, max_lines=3)
    password_sym = ft.TextField(label="Password", password=True, can_reveal_password=True)
    output_sym = ft.TextField(label="Result", read_only=True, multiline=True, min_lines=2, max_lines=3)
    sym_algo = ft.Dropdown(
        label="Algorithm",
        options=[ft.dropdown.Option(x) for x in [
            "AES Encrypt", "AES Decrypt", "DES Encrypt", "DES Decrypt", "RC4 Encrypt", "RC4 Decrypt"
        ]],
        value="AES Encrypt",
    )

    def run_symmetric(e):
        text = input_sym.value
        password = password_sym.value
        if not text or not password:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Enter text and password!")))
            return
        try:
            fn = {
                "AES Encrypt": engine.aes_encrypt, "AES Decrypt": engine.aes_decrypt,
                "DES Encrypt": engine.des_encrypt, "DES Decrypt": engine.des_decrypt,
                "RC4 Encrypt": engine.rc4_encrypt, "RC4 Decrypt": engine.rc4_decrypt,
            }[sym_algo.value]
            output_sym.value = fn(text, password)
        except Exception as ex:
            output_sym.value = f"Error: {ex}"
        page.update()

    sym_view = ft.Column([
        ft.Text("Symmetric Encryption", size=22, weight=ft.FontWeight.BOLD),
        ft.Text("Password required", size=12, color=ft.Colors.GREY_400),
        input_sym,
        password_sym,
        sym_algo,
        ft.Row([
            ft.ElevatedButton("Process", on_click=run_symmetric, expand=True),
            ft.ElevatedButton("Copy", on_click=lambda e: copy_result(output_sym.value, "result")),
        ]),
        output_sym,
    ], spacing=12, scroll=ft.ScrollMode.AUTO)

    # ===== RSA TAB =====
    rsa_pub = ft.TextField(label="Public Key", read_only=True, multiline=True, min_lines=2, max_lines=4, text_size=10)
    rsa_priv = ft.TextField(label="Private Key", read_only=True, multiline=True, min_lines=2, max_lines=4, text_size=10, password=True, can_reveal_password=True)
    rsa_input = ft.TextField(label="Input text", multiline=True, min_lines=2, max_lines=3)
    rsa_output = ft.TextField(label="Result", read_only=True, multiline=True, min_lines=2, max_lines=3)
    rsa_algo = ft.Dropdown(
        label="Operation",
        options=[ft.dropdown.Option(x) for x in ["Generate Keys", "RSA Encrypt", "RSA Decrypt"]],
        value="Generate Keys",
    )

    def run_rsa(e):
        algo = rsa_algo.value
        try:
            if algo == "Generate Keys":
                priv, pub = engine.generate_rsa_keys(2048)
                page.session_set("rsa_priv", priv)
                page.session_set("rsa_pub", pub)
                rsa_pub.value = pub
                rsa_priv.value = priv
                rsa_output.value = "Keys generated!"
                page.show_snack_bar(ft.SnackBar(content=ft.Text("RSA Keys Generated!")))
            elif algo == "RSA Encrypt":
                text = rsa_input.value
                pub_key = page.session_get("rsa_pub")
                if not text or not pub_key:
                    page.show_snack_bar(ft.SnackBar(content=ft.Text("Enter text and generate keys first!")))
                    return
                rsa_output.value = engine.rsa_encrypt_text(text, pub_key)
            elif algo == "RSA Decrypt":
                text = rsa_input.value
                priv_key = page.session_get("rsa_priv")
                if not text or not priv_key:
                    page.show_snack_bar(ft.SnackBar(content=ft.Text("Enter ciphertext and generate keys first!")))
                    return
                rsa_output.value = engine.rsa_decrypt_text(text, priv_key)
        except Exception as ex:
            rsa_output.value = f"Error: {ex}"
        page.update()

    rsa_view = ft.Column([
        ft.Text("Asymmetric (RSA)", size=22, weight=ft.FontWeight.BOLD),
        ft.Text("Key pair required", size=12, color=ft.Colors.GREY_400),
        rsa_algo,
        ft.Row([
            ft.ElevatedButton("Process", on_click=run_rsa, expand=True),
            ft.ElevatedButton("Copy", on_click=lambda e: copy_result(rsa_output.value, "result")),
        ]),
        ft.Divider(),
        ft.Text("Keys (session):", size=13, weight=ft.FontWeight.W_500),
        rsa_pub,
        ft.Row([ft.ElevatedButton("Copy Pub", on_click=lambda e: copy_result(rsa_pub.value, "pub key"))], alignment=ft.MainAxisAlignment.END),
        rsa_priv,
        ft.Row([ft.ElevatedButton("Copy Priv", on_click=lambda e: copy_result(rsa_priv.value, "priv key"))], alignment=ft.MainAxisAlignment.END),
        ft.Divider(),
        rsa_input,
        rsa_output,
    ], spacing=10, scroll=ft.ScrollMode.AUTO)

    # ===== VIEW SWITCHER using NavigationBar =====
    views = [hash_view, sym_view, rsa_view]

    def on_nav_change(e):
        container.content = views[e.control.selected_index]
        page.update()

    nav = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.FINGERPRINT, label="Hash"),
            ft.NavigationBarDestination(icon=ft.Icons.KEY, label="Symmetric"),
            ft.NavigationBarDestination(icon=ft.Icons.LOCK, label="RSA"),
        ],
        on_change=on_nav_change,
        selected_index=0,
    )

    container = ft.Container(content=hash_view, expand=True)

    page.add(
        ft.Column([
            ft.Text("Crypto Tool", size=26, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            container,
        ], expand=True, spacing=0),
        nav,
    )


if __name__ == '__main__':
    ft.app(target=main)
