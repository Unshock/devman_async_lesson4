import asyncio
import json

from chat.exceptions import AuthorizationError
from chat.logging import reader_logger, sender_logger, logger
import chat.constants as c


async def register_user(
    host: str,
    port: str,
    user_name: str,
    show_messages: bool = True
):

    reader, writer = await asyncio.open_connection(host, port)
    user_token = None

    try:
        while True:
            line_bytes = await reader.readline()
            line = line_bytes.decode().strip()

            if line:
                reader_logger.debug(line)

            if line.strip() == c.INVITE_MESSAGE:
                writer.write('\n'.encode())
                continue

            if line.strip() == c.ENTER_NICKNAME_MESSAGE:

                username = _add_empty_line(user_name)
                encoded_message = username.encode()

                sender_logger.debug(encoded_message)
                writer.write(encoded_message)
                continue

            registered_user = json.loads(line)
            user_name = registered_user.get('nickname')
            user_token = registered_user.get('account_hash')

            if show_messages:
                print(
                    f'User successfully registered with name:'
                    f' "{user_name}", token: "{user_token}"'
                )

            break

    finally:
        writer.close()
        await writer.wait_closed()

    return user_name, user_token


async def authorize_user(reader, writer, user_token: str):
    user_token += '\n'
    writer.write(user_token.encode())

    line_bytes = await reader.readline()
    line = line_bytes.decode().strip()
    reader_logger.debug(line)

    line = json.loads(line)

    if line:
        user_name = line['nickname']
        user_token = line['account_hash']

        return user_name, user_token

    if not line:
        print(c.WRONG_TOKEN_MESSAGE)
        logger.debug(f'User entered wrong token: {user_token}')

        writer.close()
        await writer.wait_closed()

        raise AuthorizationError


async def connect_chat_for_messaging(
    host: str,
    port: str,
    *,
    user_token: str = None,
    user_name: str = None,
):

    reader, writer = await asyncio.open_connection(host, port)
    try:
        while True:
            line_bytes = await reader.readline()
            line = line_bytes.decode().strip()
            if line and line != c.INVITE_MESSAGE:
                print(line)

            if line.strip() == c.INVITE_MESSAGE:

                if not user_name and not user_token:
                    logger.debug(
                        'User has not provided any credentials,'
                        ' message will be send anonymously.'
                    )
                    user_name = c.ANONYMOUS_NAME

                if user_token:
                    logger.debug('Try to authorize with passed user_token')
                    try:
                        user_name, user_token = await authorize_user(
                            reader,
                            writer,
                            user_token,
                        )
                    except AuthorizationError:
                        return
                else:
                    if not user_name:
                        user_name = input()

                    logger.debug(
                        f'Try to register user with nickname: {user_name}',
                    )

                    user_name, user_token = await register_user(
                        host,
                        port,
                        user_name=user_name,
                        show_messages=False,
                    )

                    # open new connection
                    reader, writer = await asyncio.open_connection(host, port)

            if line.strip() in (c.WELCOME_MESSAGE, c.SEND_MESSAGE):
                if line.strip() == c.WELCOME_MESSAGE:
                    logger.debug(
                        f'User successfully authorized in'
                        f' chat with nickname: {user_name}'
                    )

                message = _get_multiline_input()
                message = _add_empty_line(message)
                encoded_message = message.encode()

                sender_logger.debug(encoded_message)
                writer.write(encoded_message)
                continue

    except asyncio.CancelledError:
        logger.warning('Messaging chat has been interrupted')
        raise

    except Exception as exc:
        logger.error(f'Exception registered during chat messaging: {exc}')
        raise

    finally:
        writer.close()
        await writer.wait_closed()


async def send_message(
    host: str,
    port: str,
    message: str,
    *,
    user_token: str | None = None,
    user_name: str | None = None,
):
    reader, writer = await asyncio.open_connection(host, port)

    try:
        while True:
            line_bytes = await reader.readline()
            line = line_bytes.decode().strip()

            if line.strip() == c.INVITE_MESSAGE:

                if not user_name and not user_token:
                    logger.debug(
                        'User has not provided any credentials,'
                        ' message will be send anonymously.'
                    )
                    user_name = c.ANONYMOUS_NAME

                if user_token:
                    logger.debug(
                        f'Try to authorize with passed user_token: {user_token}'
                    )
                    try:
                        user_name, user_token = await authorize_user(
                            reader,
                            writer,
                            user_token
                        )
                    except AuthorizationError:
                        raise
                else:
                    logger.debug(
                        f'Try to register user with nickname: {user_name}'
                    )
                    user_name, user_token = await register_user(
                        host,
                        port,
                        user_name=user_name,
                        show_messages=False,
                    )

                    # open new connection
                    reader, writer = await asyncio.open_connection(host, port)

            if line.strip() in (c.WELCOME_MESSAGE, c.SEND_MESSAGE):
                if line.strip() == c.WELCOME_MESSAGE:
                    logger.debug(
                        f'User successfully authorized'
                        f' in chat with nickname: {user_name}'
                    )

                message = message.strip()
                message = _add_empty_line(message)
                encoded_message = message.encode()

                sender_logger.debug(encoded_message)
                writer.write(encoded_message)

                break

    except asyncio.CancelledError:
        logger.warning('Messaging chat has been interrupted')
        raise

    except Exception as exc:
        logger.error(f'Exception registered during chat messaging: {exc}')
        raise

    finally:
        writer.close()
        await writer.wait_closed()


def _get_multiline_input():
    messages = []

    while True:
        m = input()
        messages.append(m)
        if messages[-1] == '':
            break

    print(messages)
    return '\n'.join(messages)


def _add_empty_line(message: str) -> str:
    return message.strip() + '\n' * 2
