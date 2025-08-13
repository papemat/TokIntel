#!/usr/bin/env python3
"""
Test script for TokIntel Quick Start functionality
Verifies that all GUI Makefile targets work without errors
"""

import subprocess
import sys
import os

def run_make_target(target, description):
    """Run a make target and return success status"""
    print(f"🧪 Testing: {description}")
    try:
        result = subprocess.run(
            ["make", "-n", target], 
            capture_output=True, 
            text=True, 
            cwd=os.getcwd()
        )
        if result.returncode == 0:
            print(f"✅ {description} - OK")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def test_quickstart_targets():
    """Test all Quick Start Makefile targets"""
    print("🚀 TokIntel Quick Start Test Suite")
    print("=" * 50)
    
    targets = [
        ("tokintel-gui-bg", "GUI Background Startup"),
        ("tokintel-gui-log", "GUI Log Display"),
        ("tokintel-gui-health", "GUI Health Check"),
        ("tokintel-gui-stop", "GUI Stop"),
        ("tokintel-gui-on", "GUI Custom Port"),
        ("tokintel-gui-restart", "GUI Restart"),
        ("tokintel-gui-quickstart", "Quick Start Complete")
    ]
    
    results = []
    for target, description in targets:
        success = run_make_target(target, description)
        results.append(success)
        print()
    
    # Summary
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 ALL TESTS PASSED! ({passed}/{total})")
        print("✅ TokIntel Quick Start is ready!")
        return True
    else:
        print(f"⚠️  {passed}/{total} tests passed")
        print("❌ Some Quick Start features need attention")
        return False

def test_file_structure():
    """Test that required files exist"""
    print("📁 Testing file structure...")
    
    required_files = [
        "Makefile",
        "README.md",
        "docs/images/tokintel_gui_home.png",
        "dash/app.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    return all_exist

if __name__ == "__main__":
    print("🔍 TokIntel Quick Start Validation")
    print("=" * 50)
    
    # Test file structure
    files_ok = test_file_structure()
    print()
    
    # Test Makefile targets
    targets_ok = test_quickstart_targets()
    
    # Final result
    print("=" * 50)
    if files_ok and targets_ok:
        print("🎉 QUICK START VALIDATION: PASSED")
        sys.exit(0)
    else:
        print("❌ QUICK START VALIDATION: FAILED")
        sys.exit(1)
