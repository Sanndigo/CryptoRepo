#!/bin/bash
# Build APK for CryptoTool
# Run this script to build the Android APK

set -e

export SSL_CERT_FILE=/opt/homebrew/etc/openssl@3/cert.pem

echo "========================================="
echo "  CryptoTool APK Builder"
echo "========================================="
echo ""
echo "This script will:"
echo "  1. Install Flutter SDK (one-time)"
echo "  2. Install Android SDK (one-time)"
echo "  3. Build the APK"
echo ""
echo "Note: First build takes ~10-20 minutes to download SDKs."
echo "Subsequent builds will be much faster."
echo ""

cd "$(dirname "$0")"

echo "Running: flet build apk"
echo "When prompted, confirm Flutter and Android SDK installation by typing 'y'"
echo ""

flet build apk

echo ""
echo "========================================="
echo "  Build Complete!"
echo "========================================="
echo "APK location: build/android/app/outputs/apk/release/"
echo "========================================="
