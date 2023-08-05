
import csv
from pynvn.string import no_accent_vietnamese
def dicttocsv (dictl = None, path = None):
    """ dict to csv """
    a_file = open(path, "w")
    writer = csv.writer(a_file,lineterminator='\n')
    for key, value in dictl.items():
        key = no_accent_vietnamese(key)
        writer.writerow([key, value])
    a_file.close()
