from pathlib import Path
from html import escape as e
import argparse
import json
import re
import shutil
from datetime import date
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


products = c['products']
for product in products:
    slug = product['slug']
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
        raise SystemExit('Invalid product slug')
    logo_path = Path(product['logo'])
    if logo_path.is_absolute() or '..' in logo_path.parts or not (ROOT / logo_path).is_file():
        raise SystemExit('Invalid product logo')

cards = []
for product in products:
    slug = product['slug']
    cards.append(f'''<article class="card product-card">{logo(product, './')}<div class="product-copy"><h3>{e(product['name'])}</h3>
<p class="product-tagline">{e(product['tagline'])}</p><p>{e(product['description'])}</p>{tags(product)}
<div class="links"><a href="privacy/index.html">Privacy Policy</a><a href="terms/index.html">Terms of Service</a></div></div></article>''')
body = f'''<div class="home-hero"><div class="hero"><span class="eyebrow">Independent apps by Oddmatter</span>
<h1>Thoughtful apps.<br>For everyday life.</h1><p class="lead">Oddmatter is a home for independent apps that help you keep track of what matters and make everyday tasks a little simpler.</p></div>
<div class="brand-panel"><img src="./assets/oddmatter-logo-pack/lockup-stacked-color.svg" alt="" width="605" height="262"></div></div>
<section id="products"><div class="section-head"><h2>Our apps</h2><span class="meta">Made for everyday use</span></div><div class="cards">{''.join(cards)}</div></section>
<section class="info"><div><span class="eyebrow">Say hello</span><h2>Ideas, questions, or feedback?</h2></div><div><p>We’d love to hear from you.</p><p><a href="mailto:{e(c['email'])}">{e(c['email'])}</a></p><a href="about/index.html">About Oddmatter →</a></div></section>'''
page('index.html', 'Home', body, './', 'home')

# Render site-wide privacy wording and user-requested disclosures.
privacy = (ROOT / 'content/privacy.txt').read_text()
privacy_toc, privacy_sections = [], []
privacy_headings = {'We Do Not Collect Personal Information', 'Non-Personal Information',
                    '1. Session and Available Data：', '2. Log Data:',
                    '3. Google, Facebook and Amplitude Analytics', '4. Cookies', '5. User Feedback:', 'Your AI Interactions'}


def privacy_inline(text):
    # Render the supplied Markdown links while escaping all document text.
    parts, cursor = [], 0
    for match in re.finditer(r'\[([^\]]+)\]\((https://[^\s)]+)\)', text):
        parts.append(e(text[cursor:match.start()]))
        parts.append(f'<a href="{e(match.group(2))}">{e(match.group(1))}</a>')
        cursor = match.end()
    parts.append(e(text[cursor:]))
    return ''.join(parts)


for line in privacy.splitlines():
    if not line.strip():
        continue
    if line.strip() in privacy_headings:
        anchor = f'privacy-section-{len(privacy_toc) + 1}'
        privacy_toc.append(f'<li><a href="#{anchor}">{e(line.strip())}</a></li>')
        privacy_sections.append(f'<h2 id="{anchor}">{e(line.strip())}</h2>')
    else:
        privacy_sections.append(f'<p>{privacy_inline(line)}</p>')
body = f'''<div class="legal-head"><h1>Privacy Policy</h1>{draft_notice()}</div>
<div class="legal-grid"><aside aria-label="On this page"><strong>On this page</strong><ul class="terms-toc">{''.join(privacy_toc)}</ul></aside><article>{''.join(privacy_sections)}</article></div>'''
page('privacy/index.html', 'Privacy Policy', body, '../', 'privacy')

# Site-wide terms have their own effective date, independent of privacy review.
terms = (ROOT / 'content/terms.txt').read_text()
terms_title, terms_body = terms.split('\n', 1)
heading_pattern = re.compile(r'^(\d+\.(?:\d+)?)[ \t]+(.+?)[ \t]*$', re.MULTILINE)
headings = list(heading_pattern.finditer(terms_body))
terms_toc, terms_sections = [], []


def terms_paragraphs(text):
    return ''.join(f'<p class="terms-paragraph">{e(block.strip())}</p>'
                   for block in re.split(r'\n[ \t]*\n', text.strip()) if block.strip())


terms_sections.append(terms_paragraphs(terms_body[:headings[0].start()]))
for i, heading in enumerate(headings):
    anchor = 'section-' + heading.group(1).rstrip('.').replace('.', '-')
    label = heading.group(0).strip()
    end = headings[i + 1].start() if i + 1 < len(headings) else len(terms_body)
    paragraphs = terms_paragraphs(terms_body[heading.end():end])
    terms_toc.append(f'<li><a href="#{anchor}">{e(label)}</a></li>')
    terms_sections.append(f'<section id="{anchor}"><h2>{e(label)}</h2>{paragraphs}</section>')
terms_date = c.get('terms_effective_date', '')
terms_status = (f'<p class="meta">Effective: <time datetime="{e(terms_date)}">{date.fromisoformat(terms_date).strftime("%d %B %Y").lstrip("0")}</time></p>'
                if terms_date else draft_notice())
body = f'''<div class="legal-head"><h1>{e(terms_title)}</h1>{terms_status}</div>
<div class="legal-grid"><aside aria-label="On this page"><strong>On this page</strong><ul class="terms-toc">{''.join(terms_toc)}</ul></aside><article>{''.join(terms_sections)}</article></div>'''
page('terms/index.html', terms_title, body, '../', 'terms')

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
