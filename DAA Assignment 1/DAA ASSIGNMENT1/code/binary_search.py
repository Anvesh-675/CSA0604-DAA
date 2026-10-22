def binary_search(records, target, left, right):
    if left > right:
        return -1, 0

    mid = (left + right) // 2

    if records[mid] == target:
        return mid, 1

    if target < records[mid]:
        index, count = binary_search(
            records, target, left, mid - 1
        )
    else:
        index, count = binary_search(
            records, target, mid + 1, right
        )

    return index, count + 2


if __name__ == "__main__":
    records = [1001, 1002, 1003, 1004, 1005]
    target = 1004

    index, comparisons = binary_search(
        records, target, 0, len(records) - 1
    )

    print("Target:", target)
    print("Index:", index)
    print("Comparisons:", comparisons)