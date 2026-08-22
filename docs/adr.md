# Architecture Decision Records — ESSF Website

Scoped to the 222-photo Bharat Mandapam gallery change. Each record states what was given up.

---

## ADR-001 — A dedicated gallery page, not a fourth section on `past-events.html`

**Context.** `pages/past-events.html` currently holds four event groups. Three show 8 photos each; the
Bharat Mandapam group shows 22 (7 visible + a "+15 more" tile that reveals the rest via
`.gallery-item--hidden`). The client asked for all 222 to be reachable. The WhatsApp thread already
committed to "a dedicated page on the site — same gallery style as now."

**Options.**

| Option | Shape |
|---|---|
| Append to `past-events.html` | 222 more tiles in the existing event group |
| Dedicated page, linked from the event group | New `pages/gallery-bharat-mandapam.html`; the group on `past-events.html` keeps its 22 and gains a "View all 222 photos" link |
| Dedicated page replacing the group's photos | Same, but strip the 22 from `past-events.html` entirely |

**Choice.** The second — a dedicated page, with the existing 22-photo curated set left in place on
`past-events.html` as the teaser.

Appending is out because it makes one page carry 246 tiles and four unrelated events, and because it
breaks the visual rhythm of the page: three events showing 8 photos each next to one showing 222 reads
as a mistake rather than a choice. Stripping the 22 is out because the curated set is doing real work —
it was hand-picked for variety (venue signage, lamp lighting, handovers, performances) and is a far
better summary of the event than the first 8 photos of 222 sorted by filename would be.

**Consequences.** Every photo now has two reachable URLs when it is one of the curated 22 — the tile on
`past-events.html` and the tile on the gallery page. That is harmless for a static site but it does mean
a photo removed at the client's request (as happened for the 7 April 2024 event) has to be removed in
two places, and forgetting one is a silent failure. Also: the nav does not grow. The gallery page is
reachable only from the Bharat Mandapam event group, so a visitor who never scrolls `past-events.html`
never finds it. That is the intended hierarchy, but it does make the page invisible to anyone
navigating by the top nav alone.

---

## ADR-002 — Two image size tiers, not one

**Context.** Today one JPEG per photo serves both roles: it is the `img src` of the grid tile and the
`href` the lightbox loads. At 1600px / q82 that averages 215KB. The grid tile renders it in a 4:3 box
roughly 220–300px wide, so the browser downloads about 5× the pixels it displays. At 22 photos this
waste is invisible. At 222 it is the difference between a 9MB page and a 47MB page, on a site whose
stated design goal is loading on 2G.

**Options.**

| Option | Grid cost (222 tiles) | Storage | New moving parts |
|---|---|---|---|
| One tier, 1600px | ~47 MB | ~47 MB | none |
| One tier, lowered to ~800px | ~13 MB | ~13 MB | none, but full-size view degrades |
| Two tiers: 500px thumbs + 1600px full | ~9 MB | ~56 MB | a `thumbs/` folder, a second pipeline pass |
| Responsive `srcset` with 2–3 tiers | ~9 MB | ~70 MB | markup complexity across all galleries |

**Choice.** Two tiers — `assets/images/events/04-07-2026/thumbs/*.jpg` at 500px long edge / q78 for the
`img src`, and the existing 1600px files for the `href`.

Lowering the single tier to 800px is the tempting cheap answer and it is wrong: the lightbox is the
whole point of clicking a photo, and 800px looks soft full-screen on any modern phone. `srcset` buys
nothing over the two-tier split here because the grid tile's display size barely varies across
breakpoints — the grid is `minmax(200px, 1fr)`, so a 500px thumb is already comfortably 2× for retina at
every width.

**Consequences.** Storage roughly doubles for this event (47MB → 56MB), which is irrelevant against a
20GB plan but does mean ~444 files committed to git for one event. The pipeline gains a second pass, so
`optimize-images.py` needs a size/quality flag it does not currently have (see `api.md`). And the two
tiers can drift: if someone re-runs the full pass without re-running the thumb pass, the grid silently
shows a stale thumbnail of a photo that has changed. The manifest in ADR-004 is partly there to make
that detectable.

Deliberately **not** applied retroactively to the other three galleries. They show 8 tiles each; the
saving would be ~1.5MB total and the churn would touch every existing page.

---

## ADR-003 — Scrape file IDs from the Drive page, don't add `gdown`

**Context.** The 222 photos live in a public Drive folder. Nothing is on disk. Neither `gdown` nor
`rclone` is installed.

**Options.** `gdown --folder` is the obvious tool, but its unauthenticated folder listing caps at 50
files, which does not cover 222 without workarounds. `rclone` handles it properly but needs an OAuth
config against a Google account — real setup for a one-time pull. The precedent already in this repo
(recorded in `OPEN_ISSUES.md` 4b) is reading file IDs off the Drive folder page's DOM and fetching each
via `drive.google.com/uc?export=download&id=<id>`, which is how the current 22 were obtained.

**Choice.** Neither. **Amended during implementation (2026-08-17):** the normal folder page turned out
not to be scrapable at all — `curl` gets HTTP 200 and a valid title, but the file listing is rendered
client-side and simply isn't in the served HTML, so the DOM-scraping precedent would have required
driving a real browser.

