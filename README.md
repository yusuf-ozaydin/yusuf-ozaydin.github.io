# yusuf-ozaydin.github.io

Personal website for Yusuf Ozaydin. Built with [Quarto](https://quarto.org) and
published to GitHub Pages.

Live at <https://yusuf-ozaydin.github.io>.

## Local development

```bash
quarto preview          # live-reloading local server
quarto render           # build the full site into _site/
python scripts/build_cv.py --strict              # pull the sheet, then rebuild the CV body
python scripts/build_cv.py --strict --no-fetch   # rebuild the CV body from local CSVs only
```

You need Quarto 1.5+ and Python 3.10+. There are no other dependencies; the CV script
uses only the Python standard library.

## How the CV updates itself

The CV page is generated, not hand-written.

- **Source of truth:** a Google Sheet with one tab per section (`profile`, `education`,
  `experience`, `projects`, `activities`, `skills`). The column layout matches the
  files in `data/cv/`.
- `scripts/build_cv.py` reads `scripts/cv_config.json`. If `sheet` is set, it downloads
  each tab as CSV, overwrites the matching `data/cv/<tab>.csv`, and then renders
  `_cv/body.md`. If the sheet is unreachable it keeps the committed CSVs and still
  rebuilds, so the site never breaks on a network hiccup.
- The sheet is currently connected via its **Publish to web** URL
  (`/d/e/2PACX-.../pubhtml`), so it must stay published. `sheet` in `cv_config.json`
  also accepts a normal `/d/<id>/edit` URL, which instead uses the gviz export and
  needs link-sharing turned on.
- `cv.qmd` includes `_cv/body.md`.
- `.github/workflows/publish.yml` runs on every push, on manual trigger, and every
  Monday at 06:00 UTC. It refreshes the CV, commits any changes back to `main`, then
  renders and publishes.

### Connecting the Google Sheet

1. Create a blank Google Sheet.
2. For each file in `data/cv/` (`profile.csv`, `education.csv`, `experience.csv`,
   `projects.csv`, `activities.csv`, `skills.csv`): **File > Import > Upload**, pick the
   file, set "Import location" to **Insert new sheet(s)**, and Import. Then delete the
   empty default `Sheet1`.
3. Check each tab is named exactly `profile`, `education`, `experience`, `projects`,
   `activities`, `skills` (lowercase, no `.csv`). Rename any that differ.
4. **File > Share > Publish to web > Entire document > Publish.**
5. Put the resulting `.../d/e/2PACX-.../pubhtml` URL into the `sheet` field of
   `scripts/cv_config.json` and commit.
6. Test locally: `python scripts/build_cv.py --strict` should report
   "updated data/cv/..." for all six tabs.

After that, editing the sheet is enough; the Monday run picks it up. To publish sooner,
trigger the **Publish** workflow manually from the Actions tab.

### CSV / sheet format notes

- List fields (`bullets`, education `notes`, project `links`) separate items with
  ` | ` **or** a real newline inside the cell (Alt+Enter in Google Sheets). Either works.
- `projects.links` splits each item into label and URL with `::`, for example
  `Code::https://github.com/...`.
- `sort` is a number; lower sorts first.
- `profile` is a two-column `key,value` sheet. Keys: `name`, `pronouns`, `headline`,
  `location`, `email`, `linkedin`, `github`, `citizenship`, `summary`.

## Repository setup (one time)

- Repo must be named `yusuf-ozaydin.github.io` so Pages serves it at the root domain.
- Settings, Pages, Source: **gh-pages** branch (the workflow creates it on first run).
- Settings, Actions, General, Workflow permissions: **Read and write**.

## Editing content

- Home page: `index.qmd`
- Projects: `projects.qmd` (listing) and `projects/*.qmd` (one file per project)
- CV: edit the Google Sheet, or `data/cv/*.csv` for a local-only change
- Writing: `blog.qmd` and `blog/posts/`. The section is intentionally left off the
  navbar until there is a real post; add it to `_quarto.yml` when ready.
- Theme: `theme-light.scss`, `theme-dark.scss`, `custom.css`
