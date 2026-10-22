def build_hash(records):
    return set(records)


def hash_search(record_set, target):
    return target in record_set


if __name__ == "__main__":
    records = [1001, 1002, 1003, 1004, 1005]
    record_set = build_hash(records)
    target = 1004

    print("Target:", target)
    print("Found:", hash_search(record_set, target))