Drive's `embeddedfolderview?id=<id>#list` endpoint is server-rendered and returned **all 222 entries in
a single request**, with `id="entry-<drive_id>"` and `flip-entry-title` markup that pairs each ID with
its filename. `scripts/fetch-drive-folder.py` uses that, then downloads each file via
`uc?export=download&id=<id>` in a resumable loop that skips files already present in staging.

This is strictly better than what was originally decided here: one request instead of browser
automation, no 50-file cap, no scroll-to-load virtualisation, and no dependency on Drive's client-side
rendering.

**Consequences.** Still depends on an undocumented Google endpoint that could change or disappear, and
still only works while the folder is public — but the failure is now loud and specific (zero entries
parsed, exit 1) rather than a silently truncated listing. The script remains a one-off that will rot;
accepted, because the alternative is an OAuth credential flow for a single afternoon's work.

Also discovered: the 222 photos are not in the folder Monty shared — that folder holds a `Photos`
subfolder (`12PCLhyLQlAps8Hng_GHlSaXdQEFglHeq`) and a stray `Short Video (1).mp4`. The script takes a
folder ID, so this cost nothing, but any future re-run must target the subfolder, not the shared link.

Files over 100MB would hit Google's virus-scan interstitial and need a confirm-token round trip.
Measured average is ~7.7MB per photo, so none will; the script does not implement that path and reports
an HTML response as a failed download rather than writing a corrupt file.

---

## ADR-004 — Keep original filenames; add a manifest

**Context.** `OPEN_ISSUES.md` records that the `DSC_*` filenames are the photographer's personal
ordering and "we can rename freely." Sequential renaming (`001.jpg`…`222.jpg`) would make the gallery
markup tidier and the sort order obvious.

**Choice.** Keep the original `DSC_*` stems anyway, and write a `manifest.json` next to the images
recording each photo's source Drive file ID, original name, dimensions, and both output sizes.

Renaming is tempting and costs more than it looks. Item 4 in `OPEN_ISSUES.md` is still open — the client
owes a list mapping scholarship recipients' names to photos. That mapping, whenever it arrives, will be
phrased in the filenames the client can see, which are the Drive ones. Renaming now guarantees a
translation step later, done by hand, across 222 files. The 22 photos already in `assets/` also use
original stems, so renaming would either orphan them or force a second rename pass on
`past-events.html`.

**Amended during implementation (2026-08-17) — original names cannot be kept literally.** Enumeration
showed that **82 of the 222 files** are named `DSC_1199A (1).JPG` through `DSC_1199A (82).JPG`: a burst
series carrying spaces and parentheses. Those characters have to be percent-encoded in every `href` and
`src`, they are a known source of breakage over FTP to shared hosting, and they make the `.htaccess`
rules harder to reason about. Two more files (`DSC_1117A.jpeg`, `DSC_1117B.jpeg`) use a different
extension, and `DSC_460.JPG` is unpadded where every sibling is `DSC_0xxx`.

So filenames are **sanitised, not renamed** — the distinction being that the mapping is mechanical and
reversible rather than a re-sequencing:

| Source | Output | Why |
|---|---|---|
| `DSC_1199A (5).JPG` | `DSC_1199A_05.jpg` | strip space/parens; pad to 2 so the 82-file series sorts correctly |
| `DSC_460.JPG` | `DSC_0460.jpg` | pad to 4 to match `DSC_0xxx` siblings and sort with them, not after `DSC_1398` |
| `DSC_1117A.jpeg` | `DSC_1117A.jpg` | extension normalised by the optimizer already |

This is exactly the mapping the previous session applied by hand — the 22 photos already on disk are
`DSC_1199A_01/_05/_30/_39` and `DSC_0460`, so codifying it keeps the existing files consistent instead
of creating a second convention beside them.

The decision's *rationale* survives intact: the manifest's `name` field still records the untouched
Drive filename, so when the client sends scholarship recipient names keyed to what they see in Drive,
the join column is still there. What changed is only that the on-disk name is now a sanitised
derivative rather than a byte-identical copy.

**Consequences.** The markup is uglier — `DSC_1199A_05.jpg` carries no ordering information, and the
gallery's display order is whatever `sorted()` produces, which interleaves `DSC_0132` and `DSC_1199A_01`
in a way that is lexical rather than chronological. If chronological order turns out to matter, it has
to come from EXIF timestamps, which is a change to the emitter, not to the filenames. The sanitisation
is also a second place where source and output names can drift: anyone reading `DSC_1199A_05.jpg` on
disk has to consult the manifest to know it came from `DSC_1199A (5).JPG`. The manifest is a new file
that nothing enforces the freshness of.

---

## ADR-005 — Commit the JPEGs to git

**Context.** This adds ~444 files and ~56MB of binaries to a repo that is currently ~11MB of assets.
Git stores each JPEG whole and forever; a photo replaced later leaves both copies in history.

**Options.** Commit them; use Git LFS; or keep images out of git and upload them to the host separately.

**Choice.** Commit them, consistent with every other image in the repo.

LFS adds a dependency and a bandwidth quota to a workflow whose entire value is that a non-specialist
can clone and run `deploy.sh`. Keeping images out of git breaks GitHub Pages, which is the client's
preview URL and the only way the design gets approved.

**Consequences.** The repo grows to roughly 70MB and clones get slower, permanently. If the client later
asks for photos to be removed — which has already happened once, for the 7 April 2024 event — deleting
them from the working tree does not shrink the repo, and actually purging them means rewriting history.
Accepting that: at 70MB this is an annoyance, and it would take several more events at this scale before
it became a real problem worth solving with LFS.
