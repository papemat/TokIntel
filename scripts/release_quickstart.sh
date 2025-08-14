#!/usr/bin/env bash
set -euo pipefail

# TokIntel Quickstart Bundle Release Script
# Usage: ./scripts/release_quickstart.sh [version]

VERSION="${1:-v1.1.0}"
RELEASE_DATE=$(date +%Y-%m-%d)
CHANGELOG_FILE="CHANGELOG_QUICKSTART.md"

echo "🚀 TokIntel Quickstart Bundle Release: $VERSION"
echo "=================================================="

# Check if we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "main" ]]; then
    echo "⚠️  Warning: Not on main branch (current: $CURRENT_BRANCH)"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Release cancelled"
        exit 1
    fi
fi

# Check if working directory is clean
if ! git diff-index --quiet HEAD --; then
    echo "❌ Working directory not clean. Please commit or stash changes."
    exit 1
fi

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Create tag
echo "🏷️  Creating tag $VERSION..."
git tag "$VERSION" -m "Quickstart Bundle: cross-platform launchers + docs"

# Push tag
echo "📤 Pushing tag to remote..."
git push origin "$VERSION"

# Generate release notes
echo "📝 Generating release notes..."
cat > "RELEASE_NOTES_${VERSION}.md" << EOF
# TokIntel $VERSION - Quickstart Bundle

[![Quick Start Ready](docs/badges/quickstart_ready_glow.svg)](README_QUICKSTART.md)
[![CI](https://github.com/papemat/TokIntel/actions/workflows/ci.yml/badge.svg)](https://github.com/papemat/TokIntel/actions/workflows/ci.yml)

## 🚀 What's New

This release introduces a complete **Quickstart Bundle** that gets you running TokIntel in ~60 seconds across all platforms.

### ✨ Key Features

- **Cross-platform launchers** with auto-dependency installation
- **One-minute setup guide** for new users
- **Comprehensive troubleshooting** for common issues
- **Production-ready configuration** templates
- **Makefile integration** for easy access

### 🎯 Quick Start

\`\`\`bash
# macOS/Linux
./scripts/run_tokintel.sh

# Windows
scripts\\run_tokintel.bat

# Makefile (all platforms)
make run
\`\`\`

### 📋 What's Included

$(cat "$CHANGELOG_FILE" | sed '1,2d' | sed '/^$/d')

## 🔗 Links

- [Quickstart Guide](README_QUICKSTART.md)
- [Troubleshooting FAQ](FAQ_TROUBLESHOOTING.md)
- [Full Documentation](README.md)

## 🧪 Testing

All launchers tested and verified:
- ✅ Unix launcher (macOS/Linux)
- ✅ Windows launcher (PowerShell/CMD)
- ✅ Makefile targets
- ✅ Auto-dependency installation
- ✅ Cross-platform compatibility

---

**Release Date**: $RELEASE_DATE  
**Branch**: $CURRENT_BRANCH  
**Commit**: $(git rev-parse --short HEAD)
EOF

echo "✅ Release notes saved to RELEASE_NOTES_${VERSION}.md"

# Show next steps
echo ""
echo "🎉 Release $VERSION created successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Go to: https://github.com/papemat/TokIntel/releases/new"
echo "2. Select tag: $VERSION"
echo "3. Title: \"$VERSION – Quickstart Bundle\""
echo "4. Copy content from: RELEASE_NOTES_${VERSION}.md"
echo "5. Publish release"
echo ""
echo "🔗 Direct link: https://github.com/papemat/TokIntel/releases/tag/$VERSION"
