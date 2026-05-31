# ESSF Website — Open Issues

Last updated: 2026-05-31

---

## ~~1. Logos~~ — RESOLVED ✅

Both logos are in place and live:
- `assets/logos/ek1logo.png` — horizontal banner used in nav on all 5 pages
- `assets/logos/logo.png` — circular emblem used as favicon + faint nav watermark

---

## 2. Executives page — 3 placeholder cards

- **File:** `pages/executives.html`
- **Current state:** 4 cards. Card 1 filled (Sh. Jagdish Sehgal, Director). Cards 2–4 show "Name Here / Executive / Brief bio."
- **What's needed from client:**

| # | Name | Title/Designation | Short bio (1 line) | Photo |
|---|------|-------------------|--------------------|-------|
| 2 | ? | ? | ? | Drive link or file |
| 3 | ? | ? | ? | Drive link or file |
| 4 | ? | ? | ? | Drive link or file |

- **How to add photo once received:** Compress to 400×400px, save to `assets/images/executives/name.jpg`, replace `<div class="exec-photo-placeholder">👤</div>` with `<img class="exec-photo" src="../assets/images/executives/name.jpg" alt="Name" />`

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

## 5. Contact page — phone number

- **Current state:** Address + email only.
- **Issue:** No phone number in the original content doc (`ESSF Website .docx`).
- **What's needed:** Monty provides a contact number if they want it on the site.
- **Where it goes:** `pages/contact.html` — add a new `.contact-row` for phone.

---

## 6. Deploy to eksoach.in

- **Current state:** Live on GitHub Pages at `sakethv7.github.io/ESSF/` for preview only.
- **Blocker:** Awaiting client (Monty) approval of the design.
- **Steps once approved:**
  1. Get FTP credentials for eksoach.in hosting server
  2. Upload all files from `essf-website/` to `public_html/`
  3. Exclude `.git/` and `.claude/` folders
  4. Confirm site loads at eksoach.in
- **Note:** All image paths are relative — no code changes needed for production deploy.

---

## 7. Payment confirmation

- **Current state:** Advance payment verbal only (mentioned on discovery call with Monty).
- **What's needed:** Written confirmation via WhatsApp or invoice sent to Monty before proceeding with remaining work.
