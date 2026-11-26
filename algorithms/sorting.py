# This file has sorting functions - we implement our own sort (bubble sort)
# instead of using Python's built-in sorted() or .sort()

def bubble_sort(items, key):
    sorted_list = list(items)
    n = len(sorted_list)

    for i in range(n):
        for j in range(0, n - i - 1):
            value1 = sorted_list[j].get(key)
            value2 = sorted_list[j + 1].get(key)
            if value1 is None:
                should_swap = value2 is not None
            elif value2 is None:
                should_swap = False
            else:
                if isinstance(value1, str) and isinstance(value2, str):
                    value1 = value1.lower()
                    value2 = value2.lower()
                should_swap = value1 > value2
            if should_swap:
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]

    return sorted_list


def bubble_sort_by_name(records):
    sorted_list = list(records)
    n = len(sorted_list)

    for i in range(n):
        for j in range(0, n - i - 1):
            name1 = sorted_list[j]["name"].lower()
            name2 = sorted_list[j + 1]["name"].lower()
            if name1 > name2:
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]

    return sorted_list

def bubble_sort_courses_by_capacity(courses_list):
    sorted_list = list(courses_list)
    n = len(sorted_list)

    for i in range(n):
        for j in range(0, n - i - 1):
            cap1 = sorted_list[j][1]["capacity"]
            cap2 = sorted_list[j + 1][1]["capacity"]
            if cap1 > cap2:
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]

    return sorted_list
