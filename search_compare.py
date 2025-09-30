import random
import time

def sequential_search(a_list, item):
    start = time.time()
    pos = 0
    found = False

    while pos < len(a_list) and not found:
        if a_list[pos] == item:
            found = True
        else:
            pos += 1

    end = time.time()
    return found, end - start


def ordered_sequential_search(a_list, item):
    start = time.time()
    pos = 0
    found = False
    stop = False

    while pos < len(a_list) and not found and not stop:
        if a_list[pos] == item:
            found = True
        else:
            if a_list[pos] > item:
                stop = True
            else:
                pos += 1

    end = time.time()
    return found, end - start


def binary_search_iterative(a_list, item):
    start = time.time()
    first = 0
    last = len(a_list) - 1
    found = False

    while first <= last and not found:
        midpoint = (first + last) // 2
        if a_list[midpoint] == item:
            found = True
        else:
            if item < a_list[midpoint]:
                last = midpoint - 1
            else:
                first = midpoint + 1

    end = time.time()
    return found, end - start


def binary_search_recursive(a_list, item):
    start = time.time()

    def helper(lst, item):
        if len(lst) == 0:
            return False
        else:
            midpoint = len(lst) // 2
            if lst[midpoint] == item:
                return True
            else:
                if item < lst[midpoint]:
                    return helper(lst[:midpoint], item)
                else:
                    return helper(lst[midpoint + 1:], item)

    found = helper(a_list, item)
    end = time.time()
    return found, end - start

def benchmark_searches(list_size, trials=100):
    target = 99999999
    total_times = {
        "sequential": 0,
        "ordered_seq": 0,
        "binary_iter": 0,
        "binary_rec": 0,
    }

    for _ in range(trials):
        rand_list = random.sample(range(1, list_size * 10), list_size)

        # Sequential search (unsorted)
        _, t = sequential_search(rand_list, target)
        total_times["sequential"] += t

        # Ordered sequential search
        rand_list.sort()
        _, t = ordered_sequential_search(rand_list, target)
        total_times["ordered_seq"] += t

        # Binary iterative
        _, t = binary_search_iterative(rand_list, target)
        total_times["binary_iter"] += t

        # Binary recursive
        _, t = binary_search_recursive(rand_list, target)
        total_times["binary_rec"] += t

    for key in total_times:
        total_times[key] /= trials

    return total_times


def main():
    for size in [500, 1000, 5000]:
        results = benchmark_searches(size)
        print(f"\nList size: {size}")
        print(f"Sequential Search took {results['sequential']:10.7f} seconds to run, on average")
        print(f"Ordered Sequential Search took {results['ordered_seq']:10.7f} seconds to run, on average")
        print(f"Binary Search Iterative took {results['binary_iter']:10.7f} seconds to run, on average")
        print(f"Binary Search Recursive took {results['binary_rec']:10.7f} seconds to run, on average")


if __name__ == "__main__":
    main()
