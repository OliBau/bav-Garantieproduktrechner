# bAV Garantieproduktrechner

## Tech-Stack
- Single-File HTML (Vanilla JS + CSS)
- Chart.js (CDN, Stacked Area Chart)
- Python 3.13 (Obfuskierungs-Script)

## Architektur
- `index.html` – Lesbare Entwicklungsversion
- `garantieproduktrechner.html` – Obfuskierte Auslieferungsversion (in .gitignore)
- `protect.py` – Obfuskierung + Anti-Copy-Script
- `docs/` – Quelldokumente (Prompt, E-Mail, Präsentation)

## Fachlogik
- Unterstützungskasse mit 70% Beitragsgarantie (Worst-Case-Ansatz)
- Garantie-Trigger: spätester Zeitpunkt für Sicherungsvermögen-Umschichtung
- Fonds = 0 € für Garantieberechnung
- Kostenstruktur: 0,79% + 2€ Fixkosten/Monat, TER 0,5% p.a.

## Design
- Farbschema: #003B7E-Palette (aus bav-dashboard Muster)
- Neutral, kein Branding/Logo
- Responsive (Desktop/Tablet/Mobile)

## Workflow
1. Entwicklung in `index.html`
2. `python protect.py` erzeugt obfuskierte Version
3. Auslieferung: `garantieproduktrechner.html`
