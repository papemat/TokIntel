# 🧯 Mini Runbook Incident

## 🚨 **Sintomo: test rossi su main**

1. **Sync e diagnostica**:
   ```bash
   git pull
   ./scripts/dx_doctor.sh
   ```

2. **Apri issue con output del doctor**

3. **Se urgente, rollback**:
   ```bash
   git revert <sha>
   git push origin main
   ```

---

## 🔄 **Sintomo: watcher non parte**

1. **Reinstalla watcher**:
   ```bash
   make watch-install
   ```

2. **Prova con fallback**:
   ```bash
   make dev-watch
   ```

3. **Controlla PATH degli strumenti esterni**:
   ```bash
   which watchexec entr fswatch inotifywait
   ```

---

## 🏷️ **Sintomo: release tag ok ma push fallisce**

1. **Rebase e push**:
   ```bash
   git pull --rebase origin main
   git push origin main --tags
   ```

---

## 🚀 **Sintomo: dashboard non risponde**

1. **Status check**:
   ```bash
   make dev-status
   ```

2. **Restart completo**:
   ```bash
   make dev-reset
   make dev
   ```

3. **Verifica porta**:
   ```bash
   lsof -i :8501
   ```

---

## 📊 **Sintomo: CI fallisce**

1. **Test locale**:
   ```bash
   make test-fast
   ```

2. **Doctor check**:
   ```bash
   ./scripts/dx_doctor.sh
   ```

3. **Verifica ambiente**:
   ```bash
   make env-show
   ```

---

## 🔧 **Comandi di emergenza**

```bash
# Reset completo
./scripts/dx_super_setup.sh

# Rollback ultimi commit
git revert --no-edit HEAD~1..HEAD && git push origin main

# Kill processi dashboard
pkill -f "streamlit\|dash/app.py" || true

# Clear logs
make logs-clear
```
