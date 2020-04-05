"""
Parallelism is multiprocessing.

Concurrency:

    threading
    asyncio
    multiprocessing

Pre-emptive multitasking (threading) - The operating system decides when to switch tasks external to Python.
Cooperative multitasking (asyncio) - The tasks decide when to give up control.
Multiprocessing (multiprocessing) - The processes all run at the same time on different processors.

Concurrency can make a big difference for two types of problems. These are generally called CPU-bound and I/O-bound.


"""
