export class NotFoundKeywordError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NotFoundKeywordError';
  }
}
