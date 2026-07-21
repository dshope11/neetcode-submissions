# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

def isValidBSTSubtree(node: Optional[TreeNode], left: float, right: float) -> bool:
    if node is None:
        return True
    if not left < node.val < right:
        return False
    return isValidBSTSubtree(node.left, left, node.val) and isValidBSTSubtree(node.right, node.val, right)

class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        left = float("-inf")
        right = float("inf")
        return isValidBSTSubtree(root, left, right)
