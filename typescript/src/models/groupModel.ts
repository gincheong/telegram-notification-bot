import { db, getUserGroupRef } from '@tnb/db';
import { Logger } from '@tnb/utils';

class GroupModelBuilder {
  constructor() {}

  async addGroup(id: number, groupId: number, title: string) {
    const ref = getUserGroupRef(db, id);

    try {
      Logger.debug(`Try updating groups: ${id}/${groupId}/${title}`);

      await ref.update({ [groupId]: title });

      return true;
    } catch (err) {
      const error = err as Error;

      Logger.error(
        `Exception while executing /addGroup: ${id}, ${groupId}, ${title}, ${error.message}`
      );

      throw error;
    }
  }

  async getGroups(id: number) {
    const ref = getUserGroupRef(db, id);

    try {
      Logger.debug(`Try fetching groups: ${id}`);

      const snapshot = await ref.get();
      const groups = snapshot.val() as string[];

      return groups;
    } catch (err) {
      const error = err as Error;

      Logger.error(`Exception while executing /getGroups: ${id}, ${error.message}`);
      throw error;
    }
  }
}

export const GroupModel = new GroupModelBuilder();
