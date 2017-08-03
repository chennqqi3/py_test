#!/usr/bin/python
def merge(left, right):
    i, j = 0, 0
    result = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result


def merge_sort(array):
    if len(array) <= 1:
        return array
    num = len(array) / 2
    left = merge_sort(array[:num])
    right = merge_sort(array[num:])
    return merge(left, right)

if __name__ == '__main__':
    array = [2, 4, 32, 64, 34, 78, 23, 2345, 2345, 12, 1, 3]
    array = merge_sort(array)
    print array