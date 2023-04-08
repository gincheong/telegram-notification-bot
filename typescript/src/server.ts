import { Telegraf } from 'telegraf';

import { EnvironmentVariables } from './config';

const Bot = new Telegraf(EnvironmentVariables.TELEGRAM_BOT_TOKEN);

Bot.launch();

process.once('SIGINT', () => Bot.stop('SIGINT'));
process.once('SIGTERM', () => Bot.stop('SIGTERM'));

export { Bot };
