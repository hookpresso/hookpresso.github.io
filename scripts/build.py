from pathlib import Path
from html import escape as e
import argparse
import json
import hashlib
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
# Remove the supplied global motion override from generated SVG copies.
# Preserve the original logo pack; inline logos already discard embedded styles.
for svg_path in (OUT / 'assets/oddmatter-logo-animated-pack').glob('*.svg'):
    svg = svg_path.read_text()
    svg = svg.replace('@media (prefers-reduced-motion:reduce){*{animation:none!important}}', '')
    svg_path.write_text(svg)
(OUT / '.nojekyll').write_text('')
shutil.copyfile(ROOT / 'CNAME', OUT / 'CNAME')
NAVIGATION = [('home', 'index.html', 'Home'), ('privacy', 'privacy/index.html', 'Privacy Policy'),
              ('terms', 'terms/index.html', 'Terms of Service'), ('about', 'about/index.html', 'About Us')]
urls = []
style_version = hashlib.sha256((ROOT / "assets/style.css").read_bytes()).hexdigest()[:10]


def brand_svg(layout='horizontal'):
    # Keep supplied artwork; page CSS controls consistent, ongoing motion.
    svg = (ROOT / 'assets/oddmatter-logo-animated-pack' / f'lockup-{layout}-animated-white.svg').read_text()
    svg = re.sub(r'<style>.*?</style>', '', svg, flags=re.S)
    svg = re.sub(r'<title>.*?</title>', '', svg, flags=re.S)
    svg = re.sub(r' role="[^"]*"| aria-label="[^"]*"', '', svg)
    svg = svg.replace('<svg ', '<svg class="brand-logo" aria-hidden="true" focusable="false" ')
    for original, scoped in [('d', 'logo-dot'), ('f', 'logo-float'), ('o', 'logo-accent'), ('t', 'logo-type')]:
        svg = svg.replace(f'class="{original}"', f'class="{scoped}"')
    return svg


