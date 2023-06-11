import { credential, database } from 'firebase-admin';
import { initializeApp } from 'firebase-admin/app';

import { EnvironmentVariables } from '@tnb/config';

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

const serviceAccount = require(EnvironmentVariables.FIREBASE_SERVICE_ACCOUNT_KEY_PATH);

initializeApp({
  credential: credential.cert(serviceAccount),
  databaseURL: firebaseConfig.databaseURL,
});

const db = database();

export { db };
