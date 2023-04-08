import { Telegraf } from 'telegraf';

import { KeywordController } from './controllers';
import { EnvironmentVariables, BotCommands } from './config';

const Bot = new Telegraf(EnvironmentVariables.TELEGRAM_BOT_TOKEN);

Bot.launch();
Bot.hears(BotCommands.GetKeywords, KeywordController.getKeywords);

process.once('SIGINT', () => Bot.stop('SIGINT'));
process.once('SIGTERM', () => Bot.stop('SIGTERM'));
