# Manually implemented sorting algorithms in Python

def bubble_sort(elements):
    """
    Sorts the provided elements using a bubble sort
    :param elements: The list of elements to sort
    """
    length = len(elements)
    # iterate over all the elements to bubble the largest values to the end
    for outer in range(length-1):
        swapped = False
        # iterate over all the elements minus the outer index (outer equals the number of bubbled values)
        for inner in range(length-outer-1):
            # Swap (bubble up) the inner element if it is greater than the one after it
            if elements[inner] > elements[inner+1]:
                swapped = True
                elements[inner], elements[inner+1] = elements[inner+1], elements[inner]
        # if no bubbling performed in this loop, we can exit early
        if not swapped:
            break


def merge_sort(elements):
    """
    Sorts the provided elements using a merge sort
    :param elements: The list of elements to sort
    """
    size = len(elements)
    if size > 1:
        # Identify the midpoint and split the list into two
        middle = size // 2
        left_elements = elements[:middle]
        right_elements = elements[middle:]
        # Recursively sort the left and right lists
        merge_sort(left_elements)
        merge_sort(right_elements)
        # Now use indexes into the left, right, and current lists to sort
        index_elements = 0
        index_left = 0
        index_right = 0

        left_size = len(left_elements)
        right_size = len(right_elements)

        while index_left < left_size and index_right < right_size:
            if left_elements[index_left] < right_elements[index_right]:
                elements[index_elements] = left_elements[index_left]
                index_left += 1
            else:
                elements[index_elements] = right_elements[index_right]
                index_right += 1
            index_elements += 1
        # At this point only one of the two sub-lists need to be copied into the final list
        while index_left < left_size:
            elements[index_elements] = left_elements[index_left]
            index_left += 1
            index_elements += 1

        while index_right < right_size:
            elements[index_elements] = right_elements[index_right]
            index_right += 1
            index_elements += 1
