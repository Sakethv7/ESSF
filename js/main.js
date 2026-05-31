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

    function resetTimer() { clearInterval(timer); timer = setInterval(() => goTo(current + 1), 5000); }
    resetTimer();
  }
}
