import { Context } from 'telegraf';
import { Update } from 'telegraf/src/core/types/typegram';

import { KeywordModel } from '../models';
import { getContextData } from '../utils';
import { Strings } from '../strings';

class KeywordControllerBuilder {
  constructor() {}

  async getKeywords(context: Context<Update>) {
    const { id, languageCode } = getContextData(context);

    const keywords = await KeywordModel.getKeywords(id);

    const message = Strings[languageCode].GET_KEYWORDS_MESSAGE;

    context.reply(message + keywords.join(', '));
  }
}

export const KeywordController = new KeywordControllerBuilder();
