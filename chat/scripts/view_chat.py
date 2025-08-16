#!/usr/bin/env python
import asyncio

from chat import cli
from chat.logging import logger
from chat.logic.read import veiw_chat


def main():
    args = cli.parse_view_args()
    logger.debug(
        f'Start reading chat with host: {args.host},'
        f' port: {args.port}, history: {args.history}'
    )
    coroutine = veiw_chat(args.host, args.port, args.history)
    asyncio.run(coroutine)


if __name__ == '__main__':
    main()
