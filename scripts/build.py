from pathlib import Path
from html import escape as e
import argparse
import json
import re
import shutil
from xml.etree.ElementTree import Element, SubElement, ElementTree

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--production', action='store_true')
args = parser.parse_args()
c = json.loads((ROOT / 'site.json').read_text())
if args.production and (not c['publication_ready'] or not all(
    c[k].strip() for k in ['operator', 'email', 'effective_date']
)):
    raise SystemExit('Publication is not ready: complete site.json and PUBLICATION_CHECKLIST.md, then set publication_ready=true.')
OUT = ROOT / '_site'
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
(OUT / '.nojekyll').write_text('')
shutil.copyfile(ROOT / 'CNAME', OUT / 'CNAME')
NAVIGATION = [('home', 'index.html', 'Home'), ('privacy', 'privacy/index.html', 'Privacy Policy'),
              ('terms', 'terms/index.html', 'Terms of Service'), ('about', 'about/index.html', 'About Us')]
urls = []


def page(path, title, body, prefix, active):
    canonical = c['url'].rstrip('/') + '/' + path.removesuffix('index.html')
    urls.append(canonical)
    navigation = ''.join(
        f'<a href="{prefix}{destination}"' + (' aria-current="page"' if key == active else '') + f'>{label}</a>'
        for key, destination, label in NAVIGATION
    )
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{e(title)} — apps and information from {e(c['name'])}.">
<title>{e(title)} · {e(c['name'])}</title><link rel="canonical" href="{e(canonical)}">
<meta name="theme-color" content="#2433FF"><link rel="icon" type="image/svg+xml" href="{prefix}assets/oddmatter-logo-pack/favicon.svg">
<link rel="stylesheet" href="{prefix}assets/style.css"></head><body>
<a class="skip" href="#main">Skip to content</a><header><div class="wrap">
<a class="brand" href="{prefix}index.html"><img src="{prefix}assets/oddmatter-logo-pack/lockup-horizontal-color.svg" alt="{e(c['name'])}" width="862" height="162"></a>
<nav aria-label="Main">{navigation}</nav></div></header>
<main id="main" class="wrap">{body}</main><footer><div class="wrap">
<span class="footer-brand"><img src="{prefix}assets/oddmatter-logo-pack/mark-color.svg" alt="" width="120" height="120">© 2026 {e(c['operator'] or c['name'])}</span>
<a href="mailto:{e(c['email'])}">{e(c['email'])}</a></div></footer></body></html>'''
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html)


def logo(product, prefix):
    return f'<img class="product-logo" src="{prefix}{e(product["logo"])}" alt="{e(product["name"])} app icon" width="96" height="96">'


def tags(product):
    return '<div class="tags">' + ''.join(f'<span class="tag">{e(t)}</span>' for t in product['platforms']) + '</div>'


def draft_notice():
    return '' if c['publication_ready'] else '<div class="draft"><strong>Draft for review.</strong> Some policy details are awaiting confirmation. This version is not effective.</div>'


def contact():
    return f'<section class="contact"><h2>Contact</h2><p>{e(c["operator"])}</p><p>For support or questions about these policies, email <a href="mailto:{e(c["email"])}">{e(c["email"])}</a>.</p></section>'


def policy_content(doc, anchor_prefix=''):
    toc, sections = [], []
    for i, section in enumerate(doc['sections'], 1):
        anchor = f'{anchor_prefix}section-{i}'
        toc.append(f'<li><a href="#{anchor}">{e(section["title"])}</a></li>')
        sections.append(f'<section id="{anchor}"><h2>{i}. {e(section["title"])}</h2><p>{e(section["body"])}</p></section>')
    return ''.join(toc), ''.join(sections)


products = c['products']
docs = {}
for product in products:
    slug = product['slug']
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        raise SystemExit('Invalid product slug')
    logo_path = Path(product['logo'])
    if logo_path.is_absolute() or '..' in logo_path.parts or not (ROOT / logo_path).is_file():
        raise SystemExit('Invalid product logo')
    docs[slug] = {kind: json.loads((ROOT / 'content' / slug / f'{kind}.json').read_text())
                  for kind in ['privacy', 'terms']}

cards = []
for product in products:
    slug = product['slug']
    cards.append(f'''<article class="card product-card">{logo(product, './')}<div class="product-copy"><h3>{e(product['name'])}</h3>
