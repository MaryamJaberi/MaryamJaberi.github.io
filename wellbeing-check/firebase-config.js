/* Firebase connection for Workplace Wellbeing Check.
   Set to null to disconnect; the site then works as before
   (answers sent by response code, forms by e-mail).
   To connect: Firebase console → Project settings → Your apps → Web app → "SDK setup and configuration"
   → "Config", and paste the object here. These values are public by design; the security rules
   (firebase/firestore.rules) are what protect the data. */
window.FB_CONFIG = {
  apiKey: "AIzaSyDXmfRCOToQrcn6hVkFJUBRrEkyYoJ8aPY",
  authDomain: "team-weather-f6719.firebaseapp.com",
  projectId: "team-weather-f6719",
  storageBucket: "team-weather-f6719.firebasestorage.app",
  messagingSenderId: "473226422717",
  appId: "1:473226422717:web:b0c1ea99c6b70454180ad4"
  /* measurementId left out on purpose: the site does not load Google Analytics (privacy). */
};
/* Example of what it looks like when filled in:
window.FB_CONFIG = {
  apiKey: "AIza...",
  authDomain: "solonovate-wellbeing.firebaseapp.com",
  projectId: "solonovate-wellbeing",
  storageBucket: "solonovate-wellbeing.appspot.com",
  messagingSenderId: "1234567890",
  appId: "1:1234567890:web:abc123"
};
*/
