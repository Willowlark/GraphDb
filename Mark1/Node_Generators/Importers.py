import csv
from os.path import isfile

from Mark1.Node_Generators import Neo_Conversion


class Importer(object):
    """
    `Author`: Bill Clark

    The interface for an importer. An importer is an object that
    can import files of a given type.
    """

    def __init__(self):
        pass

    def import_file(self, pathname):
        pass


class CsvImporter(Importer):

    def import_file(self, pathname, lblkey=None):
        """
        `Author`: Bill Clark



        `pathname`: The path of the file to import.

        `lblkey`: The optional argument to be used to get the
         from the table.

        `return`: The subgraph made from the file data.
        """
        ret = None
        builder = Neo_Conversion.NodeBuilder()
        try:
            if lblkey is None:
                with open(pathname, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    lblkey = reader.next()[0].lower()
            with open(pathname, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    lrow = {}
                    for key, value in row.iteritems():
                        lkey = key.lower()
                        if isinstance(value, str): lvalue = value.lower()
                        lrow[lkey] = lvalue
                    row = lrow

                    if lblkey in row:  # Grab the value of the labelkey.
                        label = row[lblkey]
                        del row[lblkey]
                    else: label = lblkey
                    ret = builder.add_new_node(label, row, ret)
        except IOError:
            print "ERROR: File not found."
        return ret


class ImportFactory(object):
    """
    `Author`: Bill Clark

    A factory object that makes importers based of the file type.
    """

    def __init__(self):
        pass

    @staticmethod
    def get_importer(f):
        """
        `Author`: Bill Clark

        Returns a object that can import the file provided or
        none if nothing can.

        `f`: The file you're trying to import.
        """
        if not isfile(f):
            print "ERROR: That file doesn't exist."
            return None

        if f[-4:] == '.csv':
            return CsvImporter()
        else:
            print 'ERROR: No importer created for that file type.'
            return None
