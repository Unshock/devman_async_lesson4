#!/usr/bin/env python
import asyncio

from chat import cli
from chat.logging import logger
from chat.logic.handle_message import send_message


def main():
    args = cli.parse_send_message_args()
    logger.debug(
        f'Start chat connection to chat with host: {args.host},'
        f' port: {args.port}, user_token: {args.user_token},'
        f' user_name: {args.user_name}'
    )
    coroutine = send_message(
        args.host,
        args.port,
        args.message,
        user_token=args.user_token,
        user_name=args.user_name,
    )
    asyncio.run(coroutine)


if __name__ == '__main__':
    main()
