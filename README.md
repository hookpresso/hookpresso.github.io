# oddmatter.space

A dependency-free, multi-product website for GitHub Pages. TrackLogs is the first product. The Privacy Policy uses original Oddmatter wording based on the supplied disclosures and is effective from 11 October 2026.

## Local preview

Requires Python 3.10+; no packages to install.

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8088 --directory _site
```

Open http://localhost:8088. Generated files stay in ignored `_site/`.

## Site map

- `/`: Oddmatter introduction and product directory, with the real TrackLogs app icon.
- `/privacy/`: site-wide Privacy Policy for Oddmatter services.
- `/terms/`: site-wide Terms of Service for Oddmatter services.
- `/about/`: About Us and contact at `ping@oddmatter.space`.

The site has only these four pages. Navigation uses directory URLs. Visits to an explicit `index.html` address are redirected in the browser to the corresponding directory URL, preserving query parameters and fragments. The build generates `sitemap.xml` for these routes and clears old generated output before rebuilding. The Privacy Policy applies across Oddmatter services and is effective from 11 October 2026. Terms of Service uses original site-wide Oddmatter wording and is effective from 11 October 2026. Its `terms_effective_date` is configured independently of the Privacy Policy's effective date.

## Edit content

- `site.json`: site name, legal operator, support email, effective date, product catalog.
- `content/privacy.txt`: original site-wide Privacy Policy wording.
- `content/terms.txt`: site-wide Terms of Service text.
- `site.json` → `terms_effective_date`: effective date for the terms only.
- `assets/style.css`: responsive space theme, print styles, keyboard focus states.
- `assets/oddmatter-logo-pack/`: supplied static artwork and favicon.
- `assets/oddmatter-logo-animated-pack/`: supplied animated SVGs used in the header, homepage, and footer; see `assets/LOGO_USAGE.md` for layout choices.
- `CNAME`: GitHub Pages custom domain, copied into the deployed site.

To add a product, add a unique lowercase slug and a local logo asset path to the catalog and verify that the shared policies accurately cover its practices. Never reuse TrackLogs disclosures without verifying the new product's behavior. Pages use relative URLs and work on a repository subpath or a custom domain. Product destinations accept HTTPS URLs only.

## Publishing

The owner authorized publication of the Privacy Policy effective 11 October 2026. `publication_ready` controls its public status; PUBLICATION_CHECKLIST.md tracks separate implementation review items. `python3 scripts/build.py --production` verifies required operator fields. This check cannot establish legal or factual accuracy.

Repository: https://github.com/hookpresso/hookpresso.github.io

Website: https://oddmatter.space/

GitHub Pages uses **GitHub Actions**. The supplied workflow checks previews for pull requests and deploys the current site on main pushes or manual runs. The Privacy Policy displays its configured effective date. Terms of Service displays its independently configured effective date. The GitHub Pages environment restricts deployment to main.

The custom domain is `oddmatter.space`, served over HTTPS. The existing GitHub repository name remains unchanged.

Policy paths: `/privacy/` and `/terms/` (both site-wide). The generated site includes only public assets/content. Never upload the entire source repository as the Pages artifact.

## Scope

This project does not modify TrackLogs or update its in-app policy links. The website uses Google Analytics (`G-K8CHP1QJ6S`) on all four pages and includes no external fonts. The measurement ID is configured with `google_analytics_id` in `site.json`. Legacy `index.html` redirects do not initialize the Analytics configuration; their clean-URL destinations do. GitHub Pages itself has hosting request processing. Review operator identity, release-build behavior, and relevant jurisdictions before publishing.
