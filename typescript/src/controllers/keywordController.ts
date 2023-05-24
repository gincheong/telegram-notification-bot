import { TelegrafContext } from '../types';

import { KeywordModel } from '../models';
import { getContextData } from '../utils';
import { NotFoundKeywordError } from '../error';
import { Strings } from '../strings';

class KeywordControllerBuilder {
  constructor() {}

  async getKeywords(context: TelegrafContext) {
    const { id, languageCode } = getContextData(context);

    const keywords = await KeywordModel.getKeywords(id);
    if (keywords.length === 0) {
      context.reply(Strings[languageCode].GET_KEYWORDS_NO_KEYWORDS);
    } else {
      context.reply(Strings[languageCode].GET_KEYWORDS_SUCCESS + keywords.join(', '));
    }
  }

  async addKeyword(context: TelegrafContext) {
    const { id, languageCode, args } = getContextData(context);

    if (args.length === 0) {
      context.reply(Strings[languageCode].ADD_KEYWORD_NO_ARGS);
      return;
    }

    const newKeyword = args[0];

    const success = await KeywordModel.addKeyword(id, newKeyword);
    if (success) {
      context.reply(`'${newKeyword}' ${Strings[languageCode].ADD_KEYWORD_SUCCESS}`);
    } else {
      context.reply(Strings[languageCode].ADD_KEYWORD_FAILURE);
    }
  }

  async deleteKeyword(context: TelegrafContext) {
    const { id, languageCode, args } = getContextData(context);

    if (args.length === 0) {
      context.reply(Strings[languageCode].DELETE_KEYWORD_NO_ARGS);
      return;
    }

    const deleteTargetKeyword = args[0];

    try {
      const isSuccess = await KeywordModel.deleteKeyword(id, deleteTargetKeyword);

      if (isSuccess) {
        context.reply(Strings[languageCode].DELETE_KEYWORD_SUCCESS);
        return;
      }
    } catch (error) {
      if (error instanceof NotFoundKeywordError) {
        context.reply(Strings[languageCode].DELETE_KEYWORD_FAILURE_NOT_FOUND);
      }
    }

    context.reply(Strings[languageCode].DELETE_KEYWORD_FAILURE);
  }
}

export const KeywordController = new KeywordControllerBuilder();
