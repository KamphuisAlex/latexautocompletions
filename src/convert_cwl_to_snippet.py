import os
from classes import CWL, Completions, Completion

CWLs = []

# find all cwl files in the current folder
for filename in os.listdir(os.getcwd()):
    if filename.endswith(".cwl"):
        # call processing function
        abstract_cwl = CWL(filename)
        CWLs.append(abstract_cwl)

# make large collector class
comps = Completions()
for cwl in CWLs:
    for cmd in cwl.commands:
        c = Completion(cmd)
        comps.add(c)

fname = 'latexCompletes.sublime-completions'
if os.path.exists(fname):
    os.remove(fname)

f = open('latexCompletes.sublime-completions', 'w')
f.write(comps.toJSON())
f.close()
