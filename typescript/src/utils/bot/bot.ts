import { ChatTypes, TelegrafContext } from '@tnb/types';
import { LanguageCode } from '@tnb/strings';

import { Logger } from '../log';

export const getContextData = (context: TelegrafContext) => {
  const languageCode = getLanguageCode(context);
  const id = context.from?.id;
  const chatType = context.chat.type;
  const args = parseArgs(context);

  /** chatType이 group, 혹은 supergroup일 때만 값을 갖는다. */
  const groupId = context.chat.id;
  /** chatType이 group, 혹은 supergroup일 때만 값을 갖는다. */
  const title = chatType !== 'private' ? context.chat.title : '';

  if (!id) {
    const logMessage = `[getContextData] 'from' property not in context. context: ${context}`;
    Logger.error(logMessage);
  }

  return { id, groupId, languageCode, args, chatType, title };
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
