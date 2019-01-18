#!/usr/bin/env python

"""update_nml.py for Ramses
by Andrew Pontzen

Run this python script from your job submission script, before starting Ramses, and it will update
your .nml file to restart at the latest output.
"""

from __future__ import print_function

import glob, sys, os.path

outputs = sorted(glob.glob("output_?????"))

if len(outputs)==0:
    print("update_nml.py: no RAMSES outputs found! Not attempting to change any nml files.")
    sys.exit(1)

last_output = outputs[-1]

last_output_id = int(last_output[-5:])

print("update_nml.py: latest output is ",last_output_id)

nml_file = glob.glob("*.nml")

if len(nml_file)!=1:
    print("update_nml.py: cannot identify a unique .nml file! Giving up.")
    if len(nml_file)>1:
        print("Candidates:")
        for nml_cand in nml_file:
            print(" ",nml_cand)
    sys.exit(1)

nml_file = nml_file[0]

with open(nml_file, "r") as f:
    lines = f.readlines()

if not os.path.exists(nml_file+".bak"):
    print("update_nml.py: Making a backup",nml_file+".bak")
    os.rename(nml_file, nml_file+".bak")
else:
    print("update_nml.py: Backup file already exists")

with open(nml_file, "w") as f:
    for l in lines:
        if l.startswith("nrestart"):
            print("nrestart=%d"%last_output_id, file=f)
        else:
            print(l.strip(), file=f)

print("update_nml.py: Updated",nml_file)
