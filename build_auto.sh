#!/bin/bash
# Automated APK build script with auto-confirmations
# Usage: ./build_auto.sh

export SSL_CERT_FILE=/opt/homebrew/etc/openssl@3/cert.pem

cd "$(dirname "$0")"

# Create expect-like input for prompts
# This sends 'y' to each prompt automatically

{
    echo "y"  # Confirm Flutter SDK
    sleep 2
    echo "y"  # Confirm Android SDK  
    sleep 2
} | flet build apk 2>&1 | tee build.log

echo ""
echo "========================================="
echo "  Build script finished"
echo "========================================="
echo "Check build.log for details"
if [ -d "build/android/app/outputs/apk/release/" ]; then
    echo "APK found at: build/android/app/outputs/apk/release/"
    ls -lh build/android/app/outputs/apk/release/*.apk 2>/dev/null || echo "No APK found yet"
else
    echo "Build directory not found - build may still be in progress or failed"
fi
echo "========================================="
