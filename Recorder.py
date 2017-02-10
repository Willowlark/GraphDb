from py2neo import Graph
from py2neo import Node
from py2neo import Relationship
from py2neo import Subgraph


class Recorder:
    graph = None

    def initialize(self, graph_address):
        self.graph = Graph(self, graph_address)

    def _subgraphify(self, graphs):
        base = graphs.pop(0)
        for graph in graphs:
            base = base | graph
        return base

    def add_topic(self, topics):
        listing = []
        for topic in topics:
            n = Node("Topic", name=topic)
            self.graph.create(n)
            listing.append(n)
        return self._subgraphify(listing)

    def fetch_topics(self, topics):
        listing = []
        for topic in topics:
            match = self.graph.find_one("Topic", property_key='name', property_value=topic)
            listing.append(match)
        return self._subgraphify(listing)

    def get_or_add_topic(self, topics):
        listing = []
        for topic in topics:
            if self.has_topic([topic]):
                listing.append(self.fetch_topics([topic]))
            else:
                listing.append(self.add_topic([topic]))
        return self._subgraphify(listing)

    def add_record(self, data):
        n = Node("Record", content=data)
        self.graph.create(n)
        return n

    def has_topic(self, topics):
        for topic in topics:
            if not self.graph.find_one("Topic", property_key="name", property_value=topic):
                return False
        return True

    def relate_then_push(self, topic_subgraph, record_node):
        related = self.relate(topic_subgraph, record_node)
        self.push(related)

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

    print rec.get_or_add_topic(["Trump"])
    print rec.get_or_add_topic(["Trump"])

    tops = rec.get_or_add_topic(["Hilary", "Trump"])
    recs = Node("Record", content="cats")

    rec.relate_then_push(tops, recs)
