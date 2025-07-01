# ── our-world-archive / main.py ──────────────────────────────────────────────
import os, hashlib, json, pathlib, datetime

# 1) Ensure the docs folder exists
DOCS_DIR = pathlib.Path("docs")
DOCS_DIR.mkdir(parents=True, exist_ok=True)   # create if missing

# 2) Helper: SHA-256 hash
def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

# 3) Walk docs/ and collect manifest entries
manifest = []
for file in DOCS_DIR.rglob("*"):
    if file.is_file() and file.suffix.lower() in (".md", ".txt"):
        rel_path = file.relative_to(DOCS_DIR).as_posix()
        manifest.append({
            "path": rel_path,
            "title": file.stem.replace("_", " "),
            "sha256": sha256(file),
            "updated": datetime.datetime.fromtimestamp(file.stat().st_mtime).isoformat()
        })

# 4) Write JSON manifest
out_file = DOCS_DIR / "ourworld_manifest.json"
out_file.write_text(json.dumps(manifest, indent=2))
print(f"✅ Manifest created: {out_file}  •  entries = {len(manifest)}")
# ─────────────────────────────────────────────────────────────────────────────