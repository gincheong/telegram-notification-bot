import { Context } from 'telegraf';
import { Update } from 'telegraf/typings/core/types/typegram';

import { LanguageCode } from '../../strings';
import { Logger } from '../log';

export const getContextData = (context: Context<Update>) => {
  const languageCode = getLanguageCode(context);
  const id = context.from?.id;

  if (!id) {
    const logMessage = `[getContextData] 'from' property not in context. context: ${context}`;
    Logger.error(logMessage);
    throw new Error(logMessage);
  }

  return { id, languageCode };
};

export const getLanguageCode = (context: Context<Update>) => {
  const languageCode = context.from?.language_code;

  if (!languageCode) {
    return LanguageCode.Ko;
  }

  return languageCode as LanguageCode;
};
