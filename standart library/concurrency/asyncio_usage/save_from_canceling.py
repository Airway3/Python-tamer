import asyncio


async def coro():
    print('start')
    await asyncio.sleep(4)
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
    shielded = asyncio.shield(task)
    asyncio.create_task(cancel(shielded))

    await asyncio.sleep(4)
    assert not task.cancelled()


if __name__ == '__main__':
    asyncio.run(main())
