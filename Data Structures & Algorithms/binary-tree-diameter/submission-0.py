# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        self.diameter = 0

        def height(node):
            node_height = 0
            if node is not None:
                left_height = height(node.left)
                right_height = height(node.right)
                node_height = 1 + max(left_height, right_height)
                self.diameter = max(self.diameter, left_height + right_height)
            return node_height

        height(root)
        return self.diameter