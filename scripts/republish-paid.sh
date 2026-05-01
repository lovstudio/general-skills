#!/usr/bin/env bash
# Republish a single paid skill (encrypted bundle).
#
# Usage:
#   bash scripts/republish-paid.sh <skill_name> <skill_id> <new_version>
#
# Example:
#   bash scripts/republish-paid.sh proposal 11 0.1.2
#   bash scripts/republish-paid.sh event-curator 49 0.1.1
#
# What it does (interactive, prints checkpoints):
#   1. Generate a fresh AES-256 key
#   2. INSERT placeholder skill_versions row, RETURN id
#   3. Run pack-skill.py with that id and key → produces dist/
#   4. Run decrypt-local.py to verify roundtrip
#   5. UPDATE skill_versions.manifest with the real cipher manifest, set active=true
#   6. Copy dist/{MANIFEST.enc.json,SKILL.md.enc} into ../index/skills/<name>/
#   7. Print follow-up git steps (does NOT auto-commit)

set -euo pipefail

SKILL_NAME="${1:?skill name required}"
SKILL_ID="${2:?skill_id required}"
NEW_VERSION="${3:?new version required}"

PROJECT_REF="nouchjcfeoobplxkwasg"
SQL_URL="https://api.supabase.com/v1/projects/$PROJECT_REF/database/query"

SKILLS_ROOT="$HOME/lovstudio/coding/skills"
SKILL_REPO="$SKILLS_ROOT/${SKILL_NAME}-skill"
INDEX_REPO="$SKILLS_ROOT/index"
MIRROR_DIR="$INDEX_REPO/skills/$SKILL_NAME"

cd "$SKILL_REPO"

echo "== Republishing $SKILL_NAME @ $NEW_VERSION =="
echo "  repo: $SKILL_REPO"
echo "  skill_id: $SKILL_ID"
echo

# --- 0. proxy + token
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7891

TOKEN=$(security find-generic-password -s "Supabase CLI" -w | sed 's/^go-keyring-base64://' | base64 -d)

# --- 1. Generate key
KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
echo "Step 1: Generated AES-256 key"
echo "  KEY=$KEY"
echo "  (save this somewhere safe — once committed, you can't recover from disk)"
echo

# --- 2. INSERT placeholder, get version_id
echo "Step 2: INSERT placeholder skill_versions row"
QUERY=$(SKILL_ID="$SKILL_ID" NEW_VERSION="$NEW_VERSION" KEY="$KEY" python3 -c "
import json, os
q = (
    \"insert into skill_versions (skill_id, version, decryption_key, manifest, active) \"
    \"values (\" + os.environ['SKILL_ID'] + \", '\" + os.environ['NEW_VERSION'] + \"', '\"
    + os.environ['KEY'] + \"', '{}'::jsonb, false) returning id\"
)
print(json.dumps({'query': q}))
")

RESP=$(echo "$QUERY" | curl -sH "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" --data-binary @- "$SQL_URL")
echo "  response: $RESP"

VERSION_ID=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)[0]['id'])")
echo "  version_id=$VERSION_ID"
echo

# --- 3. Pack
echo "Step 3: Run pack-skill.py"
python3 scripts/pack-skill.py \
    --skill-name "$SKILL_NAME" \
    --skill-version "$NEW_VERSION" \
    --skill-id "$SKILL_ID" \
    --skill-version-id "$VERSION_ID" \
    --key-hex "$KEY"
echo

# --- 4. Verify roundtrip
echo "Step 4: Verify decrypt roundtrip"
DECRYPT_OUT=$(mktemp -d)
python3 scripts/decrypt-local.py --key-hex "$KEY" --out "$DECRYPT_OUT"
if diff -q src/SKILL.md "$DECRYPT_OUT/SKILL.md" >/dev/null; then
    echo "  ✓ decrypt roundtrip matches src/SKILL.md byte-for-byte"
    rm -rf "$DECRYPT_OUT"
else
    echo "  ✗ MISMATCH — aborting (decrypted dir kept at $DECRYPT_OUT)"
    exit 1
fi
echo

# --- 5. UPDATE manifest + activate
echo "Step 5: UPDATE skill_versions with real manifest, activate"
QUERY=$(VERSION_ID="$VERSION_ID" python3 <<'PY'
import json, os
manifest_str = open('dist/MANIFEST.enc.json').read()
# Use Postgres dollar-quoting to avoid escaping hell. The tag $mfst$ is unlikely
# to appear in cipher payloads (manifest is JSON; only base64 + hex inside).
vid = os.environ['VERSION_ID']
q = f"update skill_versions set manifest=$mfst${manifest_str}$mfst$::jsonb, active=true where id={vid}"
print(json.dumps({'query': q}))
PY
)

RESP=$(echo "$QUERY" | curl -sH "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" --data-binary @- "$SQL_URL")
echo "  response: $RESP"
echo

# --- 6. Copy cipher into index mirror
echo "Step 6: Copy cipher into $MIRROR_DIR/"
mkdir -p "$MIRROR_DIR"
cp dist/MANIFEST.enc.json "$MIRROR_DIR/"
cp dist/SKILL.md.enc "$MIRROR_DIR/"
cp public/SKILL.md "$MIRROR_DIR/"
echo "  ✓ copied MANIFEST.enc.json, SKILL.md.enc, public/SKILL.md"
echo

# --- 7. Next steps
echo "== Done. Next steps =="
echo
echo "In $SKILL_REPO:"
echo "  git add -A && git commit -m 'feat: publish $SKILL_NAME@$NEW_VERSION (encrypted)' && git push"
echo
echo "In $INDEX_REPO (after bumping version in skills.yaml):"
echo "  git add skills/$SKILL_NAME/ skills.yaml && git commit -m 'chore: bump $SKILL_NAME -> $NEW_VERSION' && git push"
echo
