# bAV Garantieproduktrechner

## Tech-Stack
- Single-File HTML (Vanilla JS + CSS)
- Chart.js 4.4.7 (CDN, Stacked Area Chart + Annotation Plugin)
- Python 3.13 (Obfuskierungs-Script)

## Architektur
- `index.html` – Lesbare Entwicklungsversion (alle Aenderungen hier)
- `garantieproduktrechner.html` – Obfuskierte Auslieferungsversion (in .gitignore)
- `protect.py` – JS/CSS-Minifizierung + Anti-Copy-Script (Rechtsklick, F12, DevTools-Erkennung)
- `docs/` – Quelldokumente (Prompt von Nanno, Begleit-Mail, PPTX Praesentation)

## Fachlogik (Versicherungsmathematik)
- **Produkt**: Unterstützungskasse (U-Kasse) mit 70% Beitragsgarantie
- **Worst-Case-Ansatz**: Fondsguthaben = 0 EUR fuer Garantieberechnung
- **Garantie-Trigger**: Spaetester Zeitpunkt fuer Umschichtung ins Sicherungsvermoegen
  - Formel: FV = netto * ((1+i)^m - 1) / i >= Garantieziel
  - Trigger = Laufzeitmonate - m
  - Haengt primaer von der Laufzeit ab (Beitrag kuerzt sich raus)
- **Kostenstruktur**: 0,79% Beitrag + 2 EUR Fix/Monat, TER 0,5% p.a.
- **Garantiezins**: 1,0% p.a. (Sicherungsvermoegen)
- **Zwei Anlagemodelle**:
  1. Nur U-Kasse (Garantieprodukt) – Gesamtbeitrag ins Garantieprodukt
  2. Kombi: U-Kasse + DV (Direktversicherung) – Aufteilung einstellbar
     - DV: max 676 EUR (8% BBG 2026), reine Fondsanlage ohne Garantie
     - U-Kasse: Gesamtbeitrag minus DV-Anteil

## Eingabeparameter
- Laufzeit: 5-40 Jahre (Slider + Input)
- Gesamtbeitrag: 50-10.000 EUR/Monat (Slider + Input)
- Fondsrendite: 1,5% / 3% / 4,5% / 6% (Pill-Buttons)
- Anlagemodell: Nur U-Kasse oder Kombi (Toggle)
- DV-Beitrag: 0-676 EUR (Slider + Input, nur bei Kombi)

## Chart-Design (Nanno/Zurich-Stil)
- Grauer Hintergrund (#f0f2f5) fuer Kontrast
- 3 gestapelte Flaechen (dunkel→hell von unten nach oben):
  - #08306B (Garantiesicherheit)
  - #2171B5 (Fonds Garantieprodukt)
  - #6BAED6 (Zusatzfonds DV)
- Zeichenreihenfolge: Groesste Flaeche zuerst (hinten), kleinste zuletzt (vorne)
- Schwarze Gesamtvermoegen-Linie, weiss gestrichelte Beitrags-Linie
- Garantie-Trigger (vertikal) + Garantieziel (horizontal)
- Fondsquoten-Labels alle 5 Jahre
- EUR-Betraege rechts am Laufzeitende fuer Druckversion

## Layout
- Obere Zeile: Eingaben (340px links) + Ergebnisse (rechts)
- Darunter: Chart in voller Breite (440px Hoehe)
- Darunter: FAQ-Sektion (6 Erklaerungen fuer Kunden)
- Responsive: 3 Breakpoints (Desktop/Tablet/Mobile)

## UI-Pattern (konsistent mit bav-dashboard)
- Slider + Input bidirektional synchronisiert
- Pill-Buttons fuer Rendite-Auswahl
- Toggle-Buttons fuer Anlagemodell
- Hero-Box fuer Gesamtvermoegen
- Proportionaler Vermoegensbalken mit Labels unter Segmenten
- CSS-Variablen fuer Farbschema

## Workflow
1. Entwicklung in `index.html`
2. `python protect.py` erzeugt obfuskierte Version
3. Auslieferung: `garantieproduktrechner.html`
