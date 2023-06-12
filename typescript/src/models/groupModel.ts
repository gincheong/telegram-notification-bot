import { db, getGroupRef, getUserGroupRef } from '@tnb/db';
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
      const groups = Object.keys(snapshot.val()) as string[];

      return groups.map(parseInt);
    } catch (err) {
      const error = err as Error;

      Logger.error(`Exception while executing /getGroups: ${id}, ${error.message}`);
      throw error;
    }
  }

  async getGroupName(groupId: number) {
    const ref = getGroupRef(db, groupId, '/info/groupname');

    try {
      Logger.debug(`Try fetching groupName: ${groupId}`);

      const snapshot = await ref.get();
      const groupName = snapshot.val() as string;

      return groupName;
    } catch (err) {
      const error = err as Error;

      Logger.error(`Exception while executing /getGroupName: ${groupId}, ${error.message}`);
      throw error;
    }
  }

  async updateGroupName(groupId: number, title: string) {
    const ref = getGroupRef(db, groupId, '/info/groupname');

    try {
      Logger.debug(`Try updating groupName: ${groupId}/${title}`);

      await ref.push(title);
    } catch (err) {
      const error = err as Error;

      Logger.error(`Exception while executing /updateGroupName: ${groupId}/${title}`);
      throw error;
    }
  }
}

export const GroupModel = new GroupModelBuilder();
