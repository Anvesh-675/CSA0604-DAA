def linear_search(records, target):
    comparisons = 0

    for i, record in enumerate(records):
        comparisons += 1
        if record == target:
            return i, comparisons

    return -1, comparisons


if __name__ == "__main__":
    records = [1001, 1002, 1003, 1004, 1005]
    target = 1004

    index, comparisons = linear_search(records, target)
    print("Target:", target)
    print("Index:", index)
    print("Comparisons:", comparisons)
