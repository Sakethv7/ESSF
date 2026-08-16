# ESSF Website — Open Issues

Last updated: 2026-08-15

---

## ~~0. Past-events galleries — "Show all" pagination~~ — RESOLVED ✅ (2026-08-15)

- **Issue:** The 3 pre-2026 event galleries linked to every photo in the folder behind a
  "Show all N photos" button (67 for 6 July 2024, 12 for 7 April 2024, 140 for 9 July 2023) — user
  felt this was too much to have reachable at all, not just too much to show by default.
- **Fix:** Trimmed each gallery's HTML down to 8 `.gallery-item` photos (the same 8 that were
  already showing by default), removed the "Show all" button-generation logic from
  `js/main.js` entirely (was the `GALLERY COLLAPSE` block), and removed the now-unused
  `.gallery-hidden` / `.gallery-show-more` rules from `css/style.css`. Bumped the `?v=` cache-bust
  on `main.js`/`style.css` across all 5 pages (4→5) since browsers may have the old JS cached.
- **Note:** The 4 July 2026 gallery (22 hand-curated photos, all shown directly, no cap) was
  deliberately left out of this — those aren't a full photo dump, they're already a curated subset
  of the ~200+ raw event photos, which is a different situation from the other 3 galleries. Flag
  if you'd like that capped to 8 too.

---

## ~~1. Logos~~ — RESOLVED ✅

Both logos are in place and live:
- `assets/logos/ek1logo.png` — horizontal banner used in nav on all 5 pages
- `assets/logos/logo.png` — circular emblem used as favicon + faint nav watermark

---

## ~~2a. Directors~~ — RESOLVED ✅ (2026-07-15)

Sh. Jagdish Lal Sehgal (Director-cum-General Secretary, full bio + photo) and Sh. C.P.S. Teotia
(Director, photo only) are live on `pages/executives.html`, sourced from Monty's
"Director Profiles.docx". Teotia's bio was marked "will be shared soon" in that doc — still pending.

## 2b. Executives page — 19 Executive Members

- **File:** `pages/executives.html`
- **Current state:** Directors filled in (see 2a). A note under the grid says Executive Member
  profiles are pending — none of the 19 have names, titles, bios, or photos yet.
- **What's needed from client:** Per-member name, title/role, 1–2 line bio, and a headshot photo
  for each of the 19 Executive Members. Requested from Monty 2026-07-15.
- **How to add once received:** Run photos through `scripts/optimize-images.py` (see item 8),
  save to `assets/images/executives/name.jpg`, copy an `.exec-card` block in
  `pages/executives.html` and fill in the details.

---

## ~~3. Past Events — 7 April 2024 event name~~ — RESOLVED ✅ (2026-08-14)

- **Confirmed by Monty:** Official name is "Vaisakhi Celebration & Felicitation Ceremony". Updated
  in `pages/past-events.html`.
- **Also removed (per Monty, 2026-08-14):** 2 photos from this gallery — `6.jpg` (women seated at
  round table) and `9.jpg` (men seated at round table), identified from a marked-up collage Monty
  sent via WhatsApp. Gallery count updated 14 → 12. Files themselves left in
  `assets/images/events/07-04-2024/` in case they're needed elsewhere — only the site references
  were removed.

---

## 4. Scholarship recipient names

- **Current state:** Award/scholarship photos are in the gallery (06-07-2024 event) but no names are labelled.
- **Issue:** Original photos from Drive are only 420×280px — certificate text is unreadable even at full res.
- **What's needed:** Client provides a list of recipient names paired to photos (e.g., "photo 20.jpg = Priya Sharma").
- **Where it goes:** `alt` text and optionally a caption overlay on each gallery tile in `pages/past-events.html`.

---

## 4b. Past Events — 4 July 2026 (Bharat Mandapam) photos + video clips

- **File:** `pages/past-events.html`
- **Current state:** Full event video embedded and live (`youtu.be/ii1KmRe2GaM`). Photo gallery has
  a curated set of 22 photos live (see below) as a placeholder while the full 222 are pending.
- **Update (2026-08-15):** Pulled 22 photos directly from Monty's shared Drive folder (public,
  no login needed — `drive.google.com/uc?export=download&id=<file-id>`, file IDs read off the
  Drive page DOM) and ran them through `scripts/optimize-images.py` into
  `assets/images/events/04-07-2026/`. Curated for variety: venue signage, VIP arrival, lamp
  lighting, sapling/scholarship handovers, podium speakers, kids receiving Samman Scholarship
  certificates, adult trophy awards, sponsor thank-you, and 4 performance shots (dance + singing).
  Two source photos (`DSC_1025.jpg`, `DSC_1199A_05.jpg`) had no EXIF rotation flag despite being
  shot in portrait — manually rotated 90° before optimizing.
- **Still to do:** The remaining ~200 photos from the Drive folder, for the full-222 publish Monty
  originally asked for (not a curated 30–60 — the filenames are just his personal ordering, we
  can rename freely).
- **Sources shared:**
  - Photos: `drive.google.com/drive/folders/1LjINm4bXNpIQdWcG-vboCsVYQst2pYR5`
  - 18 video clips: `drive.google.com/drive/folders/12AWuzUjn3_c4uagxi3fP0n8ox1JfAb3e`
  - Short Teaser (GDrive): `drive.google.com/file/d/15-ZjCKQ50_D-l5bvVEz-RzvFyN_DQOft`
