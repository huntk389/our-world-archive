# scripts/edit_server.py
from flask import Flask, request, render_template_string, redirect
import pathlib, subprocess, urllib.parse

DOCS = pathlib.Path("docs")
app = Flask(__name__, static_folder="site")

HTML = """
<h2>Add / Edit Our-World File</h2>
<form method=post>
Path inside docs/ :<br>
<input name=path size=60 value="{{ path }}"><br><br>
<textarea name=content rows=22 style="width:95%">{{ content }}</textarea><br>
<button type=submit>💾 Save & Rebuild</button>
</form>
{% if msg %}<p style="color:green">{{ msg }}</p>{% endif %}
"""

def read(p): return p.read_text() if p.exists() else ""

@app.route("/edit", methods=["GET","POST"])
def edit():
    raw_path = request.values.get("path", "Core Directives/NEW_FILE.md")
    path = DOCS / pathlib.Path(raw_path)
    msg = ""
    if request.method == "POST":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(request.form["content"])
        # regen manifest & site
        subprocess.run(["python", "scripts/generate_manifest.py"])
        subprocess.run(["mkdocs", "build"])
        msg = f"✔ Saved {raw_path} & rebuilt manifest/site"
        return redirect(f"/edit?path={urllib.parse.quote(raw_path)}&msg={urllib.parse.quote(msg)}")
    return render_template_string(HTML, path=raw_path, content=read(path), msg=request.args.get("msg",""))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)