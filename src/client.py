import time
from utils import *
from process import Process

class Client(Process):
    def __init__(self, env, id, host, port, duration=60, max_requests=None):
        """
        Inicializa o cliente.
        :param url: URL para envio das requisições.
        :param duration: Duração do experimento em segundos.
        :param max_requests: Número máximo de requisições a serem enviadas (opcional).
        """
        Process.__init__(self, env, id, host, port)
        self.duration = duration
        self.max_requests = max_requests
        self.latencies = []
        self.count = 0
        self.result = None
        self.env.addProc(self)

    def body(self):
        """
        Executa o loop do cliente.
        """
        t0 = time.time()  # Timestamp inicial
        log_file = "client_log.txt"
        print("Here I am: ", self.id)
        
        with open(log_file, "w") as log:
            log.write("Timestamp, Latency (s)\n")

            while True:
                t1 = time.time()  # Timestamp antes de enviar requisição

                self.env.create_request_new_account(self.id, self.count)
                msg = self.getNextMessage()
                print(f"Client {self.id} received message: {msg}")

                t2 = time.time()  # Timestamp após receber resposta

                latency = t2 - t1
                self.latencies.append(latency)
                self.count += 1

                log.write(f"{t2}, {latency:.6f}\n")  # Loga a latência no arquivo

                # Verifica condições de saída
                if (time.time() - t0 >= self.duration) or (self.max_requests and self.count >= self.max_requests):
                    break

        # Finaliza o experimento
        t4 = time.time()
        throughput = self.count / (t4 - t0)
        average_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0

        print(f"Cliente finalizado. Vazão: {throughput:.2f} req/s, Média de latência: {average_latency:.6f} s.")
        print(f"Total de requisições enviadas: {self.count}")
        print(f"Log gravado em: {log_file}")
        self.result = (throughput, average_latency)