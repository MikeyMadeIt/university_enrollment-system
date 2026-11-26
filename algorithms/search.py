def linear_search(items, key, value):
    """Return index of first matching item, or -1."""
    for i, item in enumerate(items):
        if item.get(key) == value:
            return i
    return -1


def binary_search(sorted_items, key, value):
    """Binary search on a list pre-sorted by `key`. Returns index or -1."""
    lo, hi = 0, len(sorted_items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        current = sorted_items[mid].get(key)
        if current == value:
            return mid
        if current < value:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1