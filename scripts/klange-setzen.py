#!/usr/bin/env python3
"""Setzt die freien Klänge in den festgeschriebenen Quelltext-Abzug von drumhaus.

Warum überhaupt: die 99 Klangdateien des Originals stammen überwiegend aus
gekauften Klangpaketen (Sample Magic, Splice) sowie aus nicht belegten Quellen.
Gekaufte Paketware darf nicht weitergegeben werden. Diese Auslieferung enthält
deshalb ausschließlich freie Klänge (CC0 bzw. CC BY 4.0, Namensnennung im
README und in den Dateien selbst).

Ablauf (jeder Schritt prüft seinen Anker und bricht bei Abweichung ab — lieber
kein Abbild als ein stillschweigend falsches):
  1. Erwartete Gestalt des Abzugs prüfen (Kennungen, Verzeichnis der Klänge).
  2. Für jede der 80 Zieldateien: Zieldatei muss es geben (Anker), dann
     überschreiben mit dem eigenen Klang gleichen Namens.
  3. Prüfen, dass danach genau 80 Klangdateien vorliegen — keine Reste des
     Originals, keine fehlenden.
  4. Klangformat prüfen: WAV, 96 kHz, 1 Kanal, 24 Bit.
  5. package.json: den Bau von esbuild erlauben (pnpm 10 führt die Bauschritte
     der Abhängigkeiten sonst nicht aus, und ohne esbuild fehlt dem Werkzeug
     zum Erzeugen der Wellenformen die Grundlage).

Aufruf: python3 klange-setzen.py <quelltext> <klang>
"""
import glob
import json
import os
import sys
import wave
from pathlib import Path

SPITZE = -1.5          # Zielaussteuerung in dBFS
FORMAT = (96000, 1, 3)  # Abtastrate, Kanäle, Bytes je Sample


def anker(bedingung, text):
    if not bedingung:
        raise SystemExit("ANKERPRUEFUNG FEHLGESCHLAGEN: " + text)


