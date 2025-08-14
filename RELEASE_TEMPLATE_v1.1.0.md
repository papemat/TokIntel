# 🚀 TokIntel v1.1.0 – Quickstart Bundle

[![Quickstart Ready](https://img.shields.io/badge/Quickstart-Ready-brightgreen)](README_QUICKSTART.md)
[![Cross‑Platform](https://img.shields.io/badge/Launchers-macOS%2FLinux%2FWindows-blue)](README_QUICKSTART.md)
[![CI](https://github.com/papemat/TokIntel/actions/workflows/ci.yml/badge.svg)](https://github.com/papemat/TokIntel/actions/workflows/ci.yml)

## 🎯 What's New

This release introduces a complete **Quickstart Bundle** that gets you running TokIntel in ~60 seconds across all platforms.

### ✨ Key Features

- **Cross-platform launchers** with auto-dependency installation
- **One-minute setup guide** for new users
- **Comprehensive troubleshooting** for common issues
- **Production-ready configuration** templates
- **Makefile integration** for easy access
- **CI/CD automation** for quality assurance

### 🎯 Quick Start

```bash
# macOS/Linux
./scripts/run_tokintel.sh

# Windows
scripts\run_tokintel.bat

# Makefile (all platforms)
make run
```

### 📋 What's Included

#### Core Files
- `README_QUICKSTART.md` - Setup guide in ~60s
- `scripts/run_tokintel.sh` - Unix launcher (macOS/Linux)
- `scripts/run_tokintel.bat` - Windows launcher
- `streamlit_config_example.toml` - Production config
- `FAQ_TROUBLESHOOTING.md` - Top 10 issues + fixes

#### Integration
- `Makefile` targets: `run`, `run-lan`, `run-debug`, `quickstart-check`
- `.github/pull_request_template.md` - PR template with checklist
- `.github/workflows/quickstart-dryrun.yml` - CI validation
- `CHANGELOG_QUICKSTART.md` - Release notes
- `scripts/release_quickstart.sh` - Auto-release script

### 🧪 Testing

All launchers tested and verified:
- ✅ Unix launcher (macOS/Linux)
- ✅ Windows launcher (PowerShell/CMD)
- ✅ Makefile targets
- ✅ Auto-dependency installation
- ✅ Cross-platform compatibility
- ✅ CI dry-run workflow

### 🔗 Links

- [Quickstart Guide](README_QUICKSTART.md)
- [Troubleshooting FAQ](FAQ_TROUBLESHOOTING.md)
- [Full Documentation](README.md)

---

**Release Date**: 2025-08-14  
**Branch**: main  
**Commit**: [latest](https://github.com/papemat/TokIntel/commit/main)

---

## 🎉 Get Started

**TokIntel is now accessible to everyone in ~60 seconds!**

The Quickstart Bundle provides:
1. **Immediate setup** for new users
2. **Consistent experience** across all platforms
3. **Integrated troubleshooting** for common issues
4. **CI/CD automation** for continuous quality
5. **Release automation** for distribution

**Status: ✅ PRODUCTION READY** 🚀
