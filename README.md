# drumhaus — MekoTools-Auslieferung

Dieses Verzeichnis baut ein fertiges Abbild (Docker-Image) der Schlagzeug-Maschine
[drumhaus](https://github.com/mxfng/drumhaus) von Max Fung für den eigenen Betrieb.
Gebaut wird **nur** in der CI (GitHub Actions); ausgeliefert wird ein Container mit
statischen Dateien hinter nginx.

## Was das Abbild enthält

* die Web-Fassung der Schlagzeug-Maschine, gebaut aus dem festgeschriebenen
  Quelltext-Abzug (FASSUNG im `Dockerfile`: `6b3f1856a6878167954f408349b6e4297e628cb7`,
  2026-10-10),
* **80 freie Klänge** anstelle der Klänge des Originals — Herkunft und Lizenz zu
  jedem einzelnen Klang in `klang/manifest.json`,
* die **Wellenformen** (die kleine Zeichnung, die jeder Klang im Werkzeug zeigt),
  neu erzeugt aus diesen Klängen,
* sonst nichts: keine Statistik, keine Anmeldung, kein fremder Server.

## Warum die Klänge ersetzt wurden

Die Herkunft der 80 Originalklänge steht teils in der Datei selbst (RIFF-Block:
Paketname, Vertrieb), teils in der Herkunftsangabe des Werkzeugs. Beides haben wir
ausgelesen:

* **40 Klänge** tragen im Dateikopf die Kennung eines **gekauften Pakets**:
  * 8 × „Sample Magic – Neon Pop“ (Satz Bounce) — mit dem Zusatz
    „Distributed Exclusively by Splice.com“
  * 8 × „Sample Magic – Classic Jungle“ (Satz Jungle)
  * 8 × „Sample Magic – Tape & Vinyl Drums“ (Satz Studio) — über Splice
  * 16 × nur die Kennung „Distributed Exclusively by Splice.com“ (Sätze Trap und
    Eighties), ohne Paketnamen
* **16 Klänge** sind nur in der Herkunftsangabe des Werkzeugs benannt:
  8 × „Roland TR-808 Rhythm Composer“ (Roland Corporation, Satz 808) und
  8 × „Sticks & Stones“ von Dylan Kidd (Satz Organic).
* **24 Klänge** tragen **gar keine** Angabe (Sätze House, Hybrid, Techno).

Gekaufte Klangpakete dürfen wir nicht weitergeben, und Klänge ohne belegte Herkunft
wollen wir nicht weitergeben. Deshalb sind **alle 80 Klangdateien** durch freie
Aufnahmen ersetzt, deren Herkunft und Lizenz belegt ist:

| Quelle | Lizenz | Klänge | Beleg |
| --- | --- | --- | --- |
| Stargate Sample Pack | CC0 1.0 (gemeinfrei) | 39 | `github.com/stargatedaw/stargate-sample-pack` |
| VCSL (Versilian Community Sample Library) | CC0 1.0 | 16 | `github.com/sgossner/VCSL` |
| VSCO 2 Community Edition | CC0 1.0 | 2 | `github.com/sgossner/VSCO-2-CE` |
| MuldjordKit (Lars Muldjord, Fassung des FreePats-Projekts) | CC BY 4.0 (Namensnennung) | 23 | `github.com/freepats/muldjordkit` |

Die 23 Klänge aus dem MuldjordKit verlangen Namensnennung. Sie geschieht an drei
Stellen: in `NOTICE`, in der Herkunftsangabe des Werkzeugs selbst (`attribution` in
`src/core/dhkit/defaults/*.dhkit`, wird beim Bauen gesetzt) und in der Klangdatei
selbst (RIFF-Block: `artist` = Urheber, `comment` = Quelle | Lizenz | Ursprungsdatei).

## Was gegenüber dem Original geändert ist

`scripts/klange-setzen.py` ändert ausschließlich diese Punkte. Für jeden Punkt ist
der erwartete Wortlaut (Anker) hinterlegt; passt er nicht, bricht der Bau ab.

| Stelle | Original | hier |
| --- | --- | --- |
| 80 Klangdateien in `public/samples/` | gekaufte bzw. nicht belegte Klänge | freie Klänge (siehe oben) |
| Wellenformen `public/waveforms/` | passend zu den alten Klängen | aus den neuen Klängen erzeugt |
| Herkunftsangaben in den Werkzeug-Dateien | „Roland TR-808“, „Sticks & Stones“, teils leer | Herkunft der neuen Klänge |
| `package.json` | Bauschritt von `esbuild` nicht erlaubt | erlaubt (sonst lassen sich die Wellenformen nicht erzeugen) |
| Fenster „About“ | nur © Max Fung | zusätzlich Kennzeichnung dieser Fassung als geänderte Fassung |

## Klangaufbereitung

Rohaufnahmen sind für eine Schlagzeug-Maschine selten brauchbar: sie beginnen oft
mit Stille, sind stereo und unterschiedlich laut. Deshalb wird jeder Klang beim Bauen
so aufbereitet:

1. **Schnitt:** Anfang und Ende werden anhand der Hüllkurve bestimmt (Schwelle rund
   −45 dB unter der Spitze) und eng zugeschnitten, mit 5 ms Vor- und Nachlauf und
   einem kurzen Ausblenden am Ende. Harte Schläge behalten ihre Länge (Becken bis
   6,8 s), alles andere wird auf 1,5–3 s begrenzt.
2. **Format:** 1 Kanal (Mono), 96 kHz, 24 Bit — das Format, in dem das Werkzeug
   seine Klänge führt.
3. **Pegel:** jede Datei wird auf −1,5 dBFS Spitze ausgesteuert, damit die Sätze
   untereinander gleich laut sind.
4. **Herkunft in der Datei:** Urheber, Quelle, Lizenz und Ursprungsdatei werden in
   den RIFF-Block geschrieben (`IART`, `ICMT`).

Beleg: alle 80 Dateien sind 96 kHz/Mono/24 Bit; die kürzeste ist 0,09 s, die längste
6,79 s, im Mittel 0,97 s; Gesamtgröße 21,4 MB.

## Bauen und betreiben

```bash
# Bau (im Quelltext-Abzug: pnpm install, Wellenformen erzeugen, bauen)
docker build -t drumhaus .

# Betrieb (Port 80 im Container; nach außen ein freier Port)
docker run -d --name mekotools-drumhaus -p 8190:80 drumhaus
```

Die Kopfzeilen für Kreuzherkunft-Isolation und die Content-Security-Policy stehen in
`config/default.conf`. Wird das Werkzeug hinter einen Reverse Proxy gestellt, müssen
sie dort durchgereicht werden.

## Datenschutz

Zur Laufzeit ruft die Seite **keine** fremde Adresse auf: keine Zählung, keine
Statistik, keine Schrift, keine Klänge und keine Bilder von anderen Servern. Gemessen
im Browser beim Durchschalten aller zehn Sätze: 177 Anfragen, **alle** an die eigene
Adresse, davon 80 Klänge und 80 Wellenformen, keine Fehlermeldung. Die
Content-Security-Policy im ausliefernden nginx verbietet Fremdaufrufe zusätzlich
(`connect-src 'self'`).

Die Verweise im Fenster „About“ und in der Fußzeile (maxfu.ng, Ko-fi, GitHub) sind
**Links**, die erst beim Anklicken geöffnet werden — sie laden von sich aus nichts
nach.

## Prüfungen

* Einheitentests des Originals: **743 bestanden, 1 übersprungen** (42 Dateien) — mit
  den neuen Klängen und den neuen Herkunftsangaben.
* Bau: `pnpm run build` fehlerfrei; im Ergebnis 80 Klangdateien und 80 Wellenformen.
* Betrieb: im Browser geprüft (alle zehn Sätze durchgeschaltet, siehe Datenschutz),
  Fenster „About“ zeigt Version und Kennzeichnung dieser Fassung.

## Lizenzen

* drumhaus (Quelltext): **CC BY-NC-SA 4.0**, © 2023–2026 Max Fung. Eine
  nicht-kommerzielle Lizenz: **MekoTools ist nicht-kommerziell**, deshalb ist die
  Verwendung zulässig. Diese Fassung ist geändert (siehe oben) und wird unter
  derselben Lizenz weitergegeben.
  * **Wird MekoTools später kommerziell betrieben, muss dieses Werkzeug entfernt
    werden** (ebenso wie die Werkzeuge mit CC BY-NC-Klängen).
* Klänge: **CC0 1.0** bzw. **CC BY 4.0** (MuldjordKit, Namensnennung) — siehe
  `klang/manifest.json` und `NOTICE`.

Näheres in `NOTICE`.
