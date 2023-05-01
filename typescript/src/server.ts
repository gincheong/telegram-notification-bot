import { Telegraf } from 'telegraf';

import { KeywordController } from './controllers';
import { EnvironmentVariables, BotCommands } from './config';
import { Logger } from './utils';

const Bot = new Telegraf(EnvironmentVariables.TELEGRAM_BOT_TOKEN);

Logger.debug('Launching Bot ...');
Bot.launch();
Logger.debug('Bot has Launched');

Bot.hears(BotCommands.GetKeywords, async (context) => await KeywordController.getKeywords(context));

process.once('SIGINT', () => Bot.stop('SIGINT'));
process.once('SIGTERM', () => Bot.stop('SIGTERM'));
