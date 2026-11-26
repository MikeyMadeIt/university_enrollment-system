def bubble_sort(items, key):
    arr = list(items)
    n = len(arr)
    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j].get(key) > arr[j + 1].get(key):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def merge_sort(items, key):
    items = list(items)
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)
    return _merge(left, right, key)


def _merge(left, right, key):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i].get(key) <= right[j].get(key):
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result