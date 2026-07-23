# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        self.pre_idx = 0
        index_map = {}

        def build(in_lo, in_hi):
            if in_lo > in_hi:
                return None
            root_val = preorder[self.pre_idx]
            self.pre_idx += 1
            root = TreeNode(root_val)
            mid = index_map[root_val] # position of root in inorder
            root.left  = build(in_lo, mid - 1) # left window: everything before root
            root.right = build(mid + 1, in_hi) # right window: everything after root
            return root

        for idx, val in enumerate(inorder):
            index_map[val] = idx

        root = build(0, len(inorder)-1)
        return root
