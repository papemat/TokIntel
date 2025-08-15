# Release Workflow - TokIntel

## Rilasci
- **Patch**: v1.1.2, v1.1.3 (bugfix / doc-only)
- **Minor**: v1.2.0 (nuove feature backward compatible)
- **Major**: v2.0.0 (breaking changes)

## Flow
1) PR → merge su main
2) Tag: `git tag vX.Y.Z -m "<title>" && git push origin vX.Y.Z`
3) GitHub Actions crea la Release con note dal changelog

## Esempi
```bash
# Patch release
git tag v1.1.2 -m "fix: resolve page blank issue"
git push origin v1.1.2

# Minor release
git tag v1.2.0 -m "feat: add Docker support"
git push origin v1.2.0

# Major release
git tag v2.0.0 -m "feat: breaking changes in API"
git push origin v2.0.0
```

## Changelog
- Aggiorna `CHANGELOG_QUICKSTART.md` prima del tag
- Il workflow automatico estrae le note dalla sezione corrispondente
- Formato: `## vX.Y.Z - YYYY-MM-DD`
