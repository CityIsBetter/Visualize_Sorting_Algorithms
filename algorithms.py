# algorithms.py
import time

def bubble_sort(data, draw_data, tick_time):
    for i in range(len(data) - 1):
        for j in range(len(data) - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                draw_data(data, [x if x != j and x != j + 1 else 'red' for x in range(len(data))])
                time.sleep(tick_time)
    draw_data(data, ['green' for _ in range(len(data))])

def selection_sort(data, draw_data, tick_time):
    for i in range(len(data)):
        min_idx = i
        for j in range(i + 1, len(data)):
            if data[j] < data[min_idx]:
                min_idx = j
            draw_data(data, ['red' if x == j else 'yellow' if x == i else 'blue' for x in range(len(data))])
            time.sleep(tick_time)
        data[i], data[min_idx] = data[min_idx], data[i]
        draw_data(data, ['green' if x <= i else 'blue' for x in range(len(data))])
        time.sleep(tick_time)
    draw_data(data, ['green' for _ in range(len(data))])

def insertion_sort(data, draw_data, tick_time):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]
            j -= 1
            draw_data(data, ['red' if x == j or x == i else 'yellow' for x in range(len(data))])
            time.sleep(tick_time)
        data[j + 1] = key
        draw_data(data, ['green' if x <= i else 'blue' for x in range(len(data))])
        time.sleep(tick_time)
    draw_data(data, ['green' for _ in range(len(data))])

def merge_sort(data, draw_data, tick_time):
    merge_sort_alg(data, 0, len(data) - 1, draw_data, tick_time)

def merge_sort_alg(data, left, right, draw_data, tick_time):
    if left < right:
        mid = (left + right) // 2
        merge_sort_alg(data, left, mid, draw_data, tick_time)
        merge_sort_alg(data, mid + 1, right, draw_data, tick_time)
        merge(data, left, mid, right, draw_data, tick_time)

def merge(data, left, mid, right, draw_data, tick_time):
    left_copy = data[left:mid + 1]
    right_copy = data[mid + 1:right + 1]

    i = j = 0
    k = left

    while i < len(left_copy) and j < len(right_copy):
        if left_copy[i] <= right_copy[j]:
            data[k] = left_copy[i]
            i += 1
        else:
            data[k] = right_copy[j]
            j += 1
        k += 1
        draw_data(data, ['green' if x >= left and x <= right else 'blue' for x in range(len(data))])
        time.sleep(tick_time)

    while i < len(left_copy):
        data[k] = left_copy[i]
        i += 1
        k += 1
        draw_data(data, ['green' if x >= left and x <= right else 'blue' for x in range(len(data))])
        time.sleep(tick_time)

    while j < len(right_copy):
        data[k] = right_copy[j]
        j += 1
        k += 1
        draw_data(data, ['green' if x >= left and x <= right else 'blue' for x in range(len(data))])
        time.sleep(tick_time)

def quick_sort(data, draw_data, tick_time):
    quick_sort_alg(data, 0, len(data) - 1, draw_data, tick_time)

def quick_sort_alg(data, low, high, draw_data, tick_time):
    if low < high:
        pi = partition(data, low, high, draw_data, tick_time)
        quick_sort_alg(data, low, pi - 1, draw_data, tick_time)
        quick_sort_alg(data, pi + 1, high, draw_data, tick_time)

def partition(data, low, high, draw_data, tick_time):
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        if data[j] < pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
        draw_data(data, ['green' if x == i or x == j else 'yellow' if x == high else 'blue' for x in range(len(data))])
        time.sleep(tick_time)
    data[i + 1], data[high] = data[high], data[i + 1]
    draw_data(data, ['green' if x == i + 1 else 'blue' for x in range(len(data))])
    return i + 1

def heap_sort(data, draw_data, tick_time):
    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        heapify(data, n, i, draw_data, tick_time)

    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        draw_data(data, ['green' if x == i else 'blue' for x in range(len(data))])
        time.sleep(tick_time)
        heapify(data, i, 0, draw_data, tick_time)

def heapify(data, n, i, draw_data, tick_time):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and data[left] > data[largest]:
        largest = left

    if right < n and data[right] > data[largest]:
        largest = right

    if largest != i:
        data[i], data[largest] = data[largest], data[i]
        draw_data(data, ['red' if x == i or x == largest else 'blue' for x in range(len(data))])
        time.sleep(tick_time)
        heapify(data, n, largest, draw_data, tick_time)
