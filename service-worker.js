self.addEventListener("install", (event) => {
    console.log("Service Worker installé.");
    event.waitUntil(
        caches.open("v1").then((cache) => {
            return cache.addAll([
                "/",
                "app.py",
                "service-worker.js",
                "favicon.ico"
            ]);
        })
    );
});

self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
