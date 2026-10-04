"""מושך את הגיליון המפורסם (CSV) ושומר עותק עדכני ב-data/snapshot.json.

הרצה: python3 scripts/snapshot_from_sheet.py && python3 scripts/build.py
דורש גישת רשת ל-docs.google.com.
"""
import csv
import io
import json
import urllib.request
from pathlib import Path

PUB = ("https://docs.google.com/spreadsheets/d/e/2PACX-1vR3q0A13VyyvmdSKnnE-K9FVctvWY18xzu9Wj1VewceOxGvq1wg2_DaYOHmsl2FjCJmfxWjqyTaAb8C"
       "/pub?single=true&output=csv&gid=")
GIDS = {"items": 1, "rels": 2, "sources": 3}
ROOT = Path(__file__).resolve().parent.parent


def rows(gid):
    with urllib.request.urlopen(PUB + str(gid), timeout=30) as r:
        text = r.read().decode("utf-8")
    return [{k.strip(): (v or "").strip() for k, v in row.items()} for row in csv.DictReader(io.StringIO(text))]


items = [dict(id=r["מזהה"], name=r["שם"], type=r["סוג"], parent=r["מזהה אב"], definition=r["המשגה"],
              src=r["מקור"], page=r["עמוד"].lstrip("'"), link=r["קישור להרחבה"], notes=r["הערות"],
              catalog=r["מקור (קטלוג)"], aka=r.get("שמות נוספים", ""))
         for r in rows(GIDS["items"]) if r["מזהה"]]
rels = [dict(a=r["מזהה פריט א"], b=r["מזהה פריט ב"], type=r["סוג קשר"], why=r["הסבר"], status=r["סטטוס"])
        for r in rows(GIDS["rels"]) if r["מזהה פריט א"]]
sources = {r["מזהה"]: dict(name=r["שם המסמך"], link=r["קישור"], org=r["גוף"])
           for r in rows(GIDS["sources"]) if r["מזהה"]}

out = ROOT / "data" / "snapshot.json"
out.write_text(json.dumps(dict(items=items, rels=rels, sources=sources), ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{out}: {len(items)} פריטים, {len(rels)} קשרים, {len(sources)} מקורות")
