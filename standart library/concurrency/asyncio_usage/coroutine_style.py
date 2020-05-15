import asyncio


# @asyncio.coroutine and yield this is old syntax


@asyncio.coroutine
def print_nums():
    num = 1
    while True:
        print(num)
        num += 1
        yield from asyncio.sleep(1)


@asyncio.coroutine
def print_time():
    count = 0
    while True:
        if count % 3 == 0:
            print('{} seconds have passed'.format(count))
        count += 1
        yield from asyncio.sleep(1)


@asyncio.coroutine
def main():
    # ensure_future кидает в очередь событийного цикла генераторы, т.е. вызывает create_task у loop
    task1 = asyncio.ensure_future(print_nums())
    task2 = asyncio.ensure_future(print_time())
    # дожидаемся результата asyncio.gather(tasks*)
    yield from asyncio.gather(task1, task2)  # return [task.result(), task.result()]

    # можно и так было, gather сам оборачивает корутины в future
    # yield from asyncio.gather(print_nums(), print_time())


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()

    # 3.7 run
    asyncio.run(main())
