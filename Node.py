class Node:
    """
    Represents a node in a graph or search algorithm.

    Attributes:
    - name: The identifier or name of the node.
    - path: The path leading to the node (default is None).
    - cost: The cost associated with reaching the node (default is None).
    """

    def __init__(self, name, path=None, cost=None):
        """
        Initializes a new instance of the Node class.

        Parameters:
        - name: The identifier or name of the node.
        - path: The path leading to the node (default is None).
        - cost: The cost associated with reaching the node (default is None).
        """
        self.name = name
        self.path = path
        self.cost = cost
