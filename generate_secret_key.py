#!/usr/bin/env python3
"""
Generate a secure SECRET_KEY for production use
Run this and copy the output to your Render environment variables
"""
import secrets

print("\n" + "="*60)
print("SECURE SECRET KEY GENERATOR")
print("="*60)
print("\nGenerated SECRET_KEY for production:")
print("\n" + secrets.token_hex(32))
print("\n" + "="*60)
print("Copy this value and set it as SECRET_KEY in Render's")
print("environment variables section.")
print("="*60 + "\n")
