import asyncio
from datetime import datetime
import aiofiles

CHAT_HOST = 'minechat.dvmn.org'
CHAT_PORT = 5000


async def print_chat():
    reader, writer = await asyncio.open_connection(
        CHAT_HOST, CHAT_PORT
    )

    message_mask = '[{}] {}'

    async with aiofiles.open('messages.log', mode='a') as f:
        formatted_dt = _get_formatted_dt(datetime.now())
        formatted_message = message_mask.format(
            formatted_dt,
            'Установлено соединение',
        )
        await f.write(formatted_message)
        print(formatted_message)

        while True:
            line_b = await reader.readline()
            line = line_b.decode()

            formatted_dt = _get_formatted_dt(datetime.now())
            formatted_message = message_mask.format(formatted_dt, line)

            print(formatted_message)
            await f.write(formatted_message)


def _get_formatted_dt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")

    # decoded_data = ''
    #
    # while True:
    #     data = b''
    #     decoded_data = ''
    #     while not decoded_data.endswith('\n'):
    #         data += await reader.read(64)
    #         try:
    #             decoded_data += data.decode()
    #         except UnicodeDecodeError as exc:
    #             print(exc)
    #             continue
    # 
    #         print(decoded_data)
    #         data = b''
    #         decoded_data = ''


if __name__ == '__main__':
    coroutine = print_chat()
    asyncio.run(coroutine)

