from multiprocessing import Process, Queue
from multiprocessing.connection import Listener, Client


pipe_name = r'\\.\pipe\pymenu'
secret = b'c-compiler'


def server(q):
    try:
        listener = Listener(pipe_name, authkey=secret)
    except:
        q.put('client')
        return

    q.put('server')

    while True:
        client = listener.accept()
        buffer = []
        while True:
            try:
                raw_chunk = client.recv_bytes()
                chunk = raw_chunk.decode('utf8')
                buffer.append(chunk)
            except EOFError:
                break
        msg = ''.join(buffer)
        q.put(msg)


def client(msg):
    remote = Client(pipe_name, authkey=secret)
    remote.send_bytes('hello world\n'.encode('utf8'))
    remote.send_bytes('goodbye cruel world'.encode('utf8'))


if __name__ == '__main__':
    q = Queue()

    p = Process(target=server, args=(q,))
    p.start()

    mode = q.get()
    print(mode)

    if mode == 'server':
        while True:
            msg = q.get()
            print(repr(msg))
    elif mode == 'client':
        p.join()
        client('hi client')
    else:
        raise ValueError(f'unknown mode: {mode}')


