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
| `pages/past-events.html` | Event gallery — 221 photos across 3 dated events |
| `pages/social-activity.html` | Social initiatives — highlights + 8 photos |
| `pages/contact.html` | Address, email, Google Maps link |

---

## Tech stack

Pure HTML + CSS + vanilla JS. No frameworks, no build tools. Designed to load on 2G connections and basic Android browsers.

- Images compressed to ≤500px thumbnails (~25KB each) using Pillow
- All photos lazy-loaded (`loading="lazy"`)
- Total image assets: ~6MB for 236 thumbnails

---

## Project structure

```
essf-website/
├── index.html
├── pages/
│   ├── executives.html
│   ├── past-events.html
│   ├── social-activity.html
│   └── contact.html
├── assets/
│   ├── images/
│   │   ├── home/          (7 photos — hero banners + event shots)
│   │   ├── events/
│   │   │   ├── 06-07-2024/   (67 photos — Symposium: Save Environment & Kavi Sammelan)
│   │   │   ├── 07-04-2024/   (14 photos — Annual Felicitation Ceremony)
│   │   │   └── 09-07-2023/   (140 photos — Kavi Sammelan with Musical Program)
│   │   └── social/        (8 photos — donations, clay bottles, covid relief)
│   └── logos/
│       ├── logo.png       (circular emblem, 93×93, used in nav + favicon)
│       └── fav5.png       (horizontal banner logo, 400×76)
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
