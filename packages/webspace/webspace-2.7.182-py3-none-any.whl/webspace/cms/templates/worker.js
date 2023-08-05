const cacheName = 'cache-v{{ version }}';
const precacheResources = [
    {% for page in pages.items %}
    '{{ page.get_url }}',
    {% endfor %}
];

self.addEventListener('install', (event) => {
  console.log('install')
    event.waitUntil(
    caches.open(cacheName)
      .then(cache => cache.addAll(precacheResources)),
  );
});

self.addEventListener('fetch', (event) => {
  console.log('fetch')

    event.respondWith(caches.match(event.request)
    .then((cachedResponse) => {
        if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request);
    }));
});


self.addEventListener('activate', function(event) {
    console.log('activate')

    event.waitUntil(
    caches.keys().then(function(keyList) {
      return Promise.all(keyList.map(function(key) {
        return caches.delete(key);
      }));
    })
  );
});