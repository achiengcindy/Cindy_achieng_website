    /*
     * Open the drawer when the menu ison is clicked.
     */
    var menu = document.querySelector('#menu');
    var main = document.querySelector('main');
    var drawer = document.querySelector('.nav__wrapper');

    menu.addEventListener('click', function(e) {
      drawer.classList.toggle('open');
      e.stopPropagation();
    });
    main.addEventListener('click', function() {
      drawer.classList.remove('open');
    });


    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js', {
              scope: '/'
          })
          .then(function(reg) {
              if (!navigator.serviceWorker.controller) {
                  return;
              }
              // there is updated service worker ready and waiting to to take over
              if (reg.waiting) {
                  updateReady(reg.waiting)
                  return;
              }
              // there is update on the way. Although may be  be thrown away if installation fails we will listen to the stat
  
              if (reg.installing) {
                  trackInstalling(reg.installing)
                  return;
              }
  
              reg.addEventListener('updatefound', function() {
                  trackInstalling(reg.installing)
              });
          });
  }

 



// if ('serviceWorker' in navigator) {
//   navigator.serviceWorker.register('/sw.js' , {scope: '/'})
//   .then(function (reg) {
//     if (!navigator.serviceWorker.controller) {
//       return;
//     }
// // there is updated service worker ready and waiting to to take over
//     if (reg.waiting) {
//       updateReady(reg.waiting)
//       return;
//     }
// // there is update on the way. Although may be  be thrown away if installation fails we will listen to the stat

//     if (reg.installing) {
//       trackInstalling(reg.installing)
//       return;
//     }

//     reg.addEventListener('updatefound', function () {
//       trackInstalling(reg.installing)
//     });
//   });


//   // Ensure refresh is only called once.
//   // This works around a bug in "force update on reload".
//   var refreshing;
//   navigator.serviceWorker.addEventListener('controllerchange', function() {
//     if (refreshing) return;
//     window.location.reload();
//     refreshing = true;
//   });
// };

// var notification = document.getElementById('notification')
// function updateReady (worker) {
// notification.onclick = function(){
//   notification.onclick = null;
//     alert('Accept')
//     alert('Deny')
//   };

//  // The click event on the notification

// }

// // IndexController.prototype._updateReady = function(worker) {
// //   var toast = this._toastsView.show("New version available", {
// //     buttons: ['refresh', 'dismiss']
// //   });

// //   toast.answer.then(function(answer) {
// //     if (answer != 'refresh') return;
// //     worker.postMessage({action: 'skipWaiting'});
// //   });
// // };


// function trackInstalling (worker) {
//   worker.addEventListener('statechange', function () {
//     if (worker.state == 'installed') {
//       updateReady(worker)
//     }
//   });
// };


$(document).ready(function(){

  $('.comment-reply-link').click(function(){
            $(this).parent().next().find('form').fadeToggle();
    });

});

