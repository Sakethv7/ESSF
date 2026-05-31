// ===== NAV HAMBURGER =====
const toggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
if (toggle && navLinks) {
  toggle.addEventListener('click', () => navLinks.classList.toggle('open'));
}

// mark active nav link
document.querySelectorAll('.nav-links a').forEach(a => {
  if (a.href === location.href) a.classList.add('active');
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
      if (i === 0) dot.classList.add('active');
      dot.addEventListener('click', () => goTo(i));
      dotsContainer.appendChild(dot);
    });

    function goTo(n) {
      current = (n + allSlides.length) % allSlides.length;
      slides.style.transform = `translateX(-${current * 100}%)`;
      dotsContainer.querySelectorAll('span').forEach((d, i) =>
        d.classList.toggle('active', i === current));
    }

    heroEl.querySelector('.prev').addEventListener('click', () => { goTo(current - 1); resetTimer(); });
    heroEl.querySelector('.next').addEventListener('click', () => { goTo(current + 1); resetTimer(); });

    // touch swipe support
    let touchStartX = 0;
    heroEl.addEventListener('touchstart', e => {
      touchStartX = e.touches[0].clientX;
    }, { passive: true });
    heroEl.addEventListener('touchend', e => {
      const dx = e.changedTouches[0].clientX - touchStartX;
      if (Math.abs(dx) > 40) {
        goTo(dx < 0 ? current + 1 : current - 1);
        resetTimer();
      }
    }, { passive: true });

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
  btn.addEventListener('click', () => {
    grid.querySelectorAll('.gallery-hidden').forEach(el => el.classList.remove('gallery-hidden'));
    btn.remove();
  });
  grid.after(btn);
});
