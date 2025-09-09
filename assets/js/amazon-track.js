document.addEventListener('click', function (e) {
  // Match any Amazon marketplace with /dp/ASIN pattern
  var a = e.target.closest('a[href*="amazon."][href*="/dp/"]');
  if (!a) return;
  if (!window.gtag) return;

  // Extract ASIN from the URL
  var asin = (a.href.match(/\/dp\/([A-Z0-9]{10})/) || [])[1] || '';

  // Extract marketplace (e.g., amazon.com, amazon.co.uk)
  var market = (a.hostname || '').replace(/^www\./, '');

  gtag('event', 'amazon_click', {
    asin: asin,
    marketplace: market, // custom param
    link_url: a.href,
    link_text: (a.textContent || '').trim(),
    page_location: location.href
  });
});
