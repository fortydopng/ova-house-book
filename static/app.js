(function () {
  var lb = document.getElementById('lb');
  if (!lb) return;
  var strip = lb.querySelector('.lb__strip');
  var slides = strip.children;
  var count = lb.querySelector('.lb__count span');
  var closeBtn = lb.querySelector('.lb__close');
  var links = document.querySelectorAll('.gallery__link');
  var lastFocus = null;

  function slideWidth() { return strip.clientWidth; }

  function goTo(i, instant) {
    var x = i * slideWidth();
    if (instant) {
      var prev = strip.style.scrollBehavior;
      strip.style.scrollBehavior = 'auto';
      strip.scrollLeft = x;
      strip.style.scrollBehavior = prev;
    } else {
      strip.scrollTo({ left: x });
    }
    count.textContent = i + 1;
  }

  function current() { return Math.round(strip.scrollLeft / slideWidth()); }

  function open(i) {
    lastFocus = document.activeElement;
    lb.hidden = false;
    document.body.classList.add('lb-open');
    goTo(i, true);
    closeBtn.focus();
  }

  function close() {
    lb.hidden = true;
    document.body.classList.remove('lb-open');
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  Array.prototype.forEach.call(links, function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      open(parseInt(a.getAttribute('data-index'), 10) || 0);
    });
  });

  closeBtn.addEventListener('click', close);

  strip.addEventListener('scroll', function () {
    count.textContent = current() + 1;
  }, { passive: true });

  document.addEventListener('keydown', function (e) {
    if (lb.hidden) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowRight') goTo(Math.min(current() + 1, slides.length - 1));
    else if (e.key === 'ArrowLeft') goTo(Math.max(current() - 1, 0));
  });

  window.addEventListener('resize', function () {
    if (!lb.hidden) goTo(current(), true);
  });
})();
