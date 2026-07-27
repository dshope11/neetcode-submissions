# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Codec:    

    # Encodes a tree to a single string.
    def serialize(self, root: Optional[TreeNode]) -> str:
        result = []
        def dfs_serialize(node):
            if node is None:
                result.append("N")
                return
            result.append(str(node.val))
            dfs_serialize(node.left)
            dfs_serialize(node.right)
            return
        dfs_serialize(root)
        return ",".join(result)
        
    # Decodes your encoded data to tree.
    def deserialize(self, data: str) -> Optional[TreeNode]:
        self.i = 0
        data_list = data.split(",")
        def dfs_deserialize(data_list):
            c = data_list[self.i]
            if c == "N":
                node = None
                self.i += 1
            else:
                node = TreeNode(int(c))
                self.i += 1
                node.left = dfs_deserialize(data_list)
                node.right = dfs_deserialize(data_list)
            return node
        return dfs_deserialize(data_list)
