#!/usr/bin/env python3
"""
Test script for TokIntel Quick Start functionality
Verifies that all GUI Makefile targets work without errors
"""

import os, subprocess, sys, re

ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(ROOT, ".."))

def run(cmd):
    print(f"$ {' '.join(cmd)}")
    p = subprocess.run(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print(p.stdout)
    return p.returncode, p.stdout

def ensure_target(name):
    code, out = run(["make", "-n", name])
    if code != 0:
        print(f"❌ Target failed dry-run: {name}")
        sys.exit(1)

def grep_targets():
    mk = open(os.path.join(ROOT, "Makefile"), "r", encoding="utf-8").read()
    needed = [
        "tokintel-gui-bg",
        "tokintel-gui-log",
        "tokintel-gui-health",
        "tokintel-gui-stop",
        "tokintel-gui-on",
        "tokintel-gui-restart",
        "tokintel-gui-quickstart",
    ]
    missing = [t for t in needed if t not in mk]
    if missing:
        print("❌ Missing targets:", ", ".join(missing))
        sys.exit(1)
    print("✅ All required targets present.")

def main():
    grep_targets()
    ensure_target("tokintel-gui-bg")
    ensure_target("tokintel-gui-log")
    ensure_target("tokintel-gui-health")
    ensure_target("tokintel-gui-stop")
    ensure_target("tokintel-gui-quickstart")
    print("✅ Quick Start dry-run OK.")

if __name__ == "__main__":
    main()
