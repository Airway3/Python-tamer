import asyncio


async def coro():
    print('start')
    try:
        await asyncio.sleep(4)
    except asyncio.CancelledError:
        print('saved')

    print('finished')


async def cancel(task):
    await asyncio.sleep(2)
    task.cancel()

    print('task.cancel() called')
    try:
        await task
    except asyncio.CancelledError:
        print('task successfully cancelled')


async def main():
    task = asyncio.create_task(coro())
    asyncio.create_task(cancel(task))

    await asyncio.sleep(4)
    assert not task.cancelled()


if __name__ == '__main__':
    asyncio.run(main())
