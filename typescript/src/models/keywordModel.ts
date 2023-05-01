import { db } from '../db';
import { Logger } from '../utils';

class KeywordModelBuilder {
  constructor() {}

  async getKeywords(id: number) {
    const ref = db.ref(`user/${id}/keyword`);

    Logger.debug(`Try fetching keywords of id: ${id}`);

    try {
      const snapshot = await ref.get();
      const keywords = Object.values(snapshot.val());

      return keywords as string[];
    } catch (err) {
      const error = err as Error;

      Logger.error(`Exception while fetching data(/getKeywords): ${error.message}`);

      return [];
    }
  }
}

export const KeywordModel = new KeywordModelBuilder();
