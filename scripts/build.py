from pathlib import Path
from html import escape as e
import argparse,json,re,shutil
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--production',action='store_true')
a=parser.parse_args()
c=json.loads((ROOT/'site.json').read_text())
if a.production and (not c['publication_ready'] or not all(c[k].strip() for k in ['operator','email','effective_date'])):
 raise SystemExit('Publication is not ready: complete site.json and PUBLICATION_CHECKLIST.md, then set publication_ready=true.')
OUT=ROOT/'_site'
OUT.mkdir(exist_ok=True)
shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
(OUT/'.nojekyll').write_text('')
shutil.copyfile(ROOT/'CNAME',OUT/'CNAME')
def page(path,title,body,prefix):
 canonical=c['url'].rstrip('/')+'/'+path.removesuffix('index.html')
 html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(title)} — product information and policies for {e(c['name'])}."><title>{e(title)} · {e(c['name'])}</title><link rel="canonical" href="{e(canonical)}"><meta name="theme-color" content="#2433FF"><link rel="icon" type="image/svg+xml" href="{prefix}assets/oddmatter-logo-pack/favicon.svg"><link rel="stylesheet" href="{prefix}assets/style.css"></head><body><a class="skip" href="#main">Skip to content</a><header><div class="wrap"><a class="brand" href="{prefix}index.html"><img src="{prefix}assets/oddmatter-logo-pack/lockup-horizontal-color.svg" alt="{e(c['name'])}" width="862" height="162"></a><nav aria-label="Main"><a href="{prefix}index.html#products">Policies</a><a href="{e(c["profile_url"])}">GitHub ↗</a></nav></div></header><main id="main" class="wrap">{body}</main><footer><div class="wrap"><span class="footer-brand"><img src="{prefix}assets/oddmatter-logo-pack/mark-color.svg" alt="" width="120" height="120">© 2026 {e(c['operator'] or c['name'])}</span><span>Product policies. Clearly explained.</span></div></footer></body></html>'''
 target=OUT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html)
cards=[]
for p in c['products']:
 slug=p['slug']
 if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):raise SystemExit('Invalid product slug')
 tags=''.join(f'<span class="tag">{e(t)}</span>' for t in p['platforms'])
 cards.append(f'<div class="card"><div class="icon" aria-hidden="true">{e(p["emoji"])}</div><h3>{e(p["name"])}</h3><p>Privacy practices and terms for this product.</p><div class="tags">{tags}</div><div class="links"><a href="{slug}/index.html">Explore product →</a><a href="{slug}/privacy/index.html">Privacy</a><a href="{slug}/terms/index.html">Terms</a></div></div>')
 productbody=f'<div class="hero"><span class="eyebrow">{e(p["name"])}</span><h1>{e(p["name"])} policies</h1><p class="lead">Privacy practices and terms for this product.</p><div class="tags">{tags}</div><div class="links"><a href="privacy/index.html">Privacy Policy</a><a href="terms/index.html">Terms of Service</a></div></div>'
 if p.get('url'):
  if not p['url'].startswith('https://'):raise SystemExit('Product URLs must use HTTPS')
  productbody+=f'<p><a href="{e(p["url"])}">Open {e(p["name"])}</a></p>'
 page(f'{slug}/index.html',p['name'],productbody,'../')
 for kind in ['privacy','terms']:
  doc=json.loads((ROOT/'content'/slug/f'{kind}.json').read_text())
  toc=''.join(f'<li><a href="#section-{i}">{e(s["title"])}</a></li>' for i,s in enumerate(doc['sections'],1))
  sections=''.join(f'<section id="section-{i}"><h2>{i}. {e(s["title"])}</h2><p>{e(s["body"])}</p></section>' for i,s in enumerate(doc['sections'],1))
  draft='' if c['publication_ready'] else '<div class="draft"><strong>Draft for review.</strong> Operator details and some policy commitments are awaiting confirmation. This version is not effective.</div>'
  contact=f'<section class="contact"><h2>Contact</h2><p>{e(c["operator"] or "Operator to be confirmed")}</p>'
  contact+=f'<p><a href="mailto:{e(c["email"])}">{e(c["email"])}</a></p>' if c['email'] else f'<p><a href="{e(c["profile_url"])}">GitHub profile</a> · Privacy email to be confirmed.</p>'
  contact+='</section>'
  body=f'<div class="legal-head"><a href="../index.html">← {e(p["name"])}</a><h1>{e(doc["title"])}</h1><p class="meta">Last updated: {e(doc["updated"])} · Effective: {e(c["effective_date"] or "Not yet effective")}</p>{draft}</div><div class="legal-grid"><aside aria-label="On this page"><strong>On this page</strong><ol>{toc}</ol></aside><article>{sections}{contact}</article></div>'
  page(f'{slug}/{kind}/index.html',f'{p["name"]} {doc["title"]}',body,'../../')
policycards=[]
for product in c['products']:
 slug=product['slug']
 policycards.append(f'<div class="card"><div class="icon" aria-hidden="true">{e(product["emoji"])}</div><h3>{e(product["name"])}</h3><p>Privacy practices and terms for {e(product["name"])}.</p><div class="links"><a href="{slug}/privacy/index.html">Privacy Policy →</a><a href="{slug}/terms/index.html">Terms of Service →</a></div></div>')
body='<div class="home-hero"><div class="hero"><span class="eyebrow">'+e(c['name'])+' · Legal & privacy</span><h1>Clear policies.<br>For every product.</h1><p class="lead">Find the Privacy Policy and Terms of Service for the app you use.</p></div><div class="brand-panel"><img src="./assets/oddmatter-logo-pack/lockup-stacked-color.svg" alt="" width="605" height="262"></div></div><section id="products"><div class="section-head"><h2>Product policies</h2><span class="meta">Choose your app</span></div><div class="cards">'+''.join(policycards)+'</div></section><section id="policies" class="info"><div><span class="eyebrow">Questions or requests</span><h2>Get in touch.</h2></div><div><p>For questions about a product’s policies or privacy practices, use the contact details in its policy.</p><p><a href="'+e(c['profile_url'])+'">Find us on GitHub ↗</a></p><p class="meta">This policy website includes no analytics scripts, advertising SDKs, or tracking cookies. GitHub Pages may process request information to serve and secure the site.</p></div></section>'
page('index.html','Product policies',body,'./')
print(f'Built {len(list(OUT.rglob("*.html")))} pages in {OUT}')
