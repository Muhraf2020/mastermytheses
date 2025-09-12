// Only one <details> open per .faq section
document.addEventListener(
  'toggle',
  (e) => {
    const details = e.target;
    if (details.tagName !== 'DETAILS') return;     // ignore other toggles
    if (!details.open) return;                     // only when one just opened
    const container = details.closest('.faq');
    if (!container) return;

    container.querySelectorAll('details[open]').forEach((d) => {
      if (d !== details) d.open = false;          // close siblings
    });
  },
  true // use capture so it works reliably across browsers
);
