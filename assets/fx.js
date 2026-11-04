// namlabs page effects: scroll reveal, hero confetti and a gentle parallax.
// Everything here is decoration; the page reads the same without it.
(function () {
  if (!matchMedia('(prefers-reduced-motion: no-preference)').matches) return;
  var root = document.documentElement;
  root.classList.add('fx');

  // Fade cards, tiles and sections in as they scroll into view. Things already
  // on screen at load are left alone so nothing visible blinks.
  var sel = '.sec-head, .game, .tile, .step, .checks li, .shots, .cta, .pill, details.more, .guide-cta';
  var items = [].slice.call(document.querySelectorAll(sel));
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        el.classList.add('in');
        io.unobserve(el);
        // Drop the reveal styles once done so hover effects keep their own timing.
        setTimeout(function () { el.classList.remove('reveal', 'in'); }, 1500);
      });
    }, { rootMargin: '0px 0px -40px 0px' });
    // Measure everything first, then write, so the page lays out once.
    var below = items.filter(function (el) { return el.getBoundingClientRect().top >= innerHeight; });
    below.forEach(function (el) {
      // Siblings that arrive together enter one after another.
      var i = [].indexOf.call(el.parentNode.children, el);
      el.style.setProperty('--d', (i % 4) * 90 + 'ms');
      el.classList.add('reveal');
      io.observe(el);
    });
  }

  // Floating puzzle bits behind the hero.
  var hero = document.querySelector('.hero');
  if (hero) {
    var box = document.createElement('div');
    box.className = 'bits';
    box.setAttribute('aria-hidden', 'true');
    var shapes = ['sq', 'dot', 'ring', 'plus'];
    for (var n = 0, count = innerWidth < 600 ? 8 : 14; n < count; n++) {
      var b = document.createElement('i');
      b.className = shapes[n % shapes.length] + (n % 3 ? '' : ' alt');
      b.style.left = (n * 37 % 100) + '%';
      b.style.top = (n * 53 % 90) + '%';
      b.style.setProperty('--s', (10 + n * 7 % 16) + 'px');
      b.style.setProperty('--t', (9 + n * 5 % 9) + 's');
      b.style.animationDelay = (-n * 1.3) + 's';
      box.appendChild(b);
    }
    hero.insertBefore(box, hero.firstChild);
  }

  // The fanned screenshots drift a little slower than the page (capped so they
  // never reach the next section).
  var fan = document.querySelector('.fan');
  if (fan) {
    var ticking = false;
    var move = function () {
      fan.style.setProperty('--py', Math.min(scrollY, 600) * 0.05 + 'px');
      ticking = false;
    };
    move();
    addEventListener('scroll', function () {
      if (ticking || scrollY > 700) return;
      ticking = true;
      requestAnimationFrame(move);
    }, { passive: true });
  }

  // The closing band's gradient only flows while it is on screen.
  var cta = document.querySelector('.cta');
  if (cta && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      cta.classList.toggle('flowing', es[0].isIntersecting);
    }).observe(cta);
  }
})();
