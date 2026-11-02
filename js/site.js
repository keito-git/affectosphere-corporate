/* Site behaviour: the mobile menu, the scroll reveal, and loading the moving
 * town behind the home hero. Everything here is progressive: without this
 * file the pages still read, the menu is just closed and the hero shows the
 * still frame. */
(function () {
  "use strict";

  // ── Mobile menu ──────────────────────────────────────────────────────────
  var toggle = document.querySelector("[data-nav-toggle]");
  var drawer = document.querySelector("[data-nav-drawer]");
  if (toggle && drawer) {
    toggle.addEventListener("click", function () {
      var open = drawer.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "メニューを閉じる" : "メニューを開く");
    });
  }

  // ── Reveal on scroll ─────────────────────────────────────────────────────
  var targets = document.querySelectorAll(".reveal");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reduceMotion || !("IntersectionObserver" in window)) {
    for (var i = 0; i < targets.length; i++) targets[i].classList.add("is-visible");
  } else {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );
    for (var j = 0; j < targets.length; j++) io.observe(targets[j]);
    // Anything already on screen at load should not wait for a scroll.
    window.setTimeout(function () {
      for (var k = 0; k < targets.length; k++) {
        var r = targets[k].getBoundingClientRect();
        if (r.top < window.innerHeight) targets[k].classList.add("is-visible");
      }
    }, 60);
  }

  // ── Hero scene ───────────────────────────────────────────────────────────
  // Worth ~620 KB and a WebGL loop only on wide viewports, with motion
  // allowed and WebGL available. Everywhere else the still frame stands in.
  var canvas = document.querySelector("[data-hero-town]");

  function supportsWebgl() {
    try {
      var probe = document.createElement("canvas");
      return !!(
        window.WebGLRenderingContext &&
        (probe.getContext("webgl") || probe.getContext("experimental-webgl"))
      );
    } catch (e) {
      return false;
    }
  }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var el = document.createElement("script");
      el.src = src;
      el.async = false; // three.js must be in place before the scene runs
      el.onload = function () {
        resolve();
      };
      el.onerror = function () {
        reject(new Error(src));
      };
      document.head.appendChild(el);
    });
  }

  // The corner panels carry no WebGL, so they run wherever they are present.
  if (document.querySelector('[data-hero-dash="field"]')) {
    loadScript("js/hero-dash.js").catch(function () {});
  }

  if (canvas) {
    var wideEnough = window.matchMedia("(min-width: 768px)").matches;
    if (wideEnough && !reduceMotion && supportsWebgl()) {
      loadScript("js/three.min.js")
        .then(function () {
          return loadScript("js/hero-town.js");
        })
        .catch(function () {
          // Scene unavailable (offline, blocked): the still frame remains.
        });
    }
  }
})();
