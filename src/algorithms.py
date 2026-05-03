"""Algorithmic homework tasks."""


class Solution:
    """Collection of algorithmic solutions."""

    def climb_stairs(self, n: int) -> int:
        """Return count of unique ways to climb n stairs.

        Complexity analysis:
        - Time: O(n), because we compute each state from 1..n once.
        - Space: O(1), because we store only two previous values.
        """
        if n <= 2:
            return n
        prev2, prev1 = 1, 2
        for _ in range(3, n + 1):
            prev2, prev1 = prev1, prev1 + prev2
        return prev1

    def reverse_string(self, s: list[str]) -> None:
        """Reverse list of characters in-place.

        Complexity analysis:
        - Time: O(n), we swap pairs from both ends.
        - Space: O(1), only constant extra variables used.
        """
        left, right = 0, len(s) - 1
        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1

    def two_sum(self, nums: list[int], target: int) -> list[int]:
        """Return indices of two numbers that sum to target.

        Complexity analysis:
        - Time: O(n), one pass over nums with hash table lookups.
        - Space: O(n), hash table can store up to n elements.
        """
        seen: dict[int, int] = {}
        for index, value in enumerate(nums):
            need = target - value
            if need in seen:
                return [seen[need], index]
            seen[value] = index
        raise ValueError("No valid pair found")
