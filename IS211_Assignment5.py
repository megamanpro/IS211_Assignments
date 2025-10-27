import sys
import csv
from collections import deque

class Request:
    def __init__(self, timestamp, file_path, process_time):
        self.timestamp = int(timestamp)
        self.file_path = file_path
        self.process_time = int(process_time)

    def get_timestamp(self):
        return self.timestamp

    def get_process_time(self):
        return self.process_time


class Server:
    def __init__(self):
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task:
            self.time_remaining -= 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        return self.current_task is not None

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_process_time()


def read_requests(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        return [Request(*row) for row in reader]


def simulateOneServer(filename):
    requests = read_requests(filename)
    queue = deque()
    server = Server()
    current_time = 0
    wait_times = []

    while requests or queue or server.busy():
        # Add new requests to the queue
        while requests and requests[0].get_timestamp() == current_time:
            queue.append(requests.pop(0))

        if (not server.busy()) and queue:
            next_request = queue.popleft()
            wait_times.append(current_time - next_request.get_timestamp())
            server.start_next(next_request)

        server.tick()
        current_time += 1

    average_wait = sum(wait_times) / len(wait_times) if wait_times else 0
    print(f"Average Wait Time (One Server): {average_wait:.2f} seconds")
    return average_wait


def simulateManyServers(filename, num_servers):
    requests = read_requests(filename)
    queues = [deque() for _ in range(num_servers)]
    servers = [Server() for _ in range(num_servers)]
    current_time = 0
    wait_times = []
    request_index = 0

    while requests or any(q for q in queues) or any(s.busy() for s in servers):
        # Distribute new requests round-robin
        while request_index < len(requests) and requests[request_index].get_timestamp() == current_time:
            server_index = request_index % num_servers
            queues[server_index].append(requests[request_index])
            request_index += 1

        for i in range(num_servers):
            if not servers[i].busy() and queues[i]:
                next_request = queues[i].popleft()
                wait_times.append(current_time - next_request.get_timestamp())
                servers[i].start_next(next_request)

        for server in servers:
            server.tick()

        current_time += 1

    average_wait = sum(wait_times) / len(wait_times) if wait_times else 0
    print(f"Average Wait Time ({num_servers} Servers): {average_wait:.2f} seconds")
    return average_wait


def main():
    if len(sys.argv) < 2:
        print("Usage: python simulation.py <filename> [servers]")
        return

    filename = sys.argv[1]
    if len(sys.argv) == 3:
        num_servers = int(sys.argv[2])
        simulateManyServers(filename, num_servers)
    else:
        simulateOneServer(filename)


if __name__ == "__main__":
    main()
