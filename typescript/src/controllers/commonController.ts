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
    } else {
      // * Group or SuerGroup
      await GroupController.start(context);
    }
  }

  showInformation(context: TelegrafContext) {
    const { chatType, languageCode } = getContextData(context);

    if (chatType !== ChatTypes.PRIVATE) {
      return;
    }

    const message = Strings[languageCode].SHOW_INFORMATION.join('\n');

    context.reply(message, { parse_mode: 'HTML' });
  }

  showCommands(context: TelegrafContext) {
    const { chatType, languageCode } = getContextData(context);

    if (chatType !== ChatTypes.PRIVATE) {
      return;
    }

    const message = Strings[languageCode].SHOW_COMMANDS;

    context.reply(message, { parse_mode: 'HTML' });
  }
}

export const CommonController = new CommonControllerBuilder();
