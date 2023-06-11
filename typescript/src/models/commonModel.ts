import { Logger } from '../utils';
import { db, getUserGroupRef } from '../db';

class CommonModelBuilder {
  constructor() {}

  addGroup(id: number, groupId: number) {
    const ref = getUserGroupRef(db, id);

    try {
    } catch (err) {
      const error = err as Error;

      Logger.error(`Exception while executing /addGroup: ${id}, ${error.message}`);
    }
  }
}

export const CommonModel = new CommonModelBuilder();
