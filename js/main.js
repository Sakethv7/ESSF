// ===== NAV HAMBURGER =====
const toggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
if (toggle && navLinks) {
  toggle.addEventListener('click', () => navLinks.classList.toggle('open'));
}

// mark active nav link — compare by pathname to avoid query-string mismatches
document.querySelectorAll('.nav-links a').forEach(a => {
  try {
    if (new URL(a.href).pathname === location.pathname) a.classList.add('active');
  } catch (_) {}
});

// ===== HERO SLIDER =====
const heroEl = document.querySelector('.hero');
if (heroEl) {
  const slides = heroEl.querySelector('.hero-slides');
  const allSlides = heroEl.querySelectorAll('.hero-slide');
  const dotsContainer = heroEl.querySelector('.slider-dots');
  let current = 0;
  let timer;

  if (allSlides.length > 1) {
    allSlides.forEach((_, i) => {
      const dot = document.createElement('span');
      dot.setAttribute('role', 'button');
      dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
      if (i === 0) dot.classList.add('active');
      dot.addEventListener('click', () => goTo(i));
      dotsContainer.appendChild(dot);
    });

    function goTo(n) {
      current = (n + allSlides.length) % allSlides.length;
      slides.style.transform = `translateX(-${current * 100}%)`;
      dotsContainer.querySelectorAll('span').forEach((d, i) => {
        d.classList.toggle('active', i === current);
        d.setAttribute('aria-label', `Go to slide ${i + 1}${i === current ? ' (current)' : ''}`);
      });
    }

    heroEl.querySelector('.prev').addEventListener('click', () => { goTo(current - 1); resetTimer(); });
    heroEl.querySelector('.next').addEventListener('click', () => { goTo(current + 1); resetTimer(); });

    // touch swipe (mobile)
    let touchStartX = 0;
    heroEl.addEventListener('touchstart', e => {
      touchStartX = e.touches[0].clientX;
    }, { passive: true });
    heroEl.addEventListener('touchend', e => {
      const dx = e.changedTouches[0].clientX - touchStartX;
      if (Math.abs(dx) > 40) { goTo(dx < 0 ? current + 1 : current - 1); resetTimer(); }
    }, { passive: true });

    // mouse drag (desktop click-and-drag)
    let mouseStartX = 0, dragging = false;
    heroEl.addEventListener('mousedown', e => { mouseStartX = e.clientX; dragging = true; });
    document.addEventListener('mouseup', e => {
      if (!dragging) return;
      dragging = false;
      const dx = e.clientX - mouseStartX;
      if (Math.abs(dx) > 40) { goTo(dx < 0 ? current + 1 : current - 1); resetTimer(); }
    });

    // trackpad two-finger horizontal swipe (macOS)
    let wheeling = false;
    heroEl.addEventListener('wheel', e => {
      if (Math.abs(e.deltaX) < Math.abs(e.deltaY)) return; // ignore vertical scroll
      e.preventDefault();
      if (wheeling) return;
      wheeling = true;
      goTo(e.deltaX > 0 ? current + 1 : current - 1);
      resetTimer();
      setTimeout(() => { wheeling = false; }, 800); // block until transition finishes
    }, { passive: false });

    function resetTimer() { clearInterval(timer); timer = setInterval(() => goTo(current + 1), 5000); }
    resetTimer();
  }
}

// ===== GALLERY COLLAPSE =====
// Show first 8 photos per event group; rest hidden behind "Show all" button
document.querySelectorAll('.event-group .gallery-grid').forEach(grid => {
  const items = grid.querySelectorAll('.gallery-item');
  if (items.length <= 8) return;

  items.forEach((item, i) => {
    if (i >= 8) item.classList.add('gallery-hidden');
  });

  const btn = document.createElement('button');
  btn.className = 'gallery-show-more';
  btn.textContent = `Show all ${items.length} photos`;
  btn.setAttribute('aria-label', `Show all ${items.length} photos in this event`);
  btn.addEventListener('click', () => {
    grid.querySelectorAll('.gallery-hidden').forEach(el => el.classList.remove('gallery-hidden'));
    btn.remove();
  });
  grid.after(btn);
});

// ===== GALLERY LIGHTBOX =====
const galleryLinks = Array.from(document.querySelectorAll('.gallery-item a[href]'));
if (galleryLinks.length) {
  const lightbox = document.createElement('div');
  lightbox.className = 'lightbox';
  lightbox.setAttribute('role', 'dialog');
  lightbox.setAttribute('aria-modal', 'true');
  lightbox.setAttribute('aria-label', 'Full-size photo viewer');
  lightbox.innerHTML = `
    <button class="lightbox-button lightbox-close" type="button" aria-label="Close full-size photo">&times;</button>
    <button class="lightbox-button lightbox-prev" type="button" aria-label="Previous photo">&#8249;</button>
    <img alt="" />
    <button class="lightbox-button lightbox-next" type="button" aria-label="Next photo">&#8250;</button>
    <p class="lightbox-caption"></p>
  `;
  document.body.appendChild(lightbox);

  const lightboxImg = lightbox.querySelector('img');
  const caption = lightbox.querySelector('.lightbox-caption');
  const closeBtn = lightbox.querySelector('.lightbox-close');
  const prevBtn = lightbox.querySelector('.lightbox-prev');
  const nextBtn = lightbox.querySelector('.lightbox-next');
  let activeIndex = 0;

  function showPhoto(index) {
    activeIndex = (index + galleryLinks.length) % galleryLinks.length;
    const link = galleryLinks[activeIndex];
    const img = link.querySelector('img');
    lightboxImg.src = link.href;
    lightboxImg.alt = img ? img.alt : 'Full-size gallery photo';
    caption.textContent = img && img.alt ? img.alt : '';
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
    closeBtn.focus();
  }

  function closeLightbox() {
    lightbox.classList.remove('open');
    lightboxImg.removeAttribute('src');
    document.body.style.overflow = '';
  }

  galleryLinks.forEach((link, index) => {
    link.addEventListener('click', event => {
      event.preventDefault();
      showPhoto(index);
    });

    const item = link.closest('.gallery-item');
    if (item) {
      item.addEventListener('click', event => {
        if (event.target.closest('a')) return;
        showPhoto(index);
      });
    }
  });

  closeBtn.addEventListener('click', closeLightbox);
  prevBtn.addEventListener('click', () => showPhoto(activeIndex - 1));
  nextBtn.addEventListener('click', () => showPhoto(activeIndex + 1));
  lightbox.addEventListener('click', event => {
    if (event.target === lightbox) closeLightbox();
  });

  document.addEventListener('keydown', event => {
    if (!lightbox.classList.contains('open')) return;
    if (event.key === 'Escape') closeLightbox();
    if (event.key === 'ArrowLeft') showPhoto(activeIndex - 1);
    if (event.key === 'ArrowRight') showPhoto(activeIndex + 1);
  });
}
