import dotenv from 'dotenv';
dotenv.config();

export const EnvironmentVariables = {
  TELEGRAM_BOT_TOKEN: process.env.TELEGRAM_BOT_TOKEN as string,
  FIREBASE_API_KEY: process.env.FIREBASE_API_KEY as string,
  FIREBASE_DATABASE_URL: process.env.FIREBASE_DATABASE_URL as string,
  FIREBASE_AUTH_DOMAIN: process.env.FIREBASE_AUTH_DOMAIN as string,
  FIREBASE_PROJECT_ID: process.env.FIREBASE_PROJECT_ID as string,
  FIREBASE_STORAGE_BUCKET: process.env.FIREBASE_STORAGE_BUCKET as string,
  FIREBASE_MESSAGING_SENDER_ID: process.env.FIREBASE_MESSAGING_SENDER_ID as string,
  FIREBASE_APP_ID: process.env.FIREBASE_APP_ID as string,
  FIREBASE_MEASUREMENT_ID: process.env.FIREBASE_MEASUREMENT_ID as string,
};
