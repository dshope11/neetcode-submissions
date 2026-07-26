# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.max_path_sum = float("-inf")

        def max_path_sum_subtree(node):
            if node is None:
                return 0
            left_gain = max(max_path_sum_subtree(node.left), 0)
            right_gain = max(max_path_sum_subtree(node.right), 0)
            self.max_path_sum = max(self.max_path_sum, node.val + left_gain + right_gain)
            return node.val + max(left_gain, right_gain)

        max_path_sum_subtree(root)
        return self.max_path_sum
