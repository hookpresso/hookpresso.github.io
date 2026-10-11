# Oddmatter logo layouts

The original static pack contains 17 SVGs and the supplied animated pack contains 9 SVGs. Original artwork is preserved.

- Header: `oddmatter-logo-animated-pack/lockup-horizontal-animated-white.svg` (862 × 162). The white horizontal lockup fits the midnight navigation background, at 244px wide on desktop and 210px on mobile.
- Homepage: `oddmatter-logo-animated-pack/lockup-stacked-animated-white.svg` (605 × 262). The stacked logo sits inside decorative orbital rings. It remains visible on mobile.
- Footer: the same white horizontal lockup as the header, at 170px wide on desktop and 150px on mobile, with adjacent operator text.
- Browser tab: `oddmatter-logo-pack/favicon.svg` (64 × 64).

The shared renderer embeds the supplied SVG artwork directly, with its original animation styles replaced by scoped page styles. The complete logo is immediately visible, white dots pulse continuously, and the yellow accent floats visibly. All pages use the same header/footer artwork and motion. CSS respects `prefers-reduced-motion`, displaying the complete artwork without animation. No page scripts are needed.

The space theme uses a midnight background, soft blue and violet glows, static stars, and pale text. Decorative orbits are CSS shapes, not modifications to the logo. Preserve the artwork's proportions, spacing, and suffix opacity; do not crop or reconstruct the wordmark.

The header logo supplies the home link's accessible name. Repeated homepage and footer branding and orbital shapes are decorative. Print styles use a light background for policy readability.
