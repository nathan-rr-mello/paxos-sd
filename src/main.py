import matplotlib.pyplot as plt
import time
import threading
from env import Env, Config
from client import Client

NACCEPTORS = 3
NREPLICAS = 2
NLEADERS = 2
NREQUESTS = 5
NCONFIGS = 3

def run_experiments(env, initialconfig, max_failures=3, max_clients=200, step=50, duration=60):
    results = {}
    env.create_config(NREPLICAS, NACCEPTORS, NLEADERS)

    for f in range(1, max_failures + 1):  # Variar número de falhas
        results[f] = []
        round = 0

        for num_clients in range(step, max_clients + 1, step):  # Varia número de clientes
            clients = []
            # print 'maxclients {} step {}'.format(max_clients, step)
            for i in range(num_clients):
                pid = "client-%d.%d" % (round,i)
                client = env.create_client(pid, duration, NREQUESTS)
                clients.append(client)

            for client in clients:
                client.join()

            for client in clients:
                print('Client {} finished'.format(client.id))
                print('Client {} latencies: {}'.format(client.id, client.result))

            # Aggregate results
            total_throughput = sum(client.result[0] for client in clients if client.result)
            avg_latency = (sum(client.result[1] for client in clients if client.result) / len(clients))
            results[f].append((total_throughput, avg_latency))

            print('Results for f = {} and num_clients = {}'.format(f, num_clients))
            print('Total throughput: {}'.format(total_throughput))
            print('Average latency: {}'.format(avg_latency))
            round += 1
    print('Results: {}'.format(results))
    return results


# def plot_results(results):
#     plt.figure(figsize=(10, 6))

#     for f, data in results.items():
#         throughputs, latencies = zip(*data)
#         plt.plot(throughputs, latencies, label="f = {}".format(f))

#     plt.title("Curvas de Vazão x Latência")
#     plt.xlabel("Vazão (Requisições por Segundo)")
#     plt.ylabel("Latência Média (s)")
#     plt.legend()
#     plt.grid(True)
#     plt.show()

def write_results(results):
    for f, data in results.items():
        with open("results_f_{}.log".format(f), "w") as f:
            for throughput, latency in data:
                f.write("{} {}\n".format(throughput, latency))
    
def main():
    env = Env(1)
    initialconfig = Config([], [], [])
    experiment_results = run_experiments(env, initialconfig, max_failures=1, max_clients=5, step=1, duration=25)
    print('Experiment results')
    write_results(experiment_results)
    # plot_results(experiment_results)
    env._graceexit()

if __name__ == "__main__":
    main()
