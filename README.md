# TJ Lee — Systems & Automation Engineering

[View portfolio](https://leetj94-lab.github.io/profile/)

The default pages are Korean. Each `*.en.html` page contains complete English HTML; the language controls preserve the project and remember the selected language when browser storage is available. Both languages work without JavaScript. Professional experience is calculated from January 2019 at page load, using the Seoul calendar year; this is total professional experience, not a claim about software-development tenure.

## Editing content

1. Edit the English `index.en.html` or `projects/*.en.html` pages.
2. Update the corresponding Korean text in `content/ko.json`.
3. Run `python tools/build-locales.py` to regenerate Korean pages and versioned CSS/JS assets. Missing translations fail the build.
4. Run `node --test tests/site.test.cjs`.

Edit `styles.css` and `script.js`, then run the same locale builder to update content-hashed filenames. Do not edit hashed copies directly.

## Content boundaries

Actual project contributions are separate from the labeled hypothetical design exercises. Example stacks, design choices, recovery patterns, and validation criteria are illustrative; they are not assertions about the employer’s architecture or completed implementations. Replace examples only with verified, disclosure-approved experience. No performance measurements have been invented.

AI assists design, development, and conceptual imagery. Protected employer screenshots, code, operational datasets, and detailed architecture are excluded.

The existing `feature/portfolio-site` deployment branch is retained for the GitHub Pages environment.
