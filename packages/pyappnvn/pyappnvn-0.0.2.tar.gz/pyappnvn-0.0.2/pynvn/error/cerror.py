import re
pattern = re.compile("[0-9]")
P = input ("IMNAME: ")
print (pattern.match(P) is not None)
