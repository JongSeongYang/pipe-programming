import time
import sys
import win32pipe, win32file, pywintypes


def send_pipe():
    print("pipe server")
    count = 0
    pipe = win32pipe.CreateNamedPipe(
        r'\\.\pipe\Foo',  # name of pipe
        win32pipe.PIPE_ACCESS_DUPLEX,  # openmode
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,  # pipe mode
        1, 65536, 65536,  # nMaxinstances , nOutBufferSize , nInbufferSize
        0,  # nDrfaultTimeOut
        None)  # pysecurity attributes
    try:
        print("waiting for client")
        win32pipe.ConnectNamedPipe(pipe,  # handle
                                   None)  # overlapped
        print("got client")

        while count < 10:
            print(f"writing message {count}")
            some_data = str.encode(f"{count}")  # byte로 인코딩
            win32file.WriteFile(pipe, some_data)
            time.sleep(1)
            count += 1

        print("finished now")
    finally:
        win32file.CloseHandle(pipe)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("need s or c as argument")
    elif sys.argv[1] == "s":
        send_pipe()

    else:
        print(f"no can do: {sys.argv[1]}")