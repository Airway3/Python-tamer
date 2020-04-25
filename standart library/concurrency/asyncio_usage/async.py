import asyncio
from time import time


"""
AbstractEventLoopPolicy - правила сколько создавать лупов, один глобальный или на каждый тред свой и тд.
Методы класса создают и возвращают лупы в соотв с правилами которые он определяет.
По дефолту (DefaultEventLoopPolicy) на каждый тред свой луп, но автоматически создаёт только для мейнтреда.
Также устанавливает/возвращает watcher для подпроцессов.

Экземпляр DefaultEventLoopPolicy == _UnixDefaultEventLoopPolicy (в глобальной переменной _event_loop_policy) 
всегда один, даже если лупы созданы на каждый поток.

===================================================================================================
_loop_factory = _UnixSelectorEventLoop < BaseSelectorEventLoop < BaseEventLoop < AbstractEventLoop

Это монстр класс, который делает системные вызовы и проверяет дескрипторы на чтение и запись.
Связывает всё что можно в юниксе (юникс сокеты, пайпы, подпроцессы).
Создаёт Future (предок Task) и Task.

===================================================================================================
Future - This class is *almost* compatible with concurrent.futures.Future.
Task - A coroutine wrapped in a Future.

===================================================================================================


===================================================================================================


===================================================================================================

"""


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

    yield from asyncio.gather(task1, task2)  # дожидаемся результата


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
    asyncio.run(main())
