# oddmatter.space

A dependency-free, multi-product website for GitHub Pages. TrackLogs is the first product. Policy organization is inspired by the user-provided TickTick references; the text is adapted to TrackLogs rather than copied as factual promises.

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
- `/privacy/`: Privacy Policy for all listed apps, with app-specific sections.
- `/terms/`: Terms of Service for all listed apps, with app-specific sections.
- `/about/`: About Us and contact at `ping@oddmatter.space`.

The site has only these four pages. The build generates `sitemap.xml` for these routes and clears old generated output before rebuilding. The shared policy pages load each product's own documents; adding an app does not copy TrackLogs disclosures into that app's policy.

## Edit content

- `site.json`: site name, legal operator, support email, effective date, product catalog.
- `content/<product>/privacy.json` and `terms.json`: independent product policies.
- `assets/style.css`: responsive theme, print styles, keyboard focus states.
- `assets/oddmatter-logo-pack/`: supplied brand artwork; see `assets/LOGO_USAGE.md` for layout choices.
- `CNAME`: GitHub Pages custom domain, copied into the deployed site.

To add a product, add a unique lowercase slug and a local logo asset path to the catalog and create both policy files in its content directory. Never reuse TrackLogs disclosures without verifying the new product's behavior. Pages use relative URLs and work on a repository subpath or a custom domain. Product destinations accept HTTPS URLs only.

## Publishing

Complete PUBLICATION_CHECKLIST.md and set `publication_ready` to true only after resolving policy drafts. `python3 scripts/build.py --production` verifies required operator fields. This check cannot establish legal or factual accuracy.

Repository: https://github.com/hookpresso/hookpresso.github.io

Website: https://oddmatter.space/

GitHub Pages uses **GitHub Actions**. The supplied workflow checks previews for pull requests and deploys the current site on main pushes or manual runs. Draft policy notices remain visible until publication review is complete; deployment does not mark policies effective. The GitHub Pages environment restricts deployment to main.

The custom domain is `oddmatter.space`, served over HTTPS. The existing GitHub repository name remains unchanged.

Policy paths: `/privacy/` and `/terms/`, with `#tracklogs` anchors for TrackLogs. The generated site includes only public assets/content. Never upload the entire source repository as the Pages artifact.

## Scope

This project does not modify TrackLogs or update its in-app policy links. The website includes no client-side analytics or external fonts. GitHub Pages itself has hosting request processing. Review operator identity, release-build behavior, and relevant jurisdictions before publishing.
