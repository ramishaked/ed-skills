"""בונה את index.html מתוך src/template.html ו-data/snapshot.json.

הרצה: python3 scripts/build.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
template = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
data = json.loads((ROOT / "data" / "snapshot.json").read_text(encoding="utf-8"))
html = template.replace("__DATA__", json.dumps(data, ensure_ascii=False))
(ROOT / "index.html").write_text(html, encoding="utf-8")
print(f"index.html: {len(data['items'])} פריטים, {len(data['rels'])} קשרים, {len(data['sources'])} מקורות")
