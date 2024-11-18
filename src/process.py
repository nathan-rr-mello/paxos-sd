import sys
sys.dont_write_bytecode = True
import array, socket, struct
import pickle
from threading import Thread
from queue import Queue

class Process(Thread):
    def __init__(self, env, id, host, port):
        super().__init__()
        self.env = env
        self.id = id
        self.host = host
        self.port = port
        self.inbox = Queue()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.listener_thread = Thread(target=self.listen_for_messages)
        self.listener_thread.daemon = True
        self.listener_thread.start()
        self.stop = False
    
    def listen_for_messages(self):
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                while True:
                    length_data = self.recv_all(client_socket, 4)
                    if not length_data:
                        break
                    length = struct.unpack('!I', length_data)[0]
                    data = self.recv_all(client_socket, length)
                    if not data:
                        break
                    try:
                        msg = pickle.loads(data)
                        self.inbox.put(msg)
                    except (EOFError, pickle.UnpicklingError) as e:
                        print("Error decoding message")
                client_socket.close()
            except Exception as e:
                print("Error accepting connection")
    
    def recv_all(self, sock, n):
        data = array.array('b')
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.frombytes(packet)
        return data.tobytes()

    def run(self):
        try:
            self.body()
            self.env.removeProc(self.id)
        except EOFError:
            print("Exiting..")

    def getNextMessage(self):
        return self.inbox.get()

    def deliver(self, msg):
        self.inbox.put(msg)

    def sendMessage(self, dst_id, msg):
        self.env.sendMessage(dst_id, msg)
