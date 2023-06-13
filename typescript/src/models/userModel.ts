import { db, getUserGroupRef } from '@tnb/db';
import { Logger } from '@tnb/utils';

export class UserModelBuilder {
  constructor() {}

  async addGroup(id: number, groupId: number) {
    const ref = getUserGroupRef(db, id);

    try {
      Logger.debug(`Try updating groups: ${id}/${groupId}`);

      const snapshot = await ref.get();
      const groupIds = Object.keys(snapshot.val());

      if (groupIds.includes(String(groupId))) {
        return false;
      } else {
        await ref.update({ [groupId]: true });

        return true;
      }
    } catch (err) {
      const error = err as Error;

      Logger.error(`Exception while executing /addGroup: ${id}, ${groupId}, ${error.message}`);

      throw error;
    }
  }
}

export const UserModel = new UserModelBuilder();
