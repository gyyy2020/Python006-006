import socket
import pathlib

def upload_file(address, filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(address)

        with open(filename, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                s.sendall(line.encode('utf-8', errors='replace'))
 

if __name__ == "__main__":
    addr = ('127.0.0.1', 10001)

    p = pathlib.Path(__file__).parent.joinpath('local')
    file_src = '天龙八部（世纪新修版）.txt'
    file_src1 = 'python_datatypes.txt'
    file_src2 = 'Python进阶训练营（第二周）.pdf'

    filename = p.joinpath(file_src)
    upload_file(addr, filename)
