// Footer year
document.getElementById("year").textContent = new Date().getFullYear();

// ── Reading progress bar ──────────────────────────────
const progress = document.getElementById("progress");
function updateProgress() {
  const h = document.documentElement;
  const scrolled = h.scrollTop;
  const height = h.scrollHeight - h.clientHeight;
  progress.style.width = (height > 0 ? (scrolled / height) * 100 : 0) + "%";
}
window.addEventListener("scroll", updateProgress, { passive: true });
updateProgress();

// ── Section nav highlighting ──────────────────────────
const navLinks = Array.from(document.querySelectorAll(".section-nav a"));
const sections = navLinks
  .map((a) => document.querySelector(a.getAttribute("href")))
  .filter(Boolean);

if ("IntersectionObserver" in window && sections.length) {
  const navObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          navLinks.forEach((a) =>
            a.classList.toggle("active", a.getAttribute("href") === "#" + id)
          );
        }
      });
    },
    { rootMargin: "-45% 0px -50% 0px" }
  );
  sections.forEach((s) => navObserver.observe(s));
}

// ── Animated stat counters ────────────────────────────
function formatNumber(n) {
  return Math.round(n).toLocaleString("en-US");
}
function animateStat(el) {
  const target = Number(el.dataset.target);
  const prefix = el.dataset.prefix || "";
  const suffix = el.dataset.suffix || "";
  const duration = 1400;
  const start = performance.now();

  function tick(now) {
    const t = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - t, 3); // ease-out cubic
    el.textContent = prefix + formatNumber(target * eased) + suffix;
    if (t < 1) requestAnimationFrame(tick);
    else el.textContent = prefix + formatNumber(target) + suffix;
  }
  requestAnimationFrame(tick);
}

const statEls = document.querySelectorAll(".stat-value");
if ("IntersectionObserver" in window) {
  const statObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateStat(entry.target);
          statObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 }
  );
  statEls.forEach((el) => statObserver.observe(el));
} else {
  statEls.forEach((el) => animateStat(el));
}

// ── Load chart: draw-in + traveling pulse ─────────────
(function initLoadChart() {
  const chart = document.querySelector(".loadchart");
  if (!chart) return;

  const lines = chart.querySelectorAll(".lc-line");
  const spiky = chart.querySelector(".lc-spiky");
  const dot = chart.querySelector(".lc-pulse");
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Prime each line as a fully "undrawn" dash.
  lines.forEach((p) => {
    const len = p.getTotalLength();
    p.style.strokeDasharray = len;
    p.style.strokeDashoffset = reduce ? 0 : len;
  });

  function startPulse() {
    if (!spiky || !dot) return;
    const len = spiky.getTotalLength();
    const duration = 3400;
    let startT = null;
    function frame(now) {
      if (startT === null) startT = now;
      const progress = ((now - startT) % duration) / duration;
      const pt = spiky.getPointAtLength(progress * len);
      dot.setAttribute("cx", pt.x.toFixed(1));
      dot.setAttribute("cy", pt.y.toFixed(1));
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  if (reduce || !("IntersectionObserver" in window)) {
    chart.classList.add("in-view");
    return;
  }

  const obs = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          chart.classList.add("in-view");
          setTimeout(startPulse, 1800); // begin after the lines finish drawing
          obs.disconnect();
        }
      });
    },
    { threshold: 0.35 }
  );
  obs.observe(chart);
})();

// ── Stakeholder guide tabs ────────────────────────────
const tabs = Array.from(document.querySelectorAll(".tab"));
const panels = Array.from(document.querySelectorAll(".panel"));

function activateTab(key) {
  tabs.forEach((t) => {
    const on = t.dataset.tab === key;
    t.classList.toggle("is-active", on);
    t.setAttribute("aria-selected", on ? "true" : "false");
  });
  panels.forEach((p) => {
    const on = p.dataset.panel === key;
    p.classList.toggle("is-active", on);
    p.hidden = !on;
  });
}

tabs.forEach((tab) => {
  tab.addEventListener("click", () => activateTab(tab.dataset.tab));
});

// Deep-link from the action page: ?guide=<key> opens that guide and scrolls to it
const guideParam = new URLSearchParams(window.location.search).get("guide");
if (guideParam && tabs.some((t) => t.dataset.tab === guideParam)) {
  activateTab(guideParam);
  const guidesSection = document.getElementById("guides");
  if (guidesSection) {
    requestAnimationFrame(() =>
      guidesSection.scrollIntoView({ behavior: "smooth", block: "start" })
    );
  }
}

// Keyboard navigation for the tablist
const tablist = document.querySelector(".tabs");
if (tablist) {
  tablist.addEventListener("keydown", (e) => {
    if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
    const i = tabs.findIndex((t) => t.classList.contains("is-active"));
    const next =
      e.key === "ArrowRight"
        ? (i + 1) % tabs.length
        : (i - 1 + tabs.length) % tabs.length;
    activateTab(tabs[next].dataset.tab);
    tabs[next].focus();
  });
}
