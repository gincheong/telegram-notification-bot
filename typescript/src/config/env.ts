import dotenv from 'dotenv';
dotenv.config();

const getEnvironmentVariable = (envName: string) => {
  const environmentVariable = process.env[envName];

  if (environmentVariable === undefined) {
    throw new Error(`Exception while reading environment variable from '.env' file: ${envName}`);
  }

  return environmentVariable;
};

export const EnvironmentVariables = {
  TELEGRAM_BOT_TOKEN: getEnvironmentVariable('TELEGRAM_BOT_TOKEN'),
  FIREBASE_API_KEY: getEnvironmentVariable('FIREBASE_API_KEY'),
  FIREBASE_DATABASE_URL: getEnvironmentVariable('FIREBASE_DATABASE_URL'),
  FIREBASE_AUTH_DOMAIN: getEnvironmentVariable('FIREBASE_AUTH_DOMAIN'),
  FIREBASE_PROJECT_ID: getEnvironmentVariable('FIREBASE_PROJECT_ID'),
  FIREBASE_STORAGE_BUCKET: getEnvironmentVariable('FIREBASE_STORAGE_BUCKET'),
  FIREBASE_MESSAGING_SENDER_ID: getEnvironmentVariable('FIREBASE_MESSAGING_SENDER_ID'),
  FIREBASE_APP_ID: getEnvironmentVariable('FIREBASE_APP_ID'),
  FIREBASE_MEASUREMENT_ID: getEnvironmentVariable('FIREBASE_MEASUREMENT_ID'),
  FIREBASE_SERVICE_ACCOUNT_KEY_PATH: getEnvironmentVariable('FIREBASE_SERVICE_ACCOUNT_KEY_PATH'),
};
