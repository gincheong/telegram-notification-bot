export const Logger = {
  debug: (...message: string[]) => {
    // TODO: write log to local file
    console.debug(...message);
  },
  error: (...message: string[]) => {
    // TODO: write log to local file
    console.error(...message);
  },
};
