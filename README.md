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

The AI section explains reusable AI skills for UI, API, testing, reliability and code review. Public copy uses capability labels rather than instruction filenames; shared conventions guide generation across tasks and contributors, followed by review, verification and skill refinement. No API keys, analytics trackers or employer data are required.

## Project narrative and role wording

The four platform projects are ordered by development: master data and system integration → drawing/spatial context → connected 3D models → document delivery and richer, faster data updates. Data/operational automation and agent prototypes are shown separately as parallel improvement and exploration. Each project has paired `story_stage` and `story_context` fields in `content/portfolio.json`. The master-data project alone contains the September–November 2024 U.S. rollout note.

The overview uses three strengths rather than project-specific metrics. It reports Samsung tenure from January 2019 in one line; the career section explains the initial facility role and expansion into system development. Project ownership describes implementation responsibility, not a formal technical-lead position.

## Engineering details and MES/MIS operations

Each project stores explicit implementation flow and safeguards in `flow`, plus implementation scope, states/recovery, challenge/decision/reason pairs and condition/expected-behavior checks in `engineering`. Update those fields in both languages; the older `decision`/`checks` fields are retained source history and are not rendered. Existing quantitative outcomes remain unchanged. Do not introduce internal identifiers, actual schemas, infrastructure endpoints or protected source materials.

`tools/engineering.py` renders engineering sections and the MES/MIS continuous-improvement experience. Verification tables and the operating example use native accessible disclosure controls to keep the default page scannable. Actual project code/services are not executed by this static portfolio; website QA checks content, navigation and interactions.

## Hiring review: progressive detail

The active case-study reading order is problem/change → outcome → contribution → selectable implementation → decisions/checks. Core hiring evidence is always visible in the document and is never hidden behind a stage card. A stage card reveals its own `stage_details` (input/output/example) plus the existing processing and safeguard text. Maintain both language values for every field. Mobile click selection scrolls to the selected detail and respects reduced-motion preferences. Career links expose MES/MIS business-improvement experience directly.

The three-pass HR/BA/developer review and acceptance findings are recorded in `docs/PORTFOLIO_REVIEW.md`. That internal document is excluded from the public artifact.

## Requirements evidence and retained walkthrough code

Every project has an `evidence` case linking business needs, implementation decisions and acceptance criteria. Selected results have a `measurement` note separating workload scale, efficiency and estimated productivity value. Do not alter metric values in order to fit an illustrative calculation.

The former interactive validation/delivery walkthrough is preserved under `archive/retired-workflow/` with its renderer and engine tests. It is not imported, built, packaged or tested as part of the active site. Previously shared walkthrough anchors resolve to the document case's engineering section. Selectable implementation stages remain active.

## Repository cleanup and backup boundaries

Unused generated CSS/JS revisions have been removed. Current pages retain their exact content and active runtime assets. Three older generated assets referenced by the frozen HTML snapshots are retained for backup purposes: `script-9054735561.js`, `v2-script-fc61b946be.js` and `v2-styles-321b1ff776.css`; do not edit them for live updates.

`archive/legacy-notes/` holds the earlier writing/design notes and translation dictionary. `archive/legacy-assets/` holds superseded images. These files, the v1/v2 snapshots and the retired walkthrough are backups only. Do not reintroduce them into the active sources or public deployment. Only images referenced by current pages are packaged. Compatibility redirects remain because they support previously shared URLs.
