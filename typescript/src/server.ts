import { Telegraf } from 'telegraf';

import { KeywordController } from './controllers';
import { EnvironmentVariables, BotCommands } from './config';
import { Logger } from './utils';

const Bot = new Telegraf(EnvironmentVariables.TELEGRAM_BOT_TOKEN);

Logger.debug('Launching Bot ...');
Bot.launch();
Logger.debug('Bot has Launched');

Bot.hears(BotCommands.GetKeywords, KeywordController.getKeywords);
Bot.hears(BotCommands.AddKeyword, KeywordController.addKeyword);
Bot.hears(BotCommands.DeleteKeyword, KeywordController.deleteKeyword);

process.once('SIGINT', () => Bot.stop('SIGINT'));
process.once('SIGTERM', () => Bot.stop('SIGTERM'));
