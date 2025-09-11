// /assets/js/amazon-track.js
(function () {
  function handleClick(ev) {
    const a = ev.target && ev.target.closest && ev.target.closest('a[href]');
    if (!a) return;

    const href = a.getAttribute('href') || '';
    // dp / gp/product product pages only
    const isAmazonProduct = /^https?:\/\/(www\.)?amazon\.[a-z.]+\/(dp|gp\/product)\//i.test(href);
    if (!isAmazonProduct) return;

    // GA4 event (realtime -> Events)
    if (typeof gtag === 'function') {
      gtag('event', 'amazon_click', {
        link_url: href,
        link_text: (a.textContent || '').trim(),
        page_location: location.href,
        transport_type: 'beacon'   // send reliably on navigation
      });
    }
  }

  // Left/primary click
  document.addEventListener('click', handleClick, true);
  // Middle-click (open in new tab)
  document.addEventListener('auxclick', function (e) {
    if (e.button === 1) handleClick(e);
  }, true);
})();
