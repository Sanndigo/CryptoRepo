#!/usr/bin/env python3
"""
Crypto Application - Flet GUI (UI layer only)
"""

import flet as ft

from crypto_engine import CryptoEngine


class CryptoUI:
    """Flet UI for the Crypto Tool application"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.engine = CryptoEngine()
        self._setup_page()
        self._build_ui()

    def _setup_page(self):
        self.page.title = "Crypto Tool"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 15
        self.page.window_width = 480
        self.page.window_height = 850

    # ===== UTILITY =====

    def _copy_result(self, value: str, label: str = ""):
        ft.Clipboard().set_text(value)
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Copied {label}!")))

    def _show_error(self, message: str):
        self.page.show_snack_bar(ft.SnackBar(content=ft.Text(message)))

    # ===== HASH TAB =====

    def _build_hash_tab(self):
        self.input_hash = ft.TextField(
            label="Input text", multiline=True, min_lines=2, max_lines=3
        )
        self.output_hash = ft.TextField(
            label="Result", read_only=True, multiline=True, min_lines=2, max_lines=3
        )
        self.hash_dropdown = ft.Dropdown(
            label="Algorithm",
            options=[
                ft.dropdown.Option(x)
                for x in [
                    "Base64 Encode",
                    "Base64 Decode",
                    "MD5",
                    "RIPEMD-160",
                    "SHA1",
                    "SHA256",
                    "SHA512",
                ]
            ],
            value="Base64 Encode",
        )

        self.hash_mapping = {
            "Base64 Encode": self.engine.base64_encode,
            "Base64 Decode": self.engine.base64_decode,
            "MD5": self.engine.md5,
            "RIPEMD-160": self.engine.ripemd160,
            "SHA1": self.engine.sha1,
            "SHA256": self.engine.sha256,
            "SHA512": self.engine.sha512,
        }

        return ft.Column(
            [
                ft.Text("Hash / Encode", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("No key required", size=12, color=ft.Colors.GREY_400),
                self.input_hash,
                self.hash_dropdown,
                ft.Row(
                    [
                        ft.Button("Process", on_click=self._run_hash, expand=True),
                        ft.Button(
                            "Copy",
                            on_click=lambda e: self._copy_result(
                                self.output_hash.value, "result"
                            ),
                        ),
                    ]
                ),
                self.output_hash,
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
        )

    def _run_hash(self, e):
        text = self.input_hash.value
        if not text:
            self._show_error("Enter text first!")
            return
        try:
            fn = self.hash_mapping[self.hash_dropdown.value]
            self.output_hash.value = fn(text)
        except Exception as ex:
            self.output_hash.value = f"Error: {ex}"
        self.page.update()

    # ===== SYMMETRIC TAB =====

    def _build_symmetric_tab(self):
        self.input_sym = ft.TextField(
            label="Input text", multiline=True, min_lines=2, max_lines=3
        )
        self.password_sym = ft.TextField(
            label="Password", password=True, can_reveal_password=True
        )
        self.output_sym = ft.TextField(
            label="Result", read_only=True, multiline=True, min_lines=2, max_lines=3
        )
        self.sym_algo = ft.Dropdown(
            label="Algorithm",
            options=[
                ft.dropdown.Option(x)
                for x in [
                    "AES Encrypt",
                    "AES Decrypt",
                    "DES Encrypt",
                    "DES Decrypt",
                    "RC4 Encrypt",
                    "RC4 Decrypt",
                ]
            ],
            value="AES Encrypt",
        )

        self.sym_mapping = {
            "AES Encrypt": self.engine.aes_encrypt,
            "AES Decrypt": self.engine.aes_decrypt,
            "DES Encrypt": self.engine.des_encrypt,
            "DES Decrypt": self.engine.des_decrypt,
            "RC4 Encrypt": self.engine.rc4_encrypt,
            "RC4 Decrypt": self.engine.rc4_decrypt,
        }

        return ft.Column(
            [
                ft.Text("Symmetric Encryption", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Password required", size=12, color=ft.Colors.GREY_400),
                self.input_sym,
                self.password_sym,
                self.sym_algo,
                ft.Row(
                    [
                        ft.Button(
                            "Process", on_click=self._run_symmetric, expand=True
                        ),
                        ft.Button(
                            "Copy",
                            on_click=lambda e: self._copy_result(
                                self.output_sym.value, "result"
                            ),
                        ),
                    ]
                ),
                self.output_sym,
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
        )

    def _run_symmetric(self, e):
        text = self.input_sym.value
        password = self.password_sym.value
        if not text or not password:
            self._show_error("Enter text and password!")
            return
        try:
            fn = self.sym_mapping[self.sym_algo.value]
            self.output_sym.value = fn(text, password)
        except Exception as ex:
            self.output_sym.value = f"Error: {ex}"
        self.page.update()

    # ===== RSA TAB =====

    def _build_rsa_tab(self):
        self.rsa_pub = ft.TextField(
            label="Public Key",
            read_only=True,
            multiline=True,
            min_lines=2,
            max_lines=4,
            text_size=10,
        )
        self.rsa_priv = ft.TextField(
            label="Private Key",
            read_only=True,
            multiline=True,
            min_lines=2,
            max_lines=4,
            text_size=10,
            password=True,
            can_reveal_password=True,
        )
        self.rsa_input = ft.TextField(
            label="Input text", multiline=True, min_lines=2, max_lines=3
        )
        self.rsa_output = ft.TextField(
            label="Result", read_only=True, multiline=True, min_lines=2, max_lines=3
        )
        self.rsa_algo = ft.Dropdown(
            label="Operation",
            options=[
                ft.dropdown.Option(x)
                for x in ["Generate Keys", "RSA Encrypt", "RSA Decrypt"]
            ],
            value="Generate Keys",
        )

        return ft.Column(
            [
                ft.Text("Asymmetric (RSA)", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Key pair required", size=12, color=ft.Colors.GREY_400),
                self.rsa_algo,
                ft.Row(
                    [
                        ft.Button("Process", on_click=self._run_rsa, expand=True),
                        ft.Button(
                            "Copy",
                            on_click=lambda e: self._copy_result(
                                self.rsa_output.value, "result"
                            ),
                        ),
                    ]
                ),
                ft.Divider(),
                ft.Text("Keys (session):", size=13, weight=ft.FontWeight.W_500),
                self.rsa_pub,
                ft.Row(
                    [
                        ft.Button(
                            "Copy Pub",
                            on_click=lambda e: self._copy_result(
                                self.rsa_pub.value, "pub key"
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
                self.rsa_priv,
                ft.Row(
                    [
                        ft.Button(
                            "Copy Priv",
                            on_click=lambda e: self._copy_result(
                                self.rsa_priv.value, "priv key"
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Divider(),
                self.rsa_input,
                self.rsa_output,
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        )

    def _run_rsa(self, e):
        algo = self.rsa_algo.value
        try:
            if algo == "Generate Keys":
                priv, pub = self.engine.generate_rsa_keys(2048)
                self.page.session_set("rsa_priv", priv)
                self.page.session_set("rsa_pub", pub)
                self.rsa_pub.value = pub
                self.rsa_priv.value = priv
                self.rsa_output.value = "Keys generated!"
                self._show_error("RSA Keys Generated!")
            elif algo == "RSA Encrypt":
                text = self.rsa_input.value
                pub_key = self.page.session_get("rsa_pub")
                if not text or not pub_key:
                    self._show_error(
                        "Enter text and generate keys first!"
                    )
                    return
                self.rsa_output.value = self.engine.rsa_encrypt_text(text, pub_key)
            elif algo == "RSA Decrypt":
                text = self.rsa_input.value
                priv_key = self.page.session_get("rsa_priv")
                if not text or not priv_key:
                    self._show_error(
                        "Enter ciphertext and generate keys first!"
                    )
                    return
                self.rsa_output.value = self.engine.rsa_decrypt_text(
                    text, priv_key
                )
        except Exception as ex:
            self.rsa_output.value = f"Error: {ex}"
        self.page.update()

    # ===== BUILD UI =====

    def _build_ui(self):
        hash_view = self._build_hash_tab()
        sym_view = self._build_symmetric_tab()
        rsa_view = self._build_rsa_tab()

        views = [hash_view, sym_view, rsa_view]

        def on_nav_change(e):
            self.container.content = views[e.control.selected_index]
            self.page.update()

        nav = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.FINGERPRINT, label="Hash"
                ),
                ft.NavigationBarDestination(icon=ft.Icons.KEY, label="Symmetric"),
                ft.NavigationBarDestination(icon=ft.Icons.LOCK, label="RSA"),
            ],
            on_change=on_nav_change,
            selected_index=0,
        )

        self.container = ft.Container(content=hash_view, expand=True)

        self.page.add(
            ft.Column(
                [
                    ft.Text(
                        "Crypto Tool",
                        size=26,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    self.container,
                ],
                expand=True,
                spacing=0,
            ),
            nav,
        )


def main(page: ft.Page):
    CryptoUI(page)


if __name__ == '__main__':
    ft.run(main)