- **Decided:** Run all 222 photos through `scripts/optimize-images.py` before publishing
  (consistent with existing galleries). Video clips (and the Short Teaser) will be uploaded as
  **Unlisted** YouTube videos and embedded — not self-hosted on the eksoach.in FTP plan (20GB
  total, and Inauguration/Awards alone is 4GB raw — shared hosting has no CDN/adaptive bitrate
  and would eat the quota fast) and not dumped on the public channel (Unlisted keeps them off
  the channel page, search, and subscriber feed, while still being fully embeddable — this is
  what satisfies the earlier "don't upload to the channel" ask).
- ~~**Video section — RESOLVED ✅ (2026-08-14)**~~ Monty already uploaded all 20 videos (Teaser +
  Inauguration/Awards + 17 Performances + the separately-embedded Full Event) as Unlisted and
  built the playlist himself — no channel credentials were needed on our side, just the working
  link (`youtube.com/playlist?list=PLd1Wuaft1X9c` — the earlier copy with the `&si=...` param
  looked truncated but the base link resolves fine). Per Monty's answer, embedded the first 3 of
  the 18 clips directly (Inauguration & Awards, Performance 1, Performance 2 — video IDs pulled
  straight off the live playlist page), plus a 4th card linking out to the full playlist, in
  `pages/past-events.html` under the Bharat Mandapam event group.
  **Assumption to confirm with Monty:** "first 3" was read as the first 3 of the 18 numbered
  clips, skipping the Teaser (which is tracked separately above) — if he meant literal playlist
  order (Teaser, Inauguration/Awards, Performance 1) instead, swap the first embed for the
  Teaser's video ID (`g8RIUvPbqqI`).
- **Still open:**
  1. The 222-photo gallery for this event is still pending — photos need to be pulled from the
     shared Drive folder and run through `scripts/optimize-images.py` (see item 8).
  2. Whether the Short Teaser should also be embedded on-page somewhere (e.g. above the Full
     Event video), or is only meant for sharing outside the site.
- **How to add photos once pulled:** `scripts/optimize-images.py` into
  `assets/images/events/04-07-2026/`, then add `.gallery-item` blocks matching the pattern used
  for the 06-07-2024 event group.

---

## 5. Contact page — phone number

- **Current state:** Address + email only.
- **Issue:** No phone number in the original content doc (`ESSF Website .docx`).
- **What's needed:** Monty provides a contact number if they want it on the site.
- **Where it goes:** `pages/contact.html` — add a new `.contact-row` for phone.

---

## 6. Deploy to eksoach.in

- **Current state:** Live on GitHub Pages at `sakethv7.github.io/ESSF/` for preview only.
- **Blocker:** Awaiting client (Monty) approval of the design.
- **Server:** 20GB hosted plan — well within limit (site is ~6MB total).
- **FTP credentials:** ~~Awaiting~~ **In hand.**

**Steps once approved:**
1. ~~Get FTP credentials for eksoach.in from Monty/hosting provider~~ — done, credentials in hand.
2. From the project root, run: `bash deploy.sh`
3. This creates a `_deploy/` folder with:
   - Dev files stripped (.git, .github, .claude, *.md, deploy.sh)
   - Cache-buster updated to current git SHA automatically
4. Upload `_deploy/`'s contents to `public_html/` via FTP (include `.htaccess`) — either manually
   in FileZilla, or automatically by exporting `FTP_HOST`, `FTP_USER`, `FTP_PASS` before running
   `deploy.sh` (see item 8). Either way, review `_deploy/` locally first — nothing goes live until
   this step runs.
5. Verify HTTPS redirect works: `http://eksoach.in` should auto-redirect to `https://`
6. Spot-check all 5 pages at eksoach.in

**Note:** `.htaccess` handles HTTPS redirect, gzip compression, and browser cache headers — no server-side config needed beyond uploading the file. `public_html/` on the live server still has legacy
files from the old Indiafin-built site (`cgi-bin/`, `prayer-web/`, `Testing/`, old `.html` pages) —
`deploy.sh`'s automated push never deletes anything, only uploads/overwrites `_deploy/`'s files.

---

## ~~7. Payment confirmation~~ — RESOLVED ✅

- **Current state:** Written confirmation received.

---

## 8. Workflow improvements (dev-side, no production config changes)

- **`scripts/optimize-images.py`** — batch-resizes and compresses a folder of raw photos
  (max 1600px long edge, quality 82, EXIF rotation respected) into a folder ready to drop into
  `assets/images/...`. Usage: `python3 scripts/optimize-images.py <input_folder> <output_folder>`.
  Fixes the underlying cause of item 4 (Drive thumbnail links being too low-res) going forward —
  feed it real downloaded files, not `drive.google.com/thumbnail?...` links.
- **Optional automated FTP push** — `deploy.sh` will run `lftp mirror` (no `--delete`) instead of
  printing manual instructions if `FTP_HOST`, `FTP_USER`, `FTP_PASS` are set in the environment.
  Requires `lftp` (`brew install lftp`) and FTP credentials from item 6, which we don't have yet.
  Manual FileZilla upload remains the default until those are configured.
