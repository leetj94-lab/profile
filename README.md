# TJ Lee — Business Systems & Automation Engineering

[View portfolio](https://leetj94-lab.github.io/profile/)

The default and canonical pages are English (`index.html`, `projects/<slug>.html`). Korean pages use `.ko.html`. Existing `.en.html` addresses remain equivalent English aliases. An explicit language choice is remembered when browser storage is available; language links preserve the current section.

## Content and rebuild

`content/portfolio.json` is the bilingual project source. Each text field stores paired `en` and `ko` values; metrics, dates and technology lists are shared. Main-page copy lives in `tools/build-locales.py`; the optional v2 shell and shared AI philosophy copy live in `tools/presentation.py`, with paired translations.

The source resume is `Taekjun_Lee_Resume_Final.pdf`. Project periods, roles and quantitative outcomes follow that resume. Annual productivity values retain the resume’s estimation basis. The engineering-agent work remains a prototype. Source system screenshots, protected code, operational datasets, detailed deployment architecture and internal identifiers are excluded.

Edit `content/portfolio.json`, `styles.css`, `script.js` or the shared renderer, then run:

```sh
python tools/build-locales.py
python tests/check-pages.py
node --test tests/site.test.cjs tests/v2.test.cjs
```

The renderer creates complete English/Korean HTML and content-hashed CSS/JS. Do not edit hashed assets or generated HTML directly. It also keeps the former construction-progress URLs working by routing them to the updated project set.

## Interaction

Each case study includes a before/after workflow, selectable processing stages, ownership by engineering area and operational results. Stage controls support click, arrow keys, Home and End. No API keys, analytics trackers, external runtime libraries or employer data are required.

Professional experience is calculated from January 2019 using the Seoul calendar year. This is total professional tenure, separate from the Systems Engineer role beginning in 2020.

The existing `feature/portfolio-site` branch is retained for the GitHub Pages deployment environment.

## Optional streamlined version

`version2.html` (English) and `version2.ko.html` (Korean) provide persistent category navigation and hash-addressable project panels. The original page retains its layout and offers a v2 entry button. Each version links back to its counterpart; language changes retain the selected category or project. On mobile, the rail becomes a compact top menu.

Both versions explain AI as team engineering: domain context, shared `SKILL.md` instructions for UI/code/testing standards, reusable interfaces, acceptance criteria and upfront exception/test scenarios. Source CSS/JS for the new shell are `v2-styles.css` and `v2-script.js`; the renderer generates content-hashed assets.
