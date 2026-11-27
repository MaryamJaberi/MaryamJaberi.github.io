#!/usr/bin/env bash
# Brings the hosted copies of the projects up to date, then rebuilds the pulse and the pages.
# Run from the repo root. Used by .github/workflows/sync.yml; safe to run by hand.
# A project whose build fails keeps its previous copy; the others still update.
set -uo pipefail

OWNER=MaryamJaberi
SRC=_src
STATE=tools/synced.json
mkdir -p "$SRC"
[ -f "$STATE" ] || echo '{}' > "$STATE"

# repo | folder on this site | how to build | what to copy
PROJECTS=(
  "Dour-new|Dour|npm install --no-audit --no-fund && npm run build|dist"
  "Language-Learning-Party-Game-new|Language-Learning-Party-Game|npm install --legacy-peer-deps --no-audit --no-fund && npm run build && rm -rf dist/assets/aistudio|dist"
  "earth-through-time-new|earth-through-time||."
  "ganjoor-no-new|ganjoor-no||."
  "Mafia-new|mafia|npm install --no-audit --no-fund && npm run build:pages|dist-pages"
)

# repos that are not hosted here (no static build): cloned only so the pulse can read their history
SOURCE_ONLY=(hamrah ParkShare)
for repo in "${SOURCE_ONLY[@]}"; do
  if [ -d "$SRC/$repo/.git" ]; then git -C "$SRC/$repo" fetch -q origin && git -C "$SRC/$repo" reset -q --hard FETCH_HEAD
  else git clone -q --filter=blob:none "https://github.com/$OWNER/$repo.git" "$SRC/$repo" || echo "::warning::could not fetch $repo"; fi
done

get_state() { python3 -c "import json,sys;print(json.load(open('$STATE')).get(sys.argv[1],''))" "$1"; }
set_state() { python3 -c "import json,sys;d=json.load(open('$STATE'));d[sys.argv[1]]=sys.argv[2];open('$STATE','w').write(json.dumps(d,indent=2,sort_keys=True)+'\n')" "$1" "$2"; }

for entry in "${PROJECTS[@]}"; do
  IFS='|' read -r repo folder build out <<< "$entry"
  dir="$SRC/$repo"
  echo "::group::$repo"
  if [ -d "$dir/.git" ]; then
    git -C "$dir" fetch -q origin && git -C "$dir" reset -q --hard FETCH_HEAD
  else
    git clone -q --filter=blob:none "https://github.com/$OWNER/$repo.git" "$dir"
  fi
  sha=$(git -C "$dir" rev-parse HEAD 2>/dev/null || echo "")
  if [ -z "$sha" ]; then echo "could not fetch $repo"; echo "::endgroup::"; continue; fi
  if [ "$sha" = "$(get_state "$repo")" ] && [ -d "$folder" ]; then
    echo "$repo unchanged ($sha)"; echo "::endgroup::"; continue
  fi
  if [ -n "$build" ] && ! (cd "$dir" && bash -c "$build"); then
    echo "::warning::$repo failed to build; keeping the previous copy"; echo "::endgroup::"; continue
  fi
  tmp=$(mktemp -d)
  if [ "$out" = "." ]; then
    (cd "$dir" && tar --exclude=.git --exclude=.github --exclude=SECURITY.md --exclude=node_modules -cf - .) | (cd "$tmp" && tar xf -)
  else
    cp -a "$dir/$out/." "$tmp/"
  fi
  # Miz Khoda keeps the source guard (copy carries a citation), as it had before syncing
  if [ "$folder" = "mafia" ] && [ -f "$tmp/index.html" ] && ! grep -q guard.js "$tmp/index.html"; then
    sed -i 's#</body>#<script defer src="/daneshsara/core/guard.js" data-note="off"></script>\n</body>#' "$tmp/index.html"
  fi
  rm -rf "$folder" && mv "$tmp" "$folder" && chmod 755 "$folder"
  set_state "$repo" "$sha"
  echo "$repo -> $folder at $sha"
  echo "::endgroup::"
done

python3 tools/pulse.py "$SRC"
python3 tools/build.py
