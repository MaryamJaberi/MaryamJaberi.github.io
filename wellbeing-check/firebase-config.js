/* Firebase connection for Workplace Wellbeing Check.
   Leave FB_CONFIG as null until the Firebase project exists; the site then works as before
   (answers sent by response code, forms by e-mail).
   To connect: Firebase console → Project settings → Your apps → Web app → "SDK setup and configuration"
   → "Config", and paste the object here. These values are public by design; the security rules
   (firebase/firestore.rules) are what protect the data. */
window.FB_CONFIG = null;
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
