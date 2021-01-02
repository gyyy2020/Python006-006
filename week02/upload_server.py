import socket
import pathlib


def save_file(addr, filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(addr)
        s.listen(1)

        conn, addr_ = s.accept()
        print(f'connected by {addr_}')
        for data in iter(lambda: conn.recv(1024), b''):
            with open(filename, 'a', encoding='utf-8', errors='replace') as f: #
                try:
                    f.write(data.decode('utf-8'))
                except:
                    pass


if __name__ == '__main__':
    addr = ('localhost', 10001)

    p = pathlib.Path(__file__).parent.joinpath('cloud')
    dst_file = '初中数学.txt'
    filename = p.joinpath(dst_file)

    if filename.exists():
        print('file already exists')
    else:
         save_file(addr, filename)
