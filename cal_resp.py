#!/usr/bin/python


# created time : 2023-08-08
# created people: bob
# function: calculated RESP charge with RESP_ORCA.sh script

import subprocess
import glob

pdb_file = glob.glob("*.pdb")
resp_orca_dir = "/home/essex/Downloads/Multiwfn/Multiwfn_3.8_dev_bin_Linux/examples/RESP/"
for pdb in pdb_file:
    resp_cmd = resp_orca_dir + "RESP_ORCA.sh " + pdb
    subprocess.run(resp_cmd, shell=True)
