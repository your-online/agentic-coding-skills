#!/usr/bin/env python3
"""lees-oordeel.py — leest de door de browser gespiegelde staat van een
run-document (VERIFICATION.html) terug van schijf, en kan de oordeel-velden
in het HTML-bestand zetten.

De pagina spiegelt zijn localStorage via de annotator-bridge naar
~/Desktop/annotaties/<slug>/state.json (component "acb-state"). Dit script
zoekt die state bij het document, toont per criterium het menselijk oordeel
(select + notitie), en schrijft ze desgewenst het bestand in.

  lees-oordeel.py <VERIFICATION.html>               # toon oordelen (droogloop)
  lees-oordeel.py <VERIFICATION.html> --toepassen   # zet ze ook in het bestand

Bewust NIET teruggezet: de contenteditable-velden (evidence, meta). Daarin zit
precies de veroudering die eerder misging — het bestand op schijf is daarvoor
de waarheid, de browser-staat alleen voor wat de mens zelf invulde."""
import json
import re
import sys
from pathlib import Path

ANNOTATIES = Path.home() / "Desktop/annotaties"
OORDEEL = {"open": "Not yet assessed", "ok": "Met", "part": "Needs work", "fail": "Not met"}


def vind_state(doc):
    naam = doc.name
    for sj in ANNOTATIES.glob("*/state.json"):
        try:
            data = json.loads(sj.read_text())
        except (OSError, ValueError):
            continue
        page = (data.get("page") or "") + (data.get("pageFile") or "")
        entry = data.get("components", {}).get("acb-state", {}).get("state")
        if entry and naam in page:
            return sj, entry.get("state") or {}, entry.get("savedAt")
    return None, None, None


def main(argv):
    args = [a for a in argv if a != "--toepassen"]
    schrijf = "--toepassen" in argv
    if not args:
        print(__doc__, file=sys.stderr)
        return 64
    doc = Path(args[0])
    src = doc.read_text()
    sj, st, moment = vind_state(doc)
    if st is None:
        print(f"geen gespiegelde staat gevonden voor {doc.name} onder {ANNOTATIES} — "
              "is de pagina (met mirror-snippet) in de browser geopend geweest "
              "terwijl de bridge draaide?", file=sys.stderr)
        return 1
    refs = re.findall(r'<span class="ref">([^<]+)</span>', src)
    sel, ta = st.get("sel") or [], st.get("ta") or []
    print(f"staat uit {sj} (opgeslagen {moment}):")
    for i, ref in enumerate(refs):
        s = sel[i] if i < len(sel) else "?"
        n = (ta[i] if i < len(ta) else "").strip()
        print(f"  {ref}: {OORDEEL.get(s, s)}" + (f"  — {n}" if n else ""))
    if not schrijf:
        print("droogloop — niets geschreven; draai met --toepassen om de oordelen "
              "en notities in het bestand te zetten")
        return 0

    i_sel, i_ta = [-1], [-1]

    def zet_select(m):
        i_sel[0] += 1
        v = sel[i_sel[0]] if i_sel[0] < len(sel) else "open"
        blok = re.sub(r' selected', '', m.group(0))
        return re.sub(r'(<option value="' + re.escape(v) + '")', r'\1 selected', blok, count=1)

    def zet_ta(m):
        i_ta[0] += 1
        v = ta[i_ta[0]] if i_ta[0] < len(ta) else ""
        return m.group(1) + v + m.group(2) if v else m.group(0)

    src = re.sub(r'<select>.*?</select>', zet_select, src, flags=re.S)
    src = re.sub(r'(<textarea class="jdnote"[^>]*>).*?(</textarea>)', zet_ta, src, flags=re.S)
    doc.write_text(src)
    print(f"geschreven: {doc} ({i_sel[0] + 1} oordelen, notities waar aanwezig)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
