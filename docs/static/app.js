(function () {
  // Day / evening toggles on paired figures
  var pairs = document.querySelectorAll('.pair');
  Array.prototype.forEach.call(pairs, function (fig) {
    var btns = fig.querySelectorAll('.light__btn');
    Array.prototype.forEach.call(btns, function (btn) {
      btn.addEventListener('click', function () {
        var light = btn.getAttribute('data-light');
        fig.setAttribute('data-light', light);
        Array.prototype.forEach.call(btns, function (b) {
          var on = b === btn;
          b.classList.toggle('is-on', on);
          b.setAttribute('aria-pressed', on ? 'true' : 'false');
        });
        var day = fig.querySelector('.pair__day'), ev = fig.querySelector('.pair__evening');
        var show = light === 'evening' ? ev : day, hide = light === 'evening' ? day : ev;
        show.removeAttribute('aria-hidden'); show.removeAttribute('tabindex');
        hide.setAttribute('aria-hidden', 'true'); hide.setAttribute('tabindex', '-1');
      });
    });
  });

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
    openedAt = i;
    goTo(i, true);
    closeBtn.focus();
  }

  var openedAt = 0;

  function close() {
    var i = current();
    lb.hidden = true;
    document.body.classList.remove('lb-open');
    // if the viewer moved to another image, bring the page to that image
    var target = slides[i] && slides[i].getAttribute('data-anchor');
    if (i !== openedAt && target && document.getElementById(target)) {
      document.getElementById(target).scrollIntoView({ block: 'start' });
    } else if (lastFocus && lastFocus.focus) {
      lastFocus.focus();
    }
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

(function () {
  // References page: highlight the section in view in the sticky group nav
  var nav = document.querySelector('.refnav');
  if (!nav || !('IntersectionObserver' in window)) return;
  var links = {};
  Array.prototype.forEach.call(nav.querySelectorAll('a[data-group]'), function (a) {
    links[a.getAttribute('data-group')] = a;
  });
  var visible = {};
  function update() {
    var best = null, bestTop = Infinity;
    for (var id in visible) {
      if (visible[id] && visible[id] < bestTop) { best = id; bestTop = visible[id]; }
    }
    if (!best) return;
    for (var k in links) {
      var on = k === best;
      links[k].classList.toggle('is-on', on);
      if (on) links[k].setAttribute('aria-current', 'true'); else links[k].removeAttribute('aria-current');
    }
    var a = links[best], ul = a.parentNode.parentNode;
    var left = a.offsetLeft - (ul.clientWidth - a.offsetWidth) / 2;
    ul.scrollTo({ left: left, behavior: 'smooth' });
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var id = e.target.getAttribute('data-group');
      visible[id] = e.isIntersecting ? Math.abs(e.boundingClientRect.top) + 1 : 0;
    });
    update();
  }, { rootMargin: '-56px 0px -55% 0px', threshold: 0 });
  Array.prototype.forEach.call(document.querySelectorAll('.refs__group'), function (sec) { io.observe(sec); });
})();
