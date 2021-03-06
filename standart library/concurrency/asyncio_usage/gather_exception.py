import asyncio


async def hold(i):
    await asyncio.sleep(i)

    if i == 3:
        raise RuntimeError('Kaboom!')

    print(i)


async def main():
    coros = (hold(i) for i in range(5))

    # 1
    # print('gather result', await asyncio.gather(*coros))

    # 2
    # print('gather result', await asyncio.gather(*coros, return_exceptions=True))

    # 3
    try:
        print('gather result', await asyncio.gather(*coros))
    except RuntimeError as e:
        print(e)

    print('sleep(5)')
    await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main())
