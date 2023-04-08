import dotenv from 'dotenv';
dotenv.config();

export const EnvironmentVariables = {
  TELEGRAM_BOT_TOKEN: process.env.TELEGRAM_BOT_TOKEN as string,
};
