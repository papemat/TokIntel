# ✅ Checklist Velocissima - Pre Release

## 🚀 **Prima di rilasciare (2 minuti)**

- [ ] `make test-fast` → verde
- [ ] `CHANGELOG.md` aggiornato (`make changelog`)
- [ ] `RELEASE_NOTES.md` generato dal target `dx-release`
- [ ] Tag pubblicato: `git tag --list | tail -n1`

## 🔧 **Comando release completo**

```bash
# 1) Test veloci
make test-fast

# 2) Aggiorna changelog
make changelog

# 3) Release
make dx-release VER=1.0.1
```

## 📊 **Verifica post-release**

- [ ] Tag visibile su GitHub
- [ ] Badge CI verdi
- [ ] Dashboard funzionante: `make dev-status`
- [ ] CHANGELOG.md aggiornato

## 🚨 **Se qualcosa va storto**

```bash
# Rollback rapido
git revert --no-edit HEAD~1..HEAD && git push origin main

# Reset completo
./scripts/dx_super_setup.sh
```
