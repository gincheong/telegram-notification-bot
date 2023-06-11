import { Database } from 'firebase-admin/lib/database/database';

export const getKeywordRef = (database: Database, id: number, keywordKey: string = '') => {
  return database.ref(`user/${id}/keyword/${keywordKey}`);
};

export const getUserGroupRef = (database: Database, id: number) => {
  return database.ref(`user/${id}/registered_group`);
};
