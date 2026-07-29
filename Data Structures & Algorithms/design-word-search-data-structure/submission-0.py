class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_word: bool = False

class WordDictionary:

    def __init__(self) -> None:
        self.root: TrieNode = TrieNode()

    def addWord(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.is_word = True

    def search(self, word: str) -> bool:

        def dfs(i: int, node: TrieNode) -> bool:
            if i == len(word):
                return node.is_word
            ch = word[i]
            if ch != '.':
                if ch not in node.children:
                    return False
                return dfs(i+1, node.children[ch])
            else:
                match = False
                for child in node.children.values():
                    match = match or dfs(i+1, child)
                return match

        return dfs(0, self.root)
