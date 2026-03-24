#!/usr/bin/env python3
"""
Obfuskierung + Anti-Copy-Schutz für den Garantieproduktrechner.
Erzeugt aus index.html eine geschützte garantieproduktrechner.html

Identische Schutzmechanismen wie im bav-dashboard (generate.py):
1. JavaScript-Minifizierung (Kommentare, Whitespace, Operatoren)
2. CSS-Minifizierung
3. HTML-Kommentare entfernen
4. HTML-Whitespace komprimieren
5. Anti-Copy-Script (Rechtsklick, Ctrl+U/S/C, F12, DevTools-Erkennung)
"""

import re
import sys
from pathlib import Path


def minify_js(js_code: str) -> str:
    """Minifiziert JavaScript: Kommentare entfernen, Whitespace komprimieren."""
    # Einzeilige Kommentare entfernen (aber nicht in Strings/URLs)
    result = re.sub(r'(?<!:)//(?!/).*?$', '', js_code, flags=re.MULTILINE)
    # Mehrzeilige Kommentare entfernen
    result = re.sub(r'/\*.*?\*/', '', result, flags=re.DOTALL)
    # Mehrfache Leerzeichen/Tabs -> ein Leerzeichen
    result = re.sub(r'[ \t]+', ' ', result)
    # Leerzeilen entfernen
    result = re.sub(r'\n\s*\n', '\n', result)
    # Leerzeichen um Operatoren (vorsichtig)
    result = re.sub(r' ?\{ ?', '{', result)
    result = re.sub(r' ?\} ?', '}', result)
    result = re.sub(r' ?; ?', ';', result)
    result = re.sub(r' ?, ?', ',', result)
    # Fuehrende Leerzeichen pro Zeile
    result = re.sub(r'^\s+', '', result, flags=re.MULTILINE)
    return result.strip()


# Anti-Copy-Script (identisch mit bav-dashboard)
ANTI_COPY_SCRIPT = (
    "<script>"
    "(function(){var d=document;"
    "d.addEventListener('contextmenu',function(e){e.preventDefault();});"
    "d.addEventListener('keydown',function(e){"
    "if(e.ctrlKey&&(e.key==='u'||e.key==='U'||e.key==='s'||e.key==='S'"
    "||e.key==='c'||e.key==='C')){e.preventDefault();}"
    "if(e.key==='F12'){e.preventDefault();}"
    "if(e.ctrlKey&&e.shiftKey&&(e.key==='I'||e.key==='i'"
    "||e.key==='J'||e.key==='j')){e.preventDefault();}});"
    "var s=d.createElement('style');"
    "s.textContent='body,*{-webkit-user-select:none;-moz-user-select:none;"
    "-ms-user-select:none;user-select:none;}"
    "input,textarea{-webkit-user-select:text;-moz-user-select:text;"
    "-ms-user-select:text;user-select:text;}';"
    "d.head.appendChild(s);"
    "var w=170;setInterval(function(){"
    "if((window.outerWidth-window.innerWidth>200)"
    "||(window.outerHeight-window.innerHeight>200)){"
    "if(!d.getElementById('_dp')){"
    "var o=d.createElement('div');o.id='_dp';"
    "o.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;"
    "background:rgba(255,255,255,0.97);z-index:99999;"
    "display:flex;align-items:center;justify-content:center;"
    "font:600 1.2rem Arial;color:#333;';"
    "o.textContent='Bitte schliessen Sie die Entwicklertools, "
    "um den Rechner zu nutzen.';"
    "d.body.appendChild(o);}}"
    "else{var x=d.getElementById('_dp');if(x)x.remove();}},1500);"
    "})();"
    "</script>"
)


def protect_html(html: str) -> str:
    """Vollstaendiger Schutz: Minifizierung + Anti-Copy."""

    # 1. JavaScript minifizieren
    pattern = re.compile(r'(<script[^>]*>)(.*?)(</script>)', re.DOTALL)
    matches = list(pattern.finditer(html))
    result = html
    js_before = 0
    js_after = 0

    for match in reversed(matches):
        tag_open = match.group(1)
        js_code = match.group(2).strip()
        # CDN-Scripts nicht anfassen
        if 'src=' in tag_open or len(js_code) < 50:
            continue
        minified = minify_js(js_code)
        js_before += len(js_code)
        js_after += len(minified)
        new_block = tag_open + '\n' + minified + '\n' + match.group(3)
        result = result[:match.start()] + new_block + result[match.end():]

    if js_before > 0:
        print(f'  JS: {js_before:,} -> {js_after:,} Zeichen '
              f'({js_after / js_before * 100:.0f}%)')

    # 2. CSS minifizieren
    def minify_css(match):
        css = match.group(1)
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
        css = re.sub(r'\s+', ' ', css)
        css = re.sub(r' ?\{ ?', '{', css)
        css = re.sub(r' ?\} ?', '}', css)
        css = re.sub(r' ?: ?', ':', css)
        css = re.sub(r' ?; ?', ';', css)
        css = re.sub(r' ?, ?', ',', css)
        return '<style>' + css.strip() + '</style>'

    result = re.sub(r'<style>(.*?)</style>', minify_css, result, flags=re.DOTALL)
    print('  CSS minifiziert')

    # 3. HTML-Kommentare entfernen
    result = re.sub(r'<!--.*?-->', '', result, flags=re.DOTALL)
    print('  HTML-Kommentare entfernt')

    # 4. HTML-Whitespace komprimieren
    result = re.sub(r'>\s+<', '><', result)
    result = re.sub(r'\n\s*\n', '\n', result)
    print('  HTML-Whitespace komprimiert')

    # 5. Anti-Copy-Script vor </body> einfuegen
    result = result.replace('</body>', ANTI_COPY_SCRIPT + '\n</body>')
    print('  Anti-Copy-Schutz eingefuegt')
    print('    - Rechtsklick blockiert')
    print('    - Ctrl+U/S/C blockiert (gross/klein)')
    print('    - F12 blockiert')
    print('    - Ctrl+Shift+I/J blockiert')
    print('    - DevTools-Erkennung aktiv')
    print('    - Text-Selection deaktiviert (ausser Inputs)')

    return result


def main():
    src = Path(__file__).parent / 'index.html'
    dst = Path(__file__).parent / 'garantieproduktrechner.html'

    if not src.exists():
        print(f'Fehler: {src} nicht gefunden.')
        sys.exit(1)

    print(f'Quelle: {src.name}')
    print()

    html = src.read_text(encoding='utf-8')
    protected = protect_html(html)
    dst.write_text(protected, encoding='utf-8')

    src_size = len(html)
    dst_size = len(protected)
    ratio = (1 - dst_size / src_size) * 100

    print()
    print(f'Ergebnis: {dst.name}')
    print(f'  {src_size:,} -> {dst_size:,} Zeichen ({ratio:.0f}% kleiner)')
    print()
    print('Fertig. Datei kann versendet werden.')


if __name__ == '__main__':
    main()
