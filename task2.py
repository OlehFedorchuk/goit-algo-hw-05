from typing import List, Tuple, Optional

def binary_search_with_upper_bound(arr: List[float], target: float) -> Tuple[int, Optional[float]]:
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2

        if arr[mid] == target:
            return iterations, arr[mid]
        elif arr[mid] < target:
            low = mid + 1
        else:
            upper_bound = arr[mid]
            high = mid - 1

    return iterations, upper_bound


arr = [0.5, 1.2, 2.3, 3.7, 4.4, 5.5, 6.8]
target = 3.0

result = binary_search_with_upper_bound(arr, target)
print(result)  # Наприклад: (3, 3.7)