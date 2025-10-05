import csv
import sys
from collections import deque
from server import Server, Request

def read_requests(filename):
    requests = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            timestamp = int(row[0])
            file_path = row[1]
            processing_time = int(row[2])
            requests.append(Request(timestamp, file_path, processing_time))
    return requests

def simulateOneServer(filename):
    requests = read_requests(filename)
    server = Server()
    queue = deque()
    wait_times = []
    current_time = 0

    for req in requests:
        while current_time < req.timestamp:
            server.tick()
            current_time += 1

        queue.append(req)

        if not server.busy() and queue:
            next_request = queue.popleft()
            wait_times.append(current_time - next_request.timestamp)
            server.start_next(next_request)

    # Finish remaining tasks
    while queue or server.busy():
        server.tick()
        current_time += 1
        if not server.busy() and queue:
            next_request = queue.popleft()
            wait_times.append(current_time - next_request.timestamp)
            server.start_next(next_request)

    average_wait = sum(wait_times) / len(wait_times) if wait_times else 0
    print(f"Average Wait Time (One Server): {average_wait:.2f} seconds")
    return average_wait

def simulateManyServers(filename, num_servers):
    requests = read_requests(filename)
    servers = [Server() for _ in range(num_servers)]
    queues = [deque() for _ in range(num_servers)]
    wait_times = []
    current_time = 0
    server_index = 0

    for req in requests:
        while current_time < req.timestamp:
            for server in servers:
                server.tick()
            current_time += 1

        queues[server_index].append(req)
        server_index = (server_index + 1) % num_servers

        for i, server in enumerate(servers):
            if not server.busy() and queues[i]:
                next_request = queues[i].popleft()
                wait_times.append(current_time - next_request.timestamp)
                server.start_next(next_request)

    # Finish remaining tasks
    while any(queue or server.busy() for queue, server in zip(queues, servers)):
        for server in servers:
            server.tick()
        current_time += 1
        for i, server in enumerate(servers):
            if not server.busy() and queues[i]:
                next_request = queues[i].popleft()
                wait_times.append(current_time - next_request.timestamp)
                server.start_next(next_request)

    average_wait = sum(wait_times) / len(wait_times) if wait_times else 0
    print(f"Average Wait Time ({num_servers} Servers): {average_wait:.2f} seconds")
    return average_wait

def main():
    if len(sys.argv) < 2:
        print("Usage: python simulation.py <filename> [num_servers]")
        return

    filename = sys.argv[1]
    if len(sys.argv) == 3:
        num_servers = int(sys.argv[2])
        simulateManyServers(filename, num_servers)
    else:
        simulateOneServer(filename)

if __name__ == "__main__":
    main()
