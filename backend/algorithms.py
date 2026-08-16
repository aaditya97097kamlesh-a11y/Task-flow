def insertion_sort(records, key):
    for i in range(1, len(records)):
        current = records[i]
        j = i - 1

        while j >= 0 and records[j][key] > current[key]:
            records[j + 1] = records[j]
            j -= 1

        records[j + 1] = current

    return records


def binary_search(records, target_value, key):
    low = 0
    high = len(records) - 1

    while low <= high:
        mid = (low + high) // 2

        if records[mid][key] == target_value:
            return mid
        elif records[mid][key] < target_value:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def linear_search(records, target_value, key):
    for i, record in enumerate(records):
        if record[key] == target_value:
            return i

    return -1