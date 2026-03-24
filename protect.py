#!/usr/bin/env python3
"""
Obfuskierung + Anti-Copy-Schutz für den Garantieproduktrechner.
Erzeugt aus index.html eine geschützte garantieproduktrechner.html
"""

import re
import sys
from pathlib import Path


def minify_js(js_code: str) -> str:
    """Entfernt Kommentare, komprimiert Whitespace."""
    # Einzeilige Kommentare entfernen (aber nicht URLs mit //)
    result = re.sub(r'(?<!:)//(?!/).*?$', '', js_code, flags=re.MULTILINE)
    # Mehrzeilige Kommentare entfernen
    result = re.sub(r'/\*.*?\*/', '', result, flags=re.DOTALL)
    # Mehrfache Leerzeichen/Tabs -> ein Leerzeichen
    result = re.sub(r'[ \t]+', ' ', result)
    # Leerzeilen entfernen
    result = re.sub(r'\n\s*\n', '\n', result)
    # Klammern komprimieren
    result = re.sub(r' ?\{ ?', '{', result)
    result = re.sub(r' ?\} ?', '}', result)
    result = re.sub(r' ?\( ?', '(', result)
    result = re.sub(r' ?\) ?', ')', result)
    result = re.sub(r' ?= ?', '=', result)
    result = re.sub(r' ?, ?', ',', result)
    result = re.sub(r' ?; ?', ';', result)
    result = re.sub(r' ?\+ ?', '+', result)
    result = re.sub(r' ?- ?', '-', result)
    result = re.sub(r' ?\* ?', '*', result)
    # Zeilenumbrüche nach Semikolon/Klammer entfernen
    result = re.sub(r';\n', ';', result)
    result = re.sub(r'\{\n', '{', result)
    result = re.sub(r'\n\}', '}', result)
    return result.strip()


ANTI_COPY_SCRIPT = """
<script>
(function(){
var d=document;
d.addEventListener('contextmenu',function(e){e.preventDefault();});
d.addEventListener('keydown',function(e){
if(e.ctrlKey&&(e.key==='u'||e.key==='s'||e.key==='c'))e.preventDefault();
if(e.key==='F12')e.preventDefault();
if(e.ctrlKey&&e.shiftKey&&(e.key==='I'||e.key==='J'))e.preventDefault();
});
var s=d.createElement('style');
s.textContent='body,*{-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;}input,textarea{-webkit-user-select:text;-moz-user-select:text;-ms-user-select:text;user-select:text;}';
d.head.appendChild(s);
var w=170;
setInterval(function(){
if((window.outerWidth-window.innerWidth>200)||(window.outerHeight-window.innerHeight>200)){
var o=d.getElementById('dt-overlay');
if(!o){o=d.createElement('div');o.id='dt-overlay';
o.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(255,255,255,0.97);z-index:99999;display:flex;align-items:center;justify-content:center;font-family:Arial;font-size:1.2rem;color:#333;text-align:center;padding:2rem;';
o.textContent='Bitte schließen Sie die Entwicklertools, um den Rechner zu nutzen.';
d.body.appendChild(o);}
}else{var o=d.getElementById('dt-overlay');if(o)o.remove();}
},1500);
})();
</script>
"""


def protect_html(html: str) -> str:
    """Minifiziert JS und fügt Anti-Copy-Script ein."""
    # JS-Blöcke finden und minifizieren
    def minify_match(match):
        tag_open = match.group(1)
        js_content = match.group(2)
        tag_close = match.group(3)
        # CDN-Scripts nicht anfassen
        if 'src=' in tag_open:
            return match.group(0)
        return tag_open + minify_js(js_content) + tag_close

    result = re.sub(
        r'(<script[^>]*>)(.*?)(</script>)',
        minify_match,
        html,
        flags=re.DOTALL
    )

    # CSS minifizieren (inline <style>)
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

    # HTML Whitespace komprimieren
    result = re.sub(r'>\s+<', '><', result)
    result = re.sub(r'\n\s*\n', '\n', result)

    # Anti-Copy-Script vor </body> einfügen
    result = result.replace('</body>', ANTI_COPY_SCRIPT + '</body>')

    return result


def main():
    src = Path(__file__).parent / 'index.html'
    dst = Path(__file__).parent / 'garantieproduktrechner.html'

    if not src.exists():
        print(f'Fehler: {src} nicht gefunden.')
        sys.exit(1)

    html = src.read_text(encoding='utf-8')
    protected = protect_html(html)
    dst.write_text(protected, encoding='utf-8')

    src_size = len(html)
    dst_size = len(protected)
    ratio = (1 - dst_size / src_size) * 100

    print(f'Quelle:    {src.name} ({src_size:,} Zeichen)')
    print(f'Geschützt: {dst.name} ({dst_size:,} Zeichen, {ratio:.0f}% kleiner)')
    print('Fertig.')


if __name__ == '__main__':
    main()
