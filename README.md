# TJ Lee — Business Systems & Automation Engineering

[View the portfolio](https://leetj94-lab.github.io/profile/)

## Selected version — edit this version only

**The sidebar presentation previously called v2 is the single published portfolio.** It was selected because recruiters can scan the overview and open a specific project, experience or AI philosophy without scrolling through all content. There is no version selector or link to the retired layout.

- Active pages: `index.html` (English default), `index.en.html` (explicit English), `index.ko.html` (Korean).
- Project details live inside the same page at `#project-<slug>`; the navigation remains visible.
- Source presentation and paired EN/KO copy: `tools/presentation.py`.
- Project content: `content/portfolio.json`.
- Shared page and case components: `tools/build-locales.py`. Its `home()`/`project()` functions provide reusable content for the selected shell; they do not publish the retired layout.
- Active UI styling: `v2-styles.css`, with shared components in `styles.css`.
- Active behavior: `v2-script.js` (panel routing) and `script.js` (language, tenure, processing stages). The v2 filenames are retained internal implementation names, not a second public version.

**Do not edit generated HTML or hashed CSS/JS directly.** Update these source files and rebuild.

## Historical files — retained, not published

`archive/v1/` contains the retired layout and project pages; `archive/v2/` contains the optional-v2 snapshot before consolidation. These are frozen reference files: do not modify them for portfolio updates, do not link to them and do not include them in the public deployment.

Root `version2*.html` and `projects/*.html` are compatibility redirects only. Existing shared links lead to the selected portfolio and the corresponding project; they never render the retired layout. Do not add portfolio content to these redirect files.

`tools/package-public.py` publishes an explicit allowlist into `_site/`. Archive folders, README, source tools and tests are excluded. The GitHub Pages workflow publishes only `_site/`; never replace it with a repository-wide copy. Merely removing navigation links would not prevent direct access, so archive exclusion is part of deployment.

## Rebuild and verify

```sh
python tools/build-locales.py
python tools/package-public.py
python tests/check-pages.py
node --test tests/site.test.cjs tests/v2.test.cjs
```

The renderer generates complete bilingual HTML and content-hashed runtime assets. The checks verify the selected panels, EN/KO project metrics and stacks, local links, compatibility redirects and archive exclusion. GitHub Pages deploys from `feature/portfolio-site` using `.github/workflows/pages.yml`.

An explicit language choice is remembered when storage is available. Language changes preserve the current section/project. Professional tenure updates from January 2019 using the Seoul calendar year; the Systems Engineer role starts in 2020.

## Content constraints

Project periods, roles and quantitative outcomes follow the supplied resume. Estimated productivity values retain their estimation basis; engineering agents remain a prototype. Protected source code, real system screenshots, operational data and detailed internal architecture are excluded. AI-generated illustrations are disclosed.

The AI philosophy explains engineering judgment, shared `SKILL.md` instructions for UI/code/testing standards, reusable interfaces, acceptance criteria and upfront exception/test scenarios. No API keys, analytics trackers or employer data are required.
