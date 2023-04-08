class KeywordModelBuilder {
  constructor() {}

  getKeywords(id: number) {
    return ['술', '롤', '인규'];
  }
}

export const KeywordModel = new KeywordModelBuilder();
