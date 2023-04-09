// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app';
import { getDatabase } from 'firebase/database';

import { EnvironmentVariables } from 'src/config';

const firebaseConfig = {
  apiKey: EnvironmentVariables.FIREBASE_API_KEY,
  authDomain: EnvironmentVariables.FIREBASE_AUTH_DOMAIN,
  databaseURL: EnvironmentVariables.FIREBASE_DATABASE_URL,
  projectId: EnvironmentVariables.FIREBASE_PROJECT_ID,
  storageBucket: EnvironmentVariables.FIREBASE_STORAGE_BUCKET,
  messagingSenderId: EnvironmentVariables.FIREBASE_MESSAGING_SENDER_ID,
  appId: EnvironmentVariables.FIREBASE_APP_ID,
  measurementId: EnvironmentVariables.FIREBASE_MEASUREMENT_ID,
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const database = getDatabase(app);
