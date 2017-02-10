# * Created by Eliakah kakou
# csv manager.
# This class runs all of the modules in the right sequential
# order depending on the input
import sys

#def main():

class csv_manager:
    #constructor
    def __init__(self, fileName,extension,  fieldnames):
        self.fieldnames = fieldnames
        self.extension = extension
        self.fileName = fileName
        self.name = self.fileName + "." + self.extension

    #create file
    def createFile(self):
        try:

            file = open(self.name, 'a')
            file.write(self.fieldnames)
            file.close()
        except:
            print("error occured")
            sys.exit(0)

    #adding a row to the file
    def add_row(self, row):
        with open(self.name, "a") as file:
            file.write(row)
        file.close()

