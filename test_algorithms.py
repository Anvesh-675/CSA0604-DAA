
from linear_search import linear_search
from binary_search import binary_search
from hash_search import build_hash, hash_search


def test_all():
    records = [1001, 1002, 1003, 1004, 1005]

    for target in [1001, 1003, 1005, 9999]:
        expected = records.index(target) if target in records else -1

        linear_index, _ = linear_search(records, target)
        binary_index, _ = binary_search(
            records, target, 0, len(records) - 1
        )

        assert linear_index == expected
        assert binary_index == expected

    # Empty list
    assert linear_search([], 1001)[0] == -1
    assert binary_search([], 1001, 0, -1)[0] == -1

    # Hash search
    record_set = build_hash(records)
    assert hash_search(record_set, 1001) is True
    assert hash_search(record_set, 9999) is False

    print("Linear Search: PASS")
    print("Recursive Binary Search: PASS")
    print("Hash Search: PASS")
    print("Empty List Test: PASS")
    print("First, Middle, Last and Missing Record Tests: PASS")
    print("\nAll implementation tests passed!")


if __name__ == "__main__":
    test_all()
