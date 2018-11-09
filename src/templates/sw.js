var staticCacheName = 'achieng-cache-v4'; //name of our cache

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(staticCacheName).then(function(cache) {
            return cache.addAll([
                '/',
                '/static/css/styles.css',
                '/static/images/favicon.ico',
                '/static/js/main.js',
                'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
                'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/highlight.min.js',
                'https://code.jquery.com/jquery-3.2.1.slim.min.js',
                'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
            ]);
        })
    );
});


/* Deleting old cache */
self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.filter(function(cacheName) {
                    return cacheName.startsWith('achieng-') && //do not delete caches from other appthat miggt be running on the same origin
                        cacheName != staticCacheName;
                }).map(function(cacheName) {
                    return caches.delete(cacheName);
                })
            );
        })

    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
      caches.match(event.request).then(function(response) {
        if(response){
          return response;
        }
        return fetch(event.request);
      })
    );
  });

//
self.addEventListener('message', function(event) {
  if (event.data.action === 'skipWaiting') {
    self.skipWaiting();
  }
});

/* self.addEventListener('fetch', function(event) {
    event.respondWith(
      caches.open(cacheName).then(function(cache) {
        return cache.match(event.request).then(function(response) {
          var fetchPromise = fetch(event.request).then(function(networkResponse) {
            cache.put(event.request, networkResponse.clone());
            return networkResponse;
          })
          return response || fetchPromise;
        })
      })
    );
  }); */


  
  