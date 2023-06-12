import { GroupModel } from '@tnb/models';
import { getContextData } from '@tnb/utils';
import { ChatTypes, TelegrafContext } from '@tnb/types';
import { Strings } from '@tnb/strings';

class GroupControllerBuilder {
  constructor() {}

  async start(context: TelegrafContext) {
    const { id, groupId, languageCode, chatType, title } = getContextData(context);

    if (ChatTypes.GROUP === chatType || ChatTypes.SUPER_GROUP === chatType) {
      await GroupModel.addGroup(id, groupId, title);

      context.reply(Strings[languageCode].ADD_GROUP_SUCCESS_MESSAGES);
    }
  }

  async getGroups(context: TelegrafContext) {
    const { id, chatType, languageCode } = getContextData(context);

    if (chatType !== ChatTypes.PRIVATE) {
      return;
    }

    const groupIds = await GroupModel.getGroups(id);
    const promises = groupIds.map(async (groupId) => {
      return await GroupModel.getGroupName(groupId);
    });

    const groupNames = await Promise.all(promises);

    if (groupIds.length === 0) {
      context.reply(Strings[languageCode].GET_GROUPS_NO_DATA);
    } else {
      const messages = [Strings[languageCode].GET_GROUPS_SUCCESS, ...groupNames];

      context.reply(messages.join('\n'));
    }
  }
}

export const GroupController = new GroupControllerBuilder();