<p class="product-tagline">{e(product['tagline'])}</p><p>{e(product['description'])}</p>{tags(product)}
<div class="links"><a href="privacy/index.html#{slug}">Privacy Policy</a><a href="terms/index.html#{slug}">Terms of Service</a></div></div></article>''')
body = f'''<div class="home-hero"><div class="hero"><span class="eyebrow">Independent apps by Oddmatter</span>
<h1>Thoughtful apps.<br>For everyday life.</h1><p class="lead">Oddmatter is a home for independent apps that help you keep track of what matters and make everyday tasks a little simpler.</p></div>
<div class="brand-panel"><img src="./assets/oddmatter-logo-pack/lockup-stacked-color.svg" alt="" width="605" height="262"></div></div>
<section id="products"><div class="section-head"><h2>Our apps</h2><span class="meta">Made for everyday use</span></div><div class="cards">{''.join(cards)}</div></section>
<section class="info"><div><span class="eyebrow">Say hello</span><h2>Ideas, questions, or feedback?</h2></div><div><p>We’d love to hear from you.</p><p><a href="mailto:{e(c['email'])}">{e(c['email'])}</a></p><a href="about/index.html">About Oddmatter →</a></div></section>'''
page('index.html', 'Home', body, './', 'home')

for kind, title in [('privacy', 'Privacy Policy'), ('terms', 'Terms of Service')]:
    app_links, contents = [], []
    for product in products:
        slug = product['slug']
        doc = docs[slug][kind]
        toc, sections = policy_content(doc, slug + '-')
        app_links.append(f'<li><a href="#{slug}">{e(product["name"])}</a><ol>{toc}</ol></li>')
        contents.append(f'''<div class="app-policy" id="{slug}"><div class="policy-product">{logo(product, '../')}<div><span class="eyebrow">App-specific details</span>
<h2>{e(product['name'])}</h2><p class="meta">Last updated: {e(doc['updated'])} · Effective: {e(c['effective_date'] or 'Not yet effective')}</p></div></div>{sections}</div>''')
    intro = ('Learn how information is handled across our apps. Each app’s practices are explained in its section below.' if kind == 'privacy'
             else 'Find the terms for using our apps. Each app’s terms are set out in its section below.')
    body = f'''<div class="legal-head"><span class="eyebrow">All Oddmatter apps</span><h1>{title}</h1><p class="lead">{intro}</p>{draft_notice()}</div>
<div class="legal-grid"><aside aria-label="Apps and sections"><strong>On this page</strong><ol>{''.join(app_links)}</ol></aside><article>{''.join(contents)}{contact()}</article></div>'''
    page(f'{kind}/index.html', title, body, '../', kind)

body = f'''<div class="hero about-hero"><span class="eyebrow">About Us</span><h1>A little about<br>Oddmatter.</h1>
<p class="lead">We make independent apps for everyday life.</p><p class="product-description">Oddmatter brings our apps together in one place, starting with TrackLogs: a simple way to record things worth remembering.</p></div>
<section class="info about-contact"><div><span class="eyebrow">Get in touch</span><h2>Say hello.</h2></div><div><p>For product support, feedback, collaboration, or privacy questions, email us.</p>
<p><a class="contact-email" href="mailto:{e(c['email'])}">{e(c['email'])}</a></p><p>Please avoid including sensitive app records unless they are needed to explain your request.</p></div></section>'''
page('about/index.html', 'About Us', body, '../', 'about')

sitemap = Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
for url in urls:
    SubElement(SubElement(sitemap, 'url'), 'loc').text = url
ElementTree(sitemap).write(OUT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
print(f'Built {len(urls)} pages in {OUT}')
