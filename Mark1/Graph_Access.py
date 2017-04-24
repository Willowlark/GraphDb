from py2neo import Graph
from py2neo import Relationship
from py2neo import Walkable

class GraphManager(object):
    """
    `Author`: Bill Clark

    This is a class that handles interactions with a remote graph.
    It both interacts with a neo4j graph interface, and manages the
    downloaded nodes from the interface. This is simply an
    implementation of py2neo, made easier to use our purposes."""

    def __init__(self, address):
        """
        `Author`: Bill Clark

        During class initialization, we connect to the neo4j instance
        via the Graph class in py2neo. We also initialize the committed
        array here. The committed array will contained matched subgraphs
        of nodes and relationships. We pass these subgraphs to relate
        to generate relationships between nodes.

        `address`: A string containing the web address of the neo4j server.
        """
        self.graph = Graph(address)
        self.committed = []
        self.uncommitted = None
        # print self.graph.data("MATCH (a:Person) RETURN a.Name, a.age")

    def sync_new(self):
        """
        `Author`: Bill Clark

        This method uploads the uncommitted subgraph to the neo4j
        interface. No node in uncommitted should exist in the 4j
        interface.

        `return`: The index the subgraph is stored in.
        """

        if self.uncommitted is not None:
            self.graph.create(self.uncommitted)
            ret = self._track(self.uncommitted)
            self.uncommitted = None
            return ret

    def add_new(self, subgraph):
        """
        `Author`: Bill Clark

        This method takes a subgraph of nodes or relationships
        and adds them to uncommitted. If uncommitted is none and
        undeclared, the subgraph supplied is made uncommitted.

        `subgraph`: A subgraph of nodes to be added to uncommitted.
        """
        if self.uncommitted is not None: self.uncommitted = self.uncommitted | subgraph
        else: self.uncommitted = subgraph

    def subgraph_exists(self, subgraph):
        pass

    def retrieve(self, index):
        """
        `Author`: Bill Clark

        Polices the input and retrieves a subgraph from committed.

        `index`: The index to retrieve from the committed array.

        `return`: Returns uncommitted if the index given is invalid, or
         returns the subgraph at index index.
        """
        if index < 0 or index >= len(self.committed):
            if self.uncommitted is None:
                return False # No subgraph founded
            return self.uncommitted
        else: return self.committed[index]

    # def replace(self, subgraph, index):
    #     if index < 0 or index >= len(self.committed):
    #         self.uncommitted = subgraph
    #     else: self.committed[index] = subgraph

    def match_node(self, label, props, rlabel, elabel, eprops):
        """
        `Author`: Bill Clark

        Runs a match command via cypher on the neo4j. The user will
        be prompted for a label to search for a node. They will then
        be able to provide properties for that node. Newline advances
        to the label for the relationship. Another new line searches
        only for a node, if a label is added to the relationship the first
        two prompts are repeated for the tail node. The match command
        is then run and all the matched objects are returned as a
        subgraph.

        `label`: The label to search for on the first node.

        `props`: A dictionary of properties on the first node.

        `rlabel`: The label on the relationship. Optional.

        `elabel`: The label for the second node.

        `eprops`: the properties on the second node.

        `return`: A subgraph of everything matched by the statement.
        """
        propstr = self._props_as_str(props)
        label = ':'+label if label else ""
        cipher = "MATCH (m{0}{1})".format(label, propstr)
        cipher2 = " RETURN m"

        if rlabel:
            cipher+=("-[r{0}]->").format(":"+rlabel if rlabel else "")
            cipher2+=", r"

        if rlabel and elabel:
            propstr = self._props_as_str(eprops)
            elabel = "" if not elabel else ':'+elabel
            cipher+=("(n{0}{1})".format(elabel, propstr))
            cipher2+=", n"

        print cipher+cipher2
        data = self.graph.data(cipher+cipher2)
        # [{u'r': (b1231c4)-[:KNOWS]->(e0bc856), u'm': (b1231c4:Person {bearing:"40",lat:"40",long:"32",name:"bill clark",percentmatched:"40"}), u'n': (e0bc856:Person {bearing:"40",lat:"40",long:"32",name:"bob seedorf",percentmatched:"12"})}]
        # convert string to nodes.
        enter = None
        for match in data:
            for key in match:
                enter = match[key] if enter is None else enter | match[key]
                print match[key]
        #print enter
        return self._track(enter)

    def upload_subgraph(self, index):
        """
        `Author`: Bill Clark

        Uploads the subgraph at index index in the committed area.
        Things in a committed subgraph will have parallels in the graph
        so this updates, does not create.

        `index`: Index of the subgraph to update.
        """
        self.graph.push(self.committed[index])

    def relate(self, index):
        """
        `Author`: Bill Clark

        Test implementation. Will be used to build relationships
        between nodes.

        `index`: Index of the subgraph to relate nodes.
        """
        relations = None
        prior = list(self.committed[index].relationships())
        for node in self.committed[index].nodes():
            for comp in self.committed[index].nodes():
                if node == comp or Relationship(comp, node) in prior:
                    continue
                for key in node:
                    if key in comp and node[key] == comp[key]:
                        r = Relationship(node, key, comp)
                        relations = r if relations is None else relations | r
                        prior.append(r)
                        break
        self.add_new(relations)

    @staticmethod
    def _props_as_str(props):
        """
        `Author`: Bill Clark

        Used to turn a dictionary of names and their values into
         a string to be put into a cypher command.

        `props`: The dictionary to convert.

        `return`: String representation of the dictionary.
        """
        propstr = ','.join([x+':' + (y if y.isdigit() else ('"'+y+'"'))
                            for x, y in props.iteritems()])
        if propstr is not "": propstr = ' {'+propstr+'}'
        return propstr

    def _track(self, subgraph):
        """
        `Author`: Bill Clark

        adds a subgraph to the committed array. Handles the case
        that a subgraph has a duplicate in the array. Otherwise
        a new subgraph is appended. finally the index is returned.


        `subgraph`: subgraph to add to the committed list.

        `return`: the index of this subgraph in the list.
        """
        if subgraph in self.committed:
            return self.committed.index(subgraph)
        self.committed.append(subgraph)
        return self.committed.index(subgraph)
