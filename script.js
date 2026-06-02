// Current year in footer
document.getElementById("year").textContent = new Date().getFullYear();

// Animated stat counters, triggered when they scroll into view
function formatValue(el, value) {
  if (el.dataset.format === "uptime") {
    // 99999 -> "99.999"
    return (value / 1000).toFixed(3);
  }
  return Math.round(value).toString();
}

function animateStat(el) {
  const target = Number(el.dataset.target);
  const duration = 1400;
  const start = performance.now();

  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    // ease-out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = formatValue(el, target * eased);
    if (progress < 1) requestAnimationFrame(tick);
    else el.textContent = formatValue(el, target);
  }
  requestAnimationFrame(tick);
}

const statEls = document.querySelectorAll(".stat-value");
if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          animateStat(entry.target);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.4 }
  );
  statEls.forEach((el) => observer.observe(el));
} else {
  statEls.forEach((el) => animateStat(el));
}

// Contact form (demo — no backend)
function handleContact(event) {
  event.preventDefault();
  const form = event.target;
  const status = document.getElementById("formStatus");
  const name = form.name.value.trim();
  status.textContent = `Thanks${name ? ", " + name : ""}! We'll be in touch shortly.`;
  form.reset();
  return false;
}
