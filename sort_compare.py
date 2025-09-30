import random
import time


def insertion_sort(a_list):
    start = time.time()
    for index in range(1, len(a_list)):
        current_value = a_list[index]
        position = index

        while position > 0 and a_list[position - 1] > current_value:
            a_list[position] = a_list[position - 1]
            position -= 1

        a_list[position] = current_value
    end = time.time()
    return a_list, end - start


def shell_sort(a_list):
    start = time.time()
    sublist_count = len(a_list) // 2
    while sublist_count > 0:
        for start_pos in range(sublist_count):
            gap_insertion_sort(a_list, start_pos, sublist_count)
        sublist_count //= 2
    end = time.time()
    return a_list, end - start


def gap_insertion_sort(a_list, start, gap):
    for i in range(start + gap, len(a_list), gap):
        current_value = a_list[i]
        position = i
        while position >= gap and a_list[position - gap] > current_value:
            a_list[position] = a_list[position - gap]
            position -= gap
        a_list[position] = current_value


def python_sort(a_list):
    start = time.time()
    a_list.sort()
    end = time.time()
    return a_list, end - start

def benchmark_sorts(list_size, trials=100):
    total_times = {"insertion": 0, "shell": 0, "python": 0}

    for _ in range(trials):
        rand_list = random.sample(range(1, list_size * 10), list_size)

        # Insertion sort
        _, t = insertion_sort(rand_list[:])
        total_times["insertion"] += t

        # Shell sort
        _, t = shell_sort(rand_list[:])
        total_times["shell"] += t

        # Python built-in sort
        _, t = python_sort(rand_list[:])
        total_times["python"] += t

    for key in total_times:
        total_times[key] /= trials

    return total_times


def main():
    for size in [500, 1000, 5000]:
        results = benchmark_sorts(size)
        print(f"\nList size: {size}")
        print(f"Insertion Sort took {results['insertion']:10.7f} seconds to run, on average")
        print(f"Shell Sort took {results['shell']:10.7f} seconds to run, on average")
        print(f"Python Sort took {results['python']:10.7f} seconds to run, on average")


if __name__ == "__main__":
    main()
