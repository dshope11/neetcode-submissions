class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        min_so_far = float("inf")
        max_profit = 0

        for price in prices:
            min_so_far = min(min_so_far, price)
            max_profit = max(max_profit, price - min_so_far)

        if max_profit < 0:
            return 0
        else:
            return max_profit