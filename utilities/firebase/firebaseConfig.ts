import firebase from "firebase/compat/app"
import "firebase/compat/auth"
import "firebase/compat/database"
import "firebase/compat/firestore"

const firebaseConfig = {
    apiKey: "AIzaSyBKuRMMiy8dVve9TRJfYoUa57OX5VeeUgs",
    authDomain: "realtimemvp-a9dca.firebaseapp.com",
    projectId: "realtimemvp-a9dca",
    storageBucket: "realtimemvp-a9dca.firebasestorage.app",
    messagingSenderId: "964655615724",
    appId: "1:964655615724:web:f7202c7d30e66b7ffa5fc9",
    measurementId: "G-CRK7255EQC"
};

// const firebaseConfig = {
//     apiKey: "AIzaSyBtuzSoAlT11Jxq91YgRxitktDEWmfrKXI",
//     authDomain: "iylavista.firebaseapp.com",
//     projectId: "iylavista",
//     storageBucket: "iylavista.firebasestorage.app",
//     messagingSenderId: "34573481921",
//     appId: "1:34573481921:web:444a6ea818c9e3f299e140",
//     measurementId: "G-6CZRLKL7PM"
// };

if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig)
}

export const db = firebase.firestore()
export default firebase