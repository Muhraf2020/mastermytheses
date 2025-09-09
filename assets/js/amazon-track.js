document.addEventListener('click', function (e) {
  var a = e.target.closest('a[href*="amazon.com/dp/"]');
  if (!a) return;
  if (!window.gtag) return;
  gtag('event', 'amazon_click', {
    link_url: a.href,
    link_text: (a.textContent || '').trim(),
    page_location: location.href
  });
});
