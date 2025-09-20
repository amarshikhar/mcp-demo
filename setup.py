#!/usr/bin/env python3
"""Easy setup for Vendor Risk Assessment MCP Server"""
import os
import subprocess
import sys
import shutil

print("🚀 VENDOR RISK MCP SETUP")
print("=" * 30)

# Install dependencies
print("📦 Installing dependencies...")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Dependencies installed")
except:
    print("❌ Installation failed")

# Create .env if needed
if not os.path.exists('.env') and os.path.exists('.env.example'):
    shutil.copy('.env.example', '.env')
    print("📝 Created .env file")
    print("⚠️  Please edit .env with your AWS credentials")

print("\n🎉 Setup complete!")
print("\nNext steps:")
print("1. Edit .env file")
print("2. python test_client.py")
print("3. python main.py")
