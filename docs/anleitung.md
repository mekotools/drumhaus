# Anleitung: Drumhaus bedienen

Drumhaus ist eine Schlagzeug-Maschine im Browser: du setzt Schläge in ein Raster,
die Maschine spielt sie in einer Schleife. Alles läuft auf dem eigenen Server, ohne
Konto und ohne dass etwas an fremde Server geschickt wird.

**Die Oberfläche ist englisch.** Die englischen Bezeichnungen stehen hier immer
dabei; am Ende gibt es eine Wörterliste.

## 1. Was man auf dem Bildschirm sieht

* **Oben links:** das runde Zeichen mit dem Pferd — das **Menü** (About Drumhaus,
  Donate, Report an Issue, Undo, Redo, Night Mode, Debug Mode, Potato Mode,
  Resize App).
* **Oben in der Mitte:** der Name des Geräts, der **Preset**-Bereich (Save preset,
  Import preset from file, Export, Share preset) und die **Satzwahl** (Kit,
  Previous kit, Next kit).
* **Links:** acht **Stimmen** (voices) untereinander — z. B. Kick, Snare, Hat. Jede
  Stimme hat einen Namen, Regler und eine Reihe aus **16 Schritten** (steps).
* **Unten:** das **Laufwerk** (Play) mit **Tempo** (bpm), **Swing** und Tap, dazu
  die **Muster** A/B/C/D (patterns) und die **Kette** (chain) A/B/C/D.
* **Rechts unten:** die **Effekte** (compressor, saturation, filter, punch, reverb,
  phaser) und die Ausgangslautstärke (output level).

## 2. In fünf Schritten zum ersten Rhythmus

1. **Ton an:** irgendwo einmal klicken. Browser erlauben Ton erst nach einer
   Berührung.
2. **Satz wählen:** mit `Next kit` / `Previous kit` durch die zehn Klangsätze gehen.
3. **Schläge setzen:** in der Reihe einer Stimme (z. B. Kick) auf ein Schrittfeld
   klicken. Noch ein Klick nimmt den Schlag wieder weg. Mit gedrückter Maustaste
   über mehrere Felder ziehen setzt sie in einem Zug.
4. **Hören:** auf `Play` (oder die **Leertaste**) drücken.
5. **Tempo:** mit `bpm` schneller oder langsamer stellen, mit `swing` die Schläge
   leicht „schaukeln“ lassen.

## 3. Die zehn Klangsätze

Jeder Satz hat acht Stimmen. Die Namen stehen im Werkzeug über den Reglern.

* **808** — Kick, Kick2, Snare, Clap, Hat, OHat, Tom, Tom2
* **Organic** — Kick, Kick2, Snare, Clap, Hat, Stick, Perc, Chime
* **Studio** — Kick, Tom, Snare, Clap, Hat, OHat, Perc, Crash
* **Hybrid** — Kick, Kick2, Snare, Snare2, Hat, OHat, Perc, Crash
* **Bounce** — Kick, Kick2, Snare, Clap, Hat, OHat, Tom, Crash
* **Eighties** — Kick, Kick2, Snare, Clap, Hat, OHat, Perc, Crash
* **House** — Kick, Bass, Snare, Clap, Hat, OHat, Piano, Piano2
* **Techno** — Kick, Bass, Snare, Clap, Hat, OHat, Perc, Perc2
* **Trap** — Kick, Kick2, Snare, Clap, Hat, OHat, Hat2, Hat3
* **Jungle** — Kick, Kick2, Snare, Snare2, Hat, OHat, Cymbal, Crash

Kurz erklärt: **Kick** = große Trommel, **Snare** = kleine Trommel, **Clap** =
Klatschen, **Hat** = geschlossene Hi-Hat, **OHat** = offene Hi-Hat, **Tom** =
Tomtom, **Crash** = Beckenschlag, **Cymbal** = Becken, **Perc** = kleines
Schlagwerk, **Stick** = Stockschlag, **Chime** = Glocken, **Bass** = Bass, **Piano**
= Klavier.

## 4. Eine Stimme verändern

Unter dem Namen jeder Stimme liegen vier Regler; mit der Maus ziehen oder mit den
Pfeiltasten feiner stellen:

* **decay** — wie lange der Klang ausklingt
* **tune** — höher oder tiefer stimmen
* **filter** — heller oder dumpfer
* **pan** — links oder rechts im Raum

