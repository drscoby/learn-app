// Learn PWA service worker — offline shell + OTA content
const CACHE = "learn-v3";
const SHELL = ["./", "index.html", "manifest.webmanifest", "content.json", "icon-192.png", "icon-512.png", "icon-180.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks =>
    Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  // content.json -> network first (OTA), fall back to cache
  if (url.pathname.endsWith("content.json")) {
    e.respondWith(
      fetch(e.request).then(r => {
        const copy = r.clone();
        caches.open(CACHE).then(c => c.put("content.json", copy));
        return r;
      }).catch(() => caches.match("content.json"))
    );
    return;
  }
  // shell -> cache first, fall back to network
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
});
