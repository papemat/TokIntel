# Sprint 3 Orchestrator — Ops Guide

## Quick Start

### UI Headless Mode
```bash
TI_AUTO_EXPORT=1 TI_PORT=8510 make run-ui
```

### Health Check
```bash
curl "http://localhost:8510/?health=1"
# Expected: "OK"
```

### Trigger Search (E2E)
```bash
curl "http://localhost:8510/?trigger_search=1"
# Expected: "TRIGGER_OK" or "TRIGGER_EMPTY"
```

### Exports
- **Location**: `exports/{YYYYMMDD_HHMMSS}_{slug}.csv/json`
- **Auto-export**: Enabled with `TI_AUTO_EXPORT=1`
- **Format**: CSV + JSON with enriched metadata

### Logs
- **Location**: `logs/streamlit_YYYY-MM-DD.log`
- **Format**: JSON structured logging
- **Content**: Query timing, results count, export status

### CLI Orchestrator
```bash
# Basic search
python -m analyzer.orchestrator --query "alpha" --topk 5

# With export
python -m analyzer.orchestrator --query "alpha" --topk 5 --export exports/cli_alpha

# Build index
python -m analyzer.orchestrator --build
```

### Port Management
```bash
# Kill port (cross-platform)
make kill-port TI_PORT=8510

# Platform-specific
make kill-port-windows  # Windows
make kill-port-unix     # Unix/Linux/macOS
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TI_PORT` | `8510` | Streamlit server port |
| `TI_AUTO_EXPORT` | `0` | Enable auto-export on search |
| `TI_EXPORT_DIR` | `exports` | Export directory path |

## Testing

### E2E Tests
```bash
# Run E2E only
make test-e2e-only

# Run all Sprint 3 tests
make test-sprint3
```

### Coverage
```bash
# Sprint 3 coverage
make coverage-sprint3
```

### Linting
```bash
# Sprint 3 specific linting
make lint-sprint3
```

## CI/CD

### GitHub Actions
- **Workflow**: `.github/workflows/sprint3-e2e.yml`
- **Triggers**: PR to main/develop, push to main/develop
- **Matrix**: Python 3.10, 3.11
- **Artifacts**: Exports, logs uploaded on success/failure

### Badge
```markdown
![Sprint 3 E2E](https://github.com/OWNER/REPO/actions/workflows/sprint3-e2e.yml/badge.svg)
```

## Troubleshooting

### Port Already in Use
```bash
# Kill existing processes
make kill-port TI_PORT=8510

# Or use Python script directly
python scripts/kill_port.py 8510
```

### Health Check Fails
1. Check if Streamlit is running: `ps aux | grep streamlit`
2. Verify port is free: `lsof -i :8510`
3. Check logs: `tail -f logs/streamlit_*.log`

### Export Issues
1. Verify directory exists: `ls -la exports/`
2. Check permissions: `chmod 755 exports/`
3. Enable auto-export: `export TI_AUTO_EXPORT=1`

### E2E Test Failures
1. Ensure headless mode: `--server.headless true`
2. Check health endpoint: `curl "http://localhost:8510/?health=1"`
3. Verify trigger endpoint: `curl "http://localhost:8510/?trigger_search=1"`
4. Check export files: `ls -la exports/*.csv exports/*.json`
