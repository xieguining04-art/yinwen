(function () {
  "use strict";

  function forceEnglish() {
    try {
      window.localStorage.removeItem("tengyoda.language");
    } catch (_) {}
    document.documentElement.lang = "en";
  }

  function unlockPage() {
    document.documentElement.style.removeProperty("overflow");
    document.documentElement.style.removeProperty("pointer-events");
    document.documentElement.removeAttribute("data-scroll-locked");
    if (!document.body) return;
    document.body.style.removeProperty("overflow");
    document.body.style.removeProperty("pointer-events");
    document.body.style.removeProperty("padding-right");
    document.body.removeAttribute("data-scroll-locked");
  }

  forceEnglish();

  function ready() {
    forceEnglish();
    unlockPage();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ready, { once: true });
  } else {
    ready();
  }

  window.addEventListener("pageshow", ready);
  window.addEventListener("hashchange", function () {
    window.setTimeout(unlockPage, 0);
  });
  document.addEventListener("click", function (event) {
    var link = event.target.closest("a[href]");
    if (!link) return;
    var url = new URL(link.href, window.location.href);
    if (url.origin === window.location.origin && url.hash) {
      window.setTimeout(unlockPage, 0);
      window.setTimeout(unlockPage, 150);
    }
  });
})();
