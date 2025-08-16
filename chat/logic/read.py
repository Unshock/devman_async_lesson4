import asyncio
from datetime import datetime
import aiofiles

import chat.constants as c
from chat.logging import logger, reader_logger
from chat.utils import get_formatted_dt


async def veiw_chat(host: str, port: str, history: str):

    logger.debug(
        f'Connecting to chat with'
        f' host: {host}, port: {port}, chat_history: {history}')

    reader, writer = await asyncio.open_connection(
        host, port
    )

    async with aiofiles.open(history, mode='a') as history:
        formatted_dt = get_formatted_dt(datetime.now())
        formatted_message = c.MESSAGE_MASK.format(
            formatted_dt,
            'Установлено соединение',
        )

        reader_logger.debug(formatted_message)
        await history.write(formatted_message + '\n')

        try:
            while True:
                line_bytes = await reader.readline()
                line = line_bytes.decode().strip()

                formatted_dt = get_formatted_dt(datetime.now())
                formatted_message = c.MESSAGE_MASK.format(formatted_dt, line)

                reader_logger.debug(line)
                print(formatted_message)
                await history.write(formatted_message + '\n')

        except asyncio.CancelledError:
            logger.warning('Reading chat has been interrupted')
            raise

        except Exception as exc:
            logger.error(f'Exception registered during chat reading: {exc}')
            raise

        finally:
            writer.close()
            await writer.wait_closed()
