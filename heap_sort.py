def heapify(array, heap_size, root_index, key, reverse=False):
    """Преобразует поддерево в кучу."""
    largest = root_index
    left_child = 2 * root_index + 1
    right_child = 2 * root_index + 2

    if left_child < heap_size:
        left_value = array[left_child][key]
        root_value = array[largest][key]
        if ((not reverse and left_value > root_value) or
            (reverse and left_value < root_value)):
            largest = left_child

    if right_child < heap_size:
        right_value = array[right_child][key]
        largest_value = array[largest][key]
        if ((not reverse and right_value > largest_value) or
            (reverse and right_value < largest_value)):
            largest = right_child

    if largest != root_index:
        array[root_index], array[largest] = array[largest], array[root_index]
        heapify(array, heap_size, largest, key, reverse)

def heap_sort(array, key, reverse=False):
    """Сортирует список словарей по указанному ключу с помощью пирамидальной сортировки."""
    if not array:
        return

    length = len(array)

    # Построение max-heap (или min-heap, если reverse=True)
    for index in range(length // 2 - 1, -1, -1):
        heapify(array, length, index, key, reverse)

    # Извлечение элементов из кучи
    for index in range(length - 1, 0, -1):
        array[0], array[index] = array[index], array[0]
        heapify(array, index, 0, key, reverse)
