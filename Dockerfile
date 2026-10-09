# drumhaus — MekoTools-Auslieferung als fertiges Abbild
#
# Gebaut wird aus dem festgeschriebenen Quelltext-Abzug des Originals (FASSUNG
# unten). Geändert wird nur, was geändert werden muss:
#   * Die Klangdateien: die 99 Dateien des Originals stammen überwiegend aus
#     gekauften Klangpaketen (Sample Magic, Splice) sowie aus nicht belegten
#     Quellen. Gekaufte Paketware darf nicht weitergegeben werden. An ihre
#     Stelle treten 80 freie Klänge (CC0 bzw. CC BY 4.0), siehe klang/ und
#     NOTICE. scripts/klange-setzen.py prüft für jede Datei den Anker und
#     bricht bei Abweichung ab.
#   * package.json: der Bauschritt von esbuild wird erlaubt (pnpm 10 führt die
#     Bauschritte der Abhängigkeiten sonst nicht aus; ohne esbuild lassen sich
#     die Wellenformen nicht erzeugen).
#   * Die Wellenformen werden aus den neuen Klängen neu erzeugt — im Original
#     liegen sie fertig bei und passen sonst nicht mehr zu den Klängen.
#
# Sonst bleibt das Werkzeug, wie es ist: keine Statistik, keine Anmeldung, kein
# fremder Server. Zur Laufzeit ruft es keine fremde Adresse auf (im Betrieb
# geprüft).
#
# Die Grundabbilder sind austauschbar: Docker Hub drosselt anonyme Abrufe von
# geteilten Bauservern (HTTP 429). Der Bauablauf versucht es erst amtlich und
# bei Fehlschlag über den öffentlichen Spiegel (siehe .github/workflows).
ARG BASIS_NODE=node:24-bookworm
ARG BASIS_NGINX=nginx:alpine-slim

FROM ${BASIS_NODE} AS bau

# Festgeschriebener Stand: 6b3f1856a6878167954f408349b6e4297e628cb7 (2026-10-10).
ARG QUELLE=https://github.com/mxfng/drumhaus/archive/6b3f1856a6878167954f408349b6e4297e628cb7.tar.gz
ARG FASSUNG=6b3f1856a6878167954f408349b6e4297e628cb7
# pnpm in einer festen Fassung; die Sperrdatei des Originals gehört dazu.
ARG PNPM=10.30.3

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl python3 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /quelle
RUN curl -fsSL "$QUELLE" | tar xz --strip-components=1 \
 && test -f package.json && test -d public/samples && test -f scripts/generate-waveforms.ts

# Eigene Klänge setzen — mit Ankerprüfung (bricht bei Abweichung ab).
COPY klang /klang
COPY scripts/klange-setzen.py /klange-setzen.py
RUN python3 /klange-setzen.py /quelle /klang

RUN npm install -g pnpm@${PNPM} \
 && pnpm install --frozen-lockfile

# Wellenformen aus den neuen Klängen erzeugen, dann bauen.
RUN pnpm run waveforms:build \
 && pnpm run build \
 && test -s dist/index.html \
 && test -s dist/waveforms/index.json \
 && test -s dist/samples/0/kick.wav \
 && test "$(ls dist/samples/*/*.wav | wc -l)" = "80" \
 && echo "--- Buendelgroesse:" && du -sh dist \
 && echo "--- Klangdateien:" && ls dist/samples/*/*.wav | wc -l

FROM ${BASIS_NGINX}
COPY --from=bau /quelle/dist/ /usr/share/nginx/html/
COPY config/default.conf /etc/nginx/conf.d/default.conf
# Selbstkontrolle: eine fehlerhafte Konfiguration soll den Bau scheitern lassen
# und nicht erst im Betrieb zu einem Neustart-Kreis führen.
RUN nginx -t
EXPOSE 80
