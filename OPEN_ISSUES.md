# ESSF Website — Open Issues

Last updated: 2026-07-15

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

## 3. Past Events — 7 April 2024 event name

- **Current label:** "Annual Felicitation Ceremony"
- **Issue:** Name guessed from photos — banner only showed "Ek Soach Saathiya Foundation · Aapka Hardik Swagat Hai", no specific event title visible.
- **What's needed:** Monty confirms the correct event name.
- **Where it goes:** Line 122 of `pages/past-events.html` — the `<h3 class="event-date">` heading.

---

## 4. Scholarship recipient names

- **Current state:** Award/scholarship photos are in the gallery (06-07-2024 event) but no names are labelled.
- **Issue:** Original photos from Drive are only 420×280px — certificate text is unreadable even at full res.
- **What's needed:** Client provides a list of recipient names paired to photos (e.g., "photo 20.jpg = Priya Sharma").
- **Where it goes:** `alt` text and optionally a caption overlay on each gallery tile in `pages/past-events.html`.

---

## 4b. Past Events — 4 July 2026 (Bharat Mandapam) photos

- **File:** `pages/past-events.html`
- **Current state:** YouTube video embedded and live. Photo gallery shows "Photo gallery coming soon."
- **Issue:** Monty's Drive folder for this event has two unlabeled raw subfolders (STILL PHOTO,
  OUTSIDE STILL PRINTER), a "Clipped Video" folder, and a 13GB raw MP4 — not a curated set.
- **What's needed:** Monty to select ~30–60 final photos (same volume as past events) and share
  just those, not the raw folders. Requested 2026-07-15.
- **How to add once received:** Run through `scripts/optimize-images.py` into
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

**Steps once approved:**
1. Get FTP credentials for eksoach.in from Monty/hosting provider
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

## 7. Payment confirmation

- **Current state:** Advance payment verbal only (mentioned on discovery call with Monty).
- **What's needed:** Written confirmation via WhatsApp or invoice sent to Monty before proceeding with remaining work.

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
