from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote, urljoin
import json

SOURCE = Path(__file__).resolve().parents[1]
ROOT = SOURCE / '_site'
SITE = json.loads((SOURCE / 'site.json').read_text())['url'].rstrip('/') + '/'
SITE_URL = urlsplit(SITE)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])


errors, pages = [], {}
for file in ROOT.rglob('*.html'):
    parser = Links()
    parser.feed(file.read_text())
    pages[file.resolve()] = parser

checked = 0
for file, parser in pages.items():
    page_url = urljoin(SITE, file.relative_to(ROOT).as_posix().removesuffix('index.html'))
    for link in parser.links:
        url = urlsplit(urljoin(page_url, link))
        if url.scheme not in ('http', 'https') or url.netloc != SITE_URL.netloc:
            continue
        checked += 1
        path = unquote(url.path)
        if path.endswith('/index.html'):
            errors.append(f'{file}: use a clean directory URL instead of {link}')
        if not url.path:
            errors.append(f'{file}: homepage URL needs a trailing slash: {link}')
        if not path.startswith(SITE_URL.path):
            errors.append(f'{file}: link outside site base: {link}')
            continue
        target = (ROOT / path[len(SITE_URL.path):]).resolve()
        if target.is_dir():
            if path and not path.endswith('/'):
                errors.append(f'{file}: directory URL needs a trailing slash: {link}')
            target = target / 'index.html'
        if not target.exists():
            errors.append(f'{file}: missing {link}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{file}: missing anchor {link}')

if not pages:
    errors.append('No pages built')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'All {checked} internal links and anchors passed ({len(pages)} pages), including absolute site URLs and clean URL checks.')
