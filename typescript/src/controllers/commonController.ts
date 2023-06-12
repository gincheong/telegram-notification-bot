import { getContextData } from '@tnb/utils';
import { GroupController } from './groupController';
import { ChatTypes, TelegrafContext } from '@tnb/types';
import { Strings } from '@tnb/strings';

class CommonControllerBuilder {
  constructor() {}

  async start(context: TelegrafContext) {
    const { languageCode, chatType } = getContextData(context);

    if (chatType === ChatTypes.PRIVATE) {
      const message = Strings[languageCode].START_PRIVATE.join('\n');

      context.reply(message, { parse_mode: 'HTML', disable_web_page_preview: true });
    } else if (ChatTypes.GROUP === chatType || ChatTypes.SUPER_GROUP === chatType) {
      await GroupController.start(context);
    }
  }

  info(context: TelegrafContext) {
    const { chatType, languageCode } = getContextData(context);

    if (chatType === ChatTypes.PRIVATE) {
      return;
    }

    const message = Strings[languageCode].INFO.join('\n');

    context.reply(message, { parse_mode: 'HTML' });
  }

  donate(context: TelegrafContext) {
    const { chatType, languageCode } = getContextData(context);

    if (chatType === ChatTypes.PRIVATE) {
      return;
    }

    const message = Strings[languageCode].DONATE.join('\n');

    context.reply(message, { parse_mode: 'HTML' });
  }
}

export const CommonController = new CommonControllerBuilder();
