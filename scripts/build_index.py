import hashlib, json, pathlib, datetime

ROOT = pathlib.Path("docs")

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = []
for file in ROOT.rglob("*"):
    if file.is_file():
        rel = file.relative_to(ROOT).as_posix()
        manifest.append({
            "path": rel,
            "sha256": sha256(file),
            "title": file.stem.replace("_", " "),
            "updated": datetime.datetime.fromtimestamp(file.stat().st_mtime).isoformat()
        })

out = ROOT / "ourworld_manifest.json"
out.write_text(json.dumps(manifest, indent=2))
print(f"✅ Manifest created with {len(manifest)} entries")