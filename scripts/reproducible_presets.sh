#!/usr/bin/env bash
# Preset per build deterministiche/idempotenti
export LC_ALL=C
export LANG=C
export TZ=UTC
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1704067200}" # 2024-01-01
export PYTHONHASHSEED="${PYTHONHASHSEED:-0}"
export DOCS_BUILD_DATE="${DOCS_BUILD_DATE:-2024-01-01}"

# Ordinamenti stabili
repro_sort() { LC_ALL=C sort; }

# Scrub best-effort di timestamp/hash/uuid (file text)
repro_scrub_file() {
  sed -E \
    -e 's/[0-9]{4}-[0-9]{2}-[0-9]{2}/1970-01-01/g' \
    -e 's/[0-9]{2}:[0-9]{2}:[0-9]{2}/00:00:00/g' \
    -e 's/[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}/00000000-0000-0000-0000-000000000000/g' \
    -e 's/[A-Z][a-z]{2} [A-Z][a-z]{2} [ 0-9]{2} [0-9:]{8} UTC [0-9]{4}/Thu Jan  1 00:00:00 UTC 1970/g' \
    "$1" > "$1.__scrub__" && mv "$1.__scrub__" "$1"
}
