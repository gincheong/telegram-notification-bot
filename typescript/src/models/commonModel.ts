import { Logger } from '@tnb/utils';
import { db, getUserGroupRef } from '@tnb/db';

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
