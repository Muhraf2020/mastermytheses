// FAQ true-accordion (only one <details> open per .faq section)
document.addEventListener('click', (e) => {
  const summary = e.target.closest('summary');
  if (!summary) return;

  const container = summary.closest('.faq');
  const current = summary.parentElement; // the <details>

  // Only act when opening (not when closing)
  if (!container || !current.open) return;

  container.querySelectorAll('details[open]').forEach(d => {
    if (d !== current) d.removeAttribute('open');
  });
});
