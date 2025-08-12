# 🏢 Enterprise Setup Guide

## Branch Protection Setup

### 1. Proteggi il branch `main`

**GitHub → Settings → Branches → Add rule:**

```
Branch name pattern: main
✓ Require a pull request before merging
✓ Require status checks to pass before merging
  ✓ prod-check
  ✓ staging-check  
  ✓ performance-check
✓ Require branches to be up to date before merging
✓ Include administrators
```

### 2. Status Checks Configuration

I job richiesti per il merge:
- **prod-check**: Test standard su main
- **staging-check**: Test su database staging
- **performance-check**: Matrix performance (1200ms/1500ms)

## CI/CD Pipeline Overview

### Job Matrix
```
┌─────────────────┬─────────────────┬─────────────────┐
│     prod-check  │  staging-check  │ performance-check│
│   (main only)   │   (PR + manual) │   (PR + manual)  │
├─────────────────┼─────────────────┼─────────────────┤
│ • Standard test │ • Staging DB    │ • Large DB      │
│ • Export CSV/JSON│ • Prod-check   │ • Matrix 1200ms │
│ • Report gen    │ • Report gen    │ • Matrix 1500ms │
│ • Upload artifacts│ • Upload artifacts│ • PR comments  │
│                 │                 │ • Slack alerts  │
│                 │                 │ • Perf labels   │
└─────────────────┴─────────────────┴─────────────────┘
```

### Performance Thresholds
- **Early Warning**: 1200ms (sql_read, export)
- **Blocking**: 1500ms (sql_read, export)
- **Fail-fast**: false (mostra tutti i risultati)

## Production Readiness Checklist

### ✅ Automated Checks
- [ ] Branch protection enabled
- [ ] Status checks required
- [ ] Performance matrix passing
- [ ] Slack notifications configured
- [ ] Label automation working

### ✅ Dependencies Pinned
- [ ] `pandas==2.2.*` (stable performance)
- [ ] `pytest==8.*` (stable CI)
- [ ] Core dependencies versioned

### ✅ Monitoring & Alerting
- [ ] Performance regression detection
- [ ] Slack webhook configured
- [ ] PR comments with metrics
- [ ] Artifacts retention (30 days)

## Slack Integration

### 1. Create Webhook
```
Slack App → Incoming Webhooks → Add to Workspace
```

### 2. Add GitHub Secret
```
GitHub → Settings → Secrets → New repository secret
Name: SLACK_WEBHOOK_URL
Value: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### 3. Test Notification
```bash
# Trigger manual workflow
GitHub → Actions → "Prod Check" → Run workflow
```

## Performance Monitoring

### Metrics Tracked
- **sql_read_500**: Database read performance
- **export_csv**: CSV export speed
- **export_json**: JSON export speed
- **add_indexes_ms**: Index creation time

### Thresholds
```yaml
matrix:
  thresholds:
    - { sql: 1200, export: 1200 }   # Early warning
    - { sql: 1500, export: 1500 }   # Blocking
```

### Regression Detection
- Automatic label: `perf-regression`
- Slack notification on failure
- PR comments with detailed metrics

## Local Development

### Performance Testing
```bash
# Standard check
make prod-check

# Performance benchmark
make perf-check

# Custom thresholds
python scripts/perf_bench.py --max-sql-read-ms 1000
```

### Database Setup
```bash
# Standard DB
python scripts/create_sample_db.py

# Staging DB (medium)
python scripts/create_sample_db.py --staging

# Performance DB (large)
python scripts/create_sample_db.py --staging --large
```

## Troubleshooting

### Common Issues

**Performance check failing:**
- Check recent changes affecting DB queries
- Verify pandas version compatibility
- Review export logic for bottlenecks

**Slack notifications not working:**
- Verify `SLACK_WEBHOOK_URL` secret is set
- Check webhook URL validity
- Test with manual workflow trigger

**Matrix job timing out:**
- Increase runner timeout in workflow
- Optimize database queries
- Review large dataset generation

### Debug Commands
```bash
# Check current performance
make perf-check

# Verify dependencies
pip list | grep -E "(pandas|pytest)"

# Test database performance
python scripts/perf_bench.py --db data/db.sqlite
```

## Security Considerations

### Secrets Management
- Use GitHub Secrets for sensitive data
- Rotate Slack webhook URLs regularly
- Never commit API keys or tokens

### Access Control
- Limit admin access to main branch
- Require PR reviews for changes
- Use branch protection rules

---

**Status**: ✅ Enterprise Ready  
**Last Updated**: $(date +%Y-%m-%d)  
**Version**: 1.0.0
