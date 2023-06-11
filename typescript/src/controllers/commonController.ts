import { getContextData } from '../utils';
import { ChatType, TelegrafContext } from '../types';
import { Strings } from '../strings';

class HelpControllerBuilder {
  constructor() {}

  start(context: TelegrafContext) {
    const { languageCode, type } = getContextData(context);

    if (type === ChatType.PRIVATE) {
      const message = Strings[languageCode].START_PRIVATE.join('\n');

      context.reply(message, { parse_mode: 'HTML' });
    } else {
    }
  }

  info(context: TelegrafContext) {
    const { languageCode } = getContextData(context);

    const message = Strings[languageCode].INFO.join('\n');

    context.reply(message, { parse_mode: 'HTML' });
  }

  donate(context: TelegrafContext) {
    const { languageCode } = getContextData(context);

    const message = Strings[languageCode].DONATE.join('\n');

    context.reply(message, { parse_mode: 'HTML' });
  }
}

export const HelpController = new HelpControllerBuilder();
