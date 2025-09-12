// Only one <details> open per .faq section (robust: works on all pages)
(function () {
  function closeSiblings(currentDetails) {
    const container = currentDetails.closest('.faq');
    if (!container) return;
    container.querySelectorAll('details[open]').forEach((d) => {
      if (d !== currentDetails) d.open = false;
    });
  }

  // Preferred: fires after the open/close state changes
  document.addEventListener(
    'toggle',
    (e) => {
      const el = e.target;
      if (el && el.tagName === 'DETAILS' && el.open) closeSiblings(el);
    },
    true // capture for consistent behavior
  );

  // Fallback for odd browsers/edge cases: run after click toggles state
  document.addEventListener(
    'click',
    (e) => {
      const summary = e.target.closest && e.target.closest('summary');
      if (!summary) return;
      const details = summary.parentElement;
      // wait a tick for the native toggle to apply
      setTimeout(() => {
        if (details.open) closeSiblings(details);
      }, 0);
    },
    true
  );
})();
