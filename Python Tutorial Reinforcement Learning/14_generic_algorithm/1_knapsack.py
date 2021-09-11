# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

"""
solve the knapsack problem
"""


def knapsack(items, max_weight):
    """
    :param items: list of tuples (weight, value)
    :param max_weight: max weight of knapsack
    :return: tuple (max value, list of items)
    """
    # create a matrix of size (items + 1) * (max_weight + 1)
    matrix = [[0 for _ in range(max_weight + 1)] for _ in range(len(items) + 1)]

    # fill the matrix
    for i in range(1, len(items) + 1):
        for j in range(1, max_weight + 1):
            # if the weight of the current item is greater than the max weight
            # of the knapsack, we take the value of the top left cell
            if items[i - 1][0] > j:
                matrix[i][j] = matrix[i - 1][j]
            else:
                # take the max between the value of the top left cell and the
                # value of the current item + the value of the cell on the top
                # left of the cell corresponding to the weight of the current
                # item minus the weight of the current item
                matrix[i][j] = max(
                    matrix[i - 1][j],
                    items[i - 1][1] + matrix[i - 1][j - items[i - 1][0]],
                )

    # return the max value and the list of items
    return matrix[-1][-1], get_items(matrix, items)


def get_items(matrix, items):
    """
    :param matrix: matrix of the knapsack problem
    :param items: list of tuples (weight, value)
    :return: list of items
    """
    # get the max value
    max_value = matrix[-1][-1]

    # get the index of the first item with a value equal to the max value
    i = len(items) - 1
    while i > 0 and matrix[i][-1] != max_value:
        i -= 1

    # get the index of the first item with a weight equal to the max weight
    # of the knapsack
    j = len(matrix[0]) - 1
    while j > 0 and matrix[i][j] != max_value:
        j -= 1

    # get the list of items
    items_list = []
    while i > 0 and j > 0:
        if matrix[i][j] != matrix[i - 1][j]:
            items_list.append(items[i - 1])
            j -= items[i - 1][0]
        i -= 1

    return items_list


if __name__ == "__main__":
    items = [(1, 1), (2, 6), (5, 18), (6, 22), (7, 28)]
    max_weight = 11
    print(knapsack(items, max_weight))
