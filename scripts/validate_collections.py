#!/usr/bin/env python3
# Minimal validator per raccolte TikTok
import json, sys, pathlib

REQUIRED_ITEM_KEYS = {"id", "url"}            # estendibile (es. title, tags)
ALLOWED_ROOT_KEYS  = {"collections", "items"} # supporta due formati

def error(msg):
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(2)

def ok(msg):
    print(f"✅ {msg}")
    sys.exit(0)

def validate_items(items):
    if not isinstance(items, list) or not items:
        error("items deve essere una lista non vuota")
    bad = []
    for i, it in enumerate(items, 1):
        if not isinstance(it, dict):
            bad.append((i, "voce non è un oggetto"))
            continue
        missing = REQUIRED_ITEM_KEYS - it.keys()
        if missing:
            bad.append((i, f"mancano campi {sorted(missing)}"))
        if "url" in it and not str(it["url"]).startswith(("http://","https://")):
            bad.append((i, "url non valido"))
    if bad:
        for idx, why in bad[:10]:
            print(f" - item #{idx}: {why}", file=sys.stderr)
        error(f"{len(bad)} item non validi")
    return True

def main():
    if len(sys.argv) < 2:
        error("uso: validate_collections.py <input.json>")
    p = pathlib.Path(sys.argv[1])
    if not p.exists():
        error(f"file non trovato: {p}")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        error(f"JSON non valido: {e}")

    # supporta: { "items": [...] }  oppure  { "collections": [ { "items": [...] }, ... ] }
    if "items" in data:
        validate_items(data["items"])
    elif "collections" in data:
        if not isinstance(data["collections"], list) or not data["collections"]:
            error("collections deve essere una lista non vuota")
        total = 0
        for c in data["collections"]:
            if not isinstance(c, dict) or "items" not in c:
                error("ogni collection deve avere 'items'")
            validate_items(c["items"])
            total += len(c["items"])
        if total == 0:
            error("nessun item nelle collections")
    else:
        error(f"root keys non riconosciute. Usa una tra {sorted(ALLOWED_ROOT_KEYS)}")

    ok(f"Input valido: {p}")

if __name__ == "__main__":
    main()
