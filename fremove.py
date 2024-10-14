from XRootD import client
from XRootD.client.flags import OpenFlags

import os, signal
import sys
import time
import random



#-------------------------------------------------------------------------------

print("Pid", os.getpid())

f = client.File()
# status, response = f.open("root://localhost:7777//xrdpfc_command/remove_file/ /xrootd/data/BIG_FILE", OpenFlags.READ)
status, response = f.open("root://localhost:7777//xrdpfc_command/remove_file/ /xrootd/data/fake-samples/f_LEVEL_1/Bfile_0.root", OpenFlags.READ)
  # print("Open presumably finshed .. now reading first 4096 bytes, 30 sec timeout")
print('%r' % status.message)
f.close()

# time.sleep(60)
os.kill(os.getpid(), signal.SIGTERM)



