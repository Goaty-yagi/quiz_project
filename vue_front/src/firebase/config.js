import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'

const firebaseConfig = {
    apiKey: "AIzaSyD1pSVELmFcBIKvkTw36KDuFe98q_mJw3A",
    authDomain: "vue-quiz-auth.firebaseapp.com",
    projectId: "vue-quiz-auth",
    storageBucket: "vue-quiz-auth.appspot.com",
    messagingSenderId: "695515608",
    appId: "1:695515608:web:73c143ed63bf06a3cedaad"
  };

//   init firebase

initializeApp(firebaseConfig)

// init firebase auth

const auth = getAuth()

export { auth }