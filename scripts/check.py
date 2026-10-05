from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]/'_site'
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.add(d['id'])
  for k in ('href','src'):
   if k in d:self.links.append(d[k])
errors=[];pages={}
for f in ROOT.rglob('*.html'):
 p=Links();p.feed(f.read_text());pages[f.resolve()]=p
for f,p in pages.items():
 for link in p.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  target=(f.parent/unquote(u.path)).resolve() if u.path else f
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{f}: missing {link}')
  elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{f}: missing anchor {link}')
if not pages:errors.append('No pages built')
if errors:raise SystemExit('\n'.join(errors))
print(f'All internal links and anchors passed ({len(pages)} pages).')
