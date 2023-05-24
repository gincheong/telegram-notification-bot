import { Context, NarrowedContext } from 'telegraf';
import { Update, Message } from 'telegraf/src/core/types/typegram';

export type TelegrafContext = NarrowedContext<
  Context<Update> & {
    match: RegExpExecArray;
  },
  {
    message: Update.New & Update.NonChannel & Message.TextMessage;
    update_id: number;
  }
>;
