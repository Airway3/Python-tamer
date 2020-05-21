import asyncio


# 3.5 async/await syntax


async def print_nums():
    num = 1
    while True:
        print(num)
        num += 1
        await asyncio.sleep(1)


async def print_time():
    count = 0
    while True:
        if count % 3 == 0:
            print('{} seconds have passed'.format(count))
        count += 1
        await asyncio.sleep(1)


async def main():
    # 3.6 create_task
    task1 = asyncio.create_task(print_nums())
    task2 = asyncio.create_task(print_time())

    await asyncio.gather(task1, task2)  # дожидаемся результата

    # можно и так было, gather сам оборачивает корутины в future
    # await asyncio.gather(print_nums(), print_time())


if __name__ == '__main__':
    # 3.7 run
    asyncio.run(main())
