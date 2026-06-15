// Learn PWA service worker — offline shell + OTA content
const CACHE = "learn-v4";
const SHELL = ["./", "index.html", "manifest.webmanifest", "content.json", "cpd-content.json", "icon-192.png", "icon-512.png", "icon-180.png"];

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
  // content.json / cpd-content.json -> network first (OTA), fall back to cache
  if (url.pathname.endsWith("content.json") || url.pathname.endsWith("cpd-content.json")) {
    const key = url.pathname.endsWith("cpd-content.json") ? "cpd-content.json" : "content.json";
    e.respondWith(
      fetch(e.request).then(r => {
        const copy = r.clone();
        caches.open(CACHE).then(c => c.put(key, copy));
        return r;
      }).catch(() => caches.match(key))
    );
    return;
  }
  // shell -> cache first, fall back to network
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
});
