import { BotCommands } from '@tnb/config';

export const Common = {
  START_PRIVATE: [
    '1. 키워드 알림을 활성화할 그룹에 봇을 초대합니다.',
    '2. <b>그룹 내 채팅으로</b> /start@keywordNoti_Bot 을 입력합니다.',
    '3. <b>봇과의 개인 대화로</b> 키워드를 등록합니다.',
    '',
    `봇에 대한 추가 정보는 <b>${BotCommands.INFO_PLAIN_TEXT}</b> 명령어,`,
    `키워드 관련 병령어는 <b>${BotCommands.CMD_PLAIN_TEXT}</b> 명령어로 확인할 수 있습니다.`,
    '',
    '문의: @gincheong',
    '후원: [링크](https://githun.com/gincheong)',
    'Github: <a href="https://github.com/gincheong/telegram-notification-bot">telegram-notification-bot</a>',
  ],

  START_GROUP_SUCCESS: [
    '현재 그룹을 키워드 알림 봇에 등록합니다.',
    '기타 명령어는 <b>봇과의 개인 대화</b>에서만 동작합니다.',
  ],
  START_GROUP_DUPLICATED: [
    '이미 등록된 그룹입니다.',
    '기타 명령어는 <b>봇과의 개인 대화</b>에서만 동작합니다.',
  ],

  INFO: [
    '봇은 키워드 감지를 위해서만 메시지 내용에 접근하며, 내용은 기록되지 않습니다.',
    '서버에는 그룹의 이름 정보가 저장될 수는 있으나, 사용자 이름 등은 기록되지 않습니다.',
    '키워드 데이터는 암호화되지 않으므로 중요한 정보를 입력하지 마세요.',
  ],

  DONATE: ['서버 운영을 위한 후원을 받고 있습니다.', '감사합니다.', '링크: [링크]'],
};
