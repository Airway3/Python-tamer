import asyncio
import random


rate = random.randint(1, 99)


async def handle(reader, writer):
    writer.write(f'Dollar rate is {rate}.\n'.encode())
    await writer.drain()
    writer.close()


async def update_rate():
    global rate
    while True:
        rate = random.randint(1, 99)
        await asyncio.sleep(10)


async def main():
    asyncio.create_task(update_rate())
    server = await asyncio.start_server(handle, '127.0.0.1', 8888)
    async with server:  # https://www.python.org/dev/peps/pep-0492/#asynchronous-iterators-and-async-for
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
