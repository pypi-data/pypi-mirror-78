import ast
import csv
def strincsvtodict(path = None):
    """ convert list in string to dict """
    reader = csv.reader(open(path, 'r'))
    return {k:ast.literal_eval(v)  for k,v in reader}