def render_toc(entries):
    groups = []
    for anchor, label, level in entries:
        link = f'<a href="#{anchor}">{e(label)}</a>'
        if level == 2:
            groups[-1][1].append(f'<li>{link}</li>')
        else:
            groups.append((link, []))
    return ''.join('<li>' + link + ('<ul class="toc-subsections">' + ''.join(children) + '</ul>' if children else '') + '</li>'
                   for link, children in groups)


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
<meta name="theme-color" content="#080a18"><link rel="icon" type="image/svg+xml" href="{prefix}assets/oddmatter-logo-pack/favicon.svg">
<link rel="stylesheet" href="{prefix}assets/style.css?v={style_version}"></head><body>
<a class="skip" href="#main">Skip to content</a><header><div class="wrap">
<a class="brand" href="{prefix}index.html" aria-label="{e(c['name'])} home">{brand_svg()}</a>
<nav aria-label="Main">{navigation}</nav></div></header>
<main id="main" class="wrap">{body}</main><footer><div class="wrap">
<span class="footer-brand"><a class="brand" href="{prefix}index.html" aria-label="{e(c['name'])} home">{brand_svg()}</a><span>© 2026 {e(c['operator'] or c['name'])}</span></span>
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
<h1>Thoughtful apps.<br><span>For everyday life.</span></h1><p class="lead">Oddmatter is a home for independent apps that help you keep track of what matters and make everyday tasks a little simpler.</p><div class="hero-actions"><a class="button" href="#products">Explore our apps <span aria-hidden="true">↗</span></a><a href="about/index.html">Meet Oddmatter →</a></div></div>
<div class="brand-panel"><span class="orbit-dot" aria-hidden="true"></span>{brand_svg('stacked')}<span class="orbit-caption" aria-hidden="true">A little space for good ideas</span></div></div>
<section id="products"><div class="section-head"><h2>Our apps</h2><span class="meta">Made for everyday use</span></div><div class="cards">{''.join(cards)}</div></section>
<section class="info"><div><span class="eyebrow">Say hello</span><h2>Ideas, questions, or feedback?</h2></div><div><p>We’d love to hear from you.</p><p><a href="mailto:{e(c['email'])}">{e(c['email'])}</a></p><a href="about/index.html">About Oddmatter →</a></div></section>'''
page('index.html', 'Home', body, './', 'home')

# Render site-wide privacy wording and user-requested disclosures.
privacy = (ROOT / 'content/privacy.txt').read_text()
privacy_toc, privacy_sections = [], []
privacy_headings = {
    'Information we receive': ('1.', 1),
    'Account details and usage': ('1.1', 2),
    'Browsers and devices': ('1.2', 2),
    'Location-based features': ('1.3', 2),
    'Profile images': ('1.4', 2),
    'AI requests and conversations': ('1.5', 2),
    'How we use information': ('2.', 1),
    'Delivering requested features': ('2.1', 2),
    'Keeping products working': ('2.2', 2),
    'Responding and communicating': ('2.3', 2),
    'Preventing harm': ('2.4', 2),
    'Your data and service providers': ('3.', 1),
    'Website cookies': ('4.', 1),
    'Protecting information': ('5.', 1),
    'Storage and retention': ('6.', 1),
    'Access, changes, and deletion': ('7.', 1),
    'Updates to this policy': ('8.', 1),
    'Contact Oddmatter': ('9.', 1),
}


def policy_inline(text):
    # Link document references in one pass, preserving text and escaping HTML.
    pattern = re.compile(
        r'\[(?P<label>[^\]]+)\]\((?P<destination>https://[^\s)]+)\)'
        r'|(?P<url>https?://[^\s<>"\)]+)'
        r'|(?P<email>[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})'
        r'|(?P<policy>Privacy Policy|Terms of Service)'
    )
    parts, cursor = [], 0
    for match in pattern.finditer(text):
        parts.append(e(text[cursor:match.start()]))
        suffix = ''
        if match.group('destination'):
            label, destination = match.group('label'), match.group('destination')
        elif match.group('url'):
            label = match.group('url').rstrip('.,;:!?')
            suffix = match.group('url')[len(label):]
            destination = label
        elif match.group('email'):
            label = match.group('email')
            destination = 'mailto:' + label
        else:
            label = match.group('policy')
            route = 'privacy' if label == 'Privacy Policy' else 'terms'
            destination = c['url'].rstrip('/') + '/' + route + '/'
        parts.append(f'<a href="{e(destination)}">{e(label)}</a>{e(suffix)}')
        cursor = match.end()
    parts.append(e(text[cursor:]))
    return ''.join(parts)


for line in privacy.splitlines():
    if not line.strip():
        continue
    if line.strip() in privacy_headings:
        anchor = f'privacy-section-{len(privacy_toc) + 1}'
        number, level = privacy_headings[line.strip()]
        label = number + ' ' + line.strip()
        privacy_toc.append((anchor, label, level))
        tag = 'h3' if level == 2 else 'h2'
        privacy_sections.append(f'<{tag} id="{anchor}">{e(label)}</{tag}>')
    else:
        privacy_sections.append(f'<p>{policy_inline(line)}</p>')
privacy_date = c.get('effective_date', '')
privacy_status = (f'<p class="meta">Effective: <time datetime="{e(privacy_date)}">{date.fromisoformat(privacy_date).strftime("%d %B %Y").lstrip("0")}</time></p>'
                  if c['publication_ready'] and privacy_date else draft_notice())
body = f'''<div class="legal-head"><h1>Privacy Policy</h1>{privacy_status}</div>
<div class="legal-grid"><aside aria-label="On this page"><strong>On this page</strong><ul class="terms-toc">{render_toc(privacy_toc)}</ul></aside><article>{''.join(privacy_sections)}</article></div>'''
page('privacy/index.html', 'Privacy Policy', body, '../', 'privacy')

# Site-wide terms have their own effective date, independent of privacy review.
terms = (ROOT / 'content/terms.txt').read_text()
terms_title, terms_body = terms.split('\n', 1)
heading_pattern = re.compile(r'^(\d+\.(?:\d+)?)[ \t]+(.+?)[ \t]*$', re.MULTILINE)
headings = list(heading_pattern.finditer(terms_body))
terms_toc, terms_sections = [], []


def terms_paragraphs(text):
    return ''.join(f'<p class="terms-paragraph">{policy_inline(block.strip())}</p>'
                   for block in re.split(r'\n[ \t]*\n', text.strip()) if block.strip())


terms_sections.append(terms_paragraphs(terms_body[:headings[0].start()]))
for i, heading in enumerate(headings):
    anchor = 'section-' + heading.group(1).rstrip('.').replace('.', '-')
    label = heading.group(0).strip()
    end = headings[i + 1].start() if i + 1 < len(headings) else len(terms_body)
    paragraphs = terms_paragraphs(terms_body[heading.end():end])
    level = 2 if '.' in heading.group(1).rstrip('.') else 1
    terms_toc.append((anchor, label, level))
    terms_sections.append(f'<section id="{anchor}"><h2>{e(label)}</h2>{paragraphs}</section>')
terms_date = c.get('terms_effective_date', '')
terms_status = (f'<p class="meta">Effective: <time datetime="{e(terms_date)}">{date.fromisoformat(terms_date).strftime("%d %B %Y").lstrip("0")}</time></p>'
                if terms_date else draft_notice())
body = f'''<div class="legal-head"><h1>{e(terms_title)}</h1>{terms_status}</div>
<div class="legal-grid"><aside aria-label="On this page"><strong>On this page</strong><ul class="terms-toc">{render_toc(terms_toc)}</ul></aside><article>{''.join(terms_sections)}</article></div>'''
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
