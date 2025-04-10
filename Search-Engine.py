from typing import List

def insert(data, s: str)-> None:
    if s == "":
        return
    if len(s) == 1:
        if s in data:
            data[s][1] = True
        else:
            data[s] = [{}, True]
    if s[0] in data:
        insert(data[s[0]][0], s[1:])
    else:
        data[s[0]]= [{}, False]
        insert(data[s[0]][0], s[1:])


def count_words(data)->int:
    """
    Returns the number of words encoded in data. You may assume
    data is a valid trie.

    >>> data = {}
    >>> insert(data, "test")
    >>> insert(data, "testing")
    >>> insert(data, "doc")
    >>> insert(data, "docs")
    >>> insert(data, "document")
    >>> insert(data, "documenting")

    >>> count_words(data)
    6
    """

    count = 0

    for key, value in data.items():
        if value[1]:
            count += 1
        count += count_words(value[0])

    return count


def contains(data, s: str)-> bool:
    """
    Returns True if and only if s is encoded within data. You may
    assume data is a valid trie.

    >>> data = {}
    >>> insert(data, "tree")
    >>> insert(data, "trie")
    >>> insert(data, "try")
    >>> insert(data, "trying")
    
    >>> contains(data, "try")
    True
    >>> contains(data, "trying")
    True
    >>> contains(data, "the")
    False
    """
    """
    # if string is empty, return False (not in trie)
    if s == "":  
        return False

    # if first character of s is in current trie
    if s[0] in data:  
        if len(s) == 1:  # if this is the last character in s
            return data[s[0]][1]  # return True if it's marked as the end of a word
        # else, continue checking in the subtree for the rest of the string
        return contains(data[s[0]][0], s[1:])
    
    return False
    """
    
    current_node = data  

    for char in s:  
        if char in current_node:  
            current_node = current_node[char][0]  
        else:
            return False  

    return current_node and current_node[1]


def height(data)->int:
    """
    Returns the length of longest word encoded in data. You may
    assume that data is a valid trie.

    >>> data = {}
    >>> insert(data, "test")
    >>> insert(data, "testing")
    >>> insert(data, "doc")
    >>> insert(data, "docs")
    >>> insert(data, "document")
    >>> insert(data, "documenting")

    >>> height(data)
    11
    """

    # if trie is empty, height is 0
    if not data:  
        return 0

    max_depth = 0
    for key, value in data.items():
        # find the height of the current branch recursively
        subtree_height = height(value[0])  
        max_depth = max(max_depth, 1 + subtree_height)  

    return max_depth
    

def count_from_prefix(data, prefix: str)-> int:
    """
    Returns the number of words in data which starts with the string
    prefix, but is not equal to prefix. You may assume data is a valid
    trie.

    data = {}
    >>> insert(data, "python")
    >>> insert(data, "pro")
    >>> insert(data, "professionnal")
    >>> insert(data, "program")
    >>> insert(data, "programming")
    >>> insert(data, "programmer")
    >>> insert(data, "programmers")

    >>> count_from_prefix(data, 'pro')
    5
    """

    if prefix == "":
        return 0

    # go through the prefix node
    current_node = data
    for char in prefix:
        if char not in current_node:
            return 0  # if prefix is not found in the trie
        current_node = current_node[char][0]

    # count all words in the sub-trie starting at the current node
    def count_subtrie(node, is_root=True):
        count = 0
        for key, value in node.items():
            if value[1]:  # if this is the end of a word
                count += 1
            count += count_subtrie(value[0], is_root=False)
        return count

    # subtract 1 if the prefix itself is a word
    total_words = count_subtrie(current_node)
    if current_node and data.get(prefix[0], [None, False])[1] and len(prefix) > 1:
        total_words -= 1

    return total_words
    

def get_suggestions(data, prefix:str)-> List[str]:
    """
    Returns a list of words which are encoded in data, and starts with
    prefix, but is not equal to prefix. You may assume data is a valid
    trie.

    data = {}
    >>> insert(data, "python")
    >>> insert(data, "pro")
    >>> insert(data, "professionnal")
    >>> insert(data, "program")
    >>> insert(data, "programming")
    >>> insert(data, "programmer")
    >>> insert(data, "programmers")

    >>> get_suggestions(data, "progr")
    ['program', 'programming', 'programmer', 'programmers']
    """

    current_node = data
    for char in prefix:
        if char not in current_node:
            return []  # prefix not found in the trie
        current_node = current_node[char][0]

    # gather all words in the sub-trie
    def collect_words(node, current_prefix):
        suggestions = []
        for key, value in node.items():
            new_prefix = current_prefix + key
            if value[1]:  # if this node marks the end of a word
                suggestions.append(new_prefix)
            suggestions.extend(collect_words(value[0], new_prefix))
        return suggestions

    # collect all suggestions from the sub-trie
    suggestions = collect_words(current_node, prefix)

    # remove the prefix itself if it is a valid word
    if prefix in suggestions:
        suggestions.remove(prefix)

    return suggestions

    




    

    
