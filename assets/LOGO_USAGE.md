# Oddmatter logo layouts

The original static pack contains 17 SVGs and the supplied animated pack contains 9 SVGs. Original artwork is preserved.

- Header: `oddmatter-logo-animated-pack/lockup-horizontal-animated-white.svg` (862 × 162). The white horizontal lockup fits the midnight navigation background, at 244px wide on desktop and 210px on mobile.
- Homepage: `oddmatter-logo-animated-pack/lockup-stacked-animated-white.svg` (605 × 262). The stacked logo sits inside decorative orbital rings. Its single yellow accent rests in the mark, launches onto the outer ellipse, completes one orbit, and returns. It remains visible on mobile.
- Footer: the same white horizontal lockup as the header, at 170px wide on desktop and 150px on mobile, with adjacent operator text.
- Browser tab: `oddmatter-logo-pack/favicon.svg` (64 × 64).

The shared renderer embeds the supplied SVG artwork directly, with its original animation styles replaced by scoped page styles. The complete logo is immediately visible, white dots pulse continuously, and the yellow accent floats visibly. All pages use the same header/footer artwork and motion. Logo animations play regardless of the device reduced-motion setting, as requested. The build removes the supplied global reduced-motion override from generated SVG copies while preserving the original source pack. No page scripts are needed.

The space theme uses a midnight background, soft blue and violet glows, static stars, and pale text. Decorative orbits are CSS shapes, not modifications to the logo. Preserve the artwork's proportions, spacing, and suffix opacity; do not crop or reconstruct the wordmark.

The header logo supplies the home link's accessible name. Repeated homepage and footer branding and orbital shapes are decorative. Print styles use a light background for policy readability.

## Homepage orbital motion

The hero uses one yellow dot, with the supplied accent's original resting position and scale. In a 14-second SVG animation it rests for 2 seconds, launches along a curve for 1.2 seconds, follows the outer ellipse for 8 seconds, returns along a curve for 1.2 seconds, and rests for 1.6 seconds before repeating. White hero dots pulse in a staggered four-second wave, changing scale and opacity gently while retaining the dotted grid. The header and footer keep their quieter shared pulse and float animation. The orbital path and rings share one viewBox so they remain aligned at every screen size. This is a presentation extension of the mark; source SVG artwork is unchanged.
