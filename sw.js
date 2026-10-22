// Keeps Puja Puzzles working offline once it has been opened.
const CACHE = 'puja-puzzles-v4';
const FILES = [
  "./",
  "index.html",
  "manifest.webmanifest",
  "icons/apple-touch-icon.png",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "icons/icon-maskable-512.png",
  "fonts/anton-latin-400-normal.woff2",
  "fonts/baloo-2-devanagari-800-normal.woff2",
  "fonts/baloo-2-latin-800-normal.woff2",
  "fonts/luckiest-guy-latin-400-normal.woff2",
  "fonts/poppins-latin-600-normal.woff2",
  "fonts/poppins-latin-700-normal.woff2",
  "fonts/poppins-latin-800-normal.woff2",
  "fonts/poppins-latin-900-normal.woff2",
  "assets/1f195.webp",
  "assets/1f30a.webp",
  "assets/1f320.webp",
  "assets/1f333.webp",
  "assets/1f340.webp",
  "assets/1f343.webp",
  "assets/1f36f.webp",
  "assets/1f375.webp",
  "assets/1f382.webp",
  "assets/1f3a8.webp",
  "assets/1f3b6.webp",
  "assets/1f3c6.webp",
  "assets/1f3f5-fe0f.webp",
  "assets/1f3fa.webp",
  "assets/1f400.webp",
  "assets/1f407.webp",
  "assets/1f40d.webp",
  "assets/1f40f.webp",
  "assets/1f417.webp",
  "assets/1f41d.webp",
  "assets/1f41f.webp",
  "assets/1f422.webp",
  "assets/1f440.webp",
  "assets/1f441-fe0f.webp",
  "assets/1f442.webp",
  "assets/1f451.webp",
  "assets/1f45e.webp",
  "assets/1f45f.webp",
  "assets/1f463.webp",
  "assets/1f468.webp",
  "assets/1f4a1.webp",
  "assets/1f4a4.webp",
  "assets/1f4cd.webp",
  "assets/1f4e2.webp",
  "assets/1f50a.webp",
  "assets/1f511.webp",
  "assets/1f514.webp",
  "assets/1f522.webp",
  "assets/1f524.webp",
  "assets/1f527.webp",
  "assets/1f5bc-fe0f.webp",
  "assets/1f620.webp",
  "assets/1f622.webp",
  "assets/1f645.webp",
  "assets/1f64f.webp",
  "assets/1f697.webp",
  "assets/1f6a7.webp",
  "assets/1f6d5.webp",
  "assets/1f914.webp",
  "assets/1f92b.webp",
  "assets/1f947.webp",
  "assets/1f948.webp",
  "assets/1f949.webp",
  "assets/1f981.webp",
  "assets/1f9e9.webp",
  "assets/1f9ea.webp",
  "assets/1fa90.webp",
  "assets/1fa94.webp",
  "assets/2601-fe0f.webp",
  "assets/274c.webp",
  "assets/2753.webp",
  "assets/2b50.webp"
];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', event => {
  event.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return;
  if (req.mode === 'navigate') {
    // Fresh page when online, saved copy when offline.
    event.respondWith(fetch(req).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put('index.html', copy));
      return res;
    }).catch(() => caches.match('index.html')));
    return;
  }
  event.respondWith(caches.match(req, {ignoreSearch: true}).then(hit => hit || fetch(req)));
});
