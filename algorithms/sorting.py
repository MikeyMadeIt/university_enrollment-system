# This file has sorting functions - we implement our own sort (bubble sort)
# instead of using Python's built-in sorted() or .sort()

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