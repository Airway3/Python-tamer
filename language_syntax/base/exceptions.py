

def outer():
    try:
        middle()
    except Exception as e:
        print(f'Exception {e}')
        raise e


def middle():
    try:
        inner()
    finally:
        print('clean up')


def inner():
    raise RuntimeError('Kaboom')


outer()
