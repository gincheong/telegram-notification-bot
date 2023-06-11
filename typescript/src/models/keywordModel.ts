import { db, getKeywordRef } from '@tnb/db';
import { Logger } from '@tnb/utils';
import { NotFoundKeywordError } from '@tnb/error';

class KeywordModelBuilder {
  constructor() {}

  async getKeywords(id: number) {
    const ref = getKeywordRef(db, id);

    try {
      Logger.debug(`Try fetching keywords: ${id}`);
      const snapshot = await ref.get();
      const keywords = Object.values(snapshot.val());

      return keywords as string[];
    } catch (err) {
      const error = err as Error;

      Logger.error(`Exception while executing /getKeywords: ${id}, ${error.message}`);

      return [];
    }
  }

  async addKeyword(id: number, keyword: string) {
    const ref = getKeywordRef(db, id);

    try {
      Logger.debug(`Try inserting keyword: ${id}/${keyword}`);
      await ref.push(keyword);

      return true;
    } catch (err) {
      const error = err as Error;
      Logger.error(`Exception while executing /addKeyword: ${id}, ${keyword} ${error.message}`);

      return false;
    }
  }

  async deleteKeyword(id: number, keyword: string) {
    const ref = getKeywordRef(db, id);

    try {
      Logger.debug(`Try deleting keyword: ${id}/${keyword}`);

      const snapshot = await ref.get();
      const keywords = snapshot.val();

      if (!keywords) {
        throw new NotFoundKeywordError(`cannot find keyword '${keyword}' in id ${id}`);
      }

      for (const [key, val] of Object.entries(keywords)) {
        if (val === keyword) {
          const deleteRef = getKeywordRef(db, id, key);

          await deleteRef.remove();
          return true;
        }
      }

      return false;
    } catch (err) {
      const error = err as Error;
      Logger.error(`Exception while executing /deleteKeyword: ${id}, ${keyword}, ${error.message}`);
      throw error;
    }
  }
}

export const KeywordModel = new KeywordModelBuilder();
