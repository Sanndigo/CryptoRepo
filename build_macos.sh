#!/bin/bash
# Build macOS app for CryptoTool

set -e

echo "========================================="
echo "  CryptoTool - macOS Build"
echo "========================================="
echo ""

cd "$(dirname "$0")"

# Check Xcode
echo "Checking Xcode..."
if ! xcode-select -p &>/dev/null || [ "$(xcode-select -p)" = "/Library/Developer/CommandLineTools" ]; then
    echo "⚠️  Xcode not fully installed. Run these commands first:"
    echo ""
    echo "   sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer"
    echo "   sudo xcodebuild -runFirstLaunch"
    echo "   brew install cocoapods"
    echo ""
    echo "   Or install Xcode from App Store first."
    echo ""
    read -p "Continue anyway? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "Running: flet build macos --module-name main_flet"
echo ""

flet build macos --module-name main_flet

echo ""
echo "========================================="
echo "  Build Complete!"
echo "========================================="
echo "App location: build/macos/"
find build/macos -maxdepth 2 -name "*.app" -type d 2>/dev/null || echo "Check build/macos/ directory"
echo "========================================="
