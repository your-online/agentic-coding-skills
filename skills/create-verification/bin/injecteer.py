#!/usr/bin/env python3
"""injecteer.py — plaatst evidence/<ID>.txt in het evidence-veld van de
bijbehorende criteriumrij van een VERIFICATION.html, zonder iets anders aan te
raken (falsifier-verdicts, oordelen en het annotator-snippet blijven staan).

  injecteer.py <VERIFICATION.html> [<evidence-map>]              # droogloop
  injecteer.py <VERIFICATION.html> [<evidence-map>] --toepassen  # schrijft echt

Droogloop is de default: hij toont per criterium wat er zou gebeuren en of de
Test-kolom het bewijs als programmatisch zal herkennen (resultaat: PASS/FAIL of
"exit code: 0"); alles daarbuiten rendert als "handmatig" en dat wil je zien
vóór je schrijft."""
import html
import re
import sys
from pathlib import Path


def herkenning(tekst):
    if re.search(r"resultaat:\s*(PASS|FAIL)", tekst):
        return "programmatisch (resultaat: PASS/FAIL)"
    if "exit code: 0" in tekst:
        return "programmatisch (exit code: 0)"
    return "LET OP: rendert als 'handmatig' — geen resultaat:-regel of 'exit code: 0'"


def main(argv):
    args = [a for a in argv if a != "--toepassen"]
    schrijf = "--toepassen" in argv
    if not args:
        print(__doc__, file=sys.stderr)
        return 64
    doc = Path(args[0])
    evmap = Path(args[1]) if len(args) > 1 else doc.parent / "evidence"
    src = doc.read_text()
    fouten = 0
    for f in sorted(evmap.glob("*.txt")):
        ref, tekst = f.stem, f.read_text()
        pat = re.compile(r'(<span class="ref">' + re.escape(ref) +
                         r'</span>.*?<div class="evtext"[^>]*>).*?(</div>)', re.S)
        src, n = pat.subn(lambda m: m.group(1) + html.escape(tekst) + m.group(2),
                          src, count=1)
        status = herkenning(tekst)
        print(f"{ref}: {'geïnjecteerd' if n else 'GEEN RIJ GEVONDEN'} — {status}")
        if not n or status.startswith("LET OP"):
            fouten += 1
    if schrijf:
        doc.write_text(src)
        print(f"geschreven: {doc}")
    else:
        print("droogloop — niets geschreven; draai met --toepassen om te schrijven")
    return 1 if fouten else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