Dazu die Lautstärke der Stimme. Mit **Escape** kommst du aus einer Stimme wieder
zurück zur Übersicht.

## 5. Muster, Ketten und Werkzeuge

* **Muster (patterns A, B, C, D):** vier Plätze für vier Fassungen desselben
  Rhythmus. Wähle einen Buchstaben und setze die Schläge neu.
* **Kette (chain A, B, C, D):** bis zu **acht Glieder**; die Muster werden dann
  nacheinander gespielt. Mit `chain on` schaltest du die Kette ein.
* **Werkzeuge:** `copy`, `paste`, `clear`, `undo` (Strg+Z / ⌘Z), `accent` (Betonung),
  `velocity` (Anschlagstärke), `nudge` (leicht verschieben), `ratchet`
  (Mehrfachschlag), `flam` (Vorschlag).
* **Effekte:** `compressor` mit `threshold` und `ratio`, `saturation` (Verzerrung),
  `filter`, `punch`, `reverb` (Hall), `phaser` und `output level`.

## 6. Sichern und weitergeben

* **Share preset** erzeugt einen **Link**, in dem Muster, Klänge und Einstellungen
  stecken (rund 200 Zeichen). Den Link kannst du verschicken — wer ihn öffnet, hört
  denselben Rhythmus.
* **Export** gibt das Ergebnis als **Tondatei (WAV)** aus, die du weiterverwenden
  kannst.
* **Save preset** legt einen benannten Stand ab, **Import preset from file** holt
  ihn zurück.

## 7. Als App installieren

Drumhaus lässt sich als App installieren (im Browser meist „Zum Startbildschirm
hinzufügen“). Danach startet es ohne Adressleiste und funktioniert auch ohne
Internet, weil alle Klänge zum Gerät gehören.

## 8. Was diese Fassung ist

Auf dem eigenen Server von MekoTools. Alle **Klänge sind freie Aufnahmen** (CC0 bzw.
CC BY 4.0) und liegen auf demselben Server; beim Bedienen wird **keine** fremde
Adresse aufgerufen — keine Zählung, keine Statistik, keine Schrift von außen. Im
Fenster **About Drumhaus** (im Menü oben links) stehen die Fassungskennung und der
Hinweis, dass dies eine angepasste Fassung ist. Die Verweise `maxfu.ng`, Ko-fi und
GitHub im About-Fenster sind Links zum Urheber; sie laden erst, wenn man sie
anklickt.

## 9. Wörterliste (englisch → deutsch)

* about — über dieses Programm
* accent — Betonung
* bpm — Schläge je Minute (Tempo)
* chain — Kette aus Mustern
* clear — löschen
* clap — Klatschen
* copy / paste — kopieren / einsetzen
* crash / cymbal — Beckenschlag / Becken
* decay — Ausklingen
* export — ausgeben (als Tondatei)
* filter — Filter
* flam — Vorschlag (zwei kurze Schläge)
* hat / ohat — geschlossene / offene Hi-Hat
* import preset from file — Stand aus einer Datei laden
* kit — Klangsatz
* nudge — leicht verschieben
* pan — links/rechts
* pattern — Muster
* play — abspielen
* preset — gespeicherter Stand
* ratchet — Mehrfachschlag
* reverb — Hall
* sample — Klang
* saturation — Verzerrung
* save preset — Stand speichern
* sequencer — Schrittfolge
* share preset — Stand als Link teilen
* snare — kleine Trommel
* step — Schritt
* swing — Schaukeln des Tempos
* tap — Tempo klopfen
* tune — stimmen
* undo / redo — rückgängig / wiederherstellen
* velocity — Anschlagstärke
* voice — Stimme

## 10. Wenn etwas nicht geht

* **Kein Ton:** einmal in die Seite klicken (Browser geben Ton erst nach einer
  Berührung frei) und die Lautstärke des Geräts prüfen.
* **Ruckelt:** im Menü **Potato Mode** einschalten — er nimmt die aufwendige
  Darstellung weg.
* **Zu dunkel / zu hell:** im Menü **Night Mode**.
* **Etwas verschwunden:** im Menü `Undo` oder Strg+Z.
* **Seite bleibt leer:** neu laden; hilft das nicht, ist der Container auf dem
  Server zu prüfen (`https://drumhaus.mekotools.de/gesundheit` antwortet „ok“).
