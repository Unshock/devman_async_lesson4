#!/usr/bin/env python
import asyncio

from chat import cli
from chat.logging import logger
from chat.logic.handle_message import register_user


def main():
    args = cli.parse_register_user_args()
    logger.debug(
        f'Start user registration with host: {args.host},'
        f' port: {args.port}, user_name: {args.user_name}'
    )
    coroutine = register_user(
        args.host,
        args.port,
        args.user_name,
    )
    asyncio.run(coroutine)


if __name__ == '__main__':
    main()

