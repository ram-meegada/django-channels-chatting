// push-notifications.js
const publicVapidKey = 'BMS4B9X2tzeZujdzr76ed26qeuJLkH5d7BEiRCP3RZRMtJLQDeD0AFrtiaJWASyuKTziRz4QJHcugLSbOW1tEx8';

if ('Notification' in window) {
  navigator.serviceWorker.ready.then(function (serviceWorkerRegistration) {
    serviceWorkerRegistration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(publicVapidKey),
    })
    .then(function (subscription) {
      // Handle subscription
    })
    .catch(function (error) {
      console.error('Error subscribing to push notifications:', error);
    });
  });
}

// Helper function to convert VAPID public key to Uint8Array
function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }

  return outputArray;
}
