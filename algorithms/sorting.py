"""Bubble-sort helpers used by the enrollment application."""


def _order_value(value):
    """Compare text without regard to case while leaving other values intact."""
    return value.casefold() if isinstance(value, str) else value


def bubble_sort(items, key):
    """Return a stable copy of mapping records sorted by ``key``."""
    sorted_items = list(items)
    count = len(sorted_items)

    for i in range(count):
        swapped = False
        for j in range(count - i - 1):
            left = _order_value(sorted_items[j].get(key))
            right = _order_value(sorted_items[j + 1].get(key))
            if (left is None and right is not None) or (
                left is not None and right is not None and left > right
            ):
                sorted_items[j], sorted_items[j + 1] = sorted_items[j + 1], sorted_items[j]
                swapped = True
        if not swapped:
            break

    return sorted_items


def bubble_sort_by_name(records):
    """Return a copy of records in case-insensitive name order."""
    return bubble_sort(records, "name")


def bubble_sort_courses_by_capacity(courses_list):
    """Return a copy of (course_code, course_info) pairs by capacity."""
    sorted_courses = list(courses_list)
    count = len(sorted_courses)

    for i in range(count):
        swapped = False
        for j in range(count - i - 1):
            if sorted_courses[j][1]["capacity"] > sorted_courses[j + 1][1]["capacity"]:
                sorted_courses[j], sorted_courses[j + 1] = sorted_courses[j + 1], sorted_courses[j]
                swapped = True
        if not swapped:
            break

    return sorted_courses
