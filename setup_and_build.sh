#!/bin/bash
# Setup and build APK - installs all required dependencies
# Run this script to set up the build environment and create the APK

set -e

echo "========================================="
echo "  CryptoTool - APK Build Setup & Build"
echo "========================================="
echo ""

# Check if Homebrew is installed
if ! command -v brew &>/dev/null; then
    echo "❌ Homebrew not found. Install it first:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

# Check/install Java
if ! command -v java &>/dev/null; then
    echo "📦 Installing Java JDK (required for Android builds)..."
    brew install --cask zulu
    echo "✅ Java installed"
else
    echo "✅ Java already installed"
    java -version 2>&1 | head -1
fi

echo ""
echo "========================================="
echo "  Installing Python dependencies..."
echo "========================================="
pip3 install -r requirements.txt

echo ""
echo "========================================="
echo "  Building APK..."
echo "========================================="
echo ""
echo "The build will download Flutter SDK and Android SDK on first run."
echo "This takes 10-20 minutes. Subsequent builds are faster."
echo ""

export SSL_CERT_FILE=/opt/homebrew/etc/openssl@3/cert.pem

# Try auto-confirm build
{
    echo "y"
    sleep 3
    echo "y"
    sleep 3
} | flet build apk 2>&1 | tee build.log || {
    echo ""
    echo "⚠️  Automated build failed."
    echo "   Please run manually: flet build apk"
    echo "   And confirm prompts with 'y'"
    exit 1
}

echo ""
echo "========================================="
if [ -f "build/android/app/outputs/apk/release/app-release.apk" ]; then
    echo "  ✅ BUILD SUCCESS!"
    echo "  APK: build/android/app/outputs/apk/release/app-release.apk"
    ls -lh build/android/app/outputs/apk/release/app-release.apk 2>/dev/null
else
    echo "  Build completed. Checking for APK..."
    find build -name "*.apk" -type f 2>/dev/null | head -5 || echo "  No APK found"
fi
echo "========================================="
