# Ek Soach Saathiya Foundation — Website

**Live preview:** https://sakethv7.github.io/ESSF/
**Production domain:** eksoach.in

A Foundation of CGST & Customs Officers (Retired & Serving), Delhi. Incorporated 18 September 2020.

---

## Pages

| Page | Description |
|------|-------------|
| `index.html` | Home — hero slider, What We Do, Activities, Gallery, Contact strip |
| `pages/executives.html` | Executive team — photo cards with name and title |
| `pages/past-events.html` | Event gallery — curated sets across 4 dated events |
| `pages/gallery-bharat-mandapam.html` | Full 222-photo gallery for the 4 July 2026 event |
| `pages/social-activity.html` | Social initiatives — highlights + 8 photos |
| `pages/contact.html` | Address, email, Google Maps link |

---

## Tech stack

Pure HTML + CSS + vanilla JS. No frameworks, no build tools. Designed to load on 2G connections and basic Android browsers.

- Images compressed with Pillow via `scripts/optimize-images.py`
- Galleries on `past-events.html` use one 1600px tier (~225KB each)
- The 222-photo gallery uses two tiers: 500px thumbnails (~31KB) in the grid, 1600px in the lightbox
- All photos lazy-loaded (`loading="lazy"`), so page cost is proportional to how far you scroll
- Total image assets: ~67MB, of which the 4 July 2026 event is ~59MB

---

## Project structure

```
essf-website/
├── index.html
├── pages/
│   ├── executives.html
│   ├── past-events.html
│   ├── gallery-bharat-mandapam.html
│   ├── social-activity.html
│   └── contact.html
├── assets/
│   ├── images/
│   │   ├── home/          (7 photos — hero banners + event shots)
│   │   ├── events/
│   │   │   ├── 04-07-2026/   (222 photos + thumbs/ — ESSF Samman Scholarship & Cultural Fest, Bharat Mandapam)
│   │   │   ├── 06-07-2024/   (67 photos on disk, 8 shown on site — Symposium: Save Environment & Kavi Sammelan)
│   │   │   ├── 07-04-2024/   (14 photos on disk, 8 shown on site — Vaisakhi Celebration & Felicitation Ceremony)
│   │   │   └── 09-07-2023/   (140 photos on disk, 8 shown on site — Kavi Sammelan with Musical Program)
│   │   └── social/        (8 photos — donations, clay bottles, covid relief)
│   └── logos/
│       ├── ek1logo.png    (horizontal banner — circular seal + org name + tagline, used in nav on all pages)
│       ├── logo.png       (circular emblem — used as favicon + nav watermark at 9% opacity)
│       └── fav5.png       (alternative favicon)
├── css/
│   └── style.css
└── js/
    └── main.js            (hero slider + hamburger nav)
```

---

## Adding photos

### Gallery tile pattern
```html
<div class="gallery-item">
  <a href="assets/images/section/photo.jpg" target="_blank" rel="noopener">
    <img src="assets/images/section/photo.jpg" alt="Description" loading="lazy" />
  </a>
  <div class="overlay">View Full</div>
</div>
```

### Adding a hero slide
```html
<div class="hero-slide">
  <img src="assets/images/home/photo.jpg" alt="Description" />
  <div class="caption">
    <h1>Slide Title</h1>
    <p>Subtitle text</p>
  </div>
</div>
```

### Adding an executive
```html
<div class="exec-card">
  <img class="exec-photo" src="assets/images/executives/name.jpg" alt="Full Name" />
  <div class="exec-info">
    <div class="title">Director</div>
    <h3>Full Name</h3>
    <p class="bio">Brief bio.</p>
  </div>
</div>
```

---

## Deploying to eksoach.in

1. Connect to the hosting server via FTP/cPanel File Manager
2. Upload all files to `public_html/` (or the root web directory)
3. Confirm `index.html` is at the root

No server-side setup needed — fully static.

---

## Contact

**Address:** 189, Siddharth Enclave, New Delhi — 110014
**Email:** essfdelhi@gmail.com
