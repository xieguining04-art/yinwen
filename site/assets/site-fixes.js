(function () {
  "use strict";

  function replaceTextNode(element, text) {
    if (!element) return;
    for (var i = 0; i < element.childNodes.length; i += 1) {
      if (element.childNodes[i].nodeType === Node.TEXT_NODE) {
        element.childNodes[i].nodeValue = text;
        return;
      }
    }
    element.insertBefore(document.createTextNode(text), element.firstChild);
  }

  function updateAboutSection() {
    var section = document.getElementById("about");
    if (!section) return;

    var heading = section.querySelector("h2");
    var paragraphs = section.querySelectorAll(".intro-copy > p");
    var image = section.querySelector(".intro-visual img");
    var caption = section.querySelector(".intro-visual figcaption");
    var kicker = section.querySelector(".intro-copy .kicker");
    var link = section.querySelector(".intro-copy .text-link");
    if (!heading || paragraphs.length < 2) return;

    if (image) {
      image.src = "/images/about-tengyoda-team.webp";
      image.width = 1536;
      image.height = 1024;
      image.alt = "TengYoda logistics team coordinating consolidated export cargo in a warehouse connected to a container port";
    }
    if (caption) caption.textContent = "WAREHOUSE OPERATIONS. GLOBAL FREIGHT.";
    replaceTextNode(kicker, " ABOUT TENGYODA");
    heading.textContent = "Licensed logistics expertise from China to the world.";
    paragraphs[0].textContent =
      "TengYoda Supply Chain Co., Ltd. is a China-based international freight forwarder with more than ten years of experience and NVOCC qualification. Our service team of over 100 professionals coordinates ocean, air and road freight, warehousing and tailored logistics solutions.";
    paragraphs[1].textContent =
      "Through established carrier relationships and two self-operated warehouses of more than 3,000 square metres each in Lishui and Lecong, Foshan, we support cargo consolidation, labelling, sorting and palletising. Our strongest lanes include Oceania, South America and Africa, with customs-clearance and delivery solutions available in Australia, North America and Southeast Asia.";
    replaceTextNode(link, "View our China network ");
    if (link) link.setAttribute("href", "#network");
  }

  document.addEventListener(
    "click",
    function (event) {
      var link = event.target.closest("a[href]");
      if (!link) return;
      var url = new URL(link.href, window.location.href);
      if (url.origin === window.location.origin && url.pathname === "/blog") {
        event.preventDefault();
        window.location.assign("/blog/");
      }
    },
    true
  );

  window.addEventListener("load", function () {
    updateAboutSection();
    window.setTimeout(updateAboutSection, 500);
  });
})();
