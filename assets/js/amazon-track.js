<script>
// /assets/js/amazon-track.js
document.addEventListener('click', function (e) {
  var a = e.target.closest('a[href]');
  if (!a) return;

  var href = a.getAttribute('href');
  // Match amazon.* and both /dp/ and /gp/product/ patterns
  var isAmazonProduct = /https?:\/\/(www\.)?amazon\.[a-z.]+\/(dp|gp\/product)\//i.test(href);
  if (!isAmazonProduct) return;

  if (typeof gtag !== 'function') return;
  gtag('event', 'amazon_click', {
    link_url: href,
    link_text: (a.textContent || '').trim(),
    page_location: location.href
  });
});
</script>