def main():
    quelle = Path(sys.argv[1]).resolve()
    klang = Path(sys.argv[2]).resolve()

    # 1. Gestalt des Abzugs
    anker((quelle / "package.json").is_file(), "package.json fehlt")
    anker((quelle / "scripts" / "generate-waveforms.ts").is_file(),
          "scripts/generate-waveforms.ts fehlt (Wellenformen nicht erzeugbar)")
    anker((quelle / "public" / "samples").is_dir(), "public/samples fehlt")
    paket = json.loads((quelle / "package.json").read_text())
    anker("build" in paket.get("scripts", {}) and "waveforms:build" in paket.get("scripts", {}),
          "Bauschritte build/waveforms:build fehlen in package.json")

    plan = json.loads((klang / "manifest.json").read_text())
    anker(len(plan) == 80, "Belegungsplan enthält %d statt 80 Einträge" % len(plan))

    # 2. Klänge setzen
    gesetzt = 0
    for e in plan:
        ziel = quelle / e["zieldatei"]
        anker(ziel.is_file(), "Zieldatei fehlt im Abzug: %s" % e["zieldatei"])
        quelle_datei = klang / e["zieldatei"].replace("public/samples/", "")
        anker(quelle_datei.is_file(), "eigener Klang fehlt: %s" % quelle_datei)
        ziel.write_bytes(quelle_datei.read_bytes())
        gesetzt += 1
    print("gesetzt: %d Klangdateien" % gesetzt)
    anker(gesetzt == 80, "es wurden %d statt 80 Klänge gesetzt" % gesetzt)

    # 3. Vollständigkeit: genau 80 Klangdateien, keine Reste
    vorhanden = sorted(glob.glob(str(quelle / "public" / "samples" / "*" / "*.wav")))
    anker(len(vorhanden) == 80,
          "nach dem Setzen liegen %d statt 80 Klangdateien vor (Reste des Originals?)" % len(vorhanden))
    erwartet = sorted(str(quelle / e["zieldatei"]) for e in plan)
    anker(vorhanden == erwartet, "Dateiliste weicht vom Belegungsplan ab")

    # 4. Klangformat
    for p in vorhanden:
        with wave.open(p, "rb") as w:
            ist = (w.getframerate(), w.getnchannels(), w.getsampwidth())
            anker(ist == FORMAT, "Klangformat falsch bei %s: %s statt %s" % (p, ist, FORMAT))
    print("Formprüfung: %d Dateien sind WAV, 96 kHz, 1 Kanal, 24 Bit" % len(vorhanden))

    # 5. package.json: esbuild darf seinen Bauschritt ausführen
    paket.setdefault("pnpm", {})
    if "esbuild" not in paket["pnpm"].get("onlyBuiltDependencies", []):
        paket["pnpm"]["onlyBuiltDependencies"] = ["esbuild"]
        (quelle / "package.json").write_text(json.dumps(paket, indent=2, ensure_ascii=False) + "\n")
        print("package.json: pnpm.onlyBuiltDependencies = ['esbuild'] ergänzt")
    else:
        print("package.json: Bauschritt für esbuild war bereits erlaubt")

    # 6. Herkunft in den Werkzeug-Dateien richtigstellen. Das Werkzeug führt zu
    #    jedem Klang eine Herkunftsangabe ("attribution") und zeigt sie an. Die
    #    Angaben des Originals nennen teils gekaufte Klangpakete (Roland TR-808,
    #    "Sticks & Stones" von Dylan Kidd) — für unsere Klänge wäre das falsch,
    #    und die Namensnennung bei CC BY 4.0 muss stimmen.
    herkunft = {e["zieldatei"].replace("public/samples/", ""): e["herkunft"] for e in plan}
    kits = sorted((quelle / "src" / "core" / "dhkit" / "defaults").glob("*.dhkit"))
    anker(kits, "keine Werkzeug-Dateien (*.dhkit) gefunden")
    gesetzt_h = 0
    for k in kits:
        d = json.loads(k.read_text())
        geaendert = False
        for inst in d.get("instruments", []):
            s = inst.get("sample") or {}
            pfad = s.get("path")
            if pfad in herkunft:
                s["attribution"] = herkunft[pfad]
                geaendert = True
                gesetzt_h += 1
        if geaendert:
            k.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
    print("Herkunft gesetzt: %d Klänge in %d Werkzeug-Dateien" % (gesetzt_h, len(kits)))
    anker(gesetzt_h == 80, "Herkunft nur für %d statt 80 Klänge gesetzt" % gesetzt_h)

    # 7. Kennzeichnung der Änderung. Die Lizenz des Originals (CC BY-NC-SA 4.0)
    #    verlangt, dass geänderte Fassungen als geändert erkennbar sind. Das
    #    geschieht hier im Fenster "About" — an der Stelle, an der auch der
    #    Urheber genannt wird. Anker ist die Copyright-Zeile; fehlt sie, bricht
    #    der Bau ab.
    about = quelle / "src" / "shared" / "dialogs" / "about-dialog.tsx"
    anker(about.is_file(), "about-dialog.tsx fehlt")
    text = about.read_text()
    anker_kennzeichnung = '<p className="text-xs">© 2023-{currentYear} Max Fung</p>'
    anker(anker_kennzeichnung in text, "Copyright-Zeile im About-Fenster nicht gefunden")
    if "MekoTools" not in text:
        hinweis = (
            anker_kennzeichnung + "\n"
            '            <p className="text-xs">\n'
            "              Angepasste Fassung für MekoTools: alle Klänge dieser Fassung\n"
            "              sind freie Aufnahmen (CC0 bzw. CC BY 4.0). Urheber und Quellen\n"
            "              stehen in der Datei NOTICE des Quelltexts.\n"
            "            </p>"
        )
        about.write_text(text.replace(anker_kennzeichnung, hinweis, 1))
        print("About-Fenster: Kennzeichnung der Änderung ergänzt")
    else:
        print("About-Fenster: Kennzeichnung war bereits vorhanden")


if __name__ == "__main__":
    main()
