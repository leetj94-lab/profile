#!/usr/bin/env python3
"""English .en.html files are editable sources; regenerate Korean pages and asset hashes."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib, json, re

ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = json.loads((ROOT / 'content/ko.json').read_text())
UNCHANGED = {'TJ LEE', 'SYSTEMS & AUTOMATION', 'tj.', 'SKILL.md', 'ui-design/SKILL.md',
    'coding-standards/SKILL.md', 'test-generation/SKILL.md', 'Python / FastAPI', 'Vue.js',
    'SQL', 'AWS / S3', 'Linux / CI/CD', 'Vue.js / JavaScript', 'Python / APIs', 'Python',
    'APIs', 'Linux', 'CI/CD', '한국어', 'EN', 'Taekjun (TJ) Lee', 'leetj94@gmail.com ↗', 'LinkedIn ↗'}
missing = set()

def translate(value):
    key = value.strip()
    if key in TRANSLATIONS:
        return value.replace(key, TRANSLATIONS[key])
    if re.search('[A-Za-z]', key) and key not in UNCHANGED:
        missing.add(key)
    return value

class KoreanPage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.output = []
    def handle_decl(self, data): self.output.append('<!' + data + '>')
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html': attrs['lang'] = 'ko'
        if 'data-site-lang' in attrs:
            attrs.pop('aria-current', None)
            if attrs['data-site-lang'] == 'ko': attrs['aria-current'] = 'true'
        elif tag == 'a' and 'href' in attrs and not re.match(r'\w+:|//', attrs['href']):
            attrs['href'] = attrs['href'].replace('.en.html', '.html')
        for key in ['alt', 'aria-label', 'title']:
            if key in attrs: attrs[key] = translate(attrs[key])
        if tag == 'meta' and attrs.get('name') == 'description':
            attrs['content'] = translate(attrs['content'])
        self.output.append('<' + tag + ''.join(' ' + k + ('="' + escape(v, quote=True) + '"' if v is not None else '') for k,v in attrs.items()) + '>')
    def handle_endtag(self, tag): self.output.append('</' + tag + '>')
    def handle_data(self, value): self.output.append(escape(translate(value), quote=False))
    def handle_comment(self, value): self.output.append('<!--' + value + '-->')

def main():
    asset_names = {}
    for filename in ['styles.css', 'script.js']:
        data = (ROOT / filename).read_bytes()
        path = Path(filename)
        hashed = f'{path.stem}-{hashlib.sha256(data).hexdigest()[:10]}{path.suffix}'
        asset_names[path.stem] = hashed
        (ROOT / hashed).write_bytes(data)
    outputs = {}
    year = datetime.now(ZoneInfo('Asia/Seoul')).year
    for page in [ROOT / 'index.en.html', *sorted((ROOT / 'projects').glob('*.en.html'))]:
        text = page.read_text()
        for stem, hashed in asset_names.items():
            extension = 'css' if stem == 'styles' else 'js'
            text = re.sub(stem + r'(?:-[0-9a-f]+)?\.' + extension, hashed, text)
        text = re.sub(r'(<span data-career-years(?:="")?>)\d+\+', r'\g<1>' + str(max(0, year - 2019)) + '+', text)
        text = re.sub(r'(<span id="year">)\d{4}', r'\g<1>' + str(year), text)
        parser = KoreanPage(); parser.feed(text)
        korean = ''.join(parser.output).replace('</span> 년 실무 경험', '</span>년 실무 경험')
        outputs[page] = text
        outputs[page.with_name(page.name.replace('.en.html', '.html'))] = korean
    if missing:
        raise SystemExit('Add Korean translations in content/ko.json:\n' + '\n'.join(sorted(missing)))
    for path, text in outputs.items(): path.write_text(text)
    print(f'Built {len(outputs)} pages; assets: {asset_names}')

if __name__ == '__main__': main()
