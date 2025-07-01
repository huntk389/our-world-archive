# scripts/generate_manifest.py
import hashlib, json, pathlib, datetime
ROOT = pathlib.Path("docs")
ROOT.mkdir(parents=True, exist_ok=True)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = []
for f in ROOT.rglob("*"):
    if f.is_file() and f.suffix.lower() in (".md", ".txt"):
        manifest.append({
            "path": f.relative_to(ROOT).as_posix(),
            "title": f.stem.replace("_", " "),
            "sha256": sha(f),
            "updated": datetime.datetime.fromtimestamp(f.stat().st_mtime).isoformat()
        })
out = ROOT / "ourworld_manifest.json"
out.write_text(json.dumps(manifest, indent=2))
print(f"✅ Manifest written: {out}  •  entries={len(manifest)}")