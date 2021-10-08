# Will throw an exception if a short is split into two bytes
def reverseArray(port):
    numbers = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', port))
        sock.listen(1)
        sc, name = sock.accept()
        while True:
            number = struct.unpack('!h', sc.recv(2))[0]
            if number == -1:
                break
            numbers.append(number)
        pos = len(numbers)
        while pos > 0:
            pos = pos - 1
            sc.sendall(struct.pack('!h', numbers[pos]))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
    sock.close()

    return numbers



    reverseArray(12345)