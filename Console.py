import cmd
import re
import sys

import Graph_Access
from Mark1.Node_Generators.Importers import ImportFactory


class Console(cmd.Cmd):

    def __init__(self, address):
        """
        `Author`: Bill Clark

        Initializes the console to be used to interact with the graph.


        `address`: The address of the graph to interact with.
        """
        cmd.Cmd.__init__(self)
        self.manager = Graph_Access.GraphManager(address)

        self.subgraph = None
        self.subindex = None

    def do_load(self,data):
        """
        `Author`: Bill Clark

        Creates an importer based on the given file and uses it
        to import that file's nodes.

        `data`: The filepath to the file to be loaded.
        """
        f, other = self._split_path_data(data)
        importer = ImportFactory.get_importer(f)
        if importer is not None:
            self.manager.add_new(importer.import_file(f, other))

    def do_create(self, _):
        """
        `Author`: Bill Clark

        Runs synchronize on the uncommitted nodes. This creates the
         nodes created locally on the server.
        """
        print self.manager.sync_new()

    def do_print(self, line):
        """
        `Author`: Bill Clark

        Print the subgraph at the index give in line. If line isn't
        a digit, -1 is used which gets the uncommited index.

        `line`: string of the integer index of subgraph to print.
        """
        if line.isdigit(): line = int(line)
        else: line = -1

        sub = self.manager.retrieve(line)
        if sub is False: print "ERROR: No subgraph found."
        else:
            for x in sub.nodes():
                print x
            for x in sub.relationships():
                print x

    # def do_set(self, line):
    #     if line.isdigit(): line = int(line)
    #     else: line = -1
    #
    #     if self._set_graph_exists():  # save possible changes
    #         self.manager.committed[self.subindex] = self.subgraph
    #     self.subgraph = self.manager.retrieve(line)
    #     self.subindex = line

    def do_find(self, _):
        """
        `Author`: Bill Clark

        Interactive method that gets the values required to do a match
        operation via cypher. It prints the index of the subgraph
        match in the committed array.
        """
        label, props = self._ask_node()
        rlabel = ""
        elabel, eprops = "", {}

        n = raw_input("\nAdd a relationship? Newline to finish.> ")
        if (n != ""):
            rlabel = n
            elabel, eprops = self._ask_node()

        print self.manager.match_node(label, props, rlabel, elabel, eprops)

    def do_relate(self, line):
        """
        `Author`: Bill Clark

        runs the relation bulding method in the graph manager.

        `line`: the string of the index in committed to relate.
        """
        if line.isdigit():
            self.manager.relate(int(line))
        else:
            print "Not an index."

    def do_upload(self, line):
        """
        `Author`: Bill Clark

        Uploads the uncommitted subgraph to the server.

        `line`: the string of the index in committed to relate.
        """
        if line.isdigit():
            self.manager.upload_subgraph(int(line))
        else:
            print "Not an index."

    @staticmethod
    def _ask_node():
        """
        `Author`: Bill Clark

        Asks for the defining features of a node interactively.
        Requires a label to be given, then takes any number of
        keys and values for the node's properties.

        `return`: The label and props dictionary.
        """
        props = {}
        label = raw_input("Input label to search with > ")

        key = "init"
        while key is not "":
            key = raw_input("Input property key to search with, newline to finish > ")
            if key is not "":
                val = raw_input("Input property value to search with > ")
                props[key] = val
        return label, props

    @staticmethod
    def _split_path_data(data):
        """
        `Author`: Bill Clark

        Splits the string into a file address and the remainder.

        `data`: The string to split.

        `return`: The file address and the remaining string.
        """
        r = re.match("([^.]*\..{3}) (.*)", data)
        return r.groups() if r else (data, None)

if __name__ == "__main__":
    c = Console(sys.argv[1])
    c.cmdloop()
