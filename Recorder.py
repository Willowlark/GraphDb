from py2neo import Graph
from py2neo import Node
from py2neo import Relationship

class Recorder:
    graph = None
    confirm_mode = False

    def initialize(self, graph_address):
        self.graph = Graph(self, graph_address)

    def _subgraphify(self, graph_list):
        base = graph_list.pop(0)
        for graph in graph_list:
            base = base | graph
        return base

    def add_topic(self, topics):
        listing = []
        for topic in topics:
            n = Node("Topic", name=topic)
            if self.confirm_mode: self.graph.create(n)
            listing.append(n)
        return self._subgraphify(listing)

    def fetch_topics(self, topics):
        listing = []
        for topic in topics:
            match = self.graph.find_one("Topic", property_key='name', property_value=topic)
            listing.append(match)
        return self._subgraphify(listing)

    def get_or_add_topics(self, topics):
        listing = []
        for topic in topics:
            if self.has_topic([topic]):
                listing.append(self.fetch_topics([topic]))
            else:
                listing.append(self.add_topic([topic]))
        return self._subgraphify(listing)

    def add_record(self, data):
        n = Node("Record", content=data)
        if self.confirm_mode: self.graph.create(n)
        return n

    def has_topic(self, topics):
        for topic in topics:
            if not self.graph.find_one("Topic", property_key="name", property_value=topic):
                return False
        return True

    def relate_then_push(self, topic_subgraph, record_node):
        related = self.relate(topic_subgraph, record_node)
        if self.confirm_mode:
            print related
        if self.confirm_mode and raw_input("Confirm with y: ") != "y": return -1

        self.push(related)
        return 0

    def relate(self, topic_subgraph, record_node):
        listing = []
        for node in topic_subgraph.nodes():
            listing.append(Relationship(record_node, 'Related', node))
        return self._subgraphify(listing) | record_node

    def push(self, subgraph):
        self.graph.push(subgraph)
        self.graph.create(subgraph)

if __name__ == "__main__":
    rec = Recorder()
    rec.initialize('http://localhost:7474/db/data/')

    print rec.get_or_add_topics(["Trump"])
    print rec.get_or_add_topics(["Trump"])

    tops = rec.get_or_add_topics(["Hilary", "Trump"])
    recs = Node("Record", content="cats")

    rec.relate_then_push(tops, recs)
