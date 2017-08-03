#!/usr/bin/python
# coding=utf-8

"""
    插入排序
"""


def insert_sort(array):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            j -= 1

        array[j + 1] = key

if __name__ == "__main__":
    array = [2, 4, 32, 64, 34, 78, 23, 2345, 2345, 12, 1, 3]

    insert_sort(array)
    for a in array:
        print a