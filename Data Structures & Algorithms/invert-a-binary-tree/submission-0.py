# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

def invert_node(node: Optional[TreeNode]) -> None:
    if node is None:
        return
    tmp = node.left
    node.left = node.right
    node.right = tmp
    invert_node(node.left)
    invert_node(node.right)

class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        invert_node(root)
        return root