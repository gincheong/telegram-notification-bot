import { Telegraf } from 'telegraf';

import { CommonController, KeywordController } from './controllers';
import { EnvironmentVariables, BotCommands } from './config';
import { Logger } from './utils';

const Bot = new Telegraf(EnvironmentVariables.TELEGRAM_BOT_TOKEN);

Logger.debug('Launching Bot ...');
Bot.launch();
Logger.debug('Bot has Launched');

Bot.hears(BotCommands.GET_KEYWORDS, KeywordController.getKeywords);
Bot.hears(BotCommands.ADD_KEYWORD, KeywordController.addKeyword);
Bot.hears(BotCommands.DELETE_KEYWORD, KeywordController.deleteKeyword);

Bot.hears(BotCommands.START, CommonController.start);
Bot.hears(BotCommands.INFO, CommonController.info);

process.once('SIGINT', () => Bot.stop('SIGINT'));
process.once('SIGTERM', () => Bot.stop('SIGTERM'));
