import { TelegrafContext } from '../../types';
import { LanguageCode } from '../../strings';

import { Logger } from '../log';

export const getContextData = (context: TelegrafContext) => {
  const languageCode = getLanguageCode(context);
  const id = context.from?.id;
  const type = context.chat.type;
  const args = parseArgs(context);

  if (!id) {
    const logMessage = `[getContextData] 'from' property not in context. context: ${context}`;
    Logger.error(logMessage);
  }

  return { id, languageCode, args, type };
};

export const getLanguageCode = (context: TelegrafContext) => {
  const languageCode = context.from?.language_code;

  if (!languageCode) {
    return LanguageCode.Ko;
  }

  return languageCode as LanguageCode;
};

export const parseArgs = (context: TelegrafContext) => {
  const split = context.message.text.split(' ');

  return split.slice(1);
};
