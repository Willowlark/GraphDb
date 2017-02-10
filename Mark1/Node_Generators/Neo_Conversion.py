from py2neo import Node


class NodeBuilder(object):

    def __init__(self):
        pass

    def _generate(self, label, props):
        """
        `Author`: Bill Clark

        Creates a node object and returns it.

        `label`: the label of the node.

        `props`: the property dictionary for the node.

        `return`: the node generated.
        """
        n = Node(label, **props)
        #for key, value in props.items():
        #    n[key] = value
        return n

    def make_node(self, label, props):
        """
        `Author`: Bill Clark

        Calls the internal node generator.

        `label`: the label of the node.

        `props`: the property dictionary for the node.

        `return`: the node generated.
        """
        return self._generate(label, props)

    def add_new_node(self, label, props, subgraph=None):
        """
        `Author`: Bill Clark

        Calls the internal node generator. When the node is retrieved,
        it is either merged with the provided subgraph or returned
        normally.

        `label`: the label of the node.

        `props`: the property dictionary for the node.

        `return`: the node generated.
        """
        ret = self.make_node(label, props)
        return ret if subgraph is None else ret | subgraph
